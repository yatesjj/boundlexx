"""
Import world data from the public Discovery Server endpoint (with explicit transaction management)
"""

import os
import django
import requests
import json

# Setup Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings.local")
django.setup()

from boundlexx.boundless.models import World
from django.utils import timezone
from django.db import transaction

def import_worlds_from_discovery_server():
    """Import world data from the public Discovery Server endpoint"""

    print("🌍 IMPORTING WORLDS FROM DISCOVERY SERVER (FIXED)")
    print("=" * 50)

    # Check current world count
    current_count = World.objects.count()
    print(f"📊 Current worlds in database: {current_count}")

    try:
        print(f"\n🔍 Fetching world data from Discovery Server...")
        response = requests.get("https://ds.playboundless.com:8902/list-gameservers", timeout=15)

        if response.status_code != 200:
            print(f"❌ Failed to fetch world data: {response.status_code}")
            return

        worlds_data = response.json()
        print(f"✅ Retrieved {len(worlds_data)} worlds from Discovery Server")

        created_count = 0
        updated_count = 0

        # Use explicit transaction management
        with transaction.atomic():
            print(f"\n🔒 Starting database transaction...")

            for world_data in worlds_data:
                world_id = world_data.get('id')
                display_name = world_data.get('displayName', 'Unknown')

                if not world_id:
                    continue

                print(f"🌟 Processing: {display_name} (ID: {world_id})")

                # Prepare atmosphere colors
                atmosphere_color = world_data.get('atmosphereColor', [])
                atmo_r = atmosphere_color[0] if len(atmosphere_color) > 0 else None
                atmo_g = atmosphere_color[1] if len(atmosphere_color) > 1 else None
                atmo_b = atmosphere_color[2] if len(atmosphere_color) > 2 else None

                # Prepare water colors
                water_color = world_data.get('waterColor', [])
                water_r = water_color[0] if len(water_color) > 0 else None
                water_g = water_color[1] if len(water_color) > 1 else None
                water_b = water_color[2] if len(water_color) > 2 else None

                # Check if world exists
                world, created = World.objects.get_or_create(
                    id=world_id,
                    defaults={
                        'display_name': display_name,
                        'name': world_data.get('name', display_name),
                        'tier': world_data.get('tier', 0),
                        'size': world_data.get('worldSize', 192),
                        'region': world_data.get('region', 'use'),  # Default to US East
                        'owner': None,  # Will be set based on sovereign status
                        'is_creative': False,  # Assume not creative for now
                        'is_locked': False,
                        'is_public': True,
                        'active': True,
                        'world_type': None,  # Not available from Discovery Server
                        'special_type': world_data.get('specialWorldType', None),
                        'number_of_regions': world_data.get('numRegions', None),
                        'api_url': world_data.get('apiURL'),
                        'planets_url': world_data.get('planetsURL'),
                        'chunks_url': world_data.get('chunksURL'),
                        'websocket_url': world_data.get('websocketURL'),
                        'address': world_data.get('addr'),
                        'ip_address': world_data.get('ipAddr'),
                        'atmosphere_color_r': atmo_r,
                        'atmosphere_color_g': atmo_g,
                        'atmosphere_color_b': atmo_b,
                        'water_color_r': water_r,
                        'water_color_g': water_g,
                        'water_color_b': water_b,
                        'last_updated': timezone.now(),
                    }
                )

                # Set owner for sovereign worlds (use assignment as a proxy)
                if world_data.get('sovereign', False):
                    world.owner = world_data.get('assignment', 1)  # Default owner ID if sovereign
                    world.save()  # Save the owner change

                if created:
                    created_count += 1
                    print(f"   ✅ Created new world")
                else:
                    # Update existing world with fresh data
                    world.display_name = display_name
                    world.name = world_data.get('name', display_name)
                    world.tier = world_data.get('tier', 0)
                    world.size = world_data.get('worldSize', 192)
                    world.region = world_data.get('region', 'use')
                    world.active = True
                    world.special_type = world_data.get('specialWorldType', None)
                    world.number_of_regions = world_data.get('numRegions', None)
                    world.api_url = world_data.get('apiURL')
                    world.planets_url = world_data.get('planetsURL')
                    world.chunks_url = world_data.get('chunksURL')
                    world.websocket_url = world_data.get('websocketURL')
                    world.address = world_data.get('addr')
                    world.ip_address = world_data.get('ipAddr')
                    world.atmosphere_color_r = atmo_r
                    world.atmosphere_color_g = atmo_g
                    world.atmosphere_color_b = atmo_b
                    world.water_color_r = water_r
                    world.water_color_g = water_g
                    world.water_color_b = water_b

                    # Set owner for sovereign worlds
                    if world_data.get('sovereign', False):
                        world.owner = world_data.get('assignment', 1)
                    else:
                        world.owner = None

                    world.save()
                    updated_count += 1
                    print(f"   🔄 Updated existing world")

            print(f"\n🔓 Committing transaction...")

        # Check results after transaction
        final_count = World.objects.count()
        print(f"\n📊 IMPORT SUMMARY")
        print(f"=" * 30)
        print(f"🆕 New worlds created: {created_count}")
        print(f"🔄 Existing worlds updated: {updated_count}")
        print(f"📊 Total worlds in database: {final_count}")

        # Verify the import worked
        if final_count > current_count:
            print(f"✅ Database successfully updated! Added {final_count - current_count} worlds.")
        else:
            print(f"⚠️ No new worlds added to database.")

        # Show some sample worlds
        print(f"\n🏰 Sample worlds by type:")

        # Show first 5 worlds
        all_worlds = World.objects.all()[:5]
        if all_worlds:
            print(f"\n   🌍 First 5 worlds:")
            for world in all_worlds:
                print(f"      - {world.display_name} (ID: {world.id}, Tier {world.tier})")

        # Check for Hadlrebum specifically
        hadlrebum = World.objects.filter(display_name__icontains='Hadlrebum').first()
        if hadlrebum:
            print(f"\n🎯 Found Hadlrebum!")
            print(f"   Name: {hadlrebum.display_name}")
            print(f"   ID: {hadlrebum.id}")
            print(f"   Tier: {hadlrebum.tier}")
            print(f"   Region: {hadlrebum.region}")
            if hadlrebum.atmosphere_color_r is not None:
                print(f"   Atmosphere: [{hadlrebum.atmosphere_color_r:.2f}, {hadlrebum.atmosphere_color_g:.2f}, {hadlrebum.atmosphere_color_b:.2f}]")
            if hadlrebum.water_color_r is not None:
                print(f"   Water: [{hadlrebum.water_color_r:.2f}, {hadlrebum.water_color_g:.2f}, {hadlrebum.water_color_b:.2f}]")
        else:
            print(f"\n❌ Hadlrebum not found in imported worlds")

        print(f"\n✅ World import completed successfully!")

    except Exception as e:
        print(f"❌ Error during import: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    import_worlds_from_discovery_server()
