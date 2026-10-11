# RayRigAntSw

RayRigAntSw is RF StateSide LLC's through-hole RF relay board for selecting two
rigs, three antennas and an amplifier/bypass path.

**Public Engineering Reference — AS-IS.** The editable design, BOM and
manufacturing files support study, independent construction, modification and
community improvement.

## Overview

Five 12 V SPDT relays provide RF routing through external low-side drivers. Two
PTT connections pass to the external controller. RaySspaController supplied the
drivers and sequencing used in our original integration test; another
controller can use the documented interface.

The original PCBWay boards were assembled and successfully tested. D1–D5 were
installed opposite the original PCB markings to obtain correct electrical
polarity. The supplied CAD includes the subsequent correction and was not
refabricated. See [assembly and history](docs/assembly-and-history.md).

## Hardware and Integration

Open [the KiCad 9 project](hardware/RayRigAntSw.kicad_pro). Required symbols
and footprints are included in project-local libraries. Optional 3D models are
not required or bundled.

The [integration guide](docs/integration.md) provides the eight-pin J8
interface, relay truth tables and external-driver requirements. The board does
not enforce transmitter arbitration or switching delays; those responsibilities
belong to the external controller.

[View schematic](docs/images/RayRigAntSw.svg) · [View PCB
front](docs/images/pcb-front.svg)

## Manufacturing and Assembly

Use the [BOM](bom/RayRigAntSw.csv) with the [P2-prep-01 manufacturing
set](manufacturing/README.md). This identifier ties the corrected sources to
their outputs; it does not identify a newly tested board. The original v2.0
silkscreen is retained.

Four inherited clearance findings, two J6 courtyard findings and nine schematic
ERC findings are documented in the [engineering
audit](PUBLIC_RELEASE_AUDIT.md). The supplied files are not represented as
DRC/ERC-clean. Assess the retained findings and component/mechanical
suitability before manufacture.

## Repository Contents

| Location | Contents |
|---|---|
| [hardware/](hardware/) | Editable KiCad project and local libraries |
| [bom/](bom/) | Component and procurement reference |
| [manufacturing/](manufacturing/) | Corrected Gerbers, drills and assembly references |
| [docs/](docs/) | Integration, assembly, limitations and provenance |
| [tools/](tools/) | Output generation and verification utilities |
| [PUBLIC_RELEASE_AUDIT.md](PUBLIC_RELEASE_AUDIT.md) | Attributed engineering verification evidence |

Original fabrication archives and internal review records are retained
separately. No parent firmware or development-repository history is included.

## Development Tools

KiCad was used for schematic capture and PCB design. Python utilities support
source verification and manufacturing-package integrity checks. Git and GitHub
are the intended version-control and distribution tools.

ChatGPT by OpenAI and OpenAI Codex assisted with engineering review,
documentation, source organization, validation and preparation of the
open-hardware reference. RF StateSide LLC performed the original hardware
design, assembly and historical integration testing.

## Known Limitations

No guaranteed RF power handling, isolation, insertion loss, frequency range,
hot-switching capability or certification is claimed. The corrected CAD has not
been physically refabricated. No future development or technical support is
promised. Read [known limitations](docs/known-limitations.md).

## License

Copyright RF StateSide LLC. Original project contributions are provided under
**CERN-OHL-P v2.0**, SPDX **CERN-OHL-P-2.0**. The unmodified [LICENSE](LICENSE)
is authoritative; retain [NOTICE](NOTICE) and applicable third-party notices.

See [licensing](docs/licensing.md) and [provenance](docs/provenance.md) for
scope and separately licensed material.

## Credits and Acknowledgments

RF StateSide LLC developed the original hardware and custom footprints. KiCad
library contributors supplied the upstream elements identified in the library
notices. Procurement references identify candidate parts and do not establish
the identity or fit of every historically installed component.
