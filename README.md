# SpaceCapsule Vision Monitor

Projeto da Global Solution – Physical Computing / IoT & IoB.

## Objetivo

Sistema inteligente para monitoramento de temperatura interna de uma cápsula espacial, utilizando ESP32 no Wokwi, sensor DHT22 simulado, MQTT, Python, OpenCV e Node-RED Dashboard.

## Funcionamento

O ESP32 lê a temperatura do sensor DHT22 e publica os dados em MQTT. O Python recebe os dados, processa o status térmico e exibe uma visão computacional simulada da cápsula espacial usando OpenCV. O Node-RED recebe os mesmos dados via MQTT e exibe um dashboard com gauge, gráfico e alertas.

## Arquitetura

ESP32 + DHT22 no Wokwi → MQTT → Broker HiveMQ público → Python + OpenCV → Node-RED Dashboard

## Regras de Status

| Temperatura | Status |
|---|---|
| menor que 25°C | NORMAL |
| 25°C até 34.9°C | ATENÇÃO |
| 35°C até 39.9°C | CRÍTICO |
| 40°C ou mais | FALHA NO RESFRIAMENTO |

## Como executar

### Wokwi

Use os arquivos da pasta `wokwi`:

- `main.py`
- `diagram.json`

### Python

```bash
pip install -r python/requirements.txt
python python/capsule_vision_monitor.py
```

### Node-RED

Importe o arquivo:

```text
nodered/flow.json
```

Instale o dashboard clássico se necessário:

```bash
npm install node-red-dashboard
```

Acesse:

```text
http://localhost:1880/ui
```

## Tópico MQTT

```text
fiap/gs/spacecapsule/telemetry
```

## Observação

O projeto utiliza dados simulados no Wokwi, mas representa uma aplicação real de monitoramento térmico em cápsulas espaciais.
