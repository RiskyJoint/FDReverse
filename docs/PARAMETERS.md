# Parameter Map

Known parameter IDs extracted so far.  These will expand as decompilation
continues.

| ID   | Name             | Units |
|-----:|------------------|-------|
|0x0001|`motor_speed_rpm` | rpm   |
|0x0002|`bus_voltage_v`   | volts |
|0x0003|`bus_current_a`   | amps  |
|0x0004|`motor_temp_c`   | °C    |
|0x0005|`id_out_a`        | amps  |
|0x0006|`iq_out_a`        | amps  |
|0x0007|`throttle_voltage_v`| volts |
|0x0008|`brake_voltage_v`| volts |
|0x0009|`rpm_divisor`     | n/a   |

## Firmware Offsets

| Offset | Description                |
|-------:|----------------------------|
|`0x9d40`|Motor RPM counter           |
|`0x9e84`|RPM divisor                 |
|`0x9d24`|Bus voltage raw (÷10)       |
|`0x9d28`|Bus current raw (÷4)        |
|`0x9d48`|Throttle voltage sensor     |
|`0xa074`|Brake voltage sensor        |
|`0x9e38`|Output current IQ (×0.1A)   |
|`0x9e3c`|Output current ID (×0.1A)   |

