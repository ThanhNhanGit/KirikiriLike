# KirikiriLike — configuration knobs
#
# This file only DECLARES the tunables (in the `kkl` namespace) with their
# library defaults. It applies a default to a knob ONLY if the consuming
# project has not already set it, so a project can pre-set any value in its own
# init (priority 0) and the library will respect it.
#
# HOW TO CONFIGURE (in your project, NOT here):
#
#     init python:
#         kkl.side_image_tag = "sylvie"     # enable the bottom-left avatar
#         kkl.enable_wheelnav = True        # wheel-up = History, wheel-down = advance
#
# IMPORTANT: set your knobs at the default init priority (0) or anything below
# 100. The library reads them at init 100+, so values set at 100+ are ignored.

# Create the namespace as early as possible so projects can write to it.
init -100 python:
    import types
    if not hasattr(store, "kkl"):
        store.kkl = types.SimpleNamespace()

# Apply library defaults just before the project's own init (priority 0) runs,
# but only where the project has not already provided a value.
init -1 python:

    def _kkl_default(name, value):
        if not hasattr(store.kkl, name):
            setattr(store.kkl, name, value)

    # --- Master switches -----------------------------------------------------
    # Wheel-up opens History, wheel-down advances dialogue (and closes History).
    _kkl_default("enable_wheelnav", True)
    # Let the library set config.side_image_tag from `side_image_tag` below.
    _kkl_default("enable_side_image", True)

    # --- Side image ----------------------------------------------------------
    # The image tag whose currently-shown sprite drives the bottom-left avatar.
    # Leave None to not touch config.side_image_tag. Requires that you also
    # define `image side <tag> <attrs> = "..."` images and give your Character
    # image_tag="<tag>". See README.md.
    _kkl_default("side_image_tag", None)

    # --- Wheel navigation ----------------------------------------------------
    _kkl_default("wheel_up_key", "mousedown_4")     # scroll up
    _kkl_default("wheel_down_key", "mousedown_5")   # scroll down

    # --- History (backlog) screen -------------------------------------------
    # When True, a wheel-down at the newest entry closes History (KiriKiri exit).
    _kkl_default("history_closes_on_wheeldown", True)
    # Reuse the project's stock history_*/game_menu_* styles (True) or the
    # library's own kkl_history_* fallback styles (False, for non-standard GUIs).
    _kkl_default("history_use_project_styles", True)

    # --- Rollback ------------------------------------------------------------
    # The library keeps rollback available by default (wheel-up is captured
    # before the rollback binding, so History opens without disabling rollback).
    # Set True to fully disable rollback, KiriKiri-style.
    _kkl_default("force_rollback_disabled", False)
