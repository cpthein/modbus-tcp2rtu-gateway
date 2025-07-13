# Datei: modbus-tcp2rtu-gateway.py
import socket
import serial
import logging
import time
import argparse
from struct import pack

# Argumente
parser = argparse.ArgumentParser(description="Modbus TCP → RTU Gateway")
parser.add_argument("--rs485", default="/dev/ttyACM0", help="RS485-Gerät (z. B. /dev/ttyUSB0)")
parser.add_argument("--port", type=int, default=8899, help="TCP-Port (z. B. 8899)")
parser.add_argument("--quiet", action="store_true", help="Keine Konsolenausgabe")
parser.add_argument("--debug", action="store_true", help="Mehr Logging-Details")
parser.add_argument("--nolog", action="store_true", help="Kein Logging (für stabile Systeme)")
args = parser.parse_args()

# Logdateiname abhängig von Port & tty
log_file = f"modbus-gateway-{args.rs485.split('/')[-1]}-{args.port}.log"

# Logging
if not args.nolog:
    logging.basicConfig(
        filename=log_file,
        level=logging.DEBUG if args.debug else logging.INFO,
        format="%(asctime)s - %(levelname)s - %(message)s"
    )
    if not args.quiet:
        console = logging.StreamHandler()
        console.setLevel(logging.DEBUG if args.debug else logging.INFO)
        console.setFormatter(logging.Formatter("%(asctime)s - %(levelname)s - %(message)s"))
        logging.getLogger().addHandler(console)
else:
    logging.basicConfig(level=logging.CRITICAL)  # Nur Fehler intern, keine Datei

# RS485 öffnen
BAUDRATE = 9600
TIMEOUT = 0.1
rs485 = serial.Serial(args.rs485, BAUDRATE, timeout=TIMEOUT)

# Retry-Konfiguration
MAX_RETRIES = 2
RETRY_DELAY = 0.2

# TCP starten
logging.info(f"Starte TCP → RS485 Gateway auf Port {args.port}")

def crc16(data: bytes):
    crc = 0xFFFF
    for b in data:
        crc ^= b
        for _ in range(8):
            if crc & 0x0001:
                crc >>= 1
                crc ^= 0xA001
            else:
                crc >>= 1
    return pack('<H', crc)

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.bind(("0.0.0.0", args.port))
    server_socket.listen()

    while True:
        client_socket, addr = server_socket.accept()
        with client_socket:
            logging.info(f"Neue Verbindung von {addr}")
            try:
                while True:
                    data = client_socket.recv(1024)
                    if not data:
                        break

                    logging.info(f"TCP → RAW: {data.hex()}")
                    request = data[6:]
                    serial_data = request + crc16(request)
                    logging.info(f"→ RS485: {serial_data.hex()}")

                    response = None
                    for attempt in range(1, MAX_RETRIES + 2):
                        rs485.write(serial_data)
                        time.sleep(0.05)

                        time_start = time.time()
                        buffer = bytearray()
                        while time.time() - time_start < 1.5:
                            if rs485.in_waiting:
                                buffer += rs485.read(rs485.in_waiting)
                                if len(buffer) >= 5:
                                    break
                            time.sleep(0.01)

                        if buffer:
                            response = buffer
                            if attempt > 1:
                                logging.info(f"✅ Wiederholung Nr. {attempt} erfolgreich")
                            break
                        else:
                            logging.warning(f"⚠️ Keine Antwort (Versuch {attempt})")
                            time.sleep(RETRY_DELAY)

                    if response:
                        logging.info(f"← RS485: {response.hex()}")
                        mbap = data[:4] + b'\x00' + bytes([len(response)])
                        full = mbap + response
                        client_socket.sendall(full)
                        logging.info(f"← TCP: {full.hex()}")
                    else:
                        logging.error("❌ Keine Antwort vom Gerät.")

            except Exception as e:
                logging.error(f"Fehler: {e}")
            finally:
                logging.info(f"Verbindung von {addr} geschlossen")

