# Global HQ profile assets

## Original artwork

The network diagram and four node badges in this folder were authored for the `000MAK/000MAK` profile. The SVG files are the editable vector sources. `global-hq-network.gif` and `hq-node-badges.gif` are generated animated exports so movement can be displayed in GitHub profile README views where SVG animation may be restricted.

No third-party images, logos, datasets, or copied artwork are included. “Wifeyjoma” is the partner label provided by the profile owner.

## Architecture meaning and limits

The topology is a conceptual portfolio operating model. It does not claim active network connectivity, physical office ownership, live system integration, or permission to transfer confidential, corporate, academic, or personal data. Use approved, least-privilege workflows only.

## Build dependencies and attribution

- [CairoSVG](https://github.com/Kozea/CairoSVG) 2.8.2 — SVG rasterization; LGPL-3.0-or-later. No CairoSVG code is copied into this repository.
- [Pillow](https://github.com/python-pillow/Pillow) 12.3.0 — GIF frame rendering and optimization; HPND license. No Pillow code is copied into this repository.
- [actions/checkout](https://github.com/actions/checkout) and [actions/setup-python](https://github.com/actions/setup-python) are used by the rendering workflow; both projects are MIT-licensed.

Versions are pinned in `requirements-profile-assets.txt`. Review upstream license files before upgrading dependencies. The system Cairo shared library is installed by the CI runner package manager and is not redistributed here.
