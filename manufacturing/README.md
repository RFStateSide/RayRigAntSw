# Manufacturing — P2-prep-01

The P2-prep-01 directory contains newly generated KiCad 9.0.7 Gerbers, separate
plated/non-plated Excellon drills, a component-position reference, reconciled
BOM and license notices. They derive from hardware/RayRigAntSw.kicad_pcb and
match the corrected diode assignments.

This is the manufacturing reference for the supplied design. It is not the
historical PCBWay order and has not been fabricated. It retains four C3/zone
clearance-rule violations and two J6 courtyard findings; read
../PUBLIC_RELEASE_AUDIT.md and ../docs/known-limitations.md before ordering.

Use the complete set: front/back copper, masks and silkscreen, board outline
and both drill files. No solder-paste stencil is required by the through-hole
assembly represented here. Placement CSV is a reference for this through-hole
design, not a validated automated assembly program.

The geometry is an 85 mm by 130 mm, two-copper-layer board. Confirm substrate,
thickness, copper weight, finish, holes, mechanical fit and fabrication
capabilities for your build; this package does not establish the original
order's full stackup or a guaranteed RF rating.

Both earlier fabrication sets retained reversed D1–D5. They are intentionally
excluded from this current output folder. Current pad 1 / cathode goes to +12 V
for all five diodes. The original v2.0 silkscreen remains, while the package
and Gerber project attributes identify P2-prep-01.

Regenerate using Python tools/generate.py --kicad-cli <path-to-kicad-cli>, then
run tools/verify.py. Regeneration may change tool timestamps and requires a new
integrity manifest. Do not combine outputs from different source revisions.
