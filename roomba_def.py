#  Date: 03/02/2020
#  Author: mcalyer
#  Description: Code to explore Roomba capabilites
#  Reference:   iRobot Create 2 Open Interface (OI) Specification based
#               on the iRobot Roomba 600 10/10/2016
#
#  Notes: Working on Roomba 805
#   
#  
######################################################################################################################################################


################################### Imports ###############################

################################### Definitions ##########################


class Namespace(object):
    def __init__(self, **kwds):
        self.__dict__.update(kwds)
        self.reversed = dict(map(reversed,  self.__dict__.items()))

################ Commands #########################################################################

CMD                 = Namespace(
   
    OI_RESET        = 7,      # Open Interface  
    DIRT_DETECT     = 15,    
    OI_MODE         = 35,
    OI_START        = 128,  
    OI_STOP         = 173,   
    MODE_SAFE       = 131,    # Mode
    MODE_FULL       = 132,
    POWER_DOWN      = 133,   
    SEEK_DOCK       = 143,   
    DRIVE           = 137,    # Drive
    DRIVE_DIRECT    = 145,
    DRIVE_PWM       = 146,    
    LEDS            = 139,    # LED    
    SCHEDULE_LEDS   = 162,
    DIGIT_LED_ASCII = 164,
    PUSH_BUTTON     = 165,
    DIGIT_LED_RAW   = 163, 
    SET_DAY_TIME    = 168,
    SONG            = 140,    #Song
    SONG_PLAY       = 141,     
    SENSOR          = 142,    # Read Sensors
    QUERY_LIST      = 149, 
    AUX_POWER       = 138,    # Motor / AUAX Power  
    #IR_SEND         = 151, 
    #BAUD            = 129,   # No used 
    #CONTROL         = 130,   # Same as SAFE    
    #SPOT            = 134,    
    #CLEAN           = 135,
    #MAX             = 136,
    #STEAM           = 148,
    #PAUSE_RESUME_STEAM = 150
    #SCHEDULE_LEDS      = 162,    
    #PUSH_BUTTONS       = 165,
    #SCHEDULE           = 167,
    #SET_DAY_TIME       = 168,
    DELAY           = 999     # Program Internal Commands      
  
)


################################# Sensor ID ################################################################################

SENSOR_ID        = Namespace(
    GROUP_0_IDS_07_26             =   0, # Group Sensor Reads
    GROUP_1_IDS_07_16             =   1,
    GROUP_2_IDS_17_20             =   2,
    GROUP_3_IDS_21_26             =   3,
    GROUP_4_IDS_27_34             =   4,
    GROUP_5_IDS_35_42             =   5,
    GROUP_6_IDS_07_42             =   6,
    BUMPS_WHEEL_DROPS             =   7,
    WALL                          =   8,
    CLIFF_LEFT                    =   9,       
    CLIFF_FRONT_LEFT              =   10,  
    CLIFF_FRONT_RIGHT             =   11,
    CLIFF_RIGHT                   =   12,
    VIRTUAL_WALL                  =   13,
    OVER_CURRENTS                 =   14,
    DIRT_DETECT                   =   15,
    UNUSED_BYTE                   =   16,  # See spec
    INFRARED_OMINI                =   17,
    BUTTONS                       =   18,
    DISTANCE                      =   19,
    ANGLE                         =   20,
    BAT_STATE                     =   21,
    BAT_VOLTS                     =   22,
    BAT_CURRENT                   =   23,
    BAT_TEMP                      =   24,
    BAT_CHARGE                    =   25,
    BAT_CAPACITY                  =   26,
    WALL_SIGNAL                   =   27,
    CLIFF_LEFT_S                  =   28,
    CLIFF_FRONT_LEFT_S            =   29,
    CLIFF_FRONT_RIGHT_S           =   30,                
    CLIFF_RIGHT_S                 =   31,
    #NOT_USED_32                  =   32,
    #NOT_USED_33                  =   33,
    CHARGER_AVAILABLE             =   34,
    OPEN_INTERFACE_MODE           =   35,
    SONG_NUMBER                   =   36,
    SONG_PLAY                     =   37,
    OI_STREAM_NUM_PACKETS         =   38,
    VELOCITY                      =   39,
    RADIUS                        =   40,
    VELOCITY_RIGHT                =   41,
    VELOCITY_LEFT                 =   42,
    ENCODER_COUNTS_LEFT           =   43,
    ENCODER_COUNTS_RIGHT          =   44,
    LIGHT_BUMPER                  =   45,
    LIGHT_BUMPER_LEFT             =   46,
    LIGHT_BUMPER_FRONT_LEFT       =   47,
    LIGHT_BUMPER_CENTER_LEFT      =   48,
    LIGHT_BUMPER_CENTER_RIGHT     =   49,
    LIGHT_BUMPER_FRONT_RIGHT      =   50,
    LIGHT_BUMPER_RIGHT            =   51,
    IR_OPCODE_LEFT                =   52,
    IR_OPCODE_RIGHT               =   53,
    LEFT_MOTOR_CURRENT            =   54,
    RIGHT_MOTOR_CURRENT           =   55,
    MAIN_MOTOR_CURRENT            =   56,
    SIDE_MOTOR_CURRENT            =   57,
    STATIS                        =   58,
    GROUP_100_IDS_07_58           =   100,
    GROUP_101_IDS_43_58           =   101,
    GROUP_106_IDS_46_51           =   106,
    GROUP_107_IDS_54_58           =   107   
    
)

################################## SONG #####################################################################################

MIDI_TABLE = { "rest" : 0  , "G#1" : 32 , "G#3" : 56 , "G#2" : 44 ,  "G#5" : 80 , "G#4" : 68 , "G#7" : 104, "G#6" : 92,
               "G#8"  : 116, "G7"  : 103, "G6"  : 91 , "G5"  : 79 ,  "G4"  : 67 , "G3"  : 55 , "G2"  : 43 , "G1"  : 31,
               "G9"   : 127, "G8"  : 115, "A7"  : 105, "D#9" : 123,  "A8"  : 117, "B4"  : 71 , "B5"  : 83 , "B6"  : 95,
               "B7"   : 107, "B1"  : 35 , "B2"  : 47 , "B3"  : 59 ,  "B8"  : 119, "F#2" : 42 , "F#3" : 54 , "F#4" : 66,
               "F#5"  : 78 , "F#6" : 90 , "F#7" : 102, "F#8" : 114,  "F#9" : 126, "E9"  : 124, "E8"  : 112, "E5"  : 76,
               "E4"   : 64 , "E7"  : 100, "E6"  : 88 , "E3"  : 52 ,  "E2"  : 40 , "A#3" : 58 , "A#2" : 46 , "A#1" : 34,
               "pause": 0  , "A#7" : 106, "A#6" : 94 , "A#5" : 82 ,  "A#4" : 70 , "A#8" : 118, "C9"  : 120, "C8"  : 108,
               "C3"   : 48 , "C2"  : 36 , "C7"  : 96 , "C6"  : 84 ,  "C5"  : 72 , "C4"  : 60 , "R"   : 0  , "F2"  : 41,
               "F3"   : 53 , "F4"  : 65 , "F5"  : 77 , "F6"  : 89 ,  "F7"  : 101, "F8"  : 113, "F9"  : 125, "A1"  : 33,
               "A3"   : 57 , "A2"  : 45 , "A5"  : 81 , "A4"  : 69 ,  "D#8" : 111, "A6"  : 93 , "D#6" : 87 , "D#7" : 99,
               "D#4"  : 63 , "D#5" : 75 , "D#2" : 39 , "D#3" : 51 ,  "C#9" : 121, "C#8" : 109, "C#5" : 73 , "C#4" : 61,
               "C#7"  : 97 , "C#6" : 85 , "C#3" : 49 , "C#2" : 37 ,  "D8"  : 110, "D9"  : 122, "D6"  : 86 , "D7"  : 98,
               "D4"   : 62 , "D5"  : 74 , "D2"  : 38 , "D3": 50 }

SONG_BEEP_0 = [CMD.SONG,0,1,64,16]
PLAY_BEEP_0 = [CMD.SONG_PLAY,0]

############################## LEDS Command ###########################################################################################

# LEDS Command LED Byte Bits
lED_OK           = 0x80  
lED_FILTER       = 0x40 
lED_MAG          = 0x20 
lED_CLEAN        = 0x10 
LED_CHECK_ROBOT  = 0x08 
LED_DOCK         = 0x04 
LED_SPOT         = 0x02 
LED_DIRT         = 0x01 
LED_OFF          = 0
LED_ALL          = 0xFF

############################ Motors / AUX Power Command ################################################################################

# Motors or AUX Power
# B[4] = main brush direction
# B[3] = side brush CW (?)
# B[2] = Main brush
# B[1] = Vacuum 
# B[0] = side brush
# Motors removed , using to power circuity , need step down voltage converters and polarity protection
# for AUX_MAIN , AUX_SIDE


# AUX Power: How to measure
# 
# 1. Vac power: 
#      - Must be in SAFE or FULL mode
#      - Pull out bin , facing back side of Roomba bin left terminal is positive , right terminal is negative
#      - With bttery voltage at 14.25 V , measured approx. 12 V , current capablity : ?
# 2. Main Brush: 
#      - Must be in FULL mode
#      - Measured - 14.3 voltage , red wire negative , black wire positive , direction bit = 0
#      - Measured + 14.3 voltage , red wire negative , black wire positive , direction bit = 1


AUX_MAIN_PWR_ON  = 0x14
AUX_SIDE_PWR_ON  = 0x01
AUX_VAC_PWR_ON   = 0x02
AUX_ALL_PWR_OFF  = 0x00
AUX_ALL_PWR_ON   = 0x17

################################################## Sensors ############################################

# Motor Over Currents
OVER_CURRENTS_TABLE = { 0x10 : 'LEFT_WHEEL'  , 
                        0x08 : 'RIGHT_WHEEL' , 
                        0x04 : 'MAIN'        , 
                        0x01 : 'SIDE'        }
Over_Current_Decode = lambda x,f : VER_CURRENTS_TABLE.get(x,'UKNOWN')                            

BUTTON_DECODE_TABLE= { 0x80 : 'Clock'       ,  
                       0x40 : 'Schedule'    ,
                       0x20 : 'Day'         ,      
                       0x10 : 'Hour'        ,
                       0x08 : 'Minute'      ,  
                       0x04 : 'Dock'        ,
                       0x02 : 'Spot'        ,      
                       0x01 : 'Clean'       ,
                       0x00 : 'None'        }
Button_Decode = lambda x,f : BUTTON_DECODE_TABLE.get(x,'UKNOWN')                         

MODE_DECODE_TABLE   = { 0 : 'MODE_OFF'     , 
                        1 : 'MODE_PASSIVE' ,
                        2 : 'MODE_SAFE'    , 
                        3 : 'MODE_FULL'    }  
Mode_Decode = lambda x,f : MODE_DECODE_TABLE.get(x,'UKNOWN')   

CHARGE_STATE_TABLE = { 0 : 'CHARGE_STATE_NOT_CHARGING'   ,
                       1 : 'CHARGE_STATE_RECON_CHARGING' ,
                       2 : 'CHARGE_STATE_FULL'           ,
                       3 : 'CHARGE_STATE_TRICKLE'        ,
                       4 : 'CHARGE_STATE_WAIT'           ,
                       5 : 'CHARGE_STATE_FAULT'          }   
Charge_Decode =  lambda x,f : CHARGE_STATE_TABLE.get(x,'UKNOWN')                           
                
BUMP_WHEEL_TABLE  = {0x02 : 'Bump  Left'    , #Bump
                     0x03 : 'Bump  Both'    ,
                     0x01 : 'Bump  Right'   ,                               
                     0x08 : 'Wheel Left'    , # Wheel
                     0x0C : 'Wheel Both'    ,
                     0x04 : 'Wheel Right'   ,    
                     0x00 : 'NONE'          } 

# 805 Charge Station (6 inches distance) : Sends out a mixture of these IR Codes:  
#  None , red-buoy , force-field ...

IR_OPCODES = {  0 : "none"        , 129 : "left"      , 130 : "forward" , 131 : "right"    , 132 : "spot"    , 133 : "max",
              134 : "small"       , 135 : "medium"    , 136 : "clean"   , 137 : "pause"    , 138 : "power"   , 139 : "arc-left",
              140 : "arc-right"   , 141 : "drive-stop", 142 : "send-all", 143 : "seek-dock", 160 : "reserved", 161 : "force-field",
              162 : "virtual-wall", 164 : "green-buoy", 165 : "green-buoy-and-force-field",  168 : "red-buoy", 169 : "red-buoy-and-force-field",
              172 : "red-buoy-and-green-buoy",          173 : "red-buoy-and-green-buoy-and-force-field",       240 : "reserved",
              242 : "force-field",  244 : "green-buoy", 246 : "green-buoy-and-force-field",  248 : "red-buoy", 250 : "red-buoy-and-force-field",
              252 : "red-buoy-and-green-buoy",          254 : "red-buoy-and-green-buoy-and-force-field",       255 : "none"}
IR_Decode =  lambda x,f : IR_OPCODES.get(x,'UKNOWN')          


PUSH_BUTTON = { 'Clock'   : 0x80   ,
                'Scheule' : 0x40   ,
                'Day'     : 0x20   ,
                'Hour'    : 0x10   ,
                'Minute'  : 0x08   ,
                'Dock'    : 0x04   ,
                'Spot'    : 0x02   ,
                'Clean'   : 0x01   }

WEEKDAY_LED_DECODE_TABLE = { 'SAT' : 0x40 , 
                             'FRI' : 0x20 ,
                             'THU' : 0x10 ,
                             'WED' : 0x08 , 
                             'TUE' : 0x04 ,
                             'MON' : 0x02 , 
                             'SUN' : 0x01 } 
                          
SCHEDULE_LED_DECODE_TABLE = { 'SCH' : 0x10 ,
                              'CLK' : 0x08 , 
                              'AM'  : 0x04 ,
                              'PM'  : 0x02 , 
                              ':'   : 0x01 } 
                              
                              