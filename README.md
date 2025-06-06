# FARDRIVER DASHBOARD 2.0 - COMPLETE DEVELOPMENT GUIDE

## 🚨 CRITICAL: THIS IS A GROUND-UP REBUILD PROJECT

This document serves as the complete blueprint for recreating the Fardriver Dashboard application using ONLY the decompiled controller firmware (`fulldecompile.c`) and the UI file (`NEWDASH.ui`). The old version has been deprecated due to missing features and outdated architecture.

---

## 📋 TABLE OF CONTENTS

1. [Project Overview](#project-overview)
2. [Architecture Requirements](#architecture-requirements)
3. [UI Components & Functionality](#ui-components--functionality)
4. [Controller Communication Protocol](#controller-communication-protocol)
5. [Data Parsing Requirements](#data-parsing-requirements)
6. [Feature Implementation Guide](#feature-implementation-guide)
7. [Cross-Platform Considerations](#cross-platform-considerations)
8. [Testing & Validation](#testing--validation)

---

## 🎯 PROJECT OVERVIEW

### Mission Statement
Create a professional-grade electric vehicle dashboard that communicates with Fardriver motor controllers. This software must extract ALL possible data from the controllers using ONLY information found in the decompiled firmware.

### Critical Requirements
- ✅ **Universal Compatibility**: Must work with ALL Fardriver controller models
- ✅ **Cross-Platform**: Windows and Raspberry Pi support
- ✅ **Full Feature Set**: Logging, tuning, real-time monitoring
- ✅ **CRC Validation**: Proper checksum calculation for all communications
- ✅ **Professional Grade**: OEM-level quality and reliability

### What You're Building
A complete monitoring and tuning solution that:
1. Displays real-time data from up to 3 motor controllers
2. Logs all parameters to CSV files
3. Allows configuration changes
4. Performs dyno testing
5. Monitors battery status
6. Calculates efficiency metrics

---

## 🏗️ ARCHITECTURE REQUIREMENTS

### File Structure
```
FardriverDashboard2.0/
├── src/
│   ├── main.py                 # Application entry point
│   ├── ui/
│   │   ├── dashboard.py        # Main window controller
│   │   └── NEWDASH.ui          # Qt Designer UI file
│   ├── communication/
│   │   ├── serial_handler.py   # Serial port management
│   │   ├── protocol.py         # Fardriver protocol implementation
│   │   └── crc.py              # CRC calculation module
│   ├── parsing/
│   │   ├── data_parser.py      # Message parsing logic
│   │   ├── parameter_map.py    # Memory address mappings
│   │   └── value_decoder.py    # Raw value to engineering units
│   ├── features/
│   │   ├── logging.py          # CSV logging functionality
│   │   ├── tuning.py           # Parameter modification
│   │   ├── dyno.py             # Dyno testing module
│   │   └── efficiency.py       # Economy calculations
│   └── config/
│       ├── settings.json       # User preferences
│       └── controllers.json    # Controller configurations
├── docs/
│   ├── PROTOCOL.md            # Communication protocol details
│   ├── PARAMETERS.md          # Parameter definitions
│   └── CRC_ALGORITHMS.md     # CRC calculation methods
├── tests/
│   └── ...                    # Unit tests
└── README.md                  # This file
```

### Core Technologies
- **Language**: Python 3.8+
- **UI Framework**: PySide6 (Qt6)
- **Serial Communication**: pySerial
- **Data Visualization**: Matplotlib
- **Cross-Platform**: Automatic OS detection

---

## 🖥️ UI COMPONENTS & FUNCTIONALITY

### Main Dashboard (Tab 1: SIMPLE)
This is the simplified view for casual users.

#### Components:
1. **Large Speedometer** (`simplifiedSpeedLCD`)
   - Display: Current vehicle speed in MPH
   - Range: 0-999 MPH
   - Update Rate: 10Hz minimum

2. **Range Display** (`simpleRangeValue`)
   - Shows estimated miles remaining
   - Color coding: Green (>50mi), Yellow (20-50mi), Red (<20mi)

3. **Drive Mode Indicator** (`gearIndicatorLabel`)
   - Shows: D (Drive), R (Reverse), N (Neutral)
   - Background changes color based on mode

4. **Warning Labels**
   - `speedWarningLabel`: Appears when speed >60mph
   - `throttleWarningLabel`: Shows when throttle >80%

### Main Dashboard (Tab 2: DASHBOARD)
Professional view with complete information.

#### Power Display Section:
1. **Total Power LCD** (`totalPowerLCD`)
   - Shows combined power from all motors in Watts
   - 5-digit display (up to 99,999W)
   - Updates in real-time

2. **Speed Display** (`speedLCD`)
   - Vehicle speed in MPH
   - 3-digit display

3. **Odometer** (`odometerLabel`)
   - Total miles driven
   - Format: "ODO: X,XXX.X mi"

#### Individual Motor Sections (3 identical blocks):
Each motor (Front Left, Front Right, Rear) has:

1. **Power Display** (`motor1PowerValue`, etc.)
   - Individual motor power in kW
   - Precision: 0.1 kW

2. **RPM Display** (`motor1RPMValue`, etc.)
   - Motor shaft RPM
   - Update when RPM > 0

3. **Speed Display** (`motor1MPHLabel`, etc.)
   - Individual wheel speed
   - Calculated from RPM and gear ratio

4. **Temperature Bars**
   - Motor temp (`motor1MotorTemp`): 0-150°C range
   - Controller temp (`motor1ControllerTemp`): 0-150°C range
   - Color gradient: Blue→Yellow→Red

5. **Throttle Display** (`motor1TPSValue`, etc.)
   - Individual throttle percentage
   - 0-100% range

6. **Slip/Traction Status**
   - Shows RPM difference between wheels
   - Slip percentage calculation
   - Traction status: OK/SLIP/ACTIVE

#### Battery Section:
1. **Battery Bar** (`batteryBar`)
   - Visual representation of charge level
   - Color gradient based on percentage

2. **Voltage Display** (`batteryVoltageLabel`)
   - Pack voltage in volts
   - Precision: 0.1V

3. **Voltage Drop Tracking**
   - Base voltage (no load)
   - Minimum voltage (under load)
   - Peak drop calculation
   - Power at peak drop

#### Mode Selection:
Four mode buttons that light up:
- **Wife Mode** (20 MPH limit) - Blue border when active
- **Fast Mode** (30 MPH limit) - Orange border when active  
- **Warp Mode** (Race) - Green border when active
- **Reverse** - Red border when active

### Battery Tab (Tab 3: BATTERY)
Complete battery management system integration.

#### Components:
1. **Pack Overview**
   - Total voltage display
   - Current flow (charge/discharge)
   - Power calculation
   - Temperature monitoring

2. **Cell Voltage Grid**
   - Individual cell voltages
   - Configurable for 16-30 cells
   - Color coding:
     - Green: Normal (3.2-4.15V)
     - Orange: Low (<3.2V)
     - Red: Critical (<3.0V or >4.15V)

3. **BMS Integration Panel**
   - Bluetooth device scanner
   - Connection status
   - Real-time data display

### Dyno Tab (Tab 4: DYNO)
Professional dynamometer functionality.

#### Controls:
1. **TPS Trigger** (`tpsTriggerInput`)
   - Sets throttle threshold to start recording
   - Range: 1-100%
   - Default: 20%

2. **Manual Start** (`manualStartCheckbox`)
   - Override automatic triggering

3. **Mode Selector** (`dynoModeSelector`)
   - All Motors (combined)
   - Front Left Only
   - Front Right Only
   - Rear Only

4. **Control Buttons**
   - Start Pull: Begin data collection
   - Stop Pull: End and analyze
   - Save Run: Store to disk
   - Export: Generate dyno sheet image

#### Display Elements:
1. **Main Graph** (`dynoPlotWidget`)
   - X-axis: Wheel RPM
   - Y-axis 1: Horsepower (blue)
   - Y-axis 2: Torque ft-lb (red)
   - Peak markers with annotations

2. **Performance Metrics**
   - 0-30 MPH time
   - 0-60 MPH time
   - Peak acceleration (G-force)

3. **Results Display**
   - Peak HP @ RPM
   - Peak Torque @ RPM
   - Maximum RPM achieved
   - Average power output

### Gear Tab (Tab 5: GEAR)
Critical configuration for accurate calculations.

#### Front Motor Configuration:
1. **Tire Size** (`frontTireSizeInput`)
   - Diameter in inches
   - Used for speed calculation

2. **Gear Ratio** (`frontGearRatioInput`)
   - Motor-to-wheel ratio
   - Default: 1 (hub motor)

3. **Pole Pairs** (`frontPolePairsInput`)
   - Motor pole pair count
   - Affects RPM calculation

#### Rear Motor Configuration:
Same fields but typically different values:
- Higher gear ratio (e.g., 8:1)
- Different pole pairs

#### Info Display:
Shows calculated values:
- Wheel circumference
- Speed per 1000 RPM

### Economy Tab (Tab 6: ECONOMY)
Efficiency tracking and analysis.

#### Real-time Metrics:
1. **Average Consumption** (`avgWhValue`)
   - Wh/mile calculation
   - Rolling average

2. **Estimated Range** (`estRangeValue`)
   - Based on current efficiency
   - Battery state consideration

3. **Amp-hours Used** (`ahUsedValue`)
   - Lifetime accumulator
   - Precision: 0.1 Ah

4. **Trip Efficiency** (`tripEffValue`)
   - Since last reset
   - Separate from average

#### Graphs:
1. **Efficiency Trend** (`effGraphWidget`)
   - 5-minute rolling window
   - Shows Wh/mile over time

2. **Range Estimation** (`rangeGraphWidget`)
   - Projected range history
   - Helps identify trends

#### Statistics:
- Best efficiency achieved
- Worst efficiency recorded
- Total miles driven
- Trip reset button

### Connections Tab (Tab 7: CONNECTIONS)
Serial port management for all controllers.

#### Components:
1. **Port Selection** (3 dropdowns)
   - Lists all available COM ports
   - Auto-detects on Windows/Linux/Mac

2. **Connection Buttons**
   - Apply: Connect to selected port
   - Refresh: Rescan ports

3. **Serial Display**
   - Shows controller serial number
   - Firmware version info

4. **Connection Log** (`connectionLog`)
   - Real-time status updates
   - Error messages
   - Color-coded entries

### Settings Tab (Tab 8: SETTINGS)
System configuration and preferences.

#### Battery Configuration:
1. **Cell Count** (`batteryCellsInput`)
   - Number of series cells
   - Range: 16-30

2. **Voltage Limits**
   - Min cell voltage (typically 3.0V)
   - Max cell voltage (typically 4.2V)

3. **Capacity** (`batteryCapacityInput`)
   - Pack capacity in Ah
   - Used for range calculations

#### Display Preferences:
1. **Temperature Units**
   - Celsius/Fahrenheit toggle
   - Affects all temperature displays

2. **Theme Selection**
   - Dark/Light mode toggle
   - Real-time switching

#### Logging Options:
1. **CSV Comment** (`csvCommentInput`)
   - Add notes to log files
   - 255 character limit

2. **Log Controls**
   - Start/Stop logging buttons
   - File naming configuration

#### Advanced Features:
1. **Max Values Display**
   - Show peak power recorded
   - Maximum phase currents
   - Voltage drop analysis

2. **Mileage Management**
   - Odometer offset capability
   - Reset with confirmation
   - Change logging

---

## 📡 CONTROLLER COMMUNICATION PROTOCOL

### Overview
The Fardriver protocol uses a specific packet structure that MUST be reverse-engineered from `fulldecompile.c`. 

### What to Look For:

1. **Packet Structure**
   - Look for byte arrays being constructed
   - Find patterns like `0xAA` (common start byte)
   - Identify packet length definitions

2. **Command Types**
   - Search for command enumerations
   - Look for switch/case statements handling different commands
   - Find command-response pairs

3. **CRC Calculation**
   - Search for CRC, checksum, or validation functions
   - Look for XOR operations or polynomial calculations
   - Multiple CRC types may exist for different controller versions

4. **Baud Rate & Serial Settings**
   - Look for serial initialization code
   - Find references to 19200, 38400, etc.
   - Check for data bits, stop bits, parity settings

## 📊 DATA PARSING REQUIREMENTS

### Memory Address Mapping
The decompiled code contains memory addresses for all parameters. You need to find:

1. **Live Data Addresses**
   - Voltage readings
   - Current measurements
   - RPM values
   - Temperature sensors
   - Throttle position
   - Example: `0x9d40` (RPM counter) scaled by `0x9e84`

2. **Configuration Addresses**
   - Motor settings
   - Current limits
   - Voltage limits
   - Protection thresholds

3. **Status/Error Addresses**
   - Fault codes
   - Warning flags
   - System status

### Value Conversion
Raw values need conversion to engineering units:

1. **Voltage**: Often in decivolts (value / 10)
2. **Current**: May be in quarters (value / 4)
3. **Temperature**: Could be raw ADC or Kelvin
4. **RPM**: Sometimes requires scaling factors


## 🛠️ FEATURE IMPLEMENTATION GUIDE

### 1. Real-time Monitoring
**Requirement**: Update all displays at minimum 10Hz

**Implementation Steps**:
1. Create serial communication thread
2. Continuously poll controller for data
3. Parse responses into data structures
4. Emit signals to update UI
5. Handle connection loss gracefully

**Critical Points**:
- Thread safety for data access
- Smooth UI updates without flicker
- Efficient data structures

### 2. CSV Logging
**Requirement**: Log all parameters with timestamps

**File Format**:
```csv
Time,FL_Voltage,FL_Current,FL_Power,FL_RPM,...[all parameters]...,Comment
HH:MM:SS.mmm,96.5,45.2,4361.4,3250,...,Test run 1
```

**Features**:
- Automatic file naming with timestamp
- Configurable logging rate
- Comment field for notes
- Automatic file rotation
- Implemented in `features/logging.py` via the `Logger` class

### 3. Parameter Tuning
**Requirement**: Modify controller settings safely

**Safety Features**:
1. Read current values first
2. Validate new values against limits
3. Require user confirmation
4. Use proper CRC for write commands
5. Verify write success

**Common Parameters**:
- Current limits (phase and battery)
- Voltage limits
- Acceleration/deceleration rates
- Throttle curves
- Protection thresholds

### 4. Dyno Testing
**Requirement**: Professional-grade power measurement

**Data Collection**:
1. Monitor throttle position
2. Record RPM, voltage, current
3. Calculate power and torque
4. Track acceleration rates
5. Measure time intervals

**Analysis**:
- Peak power identification
- Torque curve generation
- Performance time calculations
- Export to standard dyno format

### 5. Battery Integration
**Requirement**: Support external BMS via Bluetooth

**BMS Features**:
1. Individual cell voltages
2. Pack temperature
3. Current flow
4. State of charge
5. Cell balancing status

**Protocol Support**:
- Xiaoxiang/JBD BMS
- Custom BMS protocols
- Fallback to voltage-based estimation

### 6. Efficiency Calculations
**Requirement**: Accurate consumption tracking

**Calculations**:
```python
# Wh/mile calculation
wh_per_mile = power_watts / speed_mph

# Range estimation
remaining_range = battery_wh_remaining / average_wh_per_mile

# Efficiency tracking
trip_efficiency = energy_used_wh / distance_miles
```

---

## 💻 CROSS-PLATFORM CONSIDERATIONS

### Windows-Specific:
1. **COM Port Naming**: COM1, COM2, etc.
2. **Driver Requirements**: CH340/FTDI drivers
3. **Exclusive Port Access**: Use `exclusive=True`
4. **Path Separators**: Use `os.path.join()`

### Raspberry Pi/Linux:
1. **Port Naming**: /dev/ttyUSB0, /dev/ttyACM0
2. **Permissions**: May need sudo or dialout group
3. **GPIO Access**: For additional features
4. **Lower CPU**: Optimize update rates

### Universal Practices:
```python
# OS Detection
import platform
IS_WINDOWS = platform.system() == 'Windows'
IS_LINUX = platform.system() == 'Linux'
IS_MAC = platform.system() == 'Darwin'

# Port enumeration
import serial.tools.list_ports
ports = serial.tools.list_ports.comports()
```

---

## 🧪 TESTING & VALIDATION

### 1. Communication Testing
- **Loopback Test**: Short TX/RX pins
- **Protocol Validation**: Verify packet structure
- **CRC Testing**: Ensure correct calculation
- **Timing Tests**: Measure response times

### 2. Data Accuracy
- **Voltage Calibration**: Compare with multimeter
- **Current Verification**: Use clamp meter
- **RPM Validation**: Strobe light or tachometer
- **Temperature Check**: Infrared thermometer

### 3. Feature Testing
- **Logging Integrity**: Verify no data loss
- **UI Responsiveness**: Monitor CPU usage
- **Error Handling**: Disconnect/reconnect tests
- **Edge Cases**: Max/min values, zero conditions

### 4. Performance Metrics
- **Update Rate**: Minimum 10Hz achieved?
- **CPU Usage**: <50% on Raspberry Pi 3
- **Memory Usage**: Stable over 24 hours
- **File Size**: Reasonable log growth

---

## 🎯 CRITICAL SUCCESS FACTORS

### 1. CRC Implementation
**THIS IS LIFE OR DEATH** - Without correct CRC, nothing works!

See `docs/CRC_ALGORITHMS.md` for the firmware's CRC-16 implementation used by
`src/communication/crc.py`.

Look for in decompile:
- CRC polynomial values
- Byte-by-byte calculation loops
- Initial/final XOR values
- Different CRC types for different commands

### 2. Complete Parameter Extraction
**SCRUB THE DECOMPILE THOROUGHLY**

Search for:
- All memory addresses referenced
- All conversion formulas
- All limit values
- All status flags

### 3. Controller Detection
**MUST SUPPORT ALL MODELS**

Identify:
- Model detection routines
- Version checking code
- Feature capability flags
- Protocol variations

### 4. Professional Quality
**OEM-GRADE STANDARDS**

Requirements:
- Clean, intuitive UI
- Robust error handling  
- Comprehensive logging
- Professional documentation

---

## 📚 DECOMPILE ANALYSIS GUIDE

### Step 1: Initial Survey
1. Open `fulldecompile.c` in a text editor with search
2. Search for common patterns:
   - "0xAA" - likely packet start
   - "uart" or "serial" - communication code
   - "crc" or "checksum" - validation
   - "voltage", "current", "rpm" - parameter names

### Step 2: Protocol Identification
1. Find the main communication loop
2. Identify packet reception code
3. Locate packet parsing routines
4. Map command codes to functions

### Step 3: Parameter Mapping
1. Create spreadsheet of all addresses found
2. Note data types (uint8, uint16, etc.)
3. Document scaling factors
4. Identify read vs write addresses

Known offsets mapped so far:
- `0x9d40` – motor RPM counter
- `0x9e84` – RPM divisor used when above `0x10`
- `0x9d24` – bus voltage (÷10)
- `0x9d28` – bus current (÷4)
- `0x9d48` – throttle voltage sensor
- `0xa074` – brake voltage sensor
- `0x9e38` – output current IQ (×0.1A)
- `0x9e3c` – output current ID (×0.1A)

### Step 4: CRC Extraction
1. Find CRC calculation function
2. Test with known packets if available
3. Implement in Python
4. Validate extensively

### Step 5: Feature Discovery
1. Look for menu structures
2. Find configuration routines
3. Identify special modes
4. Document all capabilities

---

## 🚀 DEVELOPMENT WORKFLOW

### Phase 1: Foundation (Week 1)
1. Set up project structure
2. Implement basic serial communication
3. Create minimal UI from NEWDASH.ui
4. Establish data flow architecture

### Phase 2: Protocol (Week 2)
1. Complete decompile analysis
2. Implement packet structure
3. Add CRC calculation
4. Basic read functionality

### Phase 3: Core Features (Week 3-4)
1. All parameter reading
2. Real-time display updates
3. CSV logging system
4. Multi-controller support

### Phase 4: Advanced Features (Week 5-6)
1. Parameter writing/tuning
2. Dyno functionality
3. BMS integration
4. Efficiency calculations

### Phase 5: Polish (Week 7-8)
1. Complete UI implementation
2. Cross-platform testing
3. Performance optimization
4. Documentation completion

---

## 📋 FINAL CHECKLIST

Before considering the project complete:

- [ ] All UI elements from NEWDASH.ui are functional
- [ ] Communication works with all Fardriver models
- [ ] CRC calculation is 100% correct
- [ ] All parameters from decompile are accessible
- [ ] Logging captures all data accurately
- [ ] Tuning functions are safe and verified
- [ ] Dyno produces professional results
- [ ] Works identically on Windows and Pi
- [ ] No memory leaks over 24hr operation
- [ ] CPU usage acceptable on Pi 3
- [ ] All error conditions handled gracefully
- [ ] User manual is complete
- [ ] Code is clean and well-commented
- [ ] Version control is properly used
- [ ] Installation package is created

---

## 💡 REMEMBER

This is not just another dashboard - it's a complete rewrite using ONLY the decompiled firmware as reference. Every byte of the protocol, every parameter address, every conversion formula must come from careful analysis of `fulldecompile.c`. 

The old version failed because it was incomplete. This version must expose EVERY feature the controller supports. When in doubt, dig deeper into the decompile. The answer is always there.

**Your success depends on treating the decompile like a treasure map - every line could contain the critical piece you need.**

Good luck, and remember: **This is life or death!** ⚡🏁
## NEXT STEPS
- Continue reversing structures near `0x9e9c` for throttle mapping.
- Integrate remaining ID/IQ parameters into the UI and logging system.

