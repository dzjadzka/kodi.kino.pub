# Kino.pub Kodi Addon - Clean Rewrite

This is a clean rewrite of the kodi.kino.pub video addon using modern architecture patterns and best practices.

## Architecture

The addon follows Clean Architecture principles with clear separation of concerns:

```
new_addon/
├── domain/          # Business logic and entities (no external dependencies)
├── application/     # Use cases and application services
├── infrastructure/  # External services (API client, storage, Kodi integration)
├── presentation/    # UI/routing layer (Kodi plugin interface)
└── tests/           # Test suite
```

## Current Status

**Status:** Scaffolding Phase  
**Epic:** EPIC-001 - Full Reverse Engineering  
**Task:** Phase 6 - New Addon Scaffolding

This is stub code with interfaces defined. Implementation will follow in EPIC-002.

## Documentation

See `.github/docs/` for complete reverse engineering documentation:
- `new_architecture.md` - Architecture design
- `routes.md` - All 34 routes
- `api_contract.md` - Complete API specification
- `playback_flow.md` - Playback mechanisms
- And more...

## Development

See `BUILD.md` for build and testing instructions.

## Requirements

- Python 3.8+
- Kodi 19.0 (Matrix) or newer
- inputstream.adaptive addon (for HLS playback)

## License

Same as original kodi.kino.pub addon
