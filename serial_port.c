#include "serial_port.h"
#include <stdio.h>
#include <stdlib.h>

SerialPort *serial_open(int port, DWORD baud, char parity, int data_bits, int stop_bits, DWORD mask) {
    char port_name[32];
    SerialPort *sp = (SerialPort *)calloc(1, sizeof(SerialPort));
    if (!sp) return NULL;
    sprintf(port_name, "\\\\.\\COM%d", port);
    sp->handle = CreateFileA(port_name, GENERIC_READ | GENERIC_WRITE, 0, NULL,
                             OPEN_EXISTING, FILE_ATTRIBUTE_NORMAL, NULL);
    if (sp->handle == INVALID_HANDLE_VALUE) {
        free(sp);
        return NULL;
    }

    DCB dcb;
    SecureZeroMemory(&dcb, sizeof(dcb));
    dcb.DCBlength = sizeof(dcb);
    if (!GetCommState(sp->handle, &dcb)) {
        CloseHandle(sp->handle);
        free(sp);
        return NULL;
    }
    dcb.BaudRate = baud;
    dcb.ByteSize = (BYTE)data_bits;
    dcb.Parity = parity;
    dcb.StopBits = (BYTE)stop_bits;
    if (!SetCommState(sp->handle, &dcb)) {
        CloseHandle(sp->handle);
        free(sp);
        return NULL;
    }

    SetCommMask(sp->handle, mask);

    COMMTIMEOUTS timeouts = {0};
    timeouts.ReadIntervalTimeout = 1000;
    timeouts.ReadTotalTimeoutConstant = 1000;
    timeouts.ReadTotalTimeoutMultiplier = 0;
    timeouts.WriteTotalTimeoutConstant = 1000;
    timeouts.WriteTotalTimeoutMultiplier = 0;
    SetCommTimeouts(sp->handle, &timeouts);
    PurgeComm(sp->handle, PURGE_RXCLEAR | PURGE_TXCLEAR);
    return sp;
}

BOOL serial_write(SerialPort *sp, const void *buf, DWORD len) {
    DWORD written = 0;
    return WriteFile(sp->handle, buf, len, &written, NULL);
}

BOOL serial_read(SerialPort *sp, BYTE *byte) {
    DWORD read = 0;
    if (!ReadFile(sp->handle, byte, 1, &read, NULL)) return FALSE;
    return read == 1;
}

void serial_close(SerialPort *sp) {
    if (!sp) return;
    if (sp->handle != INVALID_HANDLE_VALUE) {
        CloseHandle(sp->handle);
    }
    free(sp);
}
