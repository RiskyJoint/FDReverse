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
Recent scanning around lines 31k uncovered several hardcoded offsets. The value stored at `local_1c + 0x9d40` is repeatedly printed as an RPM reading, while the variable at `local_1c + 0x9e84` acts as a divisor when it exceeds `0x10`. These addresses likely correspond to the motor speed register and a scaling factor for gear ratio or field weakening.

## Next Steps
- Identify where packets are parsed by searching for length fields immediately following the start byte.
- Locate checksum logic by scanning for constants such as `0xA001` or loops operating on message bytes.
- Map command codes to functions by examining switch statements or large `if/else` chains that handle packet `command` fields.

