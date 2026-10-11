# Project-local Libraries

Open ../RayRigAntSw.kicad_pro with KiCad 9. Both library tables resolve through
KIPRJMOD to this directory. No global Ray or MyFootprints library or vendor 3D
model is required.

Definitions preserve the working schematic pins and placed PCB geometry. The
RCJ-021_1 embedded symbol alias is retained. Library references and
footprint-selection metadata were reconciled without changing connectivity.

## Original Custom Footprints

RF StateSide's owner personally created the SO-239, RCA, capacitor and
connection/RF-pad footprints in the MyFootprints/MyConnectors collection. The
included SO_239, CUI_RCJ-021, CAPRR500W50L730T250H650, Conn_Tp1 and Conn_Pad_Tp
definitions are covered as original project contributions.

## Upstream Material

Standard KiCad-derived symbols, stock footprints and retained upstream elements
remain attributed to KiCad library contributors under CC-BY-SA-4.0 with the
KiCad-libraries-exception. Original footprint authorship does not relicense
every symbol or erase upstream starting material.

Retain LICENSE-KiCad.md and KiCad-libraries-exception.txt with this mixed
collection. Full terms:
https://creativecommons.org/licenses/by-sa/4.0/legalcode

See [asset provenance](../../docs/provenance.md) for scope. Optional 3D models
are omitted. Library field orientations can differ from individual placed
display fields; the placed source remains the authority for assembly.
