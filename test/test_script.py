import unittest
from unittest.mock import MagicMock, patch
from Gripper_Control import RG2_OnRobot_Gripper_Controller

class TestRG2GripperController(unittest.TestCase):
    
    def setUp(self):
        """Set up test fixtures"""
        self.gripper = RG2_OnRobot_Gripper_Controller(ip="127.0.0.1")
        self.gripper.client = MagicMock()
        
    def test_connect_success(self):
        """Test successful connection"""
        self.gripper.client.connect.return_value = True
        result = self.gripper.connect()
        self.assertTrue(result)
        
    def test_connect_failure(self):
        """Test failed connection"""
        self.gripper.client.connect.return_value = False
        with self.assertRaises(ConnectionError):
            self.gripper.connect()
            
    def test_read_width_success(self):
        """Test successful width reading"""
        mock_response = MagicMock()
        mock_response.isError.return_value = False
        mock_response.registers = [500]  # 50.0 mm
        self.gripper.client.read_holding_registers.return_value = mock_response
        
        width = self.gripper.read_gripper_width()
        self.assertEqual(width, 50.0)
        
    def test_read_width_error(self):
        """Test error in width reading"""
        mock_response = MagicMock()
        mock_response.isError.return_value = True
        self.gripper.client.read_holding_registers.return_value = mock_response
        
        width = self.gripper.read_gripper_width()
        self.assertIsNone(width)
        
    def test_set_width_valid(self):
        """Test valid width/force setting"""
        self.gripper.client.write_register.return_value = None
        self.gripper.client.write_registers.return_value = None
        
        result = self.gripper.set_gripper_width(force=20, width=50)
        self.assertTrue(result)
        
    def test_set_width_invalid_force(self):
        """Test invalid force setting"""
        with self.assertRaises(ValueError):
            self.gripper.set_gripper_width(force=50, width=50)
            
    def test_set_width_invalid_width(self):
        """Test invalid width setting"""
        with self.assertRaises(ValueError):
            self.gripper.set_gripper_width(force=20, width=150)
            
    def test_disconnect(self):
        """Test disconnection"""
        self.gripper.disconnect()
        self.gripper.client.close.assert_called_once()

if __name__ == "__main__":
    unittest.main()