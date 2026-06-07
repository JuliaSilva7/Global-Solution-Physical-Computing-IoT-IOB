import json
from datetime import datetime

import cv2
import numpy as np
import paho.mqtt.client as mqtt

BROKER = "broker.hivemq.com"
PORT = 1883
TOPIC = "fiap/gs/spacecapsule/telemetry"

latest_data = {
    "temperatura": 0.0,
    "umidade": 0.0,
    "status": "AGUARDANDO DADOS",
    "timestamp": "-"
}


def classificar_status(temperatura: float) -> str:
    if temperatura >= 40:
        return "FALHA NO RESFRIAMENTO"
    if temperatura >= 35:
        return "CRITICO"
    if temperatura >= 25:
        return "ATENCAO"
    return "NORMAL"


def cor_por_status(status: str):
    if status == "NORMAL":
        return (0, 200, 0)
    if status == "ATENCAO":
        return (0, 200, 255)
    if status == "CRITICO":
        return (0, 0, 255)
    if status == "FALHA NO RESFRIAMENTO":
        return (0, 0, 180)
    return (180, 180, 180)


def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("Conectado ao broker MQTT.")
        client.subscribe(TOPIC)
        print(f"Inscrito no tópico: {TOPIC}")
    else:
        print(f"Erro ao conectar. Código: {rc}")


def on_message(client, userdata, msg):
    global latest_data
    try:
        payload = msg.payload.decode("utf-8")
        data = json.loads(payload)
        temperatura = float(data.get("temperatura", 0))
        umidade = float(data.get("umidade", 0))
        status = classificar_status(temperatura)
        latest_data = {
            "temperatura": temperatura,
            "umidade": umidade,
            "status": status,
            "timestamp": datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        }
        print(f"Recebido: {latest_data}")
    except Exception as erro:
        print(f"Erro ao processar mensagem MQTT: {erro}")


def desenhar_capsula():
    frame = np.zeros((620, 900, 3), dtype=np.uint8)
    frame[:] = (15, 18, 25)

    temperatura = latest_data["temperatura"]
    umidade = latest_data["umidade"]
    status = latest_data["status"]
    timestamp = latest_data["timestamp"]
    cor_status = cor_por_status(status)

    cv2.putText(frame, "SPACE CAPSULE VISION MONITOR", (45, 55),
                cv2.FONT_HERSHEY_SIMPLEX, 1.1, (255, 255, 255), 2)
    cv2.putText(frame, "Visao Computacional Simulada - Python/OpenCV", (45, 88),
                cv2.FONT_HERSHEY_SIMPLEX, 0.65, (180, 180, 180), 1)

    # Corpo da capsula
    cv2.rectangle(frame, (80, 150), (520, 510), (120, 120, 120), 3)
    cv2.rectangle(frame, (115, 185), (485, 475), (45, 50, 65), -1)
    cv2.circle(frame, (300, 270), 70, (180, 180, 180), 3)
    cv2.circle(frame, (300, 270), 55, (25, 35, 55), -1)
    cv2.rectangle(frame, (150, 380), (250, 440), (70, 90, 120), -1)
    cv2.rectangle(frame, (350, 380), (450, 440), (70, 90, 120), -1)

    # Painel de status
    cv2.rectangle(frame, (580, 150), (835, 260), cor_status, -1)
    cv2.putText(frame, "STATUS", (600, 190), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 255, 255), 2)
    cv2.putText(frame, status, (600, 230), cv2.FONT_HERSHEY_SIMPLEX, 0.55, (255, 255, 255), 2)

    # Dados
    cv2.rectangle(frame, (580, 300), (835, 510), (35, 40, 55), -1)
    cv2.putText(frame, f"Temperatura: {temperatura:.1f} C", (600, 350),
                cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)
    cv2.putText(frame, f"Umidade: {umidade:.1f} %", (600, 395),
                cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)
    cv2.putText(frame, "Atualizado:", (600, 445), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (180, 180, 180), 1)
    cv2.putText(frame, timestamp, (600, 475), cv2.FONT_HERSHEY_SIMPLEX, 0.55, (180, 180, 180), 1)

    if status == "FALHA NO RESFRIAMENTO":
        texto = "ALERTA: SISTEMA TERMICO EM FALHA!"
        cor = (0, 0, 255)
    elif status == "CRITICO":
        texto = "ALERTA: TEMPERATURA CRITICA NA CAPSULA!"
        cor = (0, 0, 255)
    elif status == "ATENCAO":
        texto = "ATENCAO: TEMPERATURA ACIMA DO IDEAL."
        cor = (0, 200, 255)
    else:
        texto = "CONDICOES INTERNAS ESTAVEIS."
        cor = (0, 200, 0)

    cv2.putText(frame, texto, (120, 575), cv2.FONT_HERSHEY_SIMPLEX, 0.8, cor, 2)
    return frame


def main():
    client = mqtt.Client(
        client_id="python_spacecapsule_monitor",
        callback_api_version=mqtt.CallbackAPIVersion.VERSION1
    )
    client.on_connect = on_connect
    client.on_message = on_message
    print("Conectando ao broker MQTT...")
    client.connect(BROKER, PORT, 60)
    client.loop_start()
    print("Abrindo janela OpenCV. Pressione Q para sair.")

    try:
        while True:
            frame = desenhar_capsula()
            cv2.imshow("Space Capsule Vision Monitor", frame)
            if cv2.waitKey(100) & 0xFF == ord("q"):
                break
    except KeyboardInterrupt:
        print("Encerrando aplicação...")
    finally:
        client.loop_stop()
        client.disconnect()
        cv2.destroyAllWindows()


if __name__ == "__main__":
    main()
