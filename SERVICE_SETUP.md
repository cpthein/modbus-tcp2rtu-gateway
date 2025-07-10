# Modbus Gateway Service Setup (systemd)

This guide explains how to configure systemd services for running multiple Modbus TCP to RS485 gateways on a Raspberry Pi or Linux system.

## 🧰 Service File Example: `modbus-gateway-0.service`

```ini
[Unit]
Description=Modbus TCP to RS485 Gateway (Adapter 0)
After=network.target

[Service]
ExecStart=/home/youruser/modbus-gateway/venv/bin/python /home/youruser/modbus-gateway/modbus-tcp2rtu-gateway.py --rs485 /dev/ttyACM0 --port 8899 --quiet
WorkingDirectory=/home/youruser/modbus-gateway
Restart=always
RestartSec=5
User=youruser

[Install]
WantedBy=multi-user.target
```

## 🔍 Explanation of Sections

### `[Unit]`

* **Description**: A human-readable name for the service.
* **After=network.target**: Ensures the service starts only after the network is up.

### `[Service]`

* **ExecStart**: Launches the gateway script with desired parameters:

  * `--rs485`: Path to RS485 adapter (e.g., `/dev/ttyACM0`)
  * `--port`: TCP listening port (e.g., `8899`)
  * `--quiet`: Suppresses stdout, logs only to file
* **WorkingDirectory**: Needed so logs and venv can be found
* **Restart=always**: Restarts service on failure
* **RestartSec=5**: Waits 5 seconds before restarting
* **User=youruser**: Runs under normal user (replace with your Linux username)

### `[Install]`

* **WantedBy=multi-user.target**: Enables startup at boot time (non-GUI runlevel)

## 🧪 Testing

```bash
sudo systemctl daemon-reload
sudo systemctl enable modbus-gateway-0.service
sudo systemctl start modbus-gateway-0.service
```

To check status:

```bash
systemctl status modbus-gateway-0.service
```

## 📦 Virtual Environment (venv)

To isolate dependencies (like pymodbus/pyserial), we recommend creating a Python virtual environment.

### Create it (only once):

```bash
cd ~/modbus-gateway
python3 -m venv venv
source venv/bin/activate
pip install pymodbus pyserial
```

### Use in `ExecStart`

Your `ExecStart` line must use the full path to the virtual environment's `python` binary, e.g.:

```bash
/home/youruser/modbus-gateway/venv/bin/python
```

---

You can repeat the above process for `modbus-gateway-1.service`, changing:

* `--rs485` to `/dev/ttyACM1`
* `--port` to `8898`
* and the service name accordingly

---

> ✅ Pro tip: keep log files separate per adapter using the built-in log filename logic in the script.

If you’re using `logrotate`, make sure to include wildcard patterns like:

```conf
/home/youruser/modbus-gateway/modbus-gateway-ttyACM*-*.log
```

