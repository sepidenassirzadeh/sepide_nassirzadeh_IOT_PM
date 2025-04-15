'''task 1'''
#topic=location,group,device,name
import paho.mqtt.client as mqtt
import RPi.GPIO as GPIO
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
        
        
    def connect_mqtt(self):
      self.mqtt_client=mqtt.Client()
      self.mqtt_client.connect(self.mqtt_broker,self.port)
      self.mqtt_client.loop_start()
        
        
    def setup_gpio(self):
      if self.device=='lamp':
          GPIO.setup(17,GPIO.OUT)
          
      elif self.device=='door':
          GPIO.setup(27,GPIO.OUT)
          
      elif self.device=='fan':
          GPIO.setup(22,GPIO.OUT)
          
      elif self.device=='camera':
          GPIO.setup(100,GPIO.OUT)
          
      else:
          raise ValueError('unknown device')
          
          
    def turn_on(self):
        self.mqtt_client.publish(self.topic,'TURN_ON')
        GPIO.output(self.pin, GPIO.HIGH)
        print('turned on successfully')
        
    def turn_off(self):
        self.mqtt_client.publish(self.topic,'TURN_OFF')
        GPIO.output(self.pin, GPIO.LOW)
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
        

a1=device(topic='home/parking/lamp/lamp100',mqtt_broker='15643',port=2345)