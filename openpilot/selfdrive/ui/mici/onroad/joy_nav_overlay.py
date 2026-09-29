import json
import time

import pyray as rl

from openpilot.common.constants import CV
from openpilot.selfdrive.ui.ui_state import ui_state, UIStatus
from openpilot.system.ui.lib.application import gui_app, FontWeight
from openpilot.system.ui.lib.multilang import tr
from openpilot.system.ui.widgets import Widget


class JoyNavPanel(Widget):
  DATA_TIMEOUT = 3.0

  def __init__(self):
    super().__init__()
    self._font_bold = gui_app.font(FontWeight.BOLD)
    self._font_medium = gui_app.font(FontWeight.MEDIUM)
    self._data = {}

  @staticmethod
  def _format_distance(distance_m):
    try:
      distance_m = float(distance_m)
    except (TypeError, ValueError):
      return "--"

    if distance_m < 0:
      return "--"
    if distance_m < 1000:
      return f"{round(distance_m):.0f} m"
    return f"{distance_m / 1000.0:.1f} km"

  @staticmethod
  def _format_time(seconds):
    try:
      seconds = float(seconds)
    except (TypeError, ValueError):
      return "--"

    if seconds < 0:
      return "--"

    minutes = max(1, round(seconds / 60.0))
    if minutes < 60:
      return f"{minutes} min"

    hours = minutes // 60
    mins = minutes % 60
    return f"{hours} h {mins} min"

  def _update_nav_data(self):
    sm = ui_state.sm

    if sm.updated["customReservedRawData1"]:
      try:
        raw = bytes(sm["customReservedRawData1"])
        if raw:
          data = json.loads(raw.decode("utf-8"))
          if isinstance(data, dict):
            self._data = data
      except (ValueError, UnicodeDecodeError, TypeError):
        self._data = {}

  def _draw_arrow(self, x, y, direction):
    white = rl.Color(255, 255, 255, 240)
    cx = x + 28
    top = y + 4
    mid = y + 28
    bottom = y + 58

    rl.draw_line_ex(
      rl.Vector2(cx, bottom),
      rl.Vector2(cx, mid),
      6,
      white,
    )

    if direction in ("left", "slight_left"):
      rl.draw_line_ex(
        rl.Vector2(cx, mid),
        rl.Vector2(cx - 22, mid),
        6,
        white,
      )
      rl.draw_triangle(
        rl.Vector2(cx - 32, mid),
        rl.Vector2(cx - 17, mid - 10),
        rl.Vector2(cx - 17, mid + 10),
        white,
      )

    elif direction in ("right", "slight_right"):
      rl.draw_line_ex(
        rl.Vector2(cx, mid),
        rl.Vector2(cx + 22, mid),
        6,
        white,
      )
      rl.draw_triangle(
        rl.Vector2(cx + 32, mid),
        rl.Vector2(cx + 17, mid + 10),
        rl.Vector2(cx + 17, mid - 10),
        white,
      )

    else:
      rl.draw_line_ex(
        rl.Vector2(cx, mid),
        rl.Vector2(cx, top + 10),
        6,
        white,
      )
      rl.draw_triangle(
        rl.Vector2(cx, top),
        rl.Vector2(cx - 10, top + 15),
        rl.Vector2(cx + 10, top + 15),
        white,
      )

  def _render(self, rect: rl.Rectangle):
    if not ui_state.params.get_bool("JoyEnabled"):
      return

    if not ui_state.params.get_bool("JoyNavEnabled"):
      return

    self._update_nav_data()

    sm = ui_state.sm
    if not sm.seen["customReservedRawData1"]:
      return

    if time.monotonic() - sm.recv_time["customReservedRawData1"] > self.DATA_TIMEOUT:
      return

    if not self._data.get("active", False):
      return

    direction = str(self._data.get("direction", "straight"))
    maneuver_distance = self._format_distance(
      self._data.get("maneuver_distance_m", -1)
    )
    remaining_distance = self._format_distance(
      self._data.get("distance_remaining_m", -1)
    )
    remaining_time = self._format_time(
      self._data.get("time_remaining_s", -1)
    )

    try:
      speed_limit_mps = float(self._data.get("speed_limit_mps", 0))
    except (TypeError, ValueError):
      speed_limit_mps = 0

    if speed_limit_mps > 0:
      conversion = CV.MS_TO_KPH if ui_state.is_metric else CV.MS_TO_MPH
      speed_limit = str(round(speed_limit_mps * conversion))
    else:
      speed_limit = "--"

    unit = tr("km/h") if ui_state.is_metric else tr("mph")

    width = 350
    height = 150

    if ui_state.params.get_bool("JoyStatusBadgeLeft"):
      x = rect.x + 18
    else:
      x = rect.x + rect.width - width - 18

    y_offset = 88 if ui_state.params.get_bool("JoyStatusBadgeEnabled") else 18
    y = rect.y + y_offset

    panel = rl.Rectangle(x, y, width, height)

    rl.draw_rectangle_rounded(
      panel,
      0.12,
      8,
      rl.Color(15, 15, 15, 220),
    )

    rl.draw_rectangle_rounded_lines_ex(
      panel,
      0.12,
      8,
      2,
      rl.Color(255, 255, 255, 130),
    )

    if ui_state.status == UIStatus.ENGAGED:
      nav_title = "조이 작동  안내"
    elif ui_state.status == UIStatus.OVERRIDE:
      nav_title = "조이 개입  안내"
    else:
      nav_title = "조이 대기  안내"

    rl.draw_text_ex(
      self._font_bold,
      nav_title,
      rl.Vector2(x + 18, y + 8),
      26,
      0,
      rl.WHITE,
    )

    self._draw_arrow(x + 18, y + 35, direction)

    rl.draw_text_ex(
      self._font_bold,
      f'{tr("Joy nav next")} {maneuver_distance}',
      rl.Vector2(x + 90, y + 42),
      28,
      0,
      rl.WHITE,
    )

    rl.draw_text_ex(
      self._font_medium,
      f'{tr("Joy nav limit")} {speed_limit} {unit}',
      rl.Vector2(x + 90, y + 78),
      24,
      0,
      rl.Color(255, 255, 255, 225),
    )

    rl.draw_text_ex(
      self._font_medium,
      remaining_distance,
      rl.Vector2(x + 18, y + 112),
      23,
      0,
      rl.Color(255, 255, 255, 225),
    )

    rl.draw_text_ex(
      self._font_medium,
      remaining_time,
      rl.Vector2(x + 205, y + 112),
      23,
      0,
      rl.Color(255, 255, 255, 225),
    )
