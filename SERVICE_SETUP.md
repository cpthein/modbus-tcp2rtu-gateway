# SERVICE\_SETUP.md

This file describes how to set up the **Modbus TCP to RS485 Gateway** as a `systemd` service on a Raspberry Pi or similar Linux-based system.

---

## 📁 Project Directory

Clone or copy the gateway script to your working directory, e.g.:

```bash
cd ~
mkdir modbus-gateway
cd modbus-gateway
```

---

## 🐍 Create Virtual Environment (venv)

It is strongly recommended to use a virtual Python environment to avoid dependency conflicts.

```bash
python3 -m venv venv
source venv/bin/activate
```

Install required packages:

```bash
pip install pymodbus==2.5.3 pyserial
```

If `pymodbus` version is incorrect, Modbus communication will not work properly. We explicitly need **version 2.5.3**.

---

## 🧠 Example systemd Service File

Create the file `/etc/systemd/system/modbus-gateway-0.service`:

```ini
[Unit]
Description=Modbus TCP to RS485 Gateway (Adapter 0)
After=network.target

[Service]
ExecStart=/home/YOURUSER/modbus-gateway/venv/bin/python /home/YOURUSER/modbus-gateway/modbus-tcp2rtu-gateway.py --rs485 /dev/ttyACM0 --port 8899 --quiet
WorkingDirectory=/home/YOURUSER/modbus-gateway
StandardOutput=journal
Restart=on-failure

[Install]
WantedBy=multi-user.target
```

Replace `YOURUSER` with your actual Linux username. Change the RS485 port and TCP port to fit your setup.

You may create a second service `/etc/systemd/system/modbus-gateway-1.service` for `/dev/ttyACM1` and another TCP port.

---

## 🧩 Enable and Start the Service

```bash
sudo systemctl daemon-reload
sudo systemctl enable modbus-gateway-0.service
sudo systemctl start modbus-gateway-0.service
```

Use `status` to verify:

```bash
systemctl status modbus-gateway-0.service
```

---

## 📋 Log File Location

Each instance writes its log to:

```bash
modbus-gateway-ttyACM0-8899.log
```

If started with `--nolog`, logging will be disabled.

---

## ♻️ Optional: Log Rotation

Add the following file:

```bash
sudo nano /etc/logrotate.d/modbus-gateway
```

```ini
/home/YOURUSER/modbus-gateway/modbus-gateway-*.log {
    daily
    rotate 7
    compress
    missingok
    notifempty
    copytruncate
}
```

---

## ✅ Summary

* Use `venv` for isolated Python environment
* Install exact version `pymodbus==2.5.3`
* Create systemd units per adapter (ACM0, ACM1...)
* Use `--quiet` and optionally `--nolog`
* Enable logrotate to protect SD card lifespan

---

Maintained  by [cpthein](https://github.com/cpthein) and ChatGPT

