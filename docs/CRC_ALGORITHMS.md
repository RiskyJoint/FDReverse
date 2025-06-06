# CRC Algorithms

The firmware calculates a standard CRC-16-IBM checksum using polynomial
`0xA001` and an initial value of `0xFFFF`.  The Python implementation can be
found in `src/communication/crc.py`.

Pseudo-code:

```
crc = 0xFFFF
for byte in data:
    crc ^= byte
    for _ in range(8):
        if crc & 1:
            crc = (crc >> 1) ^ 0xA001
        else:
            crc >>= 1
return crc & 0xFFFF
```

