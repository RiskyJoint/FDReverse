# Fardriver Dashboard 2.0 Skeleton

This project provides a minimal starting point for a cross-platform dashboard
used to communicate with Fardriver motor controllers. The repository includes a
Qt user interface, basic communication helpers, and feature stubs for logging,
tuning, dyno testing, and efficiency calculations.

The full protocol implementation is pending analysis of the decompiled
`Fulldecompile.c` firmware. Only the CRC algorithm and basic packet encoding are
provided.

## Components

- **src/communication** – Packet encoding, CRC, and serial-port utilities.
- **src/parsing** – Minimal message parser and parameter decoding map.
- **src/features** – Stubs for logging, tuning, dyno, and efficiency modules.
- **src/ui** – `NEWDASH.ui` Qt interface loaded by `Dashboard`.
- **tests** – Basic unit tests for CRC and serial port enumeration.

## Usage

```
python -m src.main
```

The application requires PySide6 for the UI. Serial port functionality works
without external dependencies and attempts to list common device names on both
Windows and Unix-like systems.
