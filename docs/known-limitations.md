# Known limitations

This is an AS-IS engineering reference. Original assembled hardware was tested
successfully with RaySspaController, with the historical diode orientation
workaround. The corrected CAD and P2-prep-01 manufacturing set have not been
physically fabricated or tested.

No RF power rating, isolation, insertion loss, return loss, operating frequency
range, switching lifetime or hot-switching rating is established here.
General-purpose relay contact ratings are not RF system ratings. No
certification, guaranteed performance, continued development or technical
support is promised.

## Retained source-check findings

KiCad 9.0.7 reports four PCB clearance errors at C3 against the existing 2.0 mm
ground-zone clearance: measured clearances are approximately 1.7045–1.8223 mm.
These are present in the original design. Zero unconnected PCB items and zero
schematic/PCB parity issues are reported for the prepared project. The
fabrication outputs preserve this geometry. The standalone check also reports
two self-intersecting courtyard findings on J6. The footprint outline is
unchanged; these findings concern retained non-copper geometry. The package is
not DRC-clean; assess the retained spacing with the fabricator and intended
application before ordering.

Nine schematic ERC findings remain: two externally supplied power nets lacking
an output-power declaration, six warnings involving unspecified RCA symbol pin
types, and one unconnected wire endpoint. The original schematic reports those
same categories. These have not been hidden by lowering rule severities.
Original and prepared schematic electrical net partitions are identical.

Full validation details are in [the engineering
audit](../PUBLIC_RELEASE_AUDIT.md). These checks verify source consistency, not
physical performance.

## Electrical and RF use

Use suitably protected +12 V wiring, drivers rated for the actual coil loads,
and appropriate grounding. Disconnect power and RF before wiring or servicing.
Prevent RF transmission during relay transitions. RF energy and amplifier
circuitry can cause burns, shock or equipment damage. Evaluate enclosure,
connectors, wiring, grounding and applicable operating requirements for the
complete installation.

The board itself does not prevent simultaneous transmit requests or establish
safe sequencing. That responsibility belongs to the external controller and
integrated station.
