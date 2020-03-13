###########################################################################
#  Python Roomba 
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


import time
import math
from   struct import Struct
from   roomba_def import *
from   roomba_control import roomba_ctrl


################################### Definitions ##########################

unpack_byte           = Struct('b').unpack   # 1 signed byte
unpack_unsigned_byte  = Struct('B').unpack   # 1 unsigned byte
unpack_short          = Struct('>h').unpack  # short  , 2 signed bytes 
unpack_unsigned_short = Struct('>H').unpack  # ushort , 2 unsigned bytes 

################################################## Sensors ############################################
# Note: Sensors updated every 15 msec. At 115200 , maximum bytes that can be sent is 172.
# Do not rquest sensor data faster than this

class SENSOR(): 
     def __init__(self,name,id,nbytes,unpack,decode = None, pprint = None):
        self.roomba_ctrl  = roomba_ctrl    
        self.name         = name        
        self.id           = id
        self.nbytes       = nbytes
        self.unpack       = unpack
        self.f_decode     = decode   
        self.pp           = pprint   
        self.delay        = .016      
        self.value        = 0      
        self.index        = 0        
        
     def read(self,delay = None ):  
        if delay is None : delay = self.delay       
        result, data =  self.roomba_ctrl.ReadSensor(self.id,self.nbytes,delay)
        if result: return result, data        
        try:        
            self.value = self.unpack(data)[0] 
            return result , self.value                 
        except:
            return 1 , 'readSensor: Sensor data unpack error'              
                                      
     def decode(self,flags = None):   
         if self.f_decode is None: return str(self.value)        
         return self.f_decode(self.value, flags)
                                      
     def pprint(self,flags = None):
         if self.pp is None: return self.name + " : " + self.decode() 
         return self.name + " : " + self.decode(flags) + self.pp(flags)  

         
         
sens_oi_mode       = SENSOR('Mode'         , SENSOR_ID.OPEN_INTERFACE_MODE , 1, unpack_unsigned_byte, Mode_Decode)  
 
# Buttons 
sens_button        = SENSOR('Button'       , SENSOR_ID.BUTTONS             , 1, unpack_unsigned_byte, Button_Decode) 

sens_statis        = SENSOR('Statis'       , SENSOR_ID.STATIS              , 1, unpack_unsigned_byte) 
sens_virtual_wall  = SENSOR('Virtual Wall' , SENSOR_ID.VIRTUAL_WALL        , 1, unpack_unsigned_byte) 

# Bumper and Wheel Drop
bump_drop_decode     = lambda x,f  : BUMP_WHEEL_TABLE.get(x & 0x03,'UNKNOWN') if f == 'b' else BUMP_WHEEL_TABLE.get(x & 0x0C,'UNKNOWN')
sens_bump_wheel_drop = SENSOR('Bump_Wheel_Drop',SENSOR_ID.BUMPS_WHEEL_DROPS, 1, unpack_unsigned_byte,bump_drop_decode) 

sens_cliff_left        = SENSOR('Cliff Left       '  , SENSOR_ID.CLIFF_LEFT        , 1, unpack_unsigned_byte)
sens_cliff_right       = SENSOR('Cliff Right      '  , SENSOR_ID.CLIFF_RIGHT       , 1, unpack_unsigned_byte)  
sens_cliff_front_left  = SENSOR('Cliff Front Left '  , SENSOR_ID.CLIFF_FRONT_LEFT  , 1, unpack_unsigned_byte)    
sens_cliff_front_right = SENSOR('Cliff Front Right'  , SENSOR_ID.CLIFF_FRONT_RIGHT , 1, unpack_unsigned_byte)

# IR
sens_ir_omni  = SENSOR('IR Omni ' , SENSOR_ID.INFRARED_OMINI  , 1, unpack_unsigned_byte, IR_Decode) 
sens_ir_left  = SENSOR('IR Left ' , SENSOR_ID.IR_OPCODE_LEFT  , 1, unpack_unsigned_byte, IR_Decode) 
sens_ir_right = SENSOR('IR Right' , SENSOR_ID.IR_OPCODE_RIGHT , 1, unpack_unsigned_byte, IR_Decode) 

# Battery 
sens_bat_state    = SENSOR('Bat State   '  , SENSOR_ID.BAT_STATE           , 1, unpack_unsigned_byte, Charge_Decode)

bat_temp_decode   = lambda x,f : str((int(x) * 9)/5 + 32) if f == 'F' else str(x)
bat_temp_pprint   = lambda f : ' F' if f == 'F' else 'C'     
sens_bat_temp     = SENSOR('Bat Temp    '  , SENSOR_ID.BAT_TEMP, 1, unpack_byte , decode = bat_temp_decode, pprint = bat_temp_pprint)


bat_volt_decode   = lambda x,f : str(float(x)/1000.0) if f == 'V' else str(x)  
bat_volt_pprint   = lambda f : ' V' if f == 'V' else ' mv'           
sens_bat_volts    = SENSOR('Bat Volt    ' , SENSOR_ID.BAT_VOLTS, 2, unpack_unsigned_short, decode = bat_volt_decode, pprint = bat_volt_pprint) 

current_decode    = lambda x,f : str(x) if f == 'ma' else str(float(x)/1000.0)  
current_pprint    = lambda f : ' ma' if f == 'ma' else ' A'        
sens_bat_current  = SENSOR('Bat Current ' , SENSOR_ID.BAT_CURRENT  , 2 , unpack_short          , decode = current_decode,  pprint = current_pprint)     
sens_bat_capacity = SENSOR('Bat Capacity' , SENSOR_ID.BAT_CAPACITY , 2 , unpack_unsigned_short , decode = current_decode,  pprint = current_pprint)  
sens_bat_charge   = SENSOR('Bat Charge  ' , SENSOR_ID.BAT_CHARGE   , 2 , unpack_unsigned_short , decode = current_decode,  pprint = current_pprint) 

# Motor Currents
sens_over_currents = SENSOR('Over Current' , SENSOR_ID.OVER_CURRENTS       , 1, unpack_unsigned_byte, Over_Current_Decode) 
sens_left_motor    = SENSOR('Left Motor  '  , SENSOR_ID.LEFT_MOTOR_CURRENT  , 2 , unpack_short, decode = current_decode,  pprint = current_pprint)  
sens_right_motor   = SENSOR('Right Motor '  , SENSOR_ID.RIGHT_MOTOR_CURRENT , 2 , unpack_short, decode = current_decode,  pprint = current_pprint)  
sens_main_motor    = SENSOR('Main        '  , SENSOR_ID.MAIN_MOTOR_CURRENT  , 2 , unpack_short, decode = current_decode,  pprint = current_pprint)  
sens_side_motor    = SENSOR('Side        '  , SENSOR_ID.SIDE_MOTOR_CURRENT  , 2 , unpack_short, decode = current_decode,  pprint = current_pprint)  

# Distance
wheel_encoder_decode   = lambda x,f  : str(x * (math.pi * 72.0/508.8)) if f == 'mm' else str( (x * (math.pi * 72.0/508.8)/100.0))
wheel_encoder_pprint   = lambda f    : ' mm' if f == 'mm' else ' cm'
sens_left_wheel_count  = SENSOR('Wheel Left'  ,SENSOR_ID.ENCODER_COUNTS_LEFT, 2 ,  unpack_short , decode = wheel_encoder_decode, pprint = wheel_encoder_pprint)
sens_right_wheel_count = SENSOR('Wheel Right' ,SENSOR_ID.ENCODER_COUNTS_LEFT, 2 ,  unpack_short , decode = wheel_encoder_decode, pprint = wheel_encoder_pprint)




############ Sensor Query Groups ######################################################################
"""
sensor_group_all = [ sens_bump_wheel_drop,    # 7
                     sens_cliff_left,         # 9   
                     sens_cliff_front_left,   # 10
                     sens_cliff_front_right,  # 11
                     sens_cliff_right,        # 12
                     sens_virtual_wall,       # 13
                     sens_over_currents,      # 14
                     sens_ir_omni,            # 17                     
                     sens_button,             # 18
                     sens_bat_state,          # 21
                     sens_bat_volts,          # 22
                     sens_bat_current,        # 23
                     sens_bat_temp,           # 24                    
                     sens_bat_charge,         # 25
                     sens_bat_capacity,       # 26
                     sens_bat_current,        # 23                   
                     sens_oi_mode,            # 35
                     sens_left_wheel_count,   # 43
                     sens_right_wheel_count,  # 44                 
                     sens_ir_left,            # 52
                     sens_ir_right,           # 53
                     sens_left_motor,         # 54
                     sens_right_motor,        # 55
                     sens_main_motor,         # 56
                     sens_side_motor,         # 57
                     sens_statis  ]           # 58
"""                  
                     
                     
BAT_STATUS =  [sens_bat_state,        
               sens_bat_volts,
               sens_bat_charge,
               sens_bat_current,
               sens_bat_capacity,
               sens_bat_temp   ]   


CLIFF = [sens_cliff_left,sens_cliff_front_left,sens_cliff_front_right,sens_cliff_right]

