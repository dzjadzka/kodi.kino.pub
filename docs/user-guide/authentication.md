# Authentication

Device-code login and token refresh are handled by `Auth` (`src/resources/lib/auth.py`) and the `/login/` route (`src/resources/lib/main.py`).

## Device-code flow
1. Open **Login** (route `/login/`). If no token is stored, the main screen shows **Activate device** linking here.
2. The add-on requests a device code from `oauth_api_url` with client `xbmc`.
3. A dialog shows the verification URL and user code; follow it in a browser and enter the code.
4. The add-on polls for authorization until approved or expired, then stores refresh/access tokens and expiry.
5. After success, the add-on registers device info via `device/notify` API.

## Token refresh
- Refresh happens automatically when access tokens expire or during playback if remaining time is shorter than the stream duration.
- If refresh fails with expiration, the flow restarts and prompts for activation again.

## Resetting auth
- Route `/reset_auth/` clears stored access/refresh tokens; re-run login afterward.

## Sources
- src/resources/lib/auth.py
- src/resources/lib/main.py (`/login/`, `/reset_auth/`)
