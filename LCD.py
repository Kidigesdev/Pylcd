import psutil
import serial
import subprocess
import time

# Serielle Verbindung zum Arduino herstellen
arduino = serial.Serial('/dev/ttyACM0', 9600, timeout=1)  # Passe den Port an
time.sleep(2)  # Warte auf die Verbindung

def get_system_stats():
    #CPU-Auslastung auslesen in Prozent
    cpu_usage = psutil.cpu_percent(interval=1)
    #Ram Auslastung in MB
    memory = psutil.virtual_memory()
    used_ram = memory.used / (1024 * 1024)
    total_ram = 32768
     
    return cpu_usage, used_ram, total_ram

def read_serial():
    if arduino.in_waiting > 0:  # Überprüfe, ob Daten im Puffer sind
        datae = arduino.readline()  # Lese eine Zeile
        print(f"Empfange Daten: {datae}")

while True:
    cpu_usage, used_ram, total_ram = get_system_stats()
    data = f"{cpu_usage:.2f},{used_ram:.2f},{total_ram:.2f},\n"
    print(f"Sende Daten: {data.strip()}")
    read_serial()
    read_serial()
    read_serial()
    read_serial()
    print(f"-------------------------------")
    arduino.write(data.encode('utf-8'))  # Daten senden
    time.sleep(1)  # Sende alle 1 Sekunde