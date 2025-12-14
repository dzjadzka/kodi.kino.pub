# Testing

Tests use pytest with podman-based Kodi + mockserver setup.

## Running
- Unit tests: `make test_unit` (runs `pytest -v tests/test_unit.py`).
- Integration tests: `make test_integration` (runs `pytest -v -k "(not test_unit)"`).

## Environment and fixtures
- `tests/conftest.py` builds the add-on into a host addons dir, substitutes VERSION, and spins a podman pod (`kodipod`) with Kodi and MockServer containers (ports 8080/1080/5999). Sets `KINO_PUB_TEST=1` for Kodi container.
- Fixtures provide `kodi` JSON-RPC client after waiting for services, and clean up containers/pod afterward.
- Helpers (`tests/helpers.py`) include podman wrapper, keyboard closing, and MockServer verify helper.

## Proxy coverage
- `tests/test_proxy.py` parametrizes HTTP/SOCKS5 proxies (with/without auth, negative cases). It configures Kodi system proxy settings via JSON-RPC, exercises bookmarks listing, and asserts proxy logs (or auth failure) from the glider container.

## Data/fixtures
- Expected results and mockserver expectations live under `tests/expected_results.py` and `fake_api/persistedExpectations.json` (referenced by MockServer env var).

## Sources
- tests/conftest.py
- tests/helpers.py
- tests/test_proxy.py
- Makefile targets
