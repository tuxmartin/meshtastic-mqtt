import uuid
import mqtt_pb2 as mqtt_pb2
from paho.mqtt import client as mqtt_client

class MeshtasticMQTT():

    ################# edit here
    broker = 'XXX'
    username = 'XXX'
    password = 'XXX'
    port = 1883
    meshtastic_channel_name = 'TEST'
    ################# edit here

    topic = "msh/2/c/" + meshtastic_channel_name + "/#"
    client_id = f'meshtastic-python-{uuid.uuid4()}'

    def connect_mqtt(self) -> mqtt_client:
        def on_connect(client, userdata, flags, rc):
            if rc == 0:
                print("Connected to MQTT Broker!")
            else:
                print("Failed to connect, return code %d\n", rc)

        client = mqtt_client.Client(self.client_id)
        client.username_pw_set(self.username, self.password)
        client.on_connect = on_connect
        client.connect(self.broker, self.port)
        return client

    def subscribe(self, client: mqtt_client):
        def on_message(client, userdata, msg):
            se = mqtt_pb2.ServiceEnvelope()
            se.ParseFromString(msg.payload)
            print('---------------------------------------')
            print(se) # print packet

        client.subscribe(self.topic)
        client.on_message = on_message

    def run(self):
        client = self.connect_mqtt()
        self.subscribe(client)
        client.loop_forever()

    def initialize(self):
        self.run(self)

def main():
    mm = MeshtasticMQTT()
    mm.run()

if __name__ == '__main__':
    main()
