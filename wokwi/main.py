import network
import time
import json
from machine import Pin
import dht
from umqtt.simple import MQTTClient

WIFI_SSID = "Wokwi-GUEST"
WIFI_PASSWORD = ""
MQTT_CLIENT_ID = "fiap-spacecapsule-esp32"
MQTT_BROKER = "broker.hivemq.com"
MQTT_PORT = 1883
MQTT_TOPIC = "fiap/gs/spacecapsule/telemetry"

sensor = dht.DHT22(Pin(15))


def conectar_wifi():
    print("Conectando ao Wi-Fi...")
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    wlan.connect(WIFI_SSID, WIFI_PASSWORD)
    while not wlan.isconnected():
        print(".", end="")
        time.sleep(0.5)
    print("\nWi-Fi conectado!")
    print("IP:", wlan.ifconfig()[0])


def conectar_mqtt():
    client = MQTTClient(MQTT_CLIENT_ID, MQTT_BROKER, port=MQTT_PORT)
    client.connect()
    print("Conectado ao broker MQTT.")
    return client


def classificar_status(temperatura):
    if temperatura >= 40:
        return "FALHA_NO_RESFRIAMENTO"
    elif temperatura >= 35:
        return "CRITICO"
    elif temperatura >= 25:
        return "ATENCAO"
    else:
        return "NORMAL"


conectar_wifi()
mqtt_client = conectar_mqtt()

while True:
    try:
        sensor.measure()
        temperatura = sensor.temperature()
        umidade = sensor.humidity()
        status = classificar_status(temperatura)
        payload = {
            "temperatura": temperatura,
            "umidade": umidade,
            "status": status,
            "origem": "ESP32_WOKWI_DHT22"
        }
        mensagem = json.dumps(payload)
        mqtt_client.publish(MQTT_TOPIC, mensagem)
        print("Dados enviados:", mensagem)
    except Exception as erro:
        print("Erro ao ler sensor ou enviar MQTT:", erro)
    time.sleep(3)
