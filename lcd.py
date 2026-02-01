#! /usr/bin/python
import json
import time
import paho.mqtt.client as mqtt
from RPLCD.i2c import CharLCD

# MQTT-Konfiguration
MQTT_BROKER = "[BROKER IP ADRESS]"
MQTT_PORT = 1883
MQTT_TOPIC = ["MQQT/TOPIC"]
MQTT_USER = ["USER_FOR_MQTT"]
MQTT_PASS = ["USER_PW"]

# LCD initialisieren
lcd = CharLCD(i2c_expander='PCF8574', address=0x27, port=1, cols=20, rows=4, dotsize=8)
lcd.clear()

# Globale Variablen f  r die Sensorwerte
cpu_usage = 0.0
used_ram = 0.0
gpu_usage = 0.0
vram_usage = 0.0
cpu_temp = 0
gpu_temp = 0


# MQTT Callback f  r empfangene Nachrichten
def on_message(client, userdata, msg):
    global cpu_usage, used_ram, gpu_usage, vram_usage, cpu_temp, gpu_temp

    try:
        data = json.loads(msg.payload.decode("utf-8"))
        cpu_usage = data.get("cpu_usage", 0)
        used_ram = data.get("used_ram", 0)
        gpu_usage = data.get("gpu_usage", 0)
        vram_usage = data.get("vram_usage", 0)
        cpu_temp = data.get("cpu_temp", 0)
        gpu_temp = data.get("gpu_temp", 0)
    except Exception as e:
        print(f"Fehler beim Verarbeiten der MQTT-Daten: {e}")

# MQTT Callback f  r Verbindungsstatus
def on_connect(client, userdata, flags, rc):
    if rc == 0:
#        print(" ^|^e Erfolgreich mit MQTT-Broker verbunden")
        client.subscribe(MQTT_TOPIC)
#    else:
#        print(f" ^z   ^o Verbindung fehlgeschlagen, Fehlercode: {rc}")

# MQTT-Client einrichten
client = mqtt.Client()
client.username_pw_set(MQTT_USER, MQTT_PASS)
client.on_connect = on_connect
client.on_message = on_message

# Verbindung herstellen
client.connect(MQTT_BROKER, MQTT_PORT, 60)
client.loop_start()

# LCD aktualisieren
while True:
    lcd.cursor_pos = (0, 0)
    lcd.write_string('CPU:  {:.1f}%'.format(cpu_usage).ljust(13) + 'T: {:.0f}C'.format(cpu_temp))

    lcd.cursor_pos = (1, 0)
    lcd.write_string('RAM:  {:.0f}/32768 MB'.format(used_ram).ljust(20))

    lcd.cursor_pos = (2, 0)
    lcd.write_string('GPU:  {:.1f}%'.format(gpu_usage).ljust(13) + 'T: {:.0f}C'.format(gpu_temp))

    lcd.cursor_pos = (3, 0)
    lcd.write_string('VRAM: {:.0f}/16384 MB'.format(vram_usage).ljust(20))

    time.sleep(1)
