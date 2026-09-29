from openpilot.system.ui.widgets.scroller import NavScroller
from openpilot.selfdrive.ui.mici.widgets.button import BigParamControl, GreyBigButton
from openpilot.system.ui.lib.multilang import tr


class JoyLayoutMici(NavScroller):
  def __init__(self):
    super().__init__()

    joy_enabled = BigParamControl(
      tr("Joy enabled"),
      "JoyEnabled",
      description=tr("Master switch for Joy custom features.")
    )

    self._scroller.add_widgets([
      GreyBigButton(tr("Joy"), tr("Version 0.1")),
      joy_enabled,
      GreyBigButton(tr("Joy custom settings"), tr("More features will be added here.")),
    ])
