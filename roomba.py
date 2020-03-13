#  Date: 03/02/2020
#  Author: mcalyer
#  Description: Code to explore Roomba capabilites
#  Reference:   iRobot Create 2 Open Interface (OI) Specification based
#               on the iRobot Roomba 600 10/10/2016
#
#  Notes: Working on Roomba 805
#   
#  
###########################################################################

################################### Imports ###############################

import sys
import time
from   roomba_def     import *
from   roomba_com     import rsp
from   roomba_sensor  import *
from   roomba_control import roomba_ctrl
from   roomba_utils   import *

def main(sys_argv):

    # Input parms:  port , flag
    #   Port Windows example:  COM47
    #   Port Liux example:     /dev/ttyAMC0
    #   Flags:   i = Dumps Roomba info 
    #            m = listen on Roomba' serial port , does not start Rommba 
    #            r = reset roomba 
    
    if len(sys_argv) < 2: print("More Args Please !") ; exit(0) 
    port = sys_argv[1] 
    
    # Roomba Connect   
    result , message = roomba_ctrl.Connect(port)
    if result: print message ; exit(0) 
    print "\n"  
    
    # Do command line options 
    if len(sys_argv) > 2:
        Run_Command(sys_argv[2])
        
    # Roomba Start  
    print 'Start Roomba\n'
    result , message = roomba_ctrl.Start()  
    if result: 
        print message
        roomba_ctrl.Disconnect() 
        exit(0)    
    
    time.sleep(1)
    result , data = sens_oi_mode.read()
    if result:
        print 'Press Power Button !\n' 
        roomba_ctrl.Disconnect()
        exit(0)        
    print sens_oi_mode.pprint() + '\n'
    time.sleep(1)   

     
    # Roomba Loop , type CTRL C to exit
    print 'Roomba Loop'
    i = 9999
    while(1):
      
        try:         
            # Flash LEDs          
            b = LED_ALL if i & 0x01 else 0x00 
            leds(b)        
           
            
            # Count down on digit LEDs
            led_int_digit_display(i)
               
          
            #result , data = sens_ir_left.read()
            #if result: print result , data  
            #print sens_ir_left.pprint() + '\n'
           
           
            #result , data = sens_button.read() 
            #if result: print result , data            
            #else: print sens_button.pprint()
            
            result , data = sens_bat_volts.read() 
            print sens_bat_volts.pprint('V') + '\n'
           
          
            """
            # Sensor scan            
            result , message = roomba_ctrl.Query_Sensors(CLIFF)  
            if result: print("Query_Sensors : Failed") ; break 
            for s in CLIFF:
               print s.pprint()
            print '\n'          
           """
            
          
            i = i - 1
            if i < 0: i = 9999
            time.sleep(1)
        
        except KeyboardInterrupt:
            break  
        
  
    # Roomba Stop , Disconnect
    roomba_ctrl.Stop()
    roomba_ctrl.Disconnect()
   

if __name__ == "__main__":
     main(sys.argv)  
