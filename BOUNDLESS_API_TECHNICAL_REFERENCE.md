# Boundless API Technical Reference
## Complete Authentication & Communication Chain Analysis

This document provides a comprehensive technical reference for the authentication and communication systems used by Boundlexx to interact with the Boundless Discovery Server, including Steam authentication, JWT tokens, and binary protocol specifications.

## Table of Contents
- [Authentication Flow Overview](#authentication-flow-overview)
- [Steam Authentication System](#steam-authentication-system)
- [JWT Token Implementation](#jwt-token-implementation)
- [Boundless Discovery Server Integration](#boundless-discovery-server-integration)
- [Binary Protocol Specifications](#binary-protocol-specifications)
- [Celery Task Communication Patterns](#celery-task-communication-patterns)
- [Rate Limiting & Caching Strategy](#rate-limiting--caching-strategy)
- [Critical Code Locations](#critical-code-locations)

## Authentication Flow Overview

The complete authentication chain follows this sequence:

```
Steam Login → Steam Session Ticket → Forum Login → JWT Token → Discovery Server Login → Query Token → API Requests
```

### High-Level Process
1. **Steam Authentication**: Generate session tickets using Steam credentials
2. **Forum Authentication**: Login to Boundless community accounts
3. **JWT Token Retrieval**: Extract game authentication tokens
4. **Discovery Server Login**: Authenticate with game servers using Steam ticket + JWT
5. **Query Token**: Receive opaque tokens for subsequent API calls
6. **Authenticated Requests**: Use query tokens for world data, shop data, etc.

## Steam Authentication System

### Components
- **Node.js Script**: `/usr/local/bin/steam-auth-ticket`
- **Steam Library**: `steam-user` npm package
- **App ID**: `324510` (Boundless game identifier)
- **2FA Persistence**: Steam Guard sentry files

### Environment Configuration
```bash
STEAM_SENTRY_DIR=/app/.steam          # 2FA persistence directory
STEAM_USERNAME=steam_account_name     # Steam account username
STEAM_PASSWORD=steam_password         # Steam account password
STEAM_APP_ID=324510                   # Boundless Steam App ID
```

### Steam Auth Script Implementation
**File**: `docker/bin/steam-auth-ticket`
```javascript
#!/usr/bin/env node
const SteamUser = require("steam-user");

sentry_dir = process.env.STEAM_SENTRY_DIR
steam_username = process.env.STEAM_USERNAME
steam_password = process.env.STEAM_PASSWORD
app_id = Number(process.env.STEAM_APP_ID)

s = new SteamUser({ "dataDirectory": sentry_dir });
s.logOn({ "accountName": steam_username, "password": steam_password, "rememberPassword": true });

callback = function (err, t) {
    if (err) {
        console.error(err);
        process.exit(1);
    }
    else {
        console.log(t.toString("hex"));  // Hex-encoded session ticket
        process.exit(0);
    }
}

setTimeout(function () {
    s.getAuthSessionTicket(app_id, callback);
}, 5000);  // 5-second delay before ticket generation
```

### Python Integration
**File**: `boundlexx/boundless/game/client.py:256-290`
```python
def _get_steam_session_ticket(self, username, password):
    env = {
        "STEAM_SENTRY_DIR": settings.STEAM_SENTRY_DIR,
        "STEAM_USERNAME": username,
        "STEAM_PASSWORD": password,
        "STEAM_APP_ID": str(settings.STEAM_APP_ID),
        "HOME": str(settings.ROOT_DIR),
        "NODE_PATH": settings.STEAM_AUTH_NODE_MODULES,
    }

    tries = 5
    while True:
        try:
            process = subprocess.run(
                [settings.STEAM_AUTH_SCRIPT],
                capture_output=True,
                check=True,
                shell=True,
                env=env,
            )
        except subprocess.CalledProcessError as e:
            if tries <= 0:
                raise
        else:
            break
        tries -= 1
        time.sleep(5)

    return process.stdout.decode("utf8").strip()  # Returns hex string
```

## JWT Token Implementation

### Authentication Chain
```
Forum Login → Session Cookies → JWT Token Request → Game Auth Token
```

### Step 1: Forum Login
**Endpoint**: `https://account.playboundless.com/dynamic/login`
**Method**: `POST`
**Content-Type**: `application/x-www-form-urlencoded`

**Request Payload**:
```
login={boundless_username}&password={boundless_password}
```

**Implementation** (`boundlexx/boundless/game/client.py:226-242`):
```python
def _get_boundless_session(self, username, password):
    session = requests.Session()
    
    data = {
        "login": username,
        "password": password,
    }
    
    response = session.post(
        f"{settings.BOUNDLESS_ACCOUNTS_BASE_URL}/dynamic/login",
        data=data,
        headers={"Content-Type": "application/x-www-form-urlencoded"},
    )
    response.raise_for_status()
    
    return session, response.json()["user"]
```

### Step 2: JWT Token Retrieval
**Endpoint**: `https://account.playboundless.com/api/v1/game-auth-token/boundless`
**Method**: `GET`
**Authentication**: Session cookies from forum login

**Response Format**:
```json
{
  "data": "JWT_TOKEN_STRING"
}
```

**Implementation** (`boundlexx/boundless/game/client.py:245-254`):
```python
def _get_game_jwt(self, username, password):
    session, _ = self._get_boundless_session(username, password)
    
    response = session.get(
        f"{settings.BOUNDLESS_ACCOUNTS_BASE_URL}/api/v1/game-auth-token/boundless"
    )
    response.raise_for_status()
    
    return response.json()["data"]
```

## Boundless Discovery Server Integration

### Configuration
```python
# Discovery Server Base URL
BOUNDLESS_API_URL_BASE = "http://host.docker.internal:8950"  # Default/local
BOUNDLESS_ACCOUNTS_BASE_URL = "https://account.playboundless.com"
BOUNDLESS_DS_REQUIRES_AUTH = False  # Controls authentication mode
```

### Authentication Modes

#### Mode 1: Authenticated Production Server
**Login Endpoint**: `POST {BOUNDLESS_API_URL_BASE}/login`
**Content-Type**: `application/json`

**Request Payload**:
```json
{
  "authToken": "JWT_FROM_BOUNDLESS_ACCOUNTS",
  "steamTicket": "HEX_ENCODED_STEAM_SESSION_TICKET",
  "vcplatform": 1,
  "gameVersion": "testing"  // Optional, when BOUNDLESS_TESTING_FEATURES=true
}
```

#### Mode 2: Local/Sandbox Server
**Request Payload**:
```json
{
  "username": "BOUNDLESS_USERNAME"
}
```

### Login Response Structure
```json
{
  "characters": [
    {
      "id": 12345,
      "name": "PlayerName",
      "level": 50,
      // ... additional character data
    }
  ],
  "queryToken": "OPAQUE_QUERY_TOKEN_STRING"
}
```

### Query Token Caching
**Structure**:
```python
QueryToken = namedtuple("QueryToken", ("player", "token", "username"))
# player: First character from characters array
# token: Opaque string from queryToken field
# username: Boundless account username
```

**Cache Configuration**:
- **Cache Key**: `boundless_client:query_token:{username}`
- **Timeout**: 43,200 seconds (12 hours)
- **Storage**: Redis cache

## Binary Protocol Specifications

### Request Authentication Formats

#### Discovery Server Requests
**Headers**: `Content-Type: application/octet-stream`
**Authentication**: Query token with prefix handling

**Implementation** (`boundlexx/boundless/game/client.py:305-312`):
```python
data = self.query_token.token
for url in PREFIXED_URLS:  # ["/worldpoll", "/gameserver/"]
    if url in path:
        data = f"q{data}"  # Prefix with 'q' for specific endpoints
        break
headers = {"Content-Type": "application/octet-stream"}
```

#### World Poll Requests (Binary Protocol)
**Binary Packet Structure** (Little Endian):
```c
struct PollRequest {
    uint8_t username_length;        // 1 byte: Length of username string
    char username[username_length]; // N bytes: UTF-8 encoded username
    uint32_t player_id;            // 4 bytes: Player account ID (little endian)
    char poll_token[];             // Variable: UTF-8 encoded poll token
}
```

**Python Implementation** (`boundlexx/boundless/game/client.py:299-304`):
```python
username = self.query_token.player["name"].lower()
data = (
    struct.pack("<b", len(username)) +      # 1 byte: username length
    username.encode("utf8") +               # N bytes: username
    struct.pack("<I", self.query_token.player["id"]) +  # 4 bytes: player ID
    poll_token.encode("utf8")               # Variable: poll token
)
```

### Discovery Server API Endpoints

#### World Data Endpoint
**URL Pattern**: `/gameserver/{username}/{world_id}/{account_id}`
**Method**: POST
**Response**: JSON world data

**Example**:
```
POST /gameserver/playername/123/12345
Authentication: Query token (prefixed with "q")
```

#### Distance Calculation Endpoint
**URL Pattern**: `/distance/{username}/{world1_id}/{world2_id}/{account_id}`
**Method**: POST
**Response**: JSON distance data

**Example Response**:
```json
{
  "distance": 123.45
}
```

#### World Poll Endpoint
**URL Pattern**: `/worldpoll`
**Method**: POST
**Authentication**: Binary poll packet
**Response**: JSON poll results

### Binary Response Formats

#### Shop Data Response (`application/octet-stream`)
**Structure**: Sequential binary records, no delimiters

**Per-Item Binary Structure**:
```c
struct ShopItem {
    uint8_t beacon_name_length;             // 1 byte
    uint8_t guild_tag_length;               // 1 byte
    char beacon_name[beacon_name_length];   // Variable: Latin-1 encoded
    char guild_tag[guild_tag_length];       // Variable: Latin-1 encoded
    uint32_t item_count;                    // 4 bytes: Little endian
    uint32_t shop_activity;                 // 4 bytes: Little endian
    int64_t price;                          // 8 bytes: Little endian (cents)
    int16_t location_x;                     // 2 bytes: Little endian
    int16_t location_z;                     // 2 bytes: Little endian (negated)
    uint8_t location_y;                     // 1 byte: Height
}
// Total per item: 23 + beacon_name_length + guild_tag_length bytes
```

**Python Parsing** (`boundlexx/boundless/game/models.py:59-95`):
```python
@staticmethod
def from_binary(binary: bytes) -> list[ShopItem]:
    items = []
    offset = 0
    
    while offset != len(binary):
        beacon_name_length, guild_tag_length = unpack_from("<BB", binary, offset)
        (
            beacon_name, guild_tag, item_count, shop_activity, price,
            location_x, location_z, location_y,
        ) = unpack_from(
            f"<{beacon_name_length}s{guild_tag_length}sIIqhhB",
            binary, offset + 2,
        )
        offset += 23 + beacon_name_length + guild_tag_length
        
        beacon_name = beacon_name.decode("latin1")
        guild_tag = guild_tag.decode("latin1")
        location = Location(location_x, location_y, -location_z)
        
        items.append(ShopItem(
            beacon_name, guild_tag, item_count, shop_activity,
            price / 100, location  # Convert cents to currency units
        ))
    
    return items
```

#### Settlement Data Response (`application/octet-stream`)
**Format**: 5-byte header + zlib-compressed binary data

**Compressed Data Structure**:
```c
struct SettlementData {
    uint8_t padding[8];           // Skip first 8 bytes
    uint32_t count;              // Little endian: Number of settlements
    struct Settlement settlements[count];
}

struct Settlement {
    uint8_t name_length;         // 1 byte
    char name[name_length];      // Variable: Latin-1 encoded
    uint32_t prestige;          // 4 bytes: Little endian
    uint32_t unknown;           // 4 bytes: Padding/unknown field
    int16_t x_chunk;            // 2 bytes: Multiply by 16 for world coords
    int16_t z_chunk;            // 2 bytes: Multiply by 16, negate for world coords
}
```

**Python Parsing** (`boundlexx/boundless/game/models.py:109-135`):
```python
@staticmethod
def from_binary(binary: bytes) -> list[Settlement]:
    binary = zlib.decompress(binary[5:])  # Skip 5-byte header, decompress
    offset = 8  # Skip padding
    
    count = unpack_from("<I", binary, offset)[0]
    offset += 4
    
    settlements: list[Settlement] = []
    
    while len(settlements) < count and offset < len(binary):
        name_length = unpack_from("<B", binary, offset)[0]
        offset += 1
        
        name, prestige, _, x, z = unpack_from(f"<{name_length}sIIhh", binary, offset)
        offset += name_length + 12
        
        settlements.append(Settlement(
            name.decode("latin1"),
            prestige,
            Location(x * 16, None, -z * 16)  # Convert chunk coords to world coords
        ))
    
    return settlements
```

## Celery Task Communication Patterns

### Task Queue Configuration
**File**: `config/celery_app.py`

```python
app.conf.task_routes = {
    "boundlexx.boundless.tasks.worlds.calculate_distances": {"queue": "distance"},
    "boundlexx.api.tasks.purge_cache": {"queue": "cache"},
    "boundlexx.notifications.*": {"queue": "notify"},
    "boundlexx.boundless.tasks.worlds.poll_*": {"queue": "poll"},
    "boundlexx.boundless.tasks.shop.*": {"queue": "shop"},
    "boundlexx.boundless.tasks.add_world_control_data": {"queue": "control"},
}
```

### Task Categories

#### World Polling Tasks (`poll` queue)
- `poll_perm_worlds`: Poll permanent worlds
- `poll_exo_worlds`: Poll exoworlds (temporary worlds)
- `poll_sovereign_worlds`: Poll player-owned worlds
- `poll_creative_worlds`: Poll creative mode worlds

#### Shop Data Tasks (`shop` queue)  
- Shop price updates
- Market data synchronization
- Item availability tracking

#### Distance Calculation (`distance` queue)
- World-to-world distance calculations
- Portal network mapping

#### Notifications (`notify` queue)
- Discord webhook notifications
- Exoworld spawn alerts
- Color change notifications

### Background Task Execution Flow

```python
# Example: World polling task
@app.task
def poll_perm_worlds():
    _poll_with_lock("perm", World.objects.filter(end__isnull=True, active=True))

def _poll_with_lock(lock_name, worlds):
    client = BoundlessClient()  # Handles all authentication
    
    for world in worlds:
        try:
            # Get world data from Discovery Server
            world_dict = client.get_world_data(SimpleWorld(world.id, world.api_url))
            
            if world_dict and "pollData" in world_dict:
                # Get detailed poll data using binary protocol
                poll_data = client.get_world_poll(
                    SimpleWorld(world.id, world.api_url),
                    world_dict["pollData"]
                )
                
                # Store results in database
                WorldPoll.objects.create_from_game_dict(world, poll_data)
                
        except Exception as e:
            logger.error(f"Failed to poll world {world.id}: {e}")
```

## Rate Limiting & Caching Strategy

### Rate Limiting Configuration
```python
# Discovery Server API rate limiting
BOUNDLESS_API_DS_DELAY = 1.0  # Seconds between Discovery Server requests

# World API rate limiting
BOUNDLESS_API_WORLD_DELAY = 0.5  # Seconds between world-specific requests
BOUNDLESS_API_WORLD_DELAY_API_KEY = 1.0  # Extended delay for API key requests

# Request timeout
BOUNDLESS_API_TIMEOUT = 30  # Seconds
```

### Cache Implementation
**Backend**: Redis with django-redis
**Lock Mechanism**: Redis distributed locks

**Discovery Server Cache**:
```python
def _authenticated_ds(self, path):
    with cache.lock("boundless_client:lock:ds", expire=30):
        cache_key = "boundless_client:ds"
        last_call = cache.get(cache_key) or 0
        now = time.monotonic()
        
        time_since = now - last_call
        if time_since < settings.BOUNDLESS_API_DS_DELAY:
            time.sleep(settings.BOUNDLESS_API_DS_DELAY - time_since)
        
        response = self._authentiated_post(path)
        cache.set(cache_key, time.monotonic(), timeout=10)
    
    return response
```

**World API Cache**:
```python
def _get_world(self, world: World, path, api_key=False):
    delay = settings.BOUNDLESS_API_WORLD_DELAY
    if api_key:
        delay = delay * 2
    
    with cache.lock(f"boundless_client:lock:world:{world.id}", expire=30):
        cache_key = f"boundless_client:{world.id}"
        last_call = cache.get(cache_key) or 0
        now = time.monotonic()
        
        time_since = now - last_call
        if time_since < delay:
            time.sleep(delay - time_since)
        
        # Make request...
        cache.set(cache_key, time.monotonic(), timeout=10)
```

## Critical Code Locations

### Authentication Chain
1. **Steam Ticket Generation**
   - File: `boundlexx/boundless/game/client.py`
   - Lines: 256-290
   - Function: `_get_steam_session_ticket()`

2. **JWT Token Retrieval**
   - File: `boundlexx/boundless/game/client.py` 
   - Lines: 245-255
   - Function: `_get_game_jwt()`

3. **Discovery Server Login**
   - File: `boundlexx/boundless/game/client.py`
   - Lines: 166-212
   - Property: `query_token`

### Request Formatting
1. **Binary Packet Construction**
   - File: `boundlexx/boundless/game/client.py`
   - Lines: 294-325
   - Function: `_authentiated_post()`

2. **API Endpoint Calls**
   - File: `boundlexx/boundless/game/client.py`
   - Lines: 375-420
   - Functions: `get_world_data()`, `get_world_poll()`, `get_world_distance()`

### Binary Data Parsing
1. **Shop Data Parsing**
   - File: `boundlexx/boundless/game/models.py`
   - Lines: 59-95
   - Function: `ShopItem.from_binary()`

2. **Settlement Data Parsing**
   - File: `boundlexx/boundless/game/models.py`
   - Lines: 109-135
   - Function: `Settlement.from_binary()`

### Background Task Management
1. **Celery Configuration**
   - File: `config/celery_app.py`
   - Lines: 20-27
   - Variable: `task_routes`

2. **World Polling Tasks**
   - File: `boundlexx/boundless/tasks/worlds.py`
   - Lines: 179-207
   - Functions: `poll_perm_worlds()`, `poll_exo_worlds()`, etc.

3. **Task Rate Limiting**
   - File: `boundlexx/boundless/game/client.py`
   - Lines: 344-370
   - Functions: `_authenticated_ds()`, `_authenticated_world()`

## Error Handling & Recovery

### Authentication Failures
- **401 Responses**: Automatically invalidate and refresh query tokens
- **Steam Ticket Failures**: Retry up to 5 times with 5-second delays
- **JWT Expiration**: Re-authenticate through forum login

### Network Failures  
- **Timeout Handling**: 30-second request timeout
- **Rate Limit Exceeded**: Automatic backoff with cache-based delays
- **Server Unavailable**: Task retry with exponential backoff

### Binary Protocol Errors
- **Malformed Packets**: Skip corrupted records, continue parsing
- **Compression Failures**: Log error, return empty results
- **Encoding Issues**: Use Latin-1 fallback for text fields

This technical reference provides the complete implementation details for integrating with the Boundless Discovery Server API, including all authentication mechanisms, binary protocols, and background task patterns used by Boundlexx.