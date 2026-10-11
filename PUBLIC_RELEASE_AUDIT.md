# RayRigAntSw — Public Release Engineering Audit

## Scope and Authorship

Prepared with OpenAI Codex. Reviewed by RF StateSide LLC.

RF StateSide LLC performed the original hardware design, assembly and
integration testing. This audit records source and manufacturing checks, not an
independent laboratory certification or a new physical test.

Record date: 2026-10-11. Engineering source/output identifier: P2-prep-01.

## Historical Hardware and Supplied Design

PCBWay fabricated the original through-hole boards. RF StateSide assembled them
and successfully tested them with RaySspaController. D1–D5 were installed
opposite the original markings to obtain correct electrical polarity.

The supplied design incorporates the later KiCad polarity correction. No
additional boards were fabricated after it. Both older fabrication packages
retain the reversed assignment and are excluded from the supplied outputs.

The original active PCB matches the November 13, 2025 backup. October 9 backups
bracket the correction between 15:08:51 and 15:17:29. [Source
traceability](docs/source-traceability.json) records baseline hashes and the
parent development commit. The corrected working files are later than that
committed baseline.

## Source Preservation

Comparisons with the original corrected design preserved schematic electrical
connections and graphics, symbol pin definitions, PCB tracks, pads, placements,
zones/fills and artwork.

Administrative changes localized libraries, reconciled project/title/revision
identifiers and footprint-selection metadata, corrected J8's descriptive value
to eight positions, and omitted optional 3D references. The original v2.0
silkscreen remains. The standalone documentation revision does not change
engineering files or fabrication data.

## Verification Results

KiCad 9.0.7 and Python checks established:

|Check|Result|
|-|-|
|Component coverage|All 27 references accounted for|
|Schematic/PCB pin-net partitions|Identical|
|KiCad schematic parity|Zero issues|
|Unconnected PCB items|Zero|
|Project portability|Required definitions resolve from local tables at a relocated path|
|D1–D5|Cathode/pad 1 connects to +12 V in source and generated copper attributes|
|Diode manufacturing positions|All ten Gerber pad coordinates match the PCB|
|Drills|All 141 holes match source centers and diameters within 0.001 mm output quantization|
|BOM|Reference, quantity, value and footprint correspondence checked|
|Source renderings|Schematic and PCB-front exports visually inspected|
|Distribution integrity|SHA256SUMS covers the supplied file set|

[Machine-readable checks](docs/validation/checks.json),
[DRC](docs/validation/drc.json), [ERC](docs/validation/erc.json) and
[generation commands](docs/validation/generation.json) retain the relevant
technical evidence. Internal selection checklists and workstation records are
kept separately.

## Retained Findings

Four inherited C3-to-ground-zone clearance errors remain against the existing
2.0 mm rule: reported spacing is approximately 1.7045–1.8223 mm. No rule was
weakened and no copper was moved to suppress the findings.

The standalone check additionally reports two self-intersecting courtyard
findings on J6. The CAD and footprint files are byte-identical to P2-prep-01,
confirming retained non-copper outlines rather than a transfer change. The
current total is six DRC findings. The earlier report listed four clearance
findings only; this audit records the fuller current result.

Nine inherited schematic ERC findings remain: two externally supplied power
nets without an output-power declaration, six unspecified RCA-pin warnings, and
one unconnected wire endpoint. These categories are also present in the
original source.

Checks use the retained project rule configuration. The project is not
DRC/ERC-clean. Zero connectivity/parity findings do not establish RF
performance or constitute unconditional fabrication acceptance.

## Licensing and Provenance

The owner approved CERN-OHL-P-2.0 for original hardware contributions and
confirmed personal creation of the custom footprints previously in question.
The earlier custom-footprint origin uncertainty is resolved by that firsthand
confirmation. Applicable KiCad notices remain for upstream-derived material.

The official CERN text is unchanged and matches its recorded reference hash.
See [licensing](docs/licensing.md) and [provenance](docs/provenance.md).

## Practical Limits

No RF rating, isolation, frequency range, switching lifetime, hot-switching
capability or certification is established. External drivers and controller
sequencing are required. The corrected manufacturing set has not been
physically fabricated or tested.

Read [integration](docs/integration.md), [assembly
history](docs/assembly-and-history.md), and [known
limitations](docs/known-limitations.md) before reproduction.

