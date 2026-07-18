# KirikiriLike - optional translucent-gradient textbox template
#
# This changes the standard window/namebox/say styles used by Ren'Py's stock
# say screen. It deliberately does not replace screen say, so SideImage(),
# custom quick menus, and normal dialogue behavior remain owned by the project.

init 105 python:

    def _kkl_textbox_template_active():
        return (
            kkl.enable_textbox_template
            and (kkl.textbox_on_small or not renpy.variant("small"))
        )

    def _kkl_textbox_resolve_font(value):
        # FontGroup and other font objects are already valid style values.
        if not isinstance(value, str):
            return value

        if renpy.loadable(value):
            return value

        return kkl.textbox_fallback_font

    def _kkl_textbox_window_properties():
        if not _kkl_textbox_template_active():
            return {}

        source = kkl.textbox_background

        if isinstance(source, str) and not renpy.loadable(source):
            background = Solid(kkl.textbox_fallback_background_color)
        else:
            background = Frame(source, 0, 0, tile=False)

        if kkl.textbox_feather_edges:
            masks = (
                kkl.textbox_horizontal_edge_mask,
                kkl.textbox_vertical_edge_mask,
            )

            for mask_source in masks:
                if isinstance(mask_source, str) and not renpy.loadable(mask_source):
                    continue

                background = AlphaMask(
                    background,
                    Frame(mask_source, 0, 0, tile=False),
                )

        if kkl.textbox_background_opacity != 1.0:
            background = Transform(
                background,
                alpha=kkl.textbox_background_opacity,
            )

        return {"background": background}

    def _kkl_textbox_namebox_properties():
        if not _kkl_textbox_template_active():
            return {}

        return {"background": kkl.textbox_namebox_background}

    def _kkl_textbox_dialogue_properties():
        if not _kkl_textbox_template_active():
            return {}

        return {
            "font": _kkl_textbox_resolve_font(kkl.textbox_font),
            "color": kkl.textbox_text_color,
            "outlines": kkl.textbox_text_outlines,
        }

    def _kkl_textbox_name_properties():
        if not _kkl_textbox_template_active():
            return {}

        return {
            "font": _kkl_textbox_resolve_font(kkl.textbox_name_font),
            "color": kkl.textbox_name_color,
            "outlines": kkl.textbox_name_outlines,
        }


# Style statements are used instead of one-shot mutation so Ren'Py reapplies
# the template after gui.rebuild(), including language changes.
init 110:

    style window:
        properties _kkl_textbox_window_properties()

    style namebox:
        properties _kkl_textbox_namebox_properties()

    style say_dialogue:
        properties _kkl_textbox_dialogue_properties()

    style say_thought:
        properties _kkl_textbox_dialogue_properties()

    style say_label:
        properties _kkl_textbox_name_properties()
