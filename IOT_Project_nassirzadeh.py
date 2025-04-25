'''

APM:

Daryaft shod


'''


'''task 1'''
#topic=location,group,device,name
#import RPi.GPIO as GPIO
#import paho.mqtt.client as mqtt
class device:
    def __init__(self,topic,mqtt_broker='localhost',port=1338):
        self.topic=topic
        self.topic_list=self.topic.split('/')
        self.location=self.topic_list[0]
        self.group=self.topic_list[1]
        self.device=self.topic_list[2]
        self.name=self.topic_list[3]
        
        self.mqtt_broker=mqtt_broker
        self.port=port
        
        self.connect_mqtt()
        self.setup_gpio()
        
        self.status='off'
        
        
    def connect_mqtt(self):
      self.mqtt_client=mqtt.Client()
      self.mqtt_client.on_message=self.on_message()
      self.mqtt_client.connect(self.mqtt_broker,self.port)
      self.mqtt_client.subscribe(self.topic)
      self.mqtt_client.loop_start()
        
        
    def setup_gpio(self):
      if self.device=='lamp':
          self.pin=17
          
      elif self.device=='door':
          self.pin=27
          
      elif self.device=='fan':
          self.pin=22
          
      elif self.device=='camera':
          self.pin=100
          
      else:
          raise ValueError('unknown device')
          
      GPIO.setup(self.pin, GPIO.OUT)
          
          
    def turn_on(self):
        self.mqtt_client.publish(self.topic,'TURN_ON')
        GPIO.output(self.pin, GPIO.HIGH)
        self.status='on'
        print('turned on successfully')
        
    def turn_off(self):
        self.mqtt_client.publish(self.topic,'TURN_OFF')
        GPIO.output(self.pin, GPIO.LOW)
        self.status='off'
        print('turned off successfully')
        
    def on_message(self, client, userdata, msg): #کنترل از بیرون برنامه
        command = msg.payload.decode()
        print(f"[MQTT] Message received on {msg.topic}: {command}")
        
        if command == 'TURN_ON':
            GPIO.output(self.pin, GPIO.HIGH)
            print('[GPIO] Turned ON from MQTT command')
        elif command == 'TURN_OFF':
            GPIO.output(self.pin, GPIO.LOW)
            print('[GPIO] Turned OFF from MQTT command')
        else:
            print('[MQTT] Unknown command received')


class admin_panel:
    def __init__(self):
        self.groups={}
    
    def create_group(self,group_name):
        if group_name not in self.groups:
            self.groups[group_name]=[]        
            print(f'group {group_name} is created')
        else:
            print(f'group{group_name} already existed')
        
    

a1=device(topic='home/parking/lamp/lamp100')
a1=admin_panel()
a1.groups
a1.create_group('wc')
a1.groups
mygp=a1.groups
a1.create_group('parking')
a1.groups




'''task 2 & 3'''

class Device:
    def __init__(self,topic):
        self.topic=topic
        self.topic_list=self.topic.split('/')
        self.location=self.topic_list[0]
        self.group=self.topic_list[1]
        self.device_type=self.topic_list[2]
        self.name=self.topic_list[3]
        
        self.status='off'
        
 
    def turn_on(self):
        self.status='on'
        print('turn on successfully')
        

    def turn_off(self):
        self.status='off'
        print('turn off successfully')


class Sensor:
    def __init__(self,topic,pin=100):
        self.topic=topic
        self.topic_list=self.topic.split('/')
        self.location=self.topic_list[0]
        self.group=self.topic_list[1]
        self.sensor_type=self.topic_list[2]
        self.name=self.topic_list[3]
    def read_sensor(self):
        return 25





class Admin_Panel:
    
    def __init__(self):
        self.groups={}
        
        
    def create_group(self,group_name):
        
        if group_name not in self.groups:

            self.groups[group_name]=[]
            
            print(f'group {group_name} has been created')        
        else:            
            print(f'group {group_name} already exists')
        
        
    def add_device_to_group(self,group_name,new_device):
        
        if group_name in self.groups:
            
            self.groups[group_name].append(new_device)
            
            print(f'{new_device.name} is added to {group_name}')            
        else:            
            print(f'group {group_name} does not exist')
        
                
    def create_device(self,group_name,device_type,name):
        
        if group_name in self.groups: 
            
            topic=f'home/{group_name}/{device_type}/{name}'
            new_device=Device(topic)
            
            self.add_device_to_group(group_name,new_device)
            print(f'device{new_device.name} with type {device_type} in group {group_name} is created')
            
        else:            
            print(f'group {group_name} does not exist')            

                        
    def create_multiple_devices(self,group_name,device_type,number_of_devices):
        
        if group_name in self.groups:
            for i in range(1,number_of_devices+1):
                topic=f'home/{group_name}/{device_type}/{device_type}{i}'
                new_device=Device(topic)
                
                self.add_device_to_group(group_name, new_device)
                
                print(f'device {device_type}{i} added to group {group_name} successfully')
        else:
            print(f'group {group_name} does not exist')
        
        
    def turn_on_devices_in_group(self,group_name):
        
        if group_name in self.groups:
            
            devices_list=self.groups[group_name]
            
            for device in devices_list:   
                device.turn_on()
            print(f'all devices in {group_name} are turned on')            
        else:
            print(f'group {group_name} does not exist')
    
    
    def turn_off_devices_in_group(self,group_name):
        if group_name in self.groups:
            devices_list=self.groups[group_name]
            
            for device in devices_list:
                device.turn_off()
            print(f'all devices in {group_name} are turned off')
        else:
            print(f'group {group_name} does not exist')
                        
        
    def turn_on_all(self):
       for devices_list in self.groups.values():
           for device in devices_list:
               device.turn_on()
       print('all devices in all groups are now on')
        
       
    def turn_off_all(self):
        for devices_list in self.groups.values():
            for device in devices_list:
                device.turn_off()
        print('all devices in all groups are now off')
    
        
    def get_status_in_group(self,group_name):
        if group_name in self.groups:
            devices_list=self.groups[group_name]
            for device in devices_list:
                print(f'{device.name} status is {device.status}') 
        else:
            print(f'group {group_name} does not exist')
    
    
    def get_status_in_device_type(self,device_type):
        matching_devices=[]
        
        for group_name,devices in self.groups.items():
            for device in devices:
                if device.device_type == device_type:
                    matching_devices.append((device.name, group_name, device.status))

        if len(matching_devices) != 0:
            for name,group,status in matching_devices:
                print(f' device {name} in group {group} status: {status}')
                    
        else:
            print('this device type does not exist')
            
    
    def create_sensor(self,group_name,sensor_type,name):
        if group_name in self.groups:
            topic=f'home/{group_name}/{sensor_type}/{name}'
            new_sensor=Sensor(topic)
            self.groups[group_name].append(new_sensor)
            print(f'sensor {name} added to group {group_name}')
            
        else:
            print(f'Group {group_name} does not exist')
        
        
    def get_status_sensor_in_group(self,group_name):
        if group_name in self.groups:
            devices=self.groups[group_name]
            for device in devices:
                if isinstance(device,Sensor):
                    value=device.read_sensor()
                    print(f'sensor {device.name} in group {group_name} value is: {value}')
        else:
            print(f'group {group_name} does not exist')
