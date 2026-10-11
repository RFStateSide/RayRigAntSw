# Integration

The board requires +12 V DC and external low-side coil drivers, such as a
suitable transistor array or MOSFET stage. MCU pins must not drive the coils
directly. The logic voltage and active level depend on the external driver.
Size its current/voltage capability from the fitted relay datasheet, including
two coils on TXRX and all simultaneously energized coils. Return coil current
to the supply with suitable wiring and common reference.

## J8 — eight positions

| Pin | Signal | Function |
|---|---|---|
| 1 | GND | Supply and control reference |
| 2 | ANT_R1 | Low-side return for K1 |
| 3 | ANT_R2 | Low-side return for K2 |
| 4 | TXRX | Low-side return for K3 and K4 together |
| 5 | RIG_AB | Low-side return for K5 |
| 6 | PTT-1 | J7 center contact; rig 1 PTT routed to controller |
| 7 | PTT-2 | J6 center contact; rig 2 PTT routed to controller |
| 8 | +12 V | Relay supply |

PTT jack shells connect to ground. These are routed connections, not onboard
logic inputs with isolation or guaranteed voltage tolerance. Provide
controller-side sensing, pull-ups, protection and grounding appropriate to the
connected rigs. The connector's historical 01x10 value was misleading; the
actual symbol, pads and pinout have eight positions.

## Relay truth tables

Here 1 means coil energized (driver sinks current), not a particular MCU logic
level.

| ANT_R1 / K1 | ANT_R2 / K2 | Selected antenna |
|---|---|---|
| 0 | 0 | ANT-1, J3 |
| 0 | 1 | ANT-1, J3; K2 has no effect on the selected path |
| 1 | 0 | ANT-2, J2 |
| 1 | 1 | ANT-3, J1 |

| RIG_AB / K5 | Selected rig |
|---|---|
| 0 | RIG-1, J5 |
| 1 | RIG-2, J4 |

| TXRX / K3 and K4 | Route |
|---|---|
| 0 | Selected rig to selected antenna through bypass |
| 1 | Selected rig to J9/RFlow (amplifier input); J10/RFhigh (amplifier output) to selected antenna |

J11 is the adjacent RF ground connection. With all coils de-energized the
static route is RIG-1 to ANT-1 through bypass. The table describes settled
contacts, not transient contact timing or a guaranteed safe state.

## Sequencing and RaySspaController

RaySspaController supplied the external drivers and integration used in the
original test. The board contains no MCU, firmware, autonomous PTT arbitration
or independent transmitter interlock.

The external controller must inhibit RF during antenna, rig and path changes;
handle conflicting PTT requests; allow appropriate relay settling; and sequence
amplifier enable/bias around RF path switching. Releasing ANT_R1 selects ANT-1
rather than disconnecting every antenna. Do not treat an antenna-switching
software comment as proof of a board-wide break interval.

No guaranteed timing is specified here. Determine timing from the fitted
relays, driver/suppression circuit and system requirements. The diode plus
capacitor network affects coil release. No hot-switching capability is claimed.
