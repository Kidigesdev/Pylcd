import json
from RPLCD.i2c import CharLCD
import time
lcd = CharLCD(i2c_expander='PCF8574', address=0x27, port=1, cols=20, rows=4, dotsize=8)
lcd.clear()

def get_data():
        try:
                #datei einlesen
                with open('/home/kidiges/data/pidata/data.json', 'r') as file:
                        data = json.load(file)

                #daten verarbeiten
                cpu = data.get("cpu_usage")
                used_ram = data.get("used_ram")
                total_ram = data.get("total_ram")
                gpu = data.get("gpu_usage")
                vram= data.get("vram_usage")

                return cpu, used_ram, total_ram, gpu, vram
        except Exception as e:
                print(f"Fehler beim Lesen der Daten: {e}")
                return 0, 0, 0
        
while True:
        cpu, used_ram, total_ram, gpu, vram = get_data()
        data = f"{used_ram:.0f}"
        data2 = f"{vram:.0f}"
        lcd.cursor_pos = (0, 0)
        lcd.write_string('CPU: ')
        lcd.write_string(str(cpu))
        lcd.write_string('%')
        lcd.cursor_pos = (1, 0)
        lcd.write_string('RAM: ')
        lcd.write_string(str(data))
        lcd.write_string('/')
        lcd.write_string(str(total_ram))
        lcd.cursor_pos = (1, 16)
        lcd.write_string('MB')
        lcd.cursor_pos = (2, 0)
        lcd.write_string("GPU: ")
        lcd.write_string(str(gpu))
        lcd.write_string("%")
        lcd.cursor_pos = (3, 0)
        lcd.write_string("VRAM: ")
        lcd.write_string(str(data2))
        lcd.write_string("/16384 MB")
        time.sleep(5)
