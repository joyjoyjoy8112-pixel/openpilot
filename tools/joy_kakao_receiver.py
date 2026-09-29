#!/usr/bin/env python3
"""
JoyPilot Kakao Route Bridge -> openpilot customReservedRawData1 receiver.

사용:
  cd /data/openpilot
  python3 openpilot/tools/joy_kakao_receiver.py

데스크톱 replay 테스트 시 replay가 customReservedRawData1 publisher를 선점하지 않도록:
  openpilot/tools/replay/replay --demo --cabin --wide-road --block customReservedRawData1
"""
import argparse
import json
import socket

from openpilot.cereal import messaging


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--bind", default="0.0.0.0")
    parser.add_argument("--port", type=int, default=48151)
    args = parser.parse_args()

    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sock.bind((args.bind, args.port))

    pm = messaging.PubMaster(["customReservedRawData1"])
    print(f"[Joy Kakao Receiver] UDP {args.bind}:{args.port}")

    while True:
        data, addr = sock.recvfrom(65535)
        try:
            obj = json.loads(data.decode("utf-8"))
            if not isinstance(obj, dict):
                continue

            payload = json.dumps(obj, ensure_ascii=False, separators=(",", ":")).encode("utf-8")
            msg = messaging.new_message("customReservedRawData1", len(payload), valid=True)
            msg.customReservedRawData1 = payload
            pm.send("customReservedRawData1", msg)

            print(
                f"[RX {addr[0]}] active={obj.get('active')} "
                f"dir={obj.get('direction')} "
                f"next={obj.get('maneuver_distance_m')}"
            )
        except Exception as e:
            print(f"[DROP {addr[0]}] {e}")


if __name__ == "__main__":
    main()
