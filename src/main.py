from Gripper_Control import RG2_OnRobot_Gripper_Controller
import time

def main():
    # Initialize gripper controller
    gripper = RG2_OnRobot_Gripper_Controller()
    
    try:
        # Connect to the OnRobot gripper
        gripper.connect()
        
        # Read current width
        current_width = gripper.read_gripper_width()
        print(f"Current width: {current_width} mm")
        
        # Test opening gripper, change width and force as you see fit
        print("Opening gripper to 50mm with 20N force")
        gripper.set_gripper_width(force=20, width=100)
        time.sleep(2)  # small delay
        
        # Read new width
        new_width = gripper.read_gripper_width()
        print(f"New width: {new_width} mm")
        time.sleep(2)  # small delay
        
        # Test closing gripper, change width and force as you see fit
        print("Closing gripper to 20mm with 30N force")
        gripper.set_gripper_width(force=30, width=10)
        time.sleep(2) # small dealay
        
    except Exception as e:
        print(f"Error in main program: {e}")
    finally:
        # Disconnect
        gripper.disconnect()

if __name__ == "__main__":
    main()