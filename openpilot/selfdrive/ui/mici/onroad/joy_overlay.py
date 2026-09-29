import pyray as rl

from openpilot.selfdrive.ui.ui_state import ui_state, UIStatus
from openpilot.system.ui.lib.application import gui_app, FontWeight
from openpilot.system.ui.lib.multilang import tr
from openpilot.system.ui.lib.text_measure import measure_text_cached
from openpilot.system.ui.widgets import Widget


class JoyStatusBadge(Widget):
  def __init__(self):
    super().__init__()

    # First-run default: show the Joy status badge.
    # Only initialize when no user value has ever been saved.
    if ui_state.params.get("JoyStatusBadgeEnabled") is None:
      ui_state.params.put_bool("JoyStatusBadgeEnabled", True, block=True)

    self._font = gui_app.font(FontWeight.BOLD)

  def _render(self, rect: rl.Rectangle):
    if not ui_state.params.get_bool("JoyEnabled"):
      return
    if not ui_state.params.get_bool("JoyStatusBadgeEnabled"):
      return

    if ui_state.status == UIStatus.ENGAGED:
      text = "조이 작동"
      bg_color = rl.Color(0, 100, 45, 210)
    elif ui_state.status == UIStatus.OVERRIDE:
      text = "조이 개입"
      bg_color = rl.Color(140, 85, 0, 210)
    else:
      text = "조이 대기"
      bg_color = rl.Color(35, 35, 35, 190)

    font_size = 34
    text_size = measure_text_cached(self._font, text, font_size)

    padding_x = 18
    padding_y = 8
    width = text_size.x + padding_x * 2
    height = text_size.y + padding_y * 2

    if ui_state.params.get_bool("JoyStatusBadgeLeft"):
      x = rect.x + 18
    else:
      x = rect.x + rect.width - width - 18

    y = rect.y + 18

    badge_rect = rl.Rectangle(x, y, width, height)

    rl.draw_rectangle_rounded(
      badge_rect,
      0.35,
      8,
      bg_color,
    )

    rl.draw_rectangle_rounded_lines_ex(
      badge_rect,
      0.35,
      8,
      2,
      rl.Color(255, 255, 255, 190),
    )

    rl.draw_text_ex(
      self._font,
      text,
      rl.Vector2(x + padding_x, y + padding_y),
      font_size,
      0,
      rl.WHITE,
    )
