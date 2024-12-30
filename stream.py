#!/usr/bin/python3

import pyamdgpuinfo
import json
import psutil
import subprocess
import time

first_gpu = pyamdgpuinfo.get_gpu(0)

def get_system_stats():
    #CPU-Auslastung auslesen in Prozent
    cpu_usage = psutil.cpu_percent(interval=1)
    #Ram Auslastung in MB
    memory = psutil.virtual_memory()
    used_ram = memory.used / (1024 * 1024)
    total_ram = 32768
     
    return cpu_usage, used_ram, total_ram

def get_gpu_data():
    #GPU auslastung lesen
    gpu_usage = first_gpu.query_load() * 100
    #VRAM auslastung lesen
    vram_usage = first_gpu.query_vram_usage() / (1024 ** 2)

    return gpu_usage, vram_usage

def daten_schreiben ():
    # zu speichernde daten
    data = {
        "cpu_usage": cpu_usage,
        "used_ram": used_ram,
        "total_ram": total_ram,
        "gpu_usage": gpu_usage,
        "vram_usage": vram_usage
    }
    # Daten abspeichern
    with open("/mnt/Storinator/pidata/data.json", "w") as json_file:
        json.dump(data, json_file, indent=4)
    
                  
while True:
    cpu_usage, used_ram, total_ram = get_system_stats()
    gpu_usage, vram_usage = get_gpu_data()
    daten_schreiben()
    #print(f"data: {cpu_usage:.2f}, {used_ram:.0f}/{total_ram:.0f}")
    time.sleep(2)