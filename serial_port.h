#ifndef SERIAL_PORT_H
#define SERIAL_PORT_H

#include <windows.h>

#ifdef __cplusplus
extern "C" {
#endif

typedef struct SerialPort {
    HANDLE handle;
} SerialPort;

SerialPort *serial_open(int port, DWORD baud, char parity, int data_bits, int stop_bits, DWORD mask);
BOOL serial_write(SerialPort *sp, const void *buf, DWORD len);
BOOL serial_read(SerialPort *sp, BYTE *byte);
void serial_close(SerialPort *sp);

#ifdef __cplusplus
}
#endif

#endif // SERIAL_PORT_H
