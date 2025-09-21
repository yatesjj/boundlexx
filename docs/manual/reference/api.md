# API Reference

Complete reference for Boundlexx REST API endpoints and usage.

## 🌐 API Overview

### Base Information
- **Base URL**: `http://127.0.0.1:28001/api/`
- **Current Version**: `v2` (default)
- **Legacy Version**: `v1` (deprecated)
- **Authentication**: Token-based, Session-based
- **Format**: JSON (primary), MessagePack (optional)
- **Rate Limiting**: 1000/hour (anonymous), 5000/hour (authenticated)

### API Versioning
```bash
# v2 (default)
GET /api/v2/items/

# v1 (legacy)
GET /api/v1/items/

# Version in headers
GET /api/items/
Accept: application/json; version=v2
```

## 🔐 Authentication

### Token Authentication
```bash
# Obtain token
POST /api/auth/token/
{
    "username": "your_username",
    "password": "your_password"
}

# Response
{
    "token": "9944b09199c62bcf9418ad846dd0e4bbdfc6ee4b"
}

# Use token in requests
GET /api/v2/items/
Authorization: Token 9944b09199c62bcf9418ad846dd0e4bbdfc6ee4b
```

### Session Authentication
```bash
# Login via web interface first
GET /api/v2/items/
Cookie: sessionid=abc123...
```

## 📦 Core Resources

### Items
Boundless game items including blocks, tools, foods, etc.

#### List Items
```bash
GET /api/v2/items/
```

**Query Parameters:**
- `search` (string): Search by name
- `item_type` (string): Filter by item type
- `tier` (integer): Filter by tier (0-8)
- `has_colors` (boolean): Items with color variants
- `craftable` (boolean): Items that can be crafted
- `burnable` (boolean): Items that can be burned as fuel
- `edible` (boolean): Items that can be eaten
- `page` (integer): Page number
- `page_size` (integer): Items per page (max 100)

**Example:**
```bash
GET /api/v2/items/?search=stone&tier=0&has_colors=true&page_size=20
```

**Response:**
```json
{
    "count": 42,
    "next": "/api/v2/items/?page=2",
    "previous": null,
    "results": [
        {
            "id": 1,
            "game_id": 7,
            "string_id": "BLOCK_STONE_SEDIMENTARY",
            "name": "Sedimentary Stone",
            "description": "A common sedimentary rock...",
            "item_type": "BLOCK",
            "tier": 0,
            "max_stack": 900,
            "prestige": 1,
            "has_colors": true,
            "craftable": false,
            "burnable": false,
            "edible": false,
            "image_url": "/media/items/stone_sedimentary.png",
            "colors": [
                {
                    "game_id": 0,
                    "name": "White",
                    "hex_value": "#FFFFFF"
                }
            ]
        }
    ]
}
```

#### Get Item Details
```bash
GET /api/v2/items/{id}/
```

**Response includes:**
- Full item details
- Available colors
- Crafting recipes (if craftable)
- Used in recipes
- Mining locations (if minable)
- Shop data
- Sovereign color data

### Colors
Color variants for blocks and items.

#### List Colors
```bash
GET /api/v2/colors/
```

**Query Parameters:**
- `search` (string): Search by color name
- `item` (integer): Colors for specific item ID
- `gleam` (boolean): Gleam colors only
- `metal` (boolean): Metal colors only
- `rock` (boolean): Rock colors only

**Response:**
```json
{
    "results": [
        {
            "game_id": 0,
            "name": "White",
            "hex_value": "#FFFFFF",
            "base_color": true,
            "gleam": false,
            "metal": false,
            "rock": true,
            "default_item": {
                "id": 1,
                "name": "Sedimentary Stone"
            }
        }
    ]
}
```

### Skills
Character skills and skill groups.

#### List Skills
```bash
GET /api/v2/skills/
```

**Query Parameters:**
- `group` (string): Filter by skill group
- `level` (integer): Filter by level requirement
- `cost` (integer): Filter by skill point cost

**Response:**
```json
{
    "results": [
        {
            "id": 1,
            "game_id": "SKILL_MINING_EPIC",
            "name": "Epic Mining",
            "description": "Increases mining speed...",
            "group": "Mining",
            "level_requirement": 25,
            "cost": 3,
            "icon_url": "/media/skills/mining_epic.png"
        }
    ]
}
```

### Recipes
Crafting recipes and requirements.

#### List Recipes
```bash
GET /api/v2/recipes/
```

**Query Parameters:**
- `search` (string): Search by recipe name
- `output_item` (integer): Recipes that produce specific item
- `input_item` (integer): Recipes that require specific item
- `machine` (string): Filter by crafting machine
- `level` (integer): Filter by required level
- `skill` (integer): Filter by required skill

**Response:**
```json
{
    "results": [
        {
            "id": 1,
            "game_id": "RECIPE_WORKBENCH_REFINED_STONE",
            "output": {
                "item": {
                    "id": 5,
                    "name": "Refined Stone"
                },
                "count": 4
            },
            "inputs": [
                {
                    "item": {
                        "id": 1,
                        "name": "Sedimentary Stone"
                    },
                    "count": 4
                }
            ],
            "machine": "WORKBENCH",
            "level": 5,
            "required_skills": [
                {
                    "id": 10,
                    "name": "Basic Crafting"
                }
            ],
            "craft_time": 30,
            "wear_requirement": 100
        }
    ]
}
```

### Worlds
Active Boundless worlds and their properties.

#### List Worlds
```bash
GET /api/v2/worlds/
```

**Query Parameters:**
- `active` (boolean): Active worlds only
- `tier` (integer): Filter by world tier
- `world_type` (string): Filter by world type
- `region` (string): Filter by region
- `special_type` (string): Filter by special world types

**Response:**
```json
{
    "results": [
        {
            "id": 1,
            "name": "Serpensarindi",
            "display_name": "Serpensarindi",
            "tier": 1,
            "world_type": "LUSH",
            "size": "LARGE",
            "region": "use",
            "active": true,
            "special_type": null,
            "protection": false,
            "coordinates": {
                "x": -1474,
                "y": 74,
                "z": 1526
            },
            "atmosphere_color": "#7FB069",
            "water_color": "#4A90E2",
            "assignment": {
                "start": "2023-01-01T00:00:00Z",
                "end": "2023-12-31T23:59:59Z"
            }
        }
    ]
}
```

## 🔍 Advanced Queries

### Search
Global search across multiple resource types.

```bash
GET /api/v2/search/?q=stone&types=items,recipes
```

**Parameters:**
- `q` (required): Search query
- `types` (optional): Comma-separated resource types to search
- `limit` (optional): Maximum results per type

### Filtering
Most endpoints support advanced filtering:

```bash
# Multiple filters
GET /api/v2/items/?tier__gte=3&tier__lte=6&craftable=true

# Range queries
GET /api/v2/recipes/?craft_time__range=30,300

# Contains queries
GET /api/v2/items/?name__icontains=stone

# Exclude queries
GET /api/v2/worlds/?tier__ne=8
```

### Ordering
```bash
# Single field
GET /api/v2/items/?ordering=name

# Multiple fields
GET /api/v2/items/?ordering=tier,name

# Descending
GET /api/v2/items/?ordering=-tier,name
```

### Field Selection
```bash
# Specific fields only
GET /api/v2/items/?fields=id,name,tier

# Exclude fields
GET /api/v2/items/?exclude=description,image_url
```

## 📊 Aggregation Endpoints

### Statistics
```bash
GET /api/v2/stats/
```

**Response:**
```json
{
    "items": {
        "total": 2847,
        "by_tier": {
            "0": 156,
            "1": 234,
            "2": 189
        },
        "by_type": {
            "BLOCK": 1203,
            "TOOL": 145,
            "FOOD": 89
        }
    },
    "worlds": {
        "total": 42,
        "active": 38,
        "by_tier": {
            "1": 8,
            "2": 6,
            "3": 8
        }
    }
}
```

### Health Check
```bash
GET /api/v2/health/
```

**Response:**
```json
{
    "status": "healthy",
    "timestamp": "2024-01-15T10:30:00Z",
    "version": "2.1.0",
    "database": "connected",
    "cache": "connected",
    "last_data_update": "2024-01-14T15:45:00Z"
}
```

## 🚀 Performance Features

### Caching
API responses are cached for improved performance:
- **Items**: 1 hour cache
- **Static data**: 24 hour cache
- **Dynamic data**: 5 minute cache

Use `Cache-Control: no-cache` header to bypass cache.

### Compression
API supports response compression:
```bash
GET /api/v2/items/
Accept-Encoding: gzip, deflate
```

### Pagination
```bash
# Default pagination
GET /api/v2/items/
{
    "count": 2847,
    "next": "/api/v2/items/?page=2",
    "previous": null,
    "results": [...]
}

# Custom page size
GET /api/v2/items/?page_size=100

# Cursor pagination for large datasets
GET /api/v2/items/?cursor=cD0yMDIzLTEyLTE%3D
```

## 🔄 Real-time Features

### WebSocket Support
Real-time updates for world data:

```javascript
// Connect to world updates
const ws = new WebSocket('ws://127.0.0.1:28001/ws/worlds/');

// Listen for world changes
ws.onmessage = function(event) {
    const data = JSON.parse(event.data);
    console.log('World updated:', data);
};
```

### Webhooks (Beta)
Register for data change notifications:

```bash
POST /api/v2/webhooks/
{
    "url": "https://your-app.com/webhook",
    "events": ["world.update", "item.create"],
    "secret": "your-webhook-secret"
}
```

## 🛠️ Development Tools

### OpenAPI Schema
```bash
# Full schema
GET /api/schema/

# Swagger UI
GET /api/docs/

# ReDoc
GET /api/redoc/
```

### API Testing
```bash
# Test API health
curl -X GET http://127.0.0.1:28001/api/v2/health/

# Test with authentication
curl -X GET http://127.0.0.1:28001/api/v2/items/ \
  -H "Authorization: Token your-token-here"

# Test search
curl -X GET "http://127.0.0.1:28001/api/v2/search/?q=stone&types=items"
```

## 📋 Response Formats

### Standard Response
```json
{
    "id": 1,
    "field1": "value1",
    "field2": "value2",
    "created_at": "2024-01-15T10:30:00Z",
    "updated_at": "2024-01-15T10:30:00Z"
}
```

### Error Response
```json
{
    "error": {
        "code": "VALIDATION_ERROR",
        "message": "Invalid parameter value",
        "details": {
            "field": ["This field is required."]
        }
    }
}
```

### Paginated Response
```json
{
    "count": 2847,
    "next": "/api/v2/items/?page=2",
    "previous": null,
    "results": [...]
}
```

## 🚫 Rate Limiting

### Limits
- **Anonymous**: 1000 requests/hour
- **Authenticated**: 5000 requests/hour
- **Premium**: 10000 requests/hour

### Headers
```
X-RateLimit-Limit: 5000
X-RateLimit-Remaining: 4987
X-RateLimit-Reset: 1642248600
```

### Handling Rate Limits
```python
import requests
import time

def api_request_with_retry(url, headers=None):
    response = requests.get(url, headers=headers)

    if response.status_code == 429:
        reset_time = int(response.headers.get('X-RateLimit-Reset', 0))
        wait_time = reset_time - int(time.time())
        time.sleep(max(wait_time, 60))
        return api_request_with_retry(url, headers)

    return response
```

## 🌍 Internationalization

### Language Support
API supports multiple languages through `Accept-Language` header:

```bash
GET /api/v2/items/1/
Accept-Language: fr-FR

# Response includes localized strings
{
    "id": 1,
    "name": "Pierre sédimentaire",
    "description": "Une roche sédimentaire commune..."
}
```

**Supported Languages:**
- `en-US` (English) - Default
- `fr-FR` (French)
- `de-DE` (German)
- `it-IT` (Italian)
- `es-ES` (Spanish)

---

## 📖 Additional Resources

- **OpenAPI Documentation**: `/api/docs/`
- **API Playground**: `/api/playground/`
- **Status Page**: `/api/status/`
- **SDK Examples**: See `/examples/` directory
- **Postman Collection**: Available in repository

For detailed integration examples, see the [Integration Guide](../workflows/integration.md).
