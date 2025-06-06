# FDReverse
FarDriver PC Software Reverse Engineer.

## Building

This project is a collection of decompiled sources. To build the helper code
added in this repository use a Windows toolchain that provides the Win32 API
(e.g. Visual Studio).  Compile all `*.c` files in the repository.

## Serial Port Helper

`serial_port.c` and `serial_port.h` implement a small wrapper around the Win32
serial API.  Typical usage:

```c
SerialPort *port = serial_open(1, 19200, 'N', 8, 1, EV_RXCHAR);
if (port) {
    BYTE b;
    serial_read(port, &b);
    serial_write(port, &b, 1);
    serial_close(port);
}
```

The main application now uses these helpers instead of the previously
decompiled `FUN_0047xxxx` routines.
