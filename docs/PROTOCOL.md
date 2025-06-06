# Communication Protocol

Preliminary notes on the packet format used by Fardriver controllers as
observed in the decompiled firmware.

## Packet Structure

| Byte | Description                               |
|-----:|-------------------------------------------|
| 0    | Start byte `0xAA`                         |
| 1    | Length (`command` + `data` + CRC bytes)   |
| 2    | Command identifier                        |
| 3..N-3 | Payload bytes                           |
| N-2..N-1 | CRC16-IBM (little endian) over bytes 0..N-3 |

The length field matches the behaviour of :class:`DataParser` and therefore
includes the command byte, payload bytes and the two CRC bytes.

