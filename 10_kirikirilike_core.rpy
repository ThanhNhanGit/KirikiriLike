# KirikiriLike — core wiring
#
# Reads the knobs (set by the project at init 0) and applies engine config.
# Runs at init 100 so any project-supplied values are already in place.

init 100 python:

    # Optional fixed-tag override. Normally this stays None, allowing Ren'Py's
    # built-in SideImage() to follow only the active Character(image=...).
    # A non-None value deliberately follows that shown sprite on every line,
    # including narration.
    if kkl.enable_side_image and kkl.side_image_tag is not None:
        config.side_image_tag = kkl.side_image_tag

    # Optional KiriKiri-style hard rollback disable (off by default).
    if kkl.force_rollback_disabled:
        config.rollback_enabled = False
