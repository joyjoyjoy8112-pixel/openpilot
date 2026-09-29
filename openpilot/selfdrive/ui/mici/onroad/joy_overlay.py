import pyray as rl

from openpilot.selfdrive.ui.ui_state import ui_state
from openpilot.system.ui.lib.application import gui_app, FontWeight
from openpilot.system.ui.lib.multilang import tr
from openpilot.system.ui.lib.text_measure import measure_text_cached
from openpilot.system.ui.widgets import Widget


class JoyStatusBadge(Widget):
  def __init__(self):
    super().__init__()
    self._font = gui_app.font(FontWeight.BOLD)

  def _render(self, rect: rl.Rectangle):
    if not ui_state.params.get_bool("JoyEnabled"):
      return

    text = tr("Joy")
    font_size = 34
    text_size = measure_text_cached(self._font, text, font_size)

    padding_x = 18
    padding_y = 8
    width = text_size.x + padding_x * 2
    height = text_size.y + padding_y * 2

    x = rect.x + rect.width - width - 18
    y = rect.y + 18

    badge_rect = rl.Rectangle(x, y, width, height)

    rl.draw_rectangle_rounded(
      badge_rect,
      0.35,
      8,
      rl.Color(0, 0, 0, 180),
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
