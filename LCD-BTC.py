#! /usr/bin/python3
import json
import time
import requests
import paho.mqtt.client as mqtt
from RPLCD.i2c import CharLCD

# =====================
# MQTT-Konfiguration
# =====================
MQTT_BROKER = "[BROKER IP ADRESS]"
MQTT_PORT = 1883
MQTT_TOPIC = ["MQQT/TOPIC"]
MQTT_USER = ["USER_FOR_MQTT"]
MQTT_PASS = ["USER_PW"]

# =====================
# LCD initialisieren
# =====================
lcd = CharLCD(
    i2c_expander='PCF8574',
    address=0x27,
    port=1,
    cols=20,
    rows=4,
    dotsize=8
)
lcd.clear()

# =====================
# Globale Sensorwerte
# =====================
cpu_usage = 0.0
used_ram = 0.0
gpu_usage = 0.0
vram_usage = 0.0
cpu_temp = 0
gpu_temp = 0

# =====================
# Seitensteuerung
# =====================
PAGE_SYSTEM = 0
PAGE_BTC = 1

current_page = PAGE_SYSTEM
last_page_switch = time.time()

# =====================
# Bitcoin-Daten
# =====================
btc_price = 0
btc_change_1h = 0.0
last_btc_update = 0

# =====================
# MQTT Callbacks
# =====================
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
        print(f"MQTT Fehler: {e}")

def on_connect(client, userdata, flags, rc):
    if rc == 0:
        client.subscribe(MQTT_TOPIC)

# =====================
# MQTT Client starten
# =====================
client = mqtt.Client()
client.username_pw_set(MQTT_USER, MQTT_PASS)
client.on_connect = on_connect
client.on_message = on_message

client.connect(MQTT_BROKER, MQTT_PORT, 60)
client.loop_start()

# =====================
# Bitcoin API (CoinGecko)
# =====================
def get_btc_price():
    try:
        r = requests.get(
            "https://api.coingecko.com/api/v3/coins/markets",
            params={
                "vs_currency": "eur",
                "ids": "bitcoin",
                "price_change_percentage": "1h"
            },
            timeout=3
        )
        data = r.json()[0]

        price = int(data["current_price"])
        change_1h = data["price_change_percentage_1h_in_currency"]

        return price, change_1h
    except Exception:
        return None, None

# =====================
# Hauptloop
# =====================
while True:
    now = time.time()

    # 🔁 Seite alle 10 Sekunden wechseln
    if now - last_page_switch >= 10:
        current_page = PAGE_BTC if current_page == PAGE_SYSTEM else PAGE_SYSTEM
        last_page_switch = now
        lcd.clear()

    # ₿ BTC nur alle 60 Sekunden aktualisieren
    if now - last_btc_update >= 60:
        price, change = get_btc_price()
        if price is not None:
            btc_price = price
            btc_change_1h = change
        last_btc_update = now

    # =====================
    # Seite 1: Systemstatus
    # =====================
    if current_page == PAGE_SYSTEM:
        lcd.cursor_pos = (0, 0)
        lcd.write_string(
            f"CPU:  {cpu_usage:4.1f}%".ljust(13) +
            f"T: {cpu_temp:.0f}C"
        )

        lcd.cursor_pos = (1, 0)
        lcd.write_string(
            f"RAM:  {used_ram:.0f}/32768 MB".ljust(20)
        )

        lcd.cursor_pos = (2, 0)
        lcd.write_string(
            f"GPU:  {gpu_usage:4.1f}%".ljust(13) +
            f"T: {gpu_temp:.0f}C"
        )

        lcd.cursor_pos = (3, 0)
        lcd.write_string(
            f"VRAM: {vram_usage:.0f}/16384 MB".ljust(20)
        )

    # =====================
    # Seite 2: Bitcoin
    # =====================
    elif current_page == PAGE_BTC:
        lcd.cursor_pos = (0, 0)
        lcd.write_string(" Bitcoin Status ".center(20))

        lcd.cursor_pos = (1, 0)
        lcd.write_string(f"Preis: {btc_price} EUR".ljust(20))

        lcd.cursor_pos = (2, 0)
        lcd.write_string(f"1h: {btc_change_1h:+.2f}%".center(20))

        lcd.cursor_pos = (3, 0)
        lcd.write_string("".ljust(20))

    time.sleep(1)
