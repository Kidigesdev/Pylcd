#!/usr/bin/python3
import json
import time
import psutil
import paho.mqtt.client as mqtt
import platform

# Für Windows-spezifische Hardwareinfos
if platform.system() == "Windows":
    import wmi
    try:
        import pynvml  # NVIDIA GPUs
        pynvml.nvmlInit()
        HAS_NVML = True
    except:
        HAS_NVML = False

# =====================
# MQTT-Konfiguration
# =====================
MQTT_BROKER = "[BROKER IP ADRESS]"
MQTT_PORT = 1883
MQTT_TOPIC = ["MQQT/TOPIC"]
MQTT_USER = ["USER_FOR_MQTT"]
MQTT_PASS = ["USER_PW"]

client = mqtt.Client()
client.username_pw_set(MQTT_USER, MQTT_PASS)
client.connect(MQTT_BROKER, MQTT_PORT, 60)

# =====================
# WMI für CPU-Temperaturen
# =====================
if platform.system() == "Windows":
    w = wmi.WMI(namespace="root\wmi")

# =====================
# Funktionen
# =====================
def get_system_stats():
    cpu_usage = psutil.cpu_percent(interval=1)
    memory = psutil.virtual_memory()
    used_ram = memory.used / (1024 * 1024)
    total_ram = memory.total / (1024 * 1024)

    # CPU-Temperatur über WMI
    cpu_temp = 0
    if platform.system() == "Windows":
        try:
            temps = w.MSAcpi_ThermalZoneTemperature()
            if temps:
                # Umrechnung Kelvin/10 -> Celsius
                cpu_temp = sum([t.CurrentTemperature for t in temps]) / len(temps) / 10 - 273.15
            else:
                cpu_temp = 50  # Default
        except:
            cpu_temp = 50
    else:
        cpu_temp = 50

    return cpu_usage, used_ram, total_ram, cpu_temp

def get_gpu_data():
    gpu_usage = 0.0
    vram_usage = 0.0
    gpu_temp = 0.0

    if platform.system() == "Windows":
        # NVIDIA GPUs
        if HAS_NVML:
            try:
                handle = pynvml.nvmlDeviceGetHandleByIndex(0)
                gpu_usage = pynvml.nvmlDeviceGetUtilizationRates(handle).gpu
                vram_usage = pynvml.nvmlDeviceGetMemoryInfo(handle).used / (1024*1024)
                gpu_temp = pynvml.nvmlDeviceGetTemperature(handle, pynvml.NVML_TEMPERATURE_GPU)
            except:
                gpu_usage = 0
                vram_usage = 0
                gpu_temp = 0
        # AMD GPUs können über OpenHardwareMonitor oder andere Tools integriert werden
        # Für jetzt setzen wir die Werte auf 0, falls keine NVIDIA
        else:
            gpu_usage = 0
            vram_usage = 0
            gpu_temp = 0

    return gpu_usage, vram_usage, gpu_temp

# =====================
# Hauptloop
# =====================
while True:
    cpu_usage, used_ram, total_ram, cpu_temp = get_system_stats()
    gpu_usage, vram_usage, gpu_temp = get_gpu_data()

    data = {
        "cpu_usage": cpu_usage,
        "used_ram": used_ram,
        "total_ram": total_ram,
        "cpu_temp": cpu_temp,
        "gpu_usage": gpu_usage,
        "vram_usage": vram_usage,
        "gpu_temp": gpu_temp
    }

    client.publish(MQTT_TOPIC, json.dumps(data))
    # print(f"Gesendet: {data}")

    time.sleep(1)
