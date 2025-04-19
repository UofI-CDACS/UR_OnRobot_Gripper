# UR5e OnRobot RG2 Gripper Controller

Driver for controlling OnRobot RG2 Gripper on Universal Robots UR5e via Modbus TCP. The RG2 Gripper uses Modbus RTU, while the conversion is done in the Compute Box that uses Modbus TCP/IP, and the RTDE is used for status update across the devices. This provides both high-level commands (open/close) and precise width/force control.

## Table of Contents

- [Features](#features)
- [Installation](#installation)
- [Quick Start](#quick-start)
- [Examples](#examples)

## Features

- **Intuitive Control**:

  - `connect()` - Create a connection to the gripper
  - `disconnect()` - Close connection
  - `read_gripper_width()` - Read the width of the gripper
  - `set_gripper_width()` - Move to specific width (0-100mm), pass the desired Force and width
- **Precision Control**:

  - Set exact width (0.0-100.0mm) and force (0-40N)
  - Real-time width feedback via `read_gripper_width()`
- **Safety**:

  - Automatic parameter validation
  - Connection management
  - Error handling

## Installation

```bash
pip install pymodbus
```

## Quickstart

```python
from Gripper_Control import RG2_OnRobot_Gripper_Controller

gripper = RG2_OnRobot_Gripper_Controller(ip="172.23.254.233")

try:
    gripper.connect()
  
    # Open gripper with 20N force
    gripper.open_gripper(force=20)  
  
    # Move to 45mm with 25N force
    gripper.move_gripper(width=45, force=25)
  
    # Read current width
    print(f"Current width: {gripper.read_gripper_width()} mm")
  
finally:
    gripper.disconnect()
```
