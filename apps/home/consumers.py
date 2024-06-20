# consumers.py
import json
import threading
import concurrent.futures
from channels.generic.websocket import AsyncWebsocketConsumer
import paho.mqtt.client as mqtt
import paho.mqtt.publish as publish
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
import logging

logging.basicConfig(level=logging.DEBUG)  # Enable debug logs

class MQTTConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.ip = self.scope['url_route']['kwargs']['ip_address']
        self.port = int(self.scope['url_route']['kwargs']['port'])
        # self.subtopiclist = json.loads(self.scope['url_route']['kwargs']['subtopics'])

        print('connect to {}:{}'.format(self.ip,self.port))

        self.client = mqtt.Client()

        self.client.on_message = self.on_message_sync
        self.client.on_connect = self.on_connect
        self.client.on_subscribe = self.on_subscribe

        with concurrent.futures.ThreadPoolExecutor() as executor:
            future = executor.submit(self.client.connect, self.ip, self.port, 60)
            try:
                future.result()  # This will raise an exception if the call to connect failed
                self.client.loop_start()
                # self.client.subscribe('parameter/#')
            except TimeoutError:
                # When MQTT connection timeout exception occurs, send 'timeout' to WebSocket
                await self.accept()  # Accept the WebSocket connection before sending data
                await self.send(text_data=json.dumps({
                    'message': '>> connection error: timeout'
                }))
                return  # Return early to avoid further processing

        # Only accept the WebSocket connection if the MQTT connection was successful
        await self.accept()

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        print('received websocket msg: {}'.format(text_data_json))

        command = text_data_json['command']
        payload = text_data_json['message']

        if command == 'publish':
            topic = payload[:payload.find('::')]
            message = payload[payload.find('::')+len('::'):]
            try:
                # Publish the MQTT message
                publish.single(topic, message, hostname=self.ip, port=self.port)
            except Exception:
                await self.send(text_data=json.dumps({
                    'message': '>> connection error: timeout'
                }))
        elif command == 'subscribe':
            topic = payload
            # Subscribe the MQTT message
            self.client.subscribe(topic + '/#')
        elif command == 'unsubscribe':
            topic = payload
            # Unsubscribe the MQTT message
            self.client.unsubscribe(topic + '/#')

    def on_connect(self, client, userdata, flags, rc):
        print("Connected with result code {} ".format(rc))

    def on_subscribe(self, client, userdata, mid, granted_qos):
        print("Subscribed: {}, {}".format(mid, granted_qos[0]))

    def on_message_sync(self, client, userdata, msg):
        # When MQTT message is received, send it to WebSocket
        # Use async_to_sync to call the asynchronous send method from a synchronous context
        print('on message: {}'.format(msg.payload.decode()))
        async_to_sync(self.send)(text_data=json.dumps({
            'message': msg.payload.decode()
        }))

    async def disconnect(self, close_code):
        self.client.loop_stop()
        self.client.disconnect()
