# Decompile Progress Notes

This document tracks ongoing findings from reviewing `Fulldecompile.c` as outlined in the README's **Decompile Analysis Guide**.

## Initial Observations
- The file is extremely large (~725k lines) and appears to be output from a decompiler.
- Functions use low-level variable names such as `FUN_00401000`, indicating automatic symbol generation.

## Packet Framing
- Several array initializations include the value `0xAA`, likely the protocol start byte. Example occurrences:
  - `local_b98[0x2f] = 0xaa` (around line 5345)
  - `local_b98[0x40] = 0xaa` (around line 5362)
  - `local_b98[0x11f] = 0xaa` (around line 5585)

## Serial Port Handling
- References to `CSerialPort::vftable` appear near line 49184, suggesting an object-oriented serial port implementation.
- Assertions reference `serialport.cpp`, hinting that this section was originally C++ source.
- Function `FUN_00472f90` opens COM ports using `CreateFileA` with paths like
  `\\.\\COM%d` and configures timeouts via `SetCommTimeouts`.
- `GetCommState` and `SetCommState` manipulate a DCB structure to apply baud
  rate and parity settings.

## Parameter Offsets
Recent scanning around lines 31k uncovered several hardcoded offsets. The value
stored at `local_1c + 0x9d40` is repeatedly printed as an RPM counter. When
`0x9e84` is greater than `0x10` the firmware multiplies this RPM value by four
and divides by the `0x9e84` register. This strongly suggests that `0x9e84`
provides a divisor used to scale the raw speed for display, likely taking the
gear ratio or field-weakening into account.

Additional offsets identified:

- `0x9d24` – bus voltage (divide by 10)
- `0x9d28` – bus current (divide by 4)
- `0x9d48` – throttle voltage sensor
- `0xa074` – brake voltage sensor
- `0x9e38` – output current *Iq*
- `0x9e3c` – output current *Id*

## Next Steps
- Identify where packets are parsed by searching for length fields immediately following the start byte.
- Locate checksum logic by scanning for constants such as `0xA001` or loops operating on message bytes.
- Map command codes to functions by examining switch statements or large `if/else` chains that handle packet `command` fields.

- Trace handling of throttle and brake voltage around offsets `0x9d48` and `0xa074`.
- Locate configuration data near `0x9e9c` to determine throttle mapping tables.

