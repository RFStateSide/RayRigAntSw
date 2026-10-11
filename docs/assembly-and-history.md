# Assembly and design history

PCBWay manufactured the original through-hole boards. RF StateSide assembled
them and successfully tested them with RaySspaController. The original
fabrication had D1–D5 polarity reversed. The owner installed the two-lead
diodes opposite the original PCB markings, producing the correct electrical
orientation. Current CAD incorporates that correction; it was not refabricated.

## Correct diode assembly

| Reference | Cathode (banded end), pad 1 | Anode, pad 2 |
|---|---|---|
| D1 | +12 V | ANT_R1 |
| D2 | +12 V | ANT_R2 |
| D3, D4 | +12 V | TXRX |
| D5 | +12 V | RIG_AB |

Use this electrical mapping and the corrected P2-prep-01 files. Instructions to
reverse the original markings apply only to the historical boards, not to this
corrected manufacturing set.

K1–K5 are SPDT relays with 12 V coils; the historical procurement reference is
Omron G2RL-14-E DC12. C1–C5 are 10 nF capacitors across the coils, with 1N5819
flyback diodes. They are not resistor-capacitor snubbers. C6 is the 47 µF
supply capacitor; its historical BOM lists a ceramic part, not a polarized
electrolytic. Check fitted-part identity, lead spacing and mechanical fit
against the source and current datasheet before substitution.

## Traceability

- Parent development commit: 16a368223ca7a0ed1fe5bd94f67c9646acec9313,
  September 9, 2025. Release preparation uses later uncommitted corrected
  files, not that commit alone.
- Original active schematic: RigAmpAntSw, revision 1.1, dated October 9, 2025.
- Original active PCB: title RayAmpAntSw, revision 2.0, dated September 9,
  2025; artwork says RayRigAntSwitch v2.0.
- October 9 backups bracket corrected PCB diode assignments between 15:08:51
  and 15:17:29.
- Active PCB exactly matches the November 13, 2025 02:25:32 backup.
- Root fabrication ZIP was generated August 28, 2025; the dated PCBWay package
  was generated September 9, 2025. Both retain pre-correction polarity. Neither
  is included as current manufacturing data.
- Exact historical order-to-package association is not established.

P2-prep-01 reconciles titles, local libraries and administrative metadata.
Existing v2.0 silkscreen remains to preserve artwork. New output files identify
P2-prep-01; do not distinguish old/new fabrication solely by the v2.0 marking.
Baseline hashes are in source-traceability.json; prepared-file integrity is in
the root manifest.

Original archives remain in the private development locations. No further
physical test result is claimed.
