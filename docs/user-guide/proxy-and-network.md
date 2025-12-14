# Proxy and network

System proxy settings are read via JSON-RPC (`XbmcProxySettings`), validated, and applied in HTTP requests (`KinoApiRequestProcessor`).

## How proxy settings are read
- Uses Kodi system settings via JSON-RPC (`Settings.GetSettingValue`) for `network.usehttpproxy`, type, host, port, username, password.
- Supported types mapped to http/https, socks4/socks4a, socks5/socks5h.

## Validation and usage
- Proxy considered valid when host length > 3 and port > 0.
- HTTP/HTTPS proxies set via `Request.set_proxy`; basic auth added when username/password present.
- SOCKS proxies configured globally via PySocks (`socks.socksocket` substitution) with optional auth.

## Error handling
- If proxy enabled but invalid, request proceeds without applying it and logs a warning.
- For HTTP errors: 401 triggers token refresh; 429 retries with backoff; other errors show user-facing popup and exit.

## User guidance
- Enable proxy in Kodi settings first; supply correct host/port and credentials if required.
- For SOCKS, choose the appropriate type (socks4/socks5); for remote DNS use socks5h.
- If requests fail, check logs for proxy validation errors and confirm credentials.

## Sources
- src/resources/lib/xbmc_settings.py
- src/resources/lib/client.py
