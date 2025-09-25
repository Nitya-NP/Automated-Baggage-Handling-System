
ip_address =  "localhost"
project_identifier = 'P3A'
#--------------------------------------------------------------------------------
import sys
sys.path.append('../')
from Common.hardware_project_library import *
from Common.barcode_checker import *

hardware = True
arm = qarm(project_identifier,ip_address,hardware)
table = servo_table(ip_address,None,hardware)
scanner = barcode_checker()

#---------------------------------------------------------------------
# Student name: Nitya Patel, Alyssa Galvin, Jingwen Liu, Emi Ojeaburu
# Date: Nov 27, 2024
# Group_ID= Mon-44
#---------------------------------------------------------------------

#--------------------------------------------------------------------------------
# STUDENT CODE BEGINS
#---------------------------------------------------------------------------------

#Home position
arm.home()

def rotary_code():
    #This just brings the rotary actuator up after the bag has landed on the end of the platform 
    
    bot.activate_stepper_motor()
    time.sleep(2)
    bot.rotate_stepper_ccw(0.7)
    time.sleep(2)


def QArm_code():
 
   time.sleep(2)
   arm.rotate_base(-90) #turning to the table

   table.stop()
   table.rotate_table_angle(90) #rotates the table
   t= scanner.barcode_check() #scanning the bar code
   
   #picks up the bag from the table 
   arm.rotate_shoulder(7)
   arm.rotate_elbow(18)
   arm.rotate_shoulder(13)
   arm.control_gripper(42)
   time.sleep(1)

   #getting back up	
   arm.rotate_shoulder(-7)
   arm.rotate_elbow(-30)
	
   #according to the bag
 
   if t=='Rejection Bin':
   # when the bag should be in the rejection bin
     
      arm.rotate_base(90) 
      time.sleep(1)
      arm.rotate_base(90)
      arm.rotate_shoulder( 5)
      arm.rotate_elbow(13)
      arm.rotate_shoulder(12)
      arm.control_gripper(-40)
      time.sleep(1)
   else:
   #when the bag should be on the platform
      
      arm.rotate_base(90)  
      arm.rotate_shoulder(5)
      arm.control_gripper(-40)
      time.sleep(4)
     
      rotary_code() #Rotary code


QArm_code() #Runs the Q-arm code

#---------------------------------------------------------------------------------
# STUDENT CODE ENDS
#---------------------------------------------------------------------------------

