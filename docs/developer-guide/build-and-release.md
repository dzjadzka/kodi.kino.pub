# Build and release

Makefile automates packaging and deployment.

## Targets
- `make video_addon VERSION=x.y.z` — builds `video.kino.pub-<VERSION>.zip` from `src/` (addon.xml templated with VERSION) and resources.
- `make repo_addon` — builds `repo.kino.pub.zip` from `repo_src/` assets.
- `make repo VERSION=x.y.z` — runs both builds, generates `repo/addons.xml` (with md5), places addon/repo zips in `repo/` tree.
- `make deploy VERSION=x.y.z NETLIFY_AUTH_TOKEN=... NETLIFY_SITE_ID=...` — runs `repo` then deploys `repo/` to Netlify via podman `quay.io/quarck/netlify`.
- `make clean` — removes build artifacts and repo/ directory.

## Inputs/outputs
- Inputs: `src/addon.py`, `src/resources/**`, `LICENSE`, `repo_src/addon.xml`, `repo_src/icon.png`.
- Outputs: add-on zip(s) and repository structure under `repo/` for hosting.

## Environment variables
- `VERSION` required for video_addon/repo/deploy.
- `NETLIFY_AUTH_TOKEN`, `NETLIFY_SITE_ID` required for deploy target.

## Sources
- Makefile
