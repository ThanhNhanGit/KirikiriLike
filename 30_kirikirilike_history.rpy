# KirikiriLike — self-contained History (backlog) screen
#
# Overrides the stock `history` screen at init 999 (so it wins over the default
# definition, which is init 0). It is fully standalone: it does NOT route
# through `game_menu`, so it shows WITHOUT the left navigation menu / divider,
# and needs no extra art asset (a plain dark wash over the scene background).
#
# Wheel behaviour inside History:
#   * wheel-up  -> scrolls up into older messages (the vpgrid/viewport handles it)
#   * wheel-down -> scrolls toward newer messages, then closes at the bottom
#
# To DISABLE this override and restore the stock game-menu History, delete this
# single file.

init 999 python:

    def _kkl_hs(project_style, fallback_style):
        # Pick the project's stock style or the library's fallback style,
        # re-evaluated each render so kkl.history_use_project_styles is live.
        return project_style if kkl.history_use_project_styles else fallback_style


    class _KKLHistoryWheelDown(Action, DictEquality):
        """Scroll History down, returning to dialogue only at the bottom."""

        def __call__(self):
            scroll = Scroll("kkl_history_scroll", "vertical increase")

            if scroll.get_sensitive():
                return scroll()

            return Return()()


init 999 screen history():

    tag menu

    ## Avoid predicting this screen, as it can be very large.
    predict False

    ## Background: the scene image (no divider) plus a dark wash. Reproduces the
    ## stock game-menu darkening without the "gui/overlay/game_menu.png" divider.
    add gui.game_menu_background
    add Solid("#000000cc")

    ## Title.
    label _("History"):
        style _kkl_hs("game_menu_label", "kkl_history_title")

    ## Backlog list. The frame fills the screen (minus padding) so the
    ## vpgrid/viewport has bounded height to scroll within.
    frame:
        style _kkl_hs("game_menu_outer_frame", "kkl_history_outer")
        background None
        xfill True
        yfill True

        if gui.history_height:

            vpgrid:
                id "kkl_history_scroll"
                cols 1
                yinitial 1.0

                scrollbars "vertical"
                mousewheel True
                draggable True
                pagekeys True

                side_yfill True

                for h in _history_list:
                    window:
                        style _kkl_hs("history_window", "kkl_history_window")

                        has fixed:
                            yfit True

                        if h.who:
                            label h.who:
                                style _kkl_hs("history_name", "kkl_history_name")
                                substitute False
                                if "color" in h.who_args:
                                    text_color h.who_args["color"]

                        $ what = renpy.filter_text_tags(h.what, allow=gui.history_allow_tags)
                        text what:
                            style _kkl_hs("history_text", "kkl_history_text")
                            substitute False

                if not _history_list:
                    label _("The dialogue history is empty."):
                        style _kkl_hs("history_label", "kkl_history_label")

        else:

            viewport:
                id "kkl_history_scroll"
                scrollbars "vertical"
                mousewheel True
                draggable True
                pagekeys True

                side_yfill True

                vbox:
                    for h in _history_list:
                        window:
                            style _kkl_hs("history_window", "kkl_history_window")

                            has fixed:
                                yfit True

                            if h.who:
                                label h.who:
                                    style _kkl_hs("history_name", "kkl_history_name")
                                    substitute False
                                    if "color" in h.who_args:
                                        text_color h.who_args["color"]

                            $ what = renpy.filter_text_tags(h.what, allow=gui.history_allow_tags)
                            text what:
                                style _kkl_hs("history_text", "kkl_history_text")
                                substitute False

                    if not _history_list:
                        label _("The dialogue history is empty."):
                            style _kkl_hs("history_label", "kkl_history_label")

    ## Return to the game.
    textbutton _("Return"):
        style _kkl_hs("return_button", "kkl_history_return")
        action Return()

    ## Wheel-down scrolls toward newer entries while more content remains, then
    ## returns to the game on the next wheel-down at the bottom.
    if kkl.enable_wheelnav and kkl.history_closes_on_wheeldown:
        key kkl.wheel_down_key action _KKLHistoryWheelDown()


## ---------------------------------------------------------------------------
## Fallback styles, used only when kkl.history_use_project_styles == False
## (i.e. a project without the standard history_*/game_menu_* styles). They are
## based on Ren'Py's base gui styles so they work standalone.
## ---------------------------------------------------------------------------

style kkl_history_title is gui_label:
    xpos 50
    ysize 120
style kkl_history_title_text is gui_label_text:
    size gui.title_text_size
    color gui.accent_color
    yalign 0.5

style kkl_history_outer is empty:
    top_padding 120
    bottom_padding 30

style kkl_history_window is empty:
    xfill True
    ysize gui.history_height

style kkl_history_name is gui_label:
    xpos gui.history_name_xpos
    xanchor gui.history_name_xalign
    ypos gui.history_name_ypos
    xsize gui.history_name_width
style kkl_history_name_text is gui_label_text:
    min_width gui.history_name_width
    textalign gui.history_name_xalign

style kkl_history_text is gui_text:
    xpos gui.history_text_xpos
    ypos gui.history_text_ypos
    xanchor gui.history_text_xalign
    xsize gui.history_text_width
    min_width gui.history_text_width
    textalign gui.history_text_xalign

style kkl_history_label is gui_label:
    xfill True
style kkl_history_label_text is gui_label_text:
    xalign 0.5

style kkl_history_return is gui_button:
    xpos gui.navigation_xpos
    yalign 1.0
    yoffset -30
style kkl_history_return_text is gui_button_text
