#  Date: 03/02/2020
#  Author: mcalyer
#  Description: Some code to explore Roomba capabilites
#  Reference:   iRobot Create 2 Open Interface (OI) Specification based
#               on the iRobot Roomba 600 10/10/2016
#
#  Notes: Working on Roomba 805
#   
#  
###########################################################################



################################### Imports ###############################


import time
import serial
from   roomba_def   import *
 
################################# Support      ####################################################

def twos_Complement(val,nbits):  
        
    if val < 0:
        val = (1 << nbits) + val
    else:
        if (val & (1 << (nbits - 1))) != 0: 
            val = val - (1 << nbits) 
            
    return ((val >> 8) & 0xFF) , val & 0xFF 

################################## Roomba Control ####################################################        

class Roomba_Control:
    def __init__(self):  
        self.connect = None    
        self.cmd_to_cmd_delay = .3   

    def Connect(self,port):
        if self.connect:
            return 0         
        # Open serial port connection
        # port is a string based on OS and where Roomba is connected connected
        # Examples: Windows 'COM12' , Linux:  '/dev/ttyACM0'
        try:   
            self.connect = serial.Serial(port, baudrate=115200, timeout=1)           
            return 0 , None           
        except:           
            self.connect = None    
            return 1 , 'Serial port connection error !'        
     
    def Disconnect(self):
        if self.connect:            
            self.connect.close()
            self.connect = None       
       
    def Command(self,cmd_list):       
        try:             
            self.connect.write(''.join(chr(e) for e in cmd_list))            
            return 0 , None
        except serial.SerialException:         
            return 1 ,'Command: Serial Port Failed'  
            
    def rxBytes(self, n, delay):          
        if delay != 0 : time.sleep(delay)      
        try:           
            nb = self.connect.inWaiting()                    
            if nb == 0: return 1 , 'rxBytes: Zero serial bytes'   
            if n == '!': n = nb                    
            if n != nb:  
                data = self.connect.read(nb)            
                return 1 , 'rxBytes: Expected : ' + str(n) + ' Received : ' + str(nb)      
            data = self.connect.read(n)                   
            return 0 , data            
        except serial.SerialException:              
            return 1, 'rxBytes: Serial Port Failed' 
            
    def CommandList(self,cmd_list):
        for cmd in cmd_list:           
            if CMD.DELAY == cmd[0]:
                time.sleep(cmd[1])               
                continue                   
            time.sleep(self.cmd_to_cmd_delay)
            result,message = self.Command(cmd)
            if result:               
                return 1 , 'CommandList: ' + message + ' ' + str(cmd)
        return 0, None 
        
    def Start(self):
        start_cmd_list = [ [CMD.OI_START],[CMD.DELAY,.3], [CMD.MODE_FULL], SONG_BEEP_0, PLAY_BEEP_0,[CMD.DELAY,.3] ]
        return self.CommandList(start_cmd_list)
            
    def Stop(self):
        stop_cmd_list = [ PLAY_BEEP_0, [CMD.DELAY,1], [CMD.OI_STOP], [CMD.POWER_DOWN] ]     
        return self.CommandList(stop_cmd_list)

        
    def ReadSensor(self,packet_id,nbytes,delay):      
        result, data = self.Command([CMD.SENSOR,packet_id])
        if result: return result, data
        result , data = self.rxBytes(nbytes,delay)  
        if result: return result, 'readSensor: ' + data   
        return result , data        
      
            
    def Query_Sensors(self,sensors,delay =.016):         
        np = len(sensors)   
        packet = [CMD.QUERY_LIST,np]   
        i = 0
        bytes = 0    
        for sensor in sensors:
            packet.append(sensor.id)
            sensor.index = i   
            bytes = bytes + sensor.nbytes
            i = i + sensor.nbytes
          
        result , data = self.Command(packet)
        if result: return result , data
        
        result , data = self.rxBytes(bytes,delay)   
        if result: return result , data 
        
        for sensor in sensors:  
            try:        
                sensor.value = sensor.unpack(data[sensor.index : sensor.index + sensor.nbytes])[0] 
            except:    
                return 1 , 'readSensor: Query sensor data unpack error'                 
        return result , data 
    
    def Dump_Info(self): 
        result , data = self.CommandList([[CMD.OI_RESET]])
        time.sleep(5)         
        result , data = self.CommandList([[CMD.OI_START]])             
        time.sleep(1)
        result , info = self.rxBytes('!', 5)  
        result , data = self.CommandList([[CMD.POWER_DOWN]])      
        time.sleep(1)        
        return info
   
                
    def Reset(self): 
        result , data = self.CommandList([[CMD.OI_RESET] , [CMD.DELAY,1] , [CMD.POWER_DOWN]])    
        return  result , data         

        
    def Drive(self, op, a, b):
            a_high_byte , a_low_byte = twos_Complement(a,16)
            b_high_byte , b_low_byte = twos_Complement(b,16)
            return self.Command([op, a_high_byte, a_low_byte, b_high_byte, b_low_byte])
            
    def Direct_Drive(self, vel_right , vel_left):        
        return self.Drive(CMD.DRIVE_DIRECT,vel_right,vel_left) 
   
       
    def LEDS(self, leds, color, intensity):
        return self.Command([CMD.LEDS, leds, color, intensity])
        
    def Digit_LED_ASCII(self,d3,d2,d1,d0):
        return self.Command([CMD.DIGIT_LED_ASCII, d3, d2, d1 , d0])
        
    def AuxPower(self,aux_pwr):    
        return self.sendCommand([CMD.AUX_POWER , aux_pwr])   
        
    def ReadSensorRaw(self,id,delay):
        result , message = self.Command([CMD.SENSOR,id])
        if result : return result , 'ReadSensorRaw : ' +  message
        result , data = self.rxBytes('!', delay)      
        if result : return result , 'ReadSensorRaw : ' + data    
        return result , data

roomba_ctrl =  Roomba_Control()