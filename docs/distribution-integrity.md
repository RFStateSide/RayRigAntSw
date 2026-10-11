# Source and Distribution Integrity

P2-prep-01 identifies the corrected editable design and matching manufacturing
outputs. The original v2.0 board artwork is retained and cannot by itself
distinguish historical fabrication from this set.

SHA256SUMS at the repository root records file hashes for this distribution.
Run the verifier from the repository root:

```text
python tools/verify.py --kicad-cli <kicad-cli executable>
```

The verifier checks the manifest, local definitions, schematic/PCB net
partitions, BOM coverage, diode Gerber attributes and coordinates, and drill
correspondence. The retained DRC/ERC findings are explicit expectations, not a
clean-check claim. See [the audit](../PUBLIC_RELEASE_AUDIT.md).

To regenerate outputs after an intentional source change:

```text
python tools/generate.py --kicad-cli <kicad-cli executable>
python tools/verify.py --kicad-cli <kicad-cli executable> --record
```

Generation uses KiCad 9 and does not redesign the editable source. Inspect the
resulting outputs and reports. Regeneration changes timestamps and invalidates
the current manifest; review and produce a new manifest before distribution.
The --record option records check results but does not renew SHA256SUMS.

Keep source, BOM and manufacturing data together. Do not mix the supplied
outputs with either historical pre-correction fabrication archive.
