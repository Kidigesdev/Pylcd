#!/usr/bin/python3

import pyamdgpuinfo
import json
import psutil
import time
import paho.mqtt.client as mqtt

# MQTT-Konfiguration
MQTT_BROKER = "[BROKER IP ADRESS]"
MQTT_PORT = 1883
MQTT_TOPIC = ["MQQT/TOPIC"]
MQTT_USER = ["USER_FOR_MQTT"]
MQTT_PASS = ["USER_PW"]

# MQTT-Client einrichten und verbinden
client = mqtt.Client(callback_api_version=mqtt.CallbackAPIVersion.VERSION2)
client.username_pw_set(MQTT_USER, MQTT_PASS)
client.connect(MQTT_BROKER, MQTT_PORT, 60)

first_gpu = pyamdgpuinfo.get_gpu(0)

def get_system_stats():
    #Erfasst CPU- und RAM-Auslastung
    cpu_usage = psutil.cpu_percent(interval=1)
    memory = psutil.virtual_memory()
    used_ram = memory.used / (1024 * 1024)
    total_ram = memory.total / (1024 * 1024)

    # CPU-Temperatur abrufen (kann je nach Sensor unterschiedlich sein)
    temp_sensors = psutil.sensors_temperatures()
    cpu_temp = temp_sensors.get("k10temp", [])[0].current if "k10temp" in temp_sensors else 39


    return cpu_usage, used_ram, total_ram, cpu_temp

def get_gpu_data():
    #Erfasst GPU- und VRAM-Auslastung
    gpu_usage = first_gpu.query_load() * 100
    vram_usage = first_gpu.query_vram_usage() / (1024 ** 2)
    gpu_temp = first_gpu.query_temperature()  # GPU-Temperatur abrufen

    return gpu_usage, vram_usage, gpu_temp

while True:
    cpu_usage, used_ram, total_ram, cpu_temp = get_system_stats()
    gpu_usage, vram_usage, gpu_temp = get_gpu_data()

    # Daten als JSON zusammenstellen
    data = {
        "cpu_usage": cpu_usage,
        "used_ram": used_ram,
        "total_ram": total_ram,
        "cpu_temp": cpu_temp,
        "gpu_usage": gpu_usage,
        "vram_usage": vram_usage,
        "gpu_temp": gpu_temp
    }

    # Daten per MQTT senden
    client.publish(MQTT_TOPIC, json.dumps(data))
    #print(f"Gesendet: {data}")

    time.sleep(1)  # Alle 1 Sekunden senden
