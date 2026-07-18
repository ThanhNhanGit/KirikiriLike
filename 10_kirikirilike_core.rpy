# KirikiriLike — core wiring
#
# Reads the knobs (set by the project at init 0) and applies engine config.
# Runs at init 100 so any project-supplied values are already in place.

init 100 python:

    # Bottom-left avatar: point config.side_image_tag at the chosen tag so the
    # built-in SideImage() in the default `say` screen resolves the currently
    # shown sprite live on every render. This works whether or not rollback is
    # enabled, and does nothing unless the matching `side <tag> <attrs>` images
    # exist and the Character has image_tag="<tag>".
    if kkl.enable_side_image and kkl.side_image_tag is not None:
        config.side_image_tag = kkl.side_image_tag

    # Optional KiriKiri-style hard rollback disable (off by default).
    if kkl.force_rollback_disabled:
        config.rollback_enabled = False
