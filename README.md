# Modbus TCP to RS485 Gateway

## 🌍 English

This repository contains a **lightweight Modbus TCP to RS485 gateway**, written in Python, designed for running on a Raspberry Pi with multiple USB RS485 adapters. It allows Modbus TCP masters (like ioBroker, Node-RED, etc.) to communicate with RS485-based Modbus RTU slaves (e.g. inverters, battery systems) over the network.

### Features

* 🔌 Bridges TCP Modbus requests to a serial RS485 device
* ⚙️ Configurable serial device and TCP port (e.g. `/dev/ttyACM0`, port `8899`)
* 🔒 Isolated log files per adapter (e.g. `modbus-gateway-ttyACM0-8899.log`)
* 🌐 Can be started as a `systemd` service (see `modbus-gateway-0.service`, `modbus-gateway-1.service`)
* ♻️ Optional log rotation via `logrotate`
* ⚡ Robust retry mechanism for failed Modbus requests
* ❌ `--nolog` disables logging completely

### Usage

```bash
python modbus-tcp2rtu-gateway.py --rs485 /dev/ttyACM0 --port 8899 --quiet
```

Optional:

* `--debug` enables debug output
* `--quiet` suppresses stdout, logs only to file
* `--nolog` disables logging completely (no log file will be written)

### systemd Integration

To autostart gateways on boot:

1. Copy and edit the included `modbus-gateway-0.service` and `modbus-gateway-1.service`
2. Enable via:

```bash
sudo systemctl enable modbus-gateway-0.service
sudo systemctl enable modbus-gateway-1.service
```

### Tested With

* Raspberry Pi OS (Debian Bookworm)
* Python 3.11
* pymodbus 2.5.3
* ioBroker Modbus Adapter
* Deye Hybrid Inverter (SUN-6K-SG03LP1-EU)
* BMS with Modbus RTU protocol

---

## 🇩🇪 Deutsch

Dieses Repository enthält ein **leichtgewichtiges Python-Gateway**, das Modbus TCP-Anfragen an ein serielles RS485-Gerät weiterleitet. Es eignet sich z. B. für den Raspberry Pi mit mehreren USB-RS485-Adaptern, um ioBroker-Modbus-Instanzen über das Netzwerk zu entkoppeln.

### Funktionen

* 🔌 Übersetzt TCP zu RS485 (Modbus RTU)
* ⚙️ Konfigurierbarer Port und RS485-Gerät
* 🔒 Pro Adapter eigene Logdatei mit automatischer Rotation
* 🌐 systemd-Services für Autostart enthalten
* ⚡ Automatische Wiederholungen bei Timeout-Fehlern
* ❌ `--nolog` deaktiviert Logging vollständig

### Beispielaufruf

```bash
python modbus-tcp2rtu-gateway.py --rs485 /dev/ttyACM0 --port 8899 --quiet
```

Weitere Optionen:

* `--debug` für Debug-Ausgabe
* `--quiet` nur Logfile, keine Terminal-Ausgabe
* `--nolog` deaktiviert Logging vollständig (es wird keine Logdatei geschrieben)

### Autostart mit systemd

1. Services anpassen (z. B. `modbus-gateway-0.service`)
2. Aktivieren mit:

```bash
sudo systemctl enable modbus-gateway-0.service
sudo systemctl start modbus-gateway-0.service
```

### Getestete Umgebung

* Raspberry Pi OS (Debian 12)
* Python 3.11
* pymodbus 2.5.3
* ioBroker mit Modbus-Adapter
* Deye Wechselrichter 1-phasig
* JK-BMS mit Modbus RTU

---

### 📦 Dateien

* `modbus-tcp2rtu-gateway.py` – Hauptskript
* `modbus-gateway-0.service` – systemd Service für ersten Adapter
* `modbus-gateway-1.service` – systemd Service für zweiten Adapter
* `.gitignore` – Logfiles und virtuelle Umgebung ausgeschlossen

> Maintained by Cpthein and ChatGPT

