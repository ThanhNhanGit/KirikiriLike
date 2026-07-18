# KirikiriLike — scroll-wheel navigation
#
# Repurposes the mouse wheel:
#   * wheel-up   -> open the History (backlog) screen
#   * wheel-down -> advance the current dialogue
#
# Wheel-up uses `key ... capture True` on an always-shown overlay screen, so it
# is consumed BEFORE the default rollback binding (config.underlay). This means
# History opens without removing mousedown_4 from config.keymap['rollback'] and
# without disabling rollback — keyboard/PageUp rollback keeps working.
#
# Wheel-down advances via the engine's built-in "dismiss" keysym (there is no
# stand-alone "advance" screen action), added to config.keymap['dismiss']. That
# only advances say/pause interactions and does not touch rollback.

screen kkl_wheelnav():
    zorder 90

    if kkl.enable_wheelnav:
        # Open the backlog, pre-empting the default rollback binding.
        key kkl.wheel_up_key action ShowMenu("history") capture True


init 150 python:
    if kkl.enable_wheelnav:
        # Show the wheel-up capture overlay during in-game interactions.
        if "kkl_wheelnav" not in config.overlay_screens:
            config.overlay_screens.append("kkl_wheelnav")

        # Wheel-down advances dialogue via the built-in dismiss behavior.
        if kkl.wheel_down_key not in config.keymap["dismiss"]:
            config.keymap["dismiss"].append(kkl.wheel_down_key)
