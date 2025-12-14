# Network Error Handling

Complete documentation of error scenarios and handling strategies in the kodi.kino.pub addon.

## Overview

The addon implements comprehensive error handling across multiple layers:

1. **HTTP Error Handlers** - urllib.request handler chain
2. **OAuth-specific Errors** - Device flow exceptions
3. **API Response Validation** - Status code checking
4. **User-facing Messages** - Localized error popups

---

## Error Handler Architecture

### Handler Chain

**Location:** `client.py:154-161`

```python
self.opener = urllib.request.build_opener(
    KinoApiRequestProcessor(self.plugin),      # 1. Request preprocessing
    KinoApiErrorProcessor(self.plugin),        # 2. Error handling (401, 429)
    KinoApiDefaultErrorHandler(self.plugin),   # 3. Default error handling
)
```

**Order:** Handlers are checked in registration order

**Pattern:** Chain of Responsibility

---

## HTTP Error Codes

### 200 - Success

**Handling:** `client.py:167-179` - `_handle_response()`

```python
def _handle_response(self, response: http.client.HTTPResponse):
    data = json.loads(response.read())
    if data and data["status"] == 200:
        return data
    elif response.status == 200:
        return {"status": 200}
    else:
        self.plugin.logger.error(f"Unknown error. Code: {data['status']}")
        popup_error(f"{localize(32006)} {data['status']}")  # Server response status code
        sys.exit()
```

**Checks:**
1. JSON body `status` field = 200
2. HTTP response `status` = 200
3. Otherwise: Log error, show popup, exit

---

### 400 - Bad Request

**Context:** OAuth flow only

**Handler:** `auth.py:100-116` - `Auth._make_request()`

```python
except urllib.error.HTTPError as e:
    if e.code == 400:
        response = json.loads(e.read())
        error = response.get("error")
        
        if error in ["code_expired", "authorization_expired", "invalid_refresh_token"]:
            raise AuthExpiredException
        
        if error == "authorization_pending":
            raise AuthPendingException
        
        if error:
            popup_error(localize(32002))  # Authentication error
            raise AuthException(error)
        
        return response
```

**Error Categories:**

#### Token/Code Expired
**Error Codes:**
- `code_expired` - Device code timed out (5 minutes)
- `authorization_expired` - Refresh token expired
- `invalid_refresh_token` - Refresh token invalid

**Response:**
```json
{
  "error": "code_expired",
  "error_description": "Device code has expired"
}
```

**Handling:**
1. Raise `AuthExpiredException`
2. Caught in `Auth._refresh_token()` → Restart device flow
3. Caught in `Auth._verify_device_code()` → Abort polling

**User Experience:** Auth dialog closes, redirects to /

---

#### Authorization Pending
**Error Code:** `authorization_pending`

**Response:**
```json
{
  "error": "authorization_pending",
  "error_description": "User has not yet authorized the device"
}
```

**Handling:**
1. Raise `AuthPendingException`
2. Caught in `Auth._verify_device_code()` polling loop
3. Continue polling (sleep 5 seconds, try again)

**User Experience:** Progress bar continues, no interruption

---

#### Unknown Auth Error
**Trigger:** Any other error in OAuth response

**Handling:**
1. Show popup: "Authentication error" (32002)
2. Raise `AuthException`
3. Propagates to caller, typically exits

**User Experience:** Error popup, addon exits

---

### 401 - Unauthorized

**Handler:** `client.py:109-130` - `KinoApiErrorProcessor.http_error_401()`

```python
def http_error_401(
    self, request, fp, code, msg, headers
) -> Union[http.client.HTTPResponse, NoReturn]:
    if request.recursion_counter_401 > 0:
        self.plugin.logger.fatal("Recursion limit exceeded in handling status code 401")
        popup_error(localize(32003))  # Authentication failed
        sys.exit()
    
    self.plugin.logger.error(f"HTTPError. Code: {code}. Attempting to refresh the token.")
    request.recursion_counter_401 += 1
    self.plugin.auth.get_token()  # Refresh token
    
    if not self.plugin.settings.access_token:
        self.plugin.logger.fatal("Access token is empty.")
        popup_error(localize(32003))
        sys.exit()
    
    return self.parent.open(request, timeout=TIMEOUT)  # Retry
```

**Flow:**

```
API returns 401
    ↓
Check recursion counter
    ├─→ > 0: Log fatal, show error, exit
    └─→ = 0: Continue
        ↓
    Increment counter
        ↓
    Call auth.get_token()
        ├─→ Refresh token
        └─→ If expired: Device flow
        ↓
    Check access_token
        ├─→ Empty: Log fatal, show error, exit
        └─→ Present: Retry original request
```

**Recursion Protection:**
- Counter attached to request object: `request.recursion_counter_401`
- Maximum 1 retry (counter starts at 0, checked if > 0)
- Prevents infinite loop if refresh fails

**User Experience:**
- **Success:** Transparent retry, user unaware
- **Failure:** "Authentication failed" popup, addon exits

---

### 429 - Too Many Requests

**Handler:** `client.py:132-151` - `KinoApiErrorProcessor.http_error_429()`

```python
def http_error_429(
    self, request, fp, code, msg, headers
) -> Union[http.client.HTTPResponse, NoReturn]:
    if request.recursion_counter_429 > 2:
        self.plugin.logger.fatal("Recursion limit exceeded in handling status code 429")
        popup_error(f"{localize(32006)} {code}. {localize(32007)}.")
        # "Server response status code 429. Try again."
        sys.exit()
    
    request.recursion_counter_429 += 1
    self.plugin.logger.error(
        f"HTTPError. Code: {code}. Retrying after 5 seconds. "
        f"Attempt {request.recursion_counter_429}."
    )
    xbmc.sleep(5000)  # 5 seconds in milliseconds
    return self.parent.open(request, timeout=TIMEOUT)
```

**Retry Strategy:**
- Maximum 3 attempts (counter 0 → 1 → 2, fails at > 2)
- Delay: 5 seconds between attempts
- Exponential backoff: No (fixed 5s delay)

**User Experience:**
- **1st-2nd retry:** Transparent, user unaware (10s total delay)
- **3rd attempt fails:** "Server response status code 429. Try again." popup, exit

---

**OAuth-specific Rate Limiting:**

**Handler:** `auth.py:118-121`

```python
elif e.code == 429:
    for _ in range(2):
        time.sleep(3)
        return self._make_request(payload)
```

**Different Strategy:**
- Maximum 2 retries (separate from main 429 handler)
- Delay: 3 seconds (OAuth endpoints may have different limits)
- Recursive retry (calls self)

---

### 5xx - Server Errors

**Handler:** `client.py:85-101` - `KinoApiDefaultErrorHandler.http_error_default()`

```python
def http_error_default(
    self, request, fp, code, msg, headers
) -> NoReturn:
    self.plugin.logger.fatal(f"HTTPError. {request.get_full_url()}. Code: {code}. Exiting.")
    popup_error(f"{localize(32006)} {code}")  # Server response status code
    sys.exit()
```

**Handling:**
- Log fatal error with URL and code
- Show popup: "Server response status code {code}"
- Exit addon

**No Retry:** Server errors considered unrecoverable

**Covered Codes:** 500, 502, 503, 504, etc.

---

## Network Connectivity Errors

### Connection Failure

**Trigger:** DNS failure, network down, firewall block, etc.

**Handler:** `client.py:189-194` - `KinoPubClient._make_request()`

```python
try:
    response = self.opener.open(request, timeout=TIMEOUT)
except Exception:
    popup_error(localize(32008))  # "kino.pub does not respond"
    raise
```

**Handling:**
- Catch all exceptions (URLError, socket errors, etc.)
- Show popup: "kino.pub does not respond" (32008)
- Re-raise exception (propagates to caller)

**User Experience:** Error popup, operation aborts

---

### Timeout

**Configuration:** `TIMEOUT = 60` seconds

**Locations:**
- `auth.py:24` - OAuth requests
- `client.py:28` - API requests

**Handling:**
- `urllib.error.URLError` with reason "timed out"
- Caught by generic exception handler above
- Shows "kino.pub does not respond" popup

---

## OAuth-specific Errors

### Exception Hierarchy

**Location:** `auth.py:27-40`

```python
class AuthException(Exception):
    pass

class AuthPendingException(AuthException):
    pass

class AuthExpiredException(AuthException):
    pass

class EmptyTokenException(AuthException):
    pass
```

### Usage Patterns

#### AuthPendingException
**Raised:** During device code polling when user hasn't authorized yet

**Caught:** `auth.py:194` - `Auth._verify_device_code()`

**Action:** Continue polling loop

---

#### AuthExpiredException
**Raised:** 
- Device code expired (5 min timeout)
- Refresh token expired/invalid

**Caught:** 
- `auth.py:166` - `Auth._refresh_token()` → Restart device flow
- `auth.py:109` - `Auth._make_request()` → Propagates

**Action:** Fallback to device authorization

---

#### EmptyTokenException
**Defined:** In code but **never raised or used**

**Status:** Dead code

---

#### AuthException (generic)
**Raised:** Unknown OAuth errors

**Caught:** Propagates to top level

**Action:** Exit addon

---

## Proxy Errors

### Proxy Configuration Validation

**Location:** `xbmc_settings.py:74-102`

**Validation:**

```python
@property
def is_correct(self) -> bool:
    if not self.is_enabled:
        return True
    
    if not self.host or not self.port:
        return False
    
    if self.with_auth and (not self.username or not self.password):
        return False
    
    return True
```

**Error Handling:** `client.py:46-48`

```python
if self.plugin.proxy_settings.is_enabled:
    if not self.plugin.proxy_settings.is_correct:
        self.plugin.logger.error("http proxy settings are not correct")
        return request  # Continue without proxy
```

**Behavior:** Invalid proxy → Log error, proceed without proxy (no user notification)

---

### Proxy Connection Errors

**SOCKS Proxy:** `client.py:69-80`

```python
socks.set_default_proxy(
    proxy_type=socks.SOCKS4 if proxy_settings.is_socks4 else socks.SOCKS5,
    addr=proxy_settings.host,
    port=proxy_settings.port,
    rdns=proxy_settings.type == "socks5r",
    username=proxy_settings.username,
    password=proxy_settings.password,
)
socket.socket = socks.socksocket
```

**Error:** If SOCKS proxy unreachable → `socket.error` → Generic network error popup

**HTTP Proxy:** `client.py:59-67`

```python
request.set_proxy(f"{proxy_settings.host}:{proxy_settings.port}", proxy_settings.type)
if proxy_settings.with_auth:
    user_pass = f"{proxy_settings.username}:{proxy_settings.password}"
    creds = base64.b64encode(user_pass.encode()).decode("ascii")
    request.add_header("Proxy-authorization", f"Basic {creds}")
```

**Error:** If HTTP proxy unreachable → `urllib.error.URLError` → Generic network error popup

**No Specific Proxy Error Handling:** Treated as generic connection failures

---

## User-facing Error Messages

All error messages are localized via `localize(string_id)`.

### Error String Mapping

| String ID | English | Trigger |
|-----------|---------|---------|
| 32002 | Authentication error | Unknown OAuth error |
| 32003 | Authentication failed | 401 recursion limit, empty token after refresh |
| 32006 | Server response status code | HTTP errors (429, 5xx, unknown) |
| 32007 | Try again | Appended to 429 error |
| 32008 | kino.pub does not respond | Network connectivity failure, timeout |

**Display Mechanism:** `utils.py` - `popup_error()`

```python
def popup_error(message: str) -> None:
    xbmcgui.Dialog().notification(
        localize(32001),  # "Device activation" (or addon name)
        message,
        xbmcgui.NOTIFICATION_ERROR,
        3000  # 3 seconds
    )
```

**UI:** Red notification toast in top-right corner, 3 second duration

---

## Logging

### Log Levels

**Location:** `logger.py:23-56`

```python
def debug(self, message: str) -> None:
    xbmc.log(f"[{self.plugin.PLUGIN_ID}] {message}", xbmc.LOGDEBUG)

def info(self, message: str) -> None:
    xbmc.log(f"[{self.plugin.PLUGIN_ID}] {message}", xbmc.LOGINFO)

def warning(self, message: str) -> None:
    xbmc.log(f"[{self.plugin.PLUGIN_ID}] {message}", xbmc.LOGWARNING)

def error(self, message: str) -> None:
    xbmc.log(f"[{self.plugin.PLUGIN_ID}] {message}", xbmc.LOGERROR)

def fatal(self, message: str) -> None:
    xbmc.log(f"[{self.plugin.PLUGIN_ID}] {message}", xbmc.LOGFATAL)
```

### Error Logging Patterns

**401 Error:**
```python
self.plugin.logger.error(f"HTTPError. Code: {code}. Attempting to refresh the token.")
# Later, if failed:
self.plugin.logger.fatal("Access token is empty.")
```

**429 Error:**
```python
self.plugin.logger.error(
    f"HTTPError. Code: {code}. Retrying after 5 seconds. Attempt {request.recursion_counter_429}."
)
# Later, if exhausted:
self.plugin.logger.fatal("Recursion limit exceeded in handling status code 429")
```

**OAuth Errors:**
```python
self.plugin.logger.fatal(f"Oauth request error; status: {e.code}; message: {e.message}")
```

**5xx Errors:**
```python
self.plugin.logger.fatal(f"HTTPError. {request.get_full_url()}. Code: {code}. Exiting.")
```

**Logs Include:**
- Timestamp (from Kodi)
- Log level
- Plugin ID prefix
- Error details (code, URL, message)

---

## Error Recovery Strategies

### Automatic Recovery

#### 401 Unauthorized
**Strategy:** Automatic token refresh + retry

**Success Rate:** High (if refresh token valid)

**Fallback:** Device flow if refresh fails

---

#### 429 Rate Limit
**Strategy:** Exponential backoff retry (up to 3 attempts)

**Success Rate:** Medium (depends on rate limit duration)

**Fallback:** None (exit after 3 failures)

---

#### Authorization Pending
**Strategy:** Polling with fixed interval (5 seconds)

**Success Rate:** High (if user completes auth within 5 minutes)

**Fallback:** Timeout after 5 minutes

---

### Manual Recovery

#### Network Errors
**User Action:** Check network, retry operation

**No Automatic Retry:** User must restart addon or navigate again

---

#### Auth Expired
**User Action:** Navigate to /login/ or use "Reset auth" setting

**Automatic Trigger:** Addon shows login option on main menu if no token

---

#### Server Errors (5xx)
**User Action:** Wait, retry later

**No Automatic Retry:** Exit immediately

---

## Error Handling Best Practices Followed

✅ **Structured Exception Hierarchy** - OAuth exceptions inherit from base  
✅ **Recursion Protection** - Prevents infinite retry loops  
✅ **Localized Messages** - User-friendly, translated errors  
✅ **Comprehensive Logging** - Errors logged before exit  
✅ **Graceful Degradation** - Invalid proxy → Continue without proxy  
✅ **User Feedback** - Popups for all fatal errors  
✅ **Automatic Retry** - For transient failures (401, 429)

---

## Error Handling Weaknesses

⚠️ **No Exponential Backoff for 429** - Fixed 5s delay, not adaptive  
⚠️ **Exit on Unrecoverable Errors** - No graceful return to menu  
⚠️ **No User Retry Option** - Must restart addon after errors  
⚠️ **Generic Network Errors** - "kino.pub does not respond" for all connectivity issues  
⚠️ **No Circuit Breaker** - No protection against cascading failures  
⚠️ **Proxy Errors Silent** - Invalid proxy → Log only, no user notification

---

## Error Scenarios Matrix

| Scenario | HTTP Code | Handler | Retry | User Message | Outcome |
|----------|-----------|---------|-------|--------------|---------|
| Invalid token | 401 | KinoApiErrorProcessor | Yes (1x) | None (transparent) or "Authentication failed" | Auto-refresh or exit |
| Rate limited | 429 | KinoApiErrorProcessor | Yes (3x, 5s delay) | "Server response status code 429. Try again." | Retry or exit |
| Server error | 5xx | KinoApiDefaultErrorHandler | No | "Server response status code {code}" | Exit |
| Network down | N/A | Generic exception | No | "kino.pub does not respond" | Exit |
| Timeout | N/A | URLError | No | "kino.pub does not respond" | Exit |
| Auth pending | 400 (OAuth) | Auth._make_request | Yes (60x, 5s delay) | None (progress bar) | Poll or timeout |
| Code expired | 400 (OAuth) | Auth._make_request | No | None (dialog closes) | Redirect to / |
| Invalid proxy | N/A | KinoApiRequestProcessor | No | None (log only) | Continue without proxy |
| Unknown error | Any | KinoApiDefaultErrorHandler | No | "Server response status code {code}" | Exit |

---

## Testing Error Handling

### Simulating Errors

**Network Errors:**
- Disconnect network → Test "kino.pub does not respond"
- Block port 443 → Test timeout

**401 Errors:**
- Manually corrupt access_token in settings
- Wait for token expiry → Test auto-refresh

**429 Errors:**
- Rapid-fire requests → Trigger rate limit (difficult without API access)

**OAuth Errors:**
- Use invalid device code → Test "authorization_pending"
- Wait > 5 minutes → Test "code_expired"

**Proxy Errors:**
- Set invalid proxy host → Test proxy fallback
- Set wrong SOCKS type → Test SOCKS errors

---

## Summary

### Error Handling Characteristics

- **Layers:** HTTP handlers + OAuth exceptions + Response validation
- **Retry Strategy:** Automatic for 401 (1x), 429 (3x), OAuth pending (60x)
- **User Feedback:** Localized popups for fatal errors
- **Logging:** Comprehensive error logging at appropriate levels
- **Recovery:** Automatic for auth errors, manual for others
- **Exit Behavior:** Most errors exit addon (not ideal UX)

### Handler Hierarchy

```
urllib.request.build_opener()
├── KinoApiRequestProcessor (preprocessing)
├── KinoApiErrorProcessor (401, 429)
└── KinoApiDefaultErrorHandler (all others)
    ↓
Generic exception handler (network errors)
```

### Critical Path

```
API Request
    ↓
[Success: 200] → Process response
[Auth Error: 401] → Refresh token → Retry
[Rate Limit: 429] → Wait 5s → Retry (up to 3x)
[Server Error: 5xx] → Log → Popup → Exit
[Network Error] → Popup → Exit
```

---

## References

- HTTP error handlers: `src/resources/lib/client.py:85-151`
- OAuth errors: `src/resources/lib/auth.py:27-40, 86-129`
- Response validation: `src/resources/lib/client.py:167-179`
- Logging: `src/resources/lib/logger.py`
- Error messages: `src/resources/language/*/strings.po`
- Proxy handling: `src/resources/lib/xbmc_settings.py`, `src/resources/lib/client.py:36-80`
