# Roteiro do Vídeo – até 3 minutos

## 1. Introdução
Olá, somos a equipe responsável pelo projeto SpaceCapsule Vision Monitor, desenvolvido para a Global Solution de Physical Computing, IoT e IoB.

## 2. Problema
Em uma cápsula espacial, a temperatura interna precisa ser monitorada constantemente para garantir a segurança dos equipamentos e dos astronautas.

## 3. Solução
Nossa solução utiliza ESP32 simulado no Wokwi, sensor DHT22, MQTT, Python, OpenCV e Node-RED para monitorar a temperatura em tempo real.

## 4. Funcionamento
O ESP32 coleta a temperatura e a umidade e envia os dados por MQTT. O Python recebe esses dados e exibe uma visão computacional simulada da cápsula usando OpenCV. O Node-RED apresenta os dados em um dashboard com gauge, gráfico e alertas.

## 5. Regras de alerta
Temperatura abaixo de 25 graus é normal. Entre 25 e 34 graus é atenção. Acima de 35 graus é crítico. Acima de 40 graus indica falha no sistema de resfriamento.

## 6. Conclusão
O projeto demonstra uma arquitetura integrada de IoT, dashboard e visão computacional aplicada ao contexto da indústria espacial.
