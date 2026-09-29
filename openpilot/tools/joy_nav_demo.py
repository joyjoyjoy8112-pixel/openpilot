#!/usr/bin/env python3
import json
import time

from openpilot.cereal import messaging


def main():
  pm = messaging.PubMaster(["customReservedRawData1"])

  directions = ["right", "straight", "left", "slight_right"]

  start = time.monotonic()

  while True:
    elapsed = time.monotonic() - start
    stage = int(elapsed // 10) % len(directions)
    phase = elapsed % 10

    maneuver_distance = max(30.0, 500.0 - phase * 45.0)
    remaining_distance = max(1000.0, 12400.0 - elapsed * 12.0)
    remaining_time = max(60.0, 1080.0 - elapsed)

    payload = {
      "active": True,
      "direction": directions[stage],
      "maneuver_distance_m": maneuver_distance,
      "distance_remaining_m": remaining_distance,
      "time_remaining_s": remaining_time,
      "speed_limit_mps": 60.0 / 3.6,
    }

    raw = json.dumps(payload).encode("utf-8")

    msg = messaging.new_message(
      "customReservedRawData1",
      len(raw),
      valid=True,
    )
    msg.customReservedRawData1 = raw

    pm.send("customReservedRawData1", msg)
    time.sleep(0.5)


if __name__ == "__main__":
  main()
