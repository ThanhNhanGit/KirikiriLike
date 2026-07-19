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
#         kkl.enable_wheelnav = True        # wheel-up = History, wheel-down = advance
#         # Leave side_image_tag as None for speaker-aware avatars.
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
    # Allow the optional fixed-tag override described below.
    _kkl_default("enable_side_image", True)
    # Apply the bundled translucent-gradient textbox and Nunito styles.
    # Opt-in so installing/upgrading KirikiriLike never replaces a project's
    # existing dialogue presentation unexpectedly.
    _kkl_default("enable_textbox_template", False)

    # --- Side image ----------------------------------------------------------
    # Leave this None for normal speaker-aware behavior. Ren'Py then uses the
    # active Character's image property, and narration has no avatar. Setting a tag
    # here intentionally pins the avatar to that shown sprite across all lines,
    # including narration and dialogue spoken by other characters.
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

    # --- Textbox template ----------------------------------------------------
    # These affect the stock say-screen styles only when
    # enable_textbox_template is True. Projects can replace any individual
    # value while keeping the rest of the template.
    _kkl_default(
        "textbox_background",
        "KirikiriLike/gui/textbox_glass_gradient.svg",
    )
    _kkl_default("textbox_feather_edges", True)
    _kkl_default(
        "textbox_horizontal_edge_mask",
        "KirikiriLike/gui/textbox_edge_horizontal.svg",
    )
    _kkl_default(
        "textbox_vertical_edge_mask",
        "KirikiriLike/gui/textbox_edge_vertical.svg",
    )
    _kkl_default("textbox_background_opacity", 1.0)
    _kkl_default("textbox_fallback_background_color", "#010204c7")
    _kkl_default("textbox_on_small", True)
    _kkl_default(
        "textbox_font",
        "KirikiriLike/fonts/Nunito-Regular.ttf",
    )
    _kkl_default(
        "textbox_name_font",
        "KirikiriLike/fonts/Nunito-SemiBold.ttf",
    )
    _kkl_default("textbox_fallback_font", "DejaVuSans.ttf")
    _kkl_default("textbox_text_color", "#f7f9fc")
    _kkl_default("textbox_name_color", "#ffffff")
    # Ren'Py outline tuples are (thickness, color, x offset, y offset).
    # Size 0 makes the first layer a glyph shadow instead of an expanded
    # outline. Its one-pixel downward offset and 20% opacity keep it subtle;
    # the centered one-pixel layer supplies the actual readability edge.
    _kkl_default(
        "textbox_text_outlines",
        [(0, "#00000033", 0, 1), (1, "#000000c0", 0, 0)],
    )
    _kkl_default(
        "textbox_name_outlines",
        [(0, "#00000033", 0, 1), (1, "#000000cc", 0, 0)],
    )
    # None removes the separate name plaque for a cleaner glass-panel look.
    # Set a displayable or image path to retain a custom namebox background.
    _kkl_default("textbox_namebox_background", None)

    # --- Rollback ------------------------------------------------------------
    # The library keeps rollback available by default (wheel-up is captured
    # before the rollback binding, so History opens without disabling rollback).
    # Set True to fully disable rollback, KiriKiri-style.
    _kkl_default("force_rollback_disabled", False)
