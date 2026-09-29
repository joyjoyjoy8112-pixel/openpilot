from openpilot.system.ui.widgets.scroller import NavScroller
from openpilot.selfdrive.ui.mici.widgets.button import BigParamControl, GreyBigButton
from openpilot.system.ui.lib.multilang import tr
from openpilot.system.ui.lib.application import gui_app


class JoyLayoutMici(NavScroller):
  def __init__(self):
    super().__init__()

    joy_enabled = BigParamControl(
      tr("Joy enabled"),
      "JoyEnabled",
      description=tr("Master switch for Joy custom features.")
    )

    def debug_callback(state: bool):
      gui_app.set_show_fps(state)
      gui_app.set_show_touches(state)

    joy_debug = BigParamControl(
      tr("Joy debug overlay"),
      "ShowDebugInfo",
      toggle_callback=debug_callback,
      description=tr("Show FPS and touch positions for Joy development.")
    )

    self._scroller.add_widgets([
      GreyBigButton(tr("Joy"), tr("Version 0.1")),
      joy_enabled,
      joy_debug,
      GreyBigButton(tr("Joy custom settings"), tr("More features will be added here.")),
    ])
