"""
Version: 1.0
Author: Davis Onyeoguzoro
Date: 18th April, 2025

Project: Assembly Line - Gripper Control from Universal Robot 

Description:
This module provides control for the OnRobot RG2 Gripper attached to a Universal Robot (UR5e).
It allows programmatic control of the gripper including setting width/force and reading current width.

Some of Features:
- Connect/disconnect from the gripper
- Read current gripper width
- Set gripper width and force
- Error handling for communication issues

Hardware Configuration:
- Robot: Universal Robot UR5e
- End-Effector: OnRobot RG2 Gripper
- Communication: Modbus TCP while the gripper is mounted on a quick change that is using Modbus RTU

Notes:
- Gripper width range: 0.0 to 100.0 mm (values are divided by 10.0 for actual width)
- Force range: 0 to 40 N
- Actual width may have an offset of 8-10mm from reported value on the UR5e Teach Pendant
"""

import time
from pymodbus.client import ModbusTcpClient

class RG2_OnRobot_Gripper_Controller:
    """
    THis is controller class for the OnRobot RG2 Gripper
    
    Attributes:
        IP (str): IP address of the robot controller, chage as you see fit
        PORT (int): Modbus TCP port (default 502)
        SLAVE_ID (int): id of the device
        client (ModbusTcpClient): Modbus TCP client instance
    """
    
    def __init__(self, ip="172.23.254.233", port=502, slave_id=65):
        """
        Initialize the gripper controller
        
        Args:
            ip (str): IP address of the robot controller
            port (int): Modbus TCP port
            slave_id (int): Modbus slave ID
        """
        self.IP = ip
        self.PORT = port
        self.SLAVE_ID = slave_id
        self.client = ModbusTcpClient(self.IP, port=self.PORT)
        
    def connect(self):
        """Connection to the gripper"""
        if not self.client.connect():
            raise ConnectionError(f"Failed to connect to Gripper server at {self.IP}:{self.PORT}")
        print(f"Connected to {self.IP} gripper successfully")
        return True
    
    def disconnect(self):
        """Disconnect from the gripper"""
        self.client.close()
        print("Disconnected from gripper")
        
    def read_gripper_width(self):
        """
        Read current gripper width
        
        Returns:
            float: Current width in mm, or None if error occurs
        """
        try:
            response = self.client.read_holding_registers(address=267, count=1, slave=self.SLAVE_ID)
            if response.isError():
                print("Error reading gripper width")
                return None
            width = response.registers[0] / 10.0
            print(f"Gripper width: {width} mm")
            return width
        except Exception as e:
            print(f"Error reading width: {e}")
            return None
    
    def set_gripper_width(self, force, width):
        """
        Set gripper width and force
        
        Args:
            force (int): Force in Newtons (0-40)
            width (float): Width in mm (0.0-100.0)
            
        Returns:
            bool: True if successful, False otherwise
        """
        try:
            if not (0 <= force <= 40):
                raise ValueError("Force must be between 0-40 N")
            if not (0.0 <= width <= 100.0):
                raise ValueError("Width must be between 0.0-100.0 mm")
                
            force_newton = int(force * 10.0)
            width_mm = int(width * 10.0)
            
            print(f"Settin Gripper width to {width} mm and force to {force} N")

            # Activate the gripper, this has to be done before width to set
            self.client.write_register(address=2, value=1, slave=self.SLAVE_ID) 

            # Set force and width
            self.client.write_registers(
                address=0,
                values=[force_newton, width_mm],
                slave=self.SLAVE_ID
            )

            print("Gripper command sent successfully")
            return True
            
        except ValueError as ve:
            print(f"Invalid parameter: {ve}")
            return False
        except Exception as e:
            print(f"Error setting gripper: {e}")
            return False