#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import paho.mqtt.client as mqtt
import json

# MQTT client to connect to the bus
mqtt_client = mqtt.Client()


def on_connect(client, userdata, flags, rc):
    client.subscribe("hermes/intent/#")

def on_message(client, userdata, msg):
    data = json.loads(msg.payload.decode('utf8'))
    intentname = data['intent']['intentName']
    deviceName = data['slots']['value']['value'] 
    session_id = data['sessionId']
    
    if intentname == "BroekerFrank:switchOnIntent":
        text = 'Das Gerät ' +deviceName + 'wurde eingeschaltet.'
        mqtt_client.publish('hermes/dialogueManager/endSession', json.dumps({'text': text, "sessionId": session_id}))

    if intentname == "BroekerFrank:switchOffIntent":
        text = 'Das Gerät ' +deviceName + 'wurde ausgeschaltet.'
        mqtt_client.publish('hermes/dialogueManager/endSession', json.dumps({'text': text, "sessionId": session_id}))

def parse_slots(data):
    # We extract the slots as a dict
    return {slot['slotName']: slot['value']['value'] for slot in data['slots']}

if __name__ == "__main__":
    mqtt_client.on_connect = on_connect
    mqtt_client.on_message = on_message
    mqtt_client.connect("localhost", 1883)
mqtt_client.loop_forever()
