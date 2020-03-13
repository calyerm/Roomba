#  Date: 03/02/2020
#  Author: mcalyer
#  Description: Some code to explore Roomba capabilites
#  Reference:   iRobot Create 2 Open Interface (OI) Specification based
#               on the iRobot Roomba 600 10/10/2016
#
#  Notes: Working on Roomba 805
#   
#  
#######################################################################################################################################################  Python Roomba 


################################### Imports ###############################


import time
from   roomba_def     import *
from   roomba_sensor  import *
from   roomba_control import roomba_ctrl


############ Utility #######################################################
   
def led_int_digit_display(n):
    if n > 9999: n = 9999
    if n < 0: n = 0
    x = str(n)
    x = (4 - len(x)) * '0' + x
    return roomba_ctrl.Digit_LED_ASCII( ord(x[0]), ord(x[1]),  ord(x[2]),  ord(x[3]))    
   
def leds(leds_bits, power = 0xFF, intensity = 0x08):    
    return roomba_ctrl.LEDS(leds_bits, power, intensity) 

def dump_roomba_info(): 
    print 'Dump Roomba Info\n'           
    print roomba_ctrl.Dump_Info()   
    roomba_ctrl.Stop()
    roomba_ctrl.Disconnect()        
    exit(0) 
    
def monitor_roomba():
    print 'Listen on Roomba serial port\n'   
    while(1):      
        try:  
            time.sleep(10.1)               
            result , data =  roomba_ctrl.rxBytes('!', 0) 
            if result: continue                             
            print data      
        except KeyboardInterrupt:
                roomba_ctrl.Disconnect()
                exit(0) 
                
def reset_roomba():              
    print 'Reset Roomba\n'         
    roomba_ctrl.Reset() 
    roomba_ctrl.Disconnect()
    exit(0)  

COMMAND_TABLE = { 'i' : dump_roomba_info  , 
                  'm' : monitor_roomba    ,
                  'r' : reset_roomba      }
                

def Run_Command(cmd):
    if 'None' == COMMAND_TABLE.get(cmd,'None'):
        return
    COMMAND_TABLE[cmd]()
         

        
      
        
   