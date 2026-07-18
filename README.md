# KirikiriLike

A drop-in Ren'Py 8.x library that gives your game a **KiriKiri / KAG-style** feel:

1. **Bottom-left character avatar** (side image) during dialogue, following the shown sprite.
2. **Scroll-wheel navigation** — wheel **up** opens the message History/backlog, wheel **down** advances dialogue.
3. **History shown without the left navigation menu** (a clean backlog, no divider).
4. **Wheel-down inside History closes it** and returns to the game (KiriKiri backlog exit).

## Install

Copy the whole `KirikiriLike/` folder into your project's `game/` directory. That's it — the
behaviours turn on with sensible defaults. Ren'Py auto-loads every `.rpy` under `game/`.

## Configure

Set knobs in **your own** project file, at the default init priority (0). Do **not** edit the
library files. Example (`game/kkl_settings.rpy`):

```renpy
init python:
    kkl.side_image_tag = "sylvie"     # enable the bottom-left avatar (see below)
    kkl.enable_wheelnav = True        # wheel-up = History, wheel-down = advance
```

> ⚠️ Set knobs at init priority **below 100** (the default `init` = 0 is fine). The library reads
> them at init 100+, so anything set at 100+ is ignored.

### Knobs (namespace `kkl`)

| Knob | Default | Effect |
|---|---|---|
| `kkl.enable_wheelnav` | `True` | Wheel-up → History, wheel-down → advance / close History. |
| `kkl.enable_side_image` | `True` | Let the lib set `config.side_image_tag`. |
| `kkl.side_image_tag` | `None` | Tag that drives the avatar. `None` = don't touch `config.side_image_tag`. |
| `kkl.wheel_up_key` | `"mousedown_4"` | Key that opens History. |
| `kkl.wheel_down_key` | `"mousedown_5"` | Key that advances / closes History. |
| `kkl.history_closes_on_wheeldown` | `True` | Wheel-down inside History returns to the game. |
| `kkl.history_use_project_styles` | `True` | Reuse your `history_*`/`game_menu_*` styles vs. the lib's `kkl_history_*` fallbacks. |
| `kkl.force_rollback_disabled` | `False` | If `True`, fully disable rollback (KiriKiri-style). Off by default so keyboard/PageUp rollback still works. |

## Enabling the bottom-left avatar (side image)

The avatar rides on Ren'Py's built-in `SideImage()` (already in the default `say` screen), so the
library only points `config.side_image_tag` at your character. You must provide, in your project:

1. A Character with an `image_tag`:
   ```renpy
   define s = Character("Sylvie", image_tag="sylvie")
   ```
2. `side <tag> <attrs>` images matching your sprites' attributes. Defining them explicitly is
   recommended (survives even with the image-folder scan disabled):
   ```renpy
   image side sylvie green normal = "images/side/side sylvie green normal.png"
   image side sylvie green smile  = "images/side/side sylvie green smile.png"
   # ...one per (color, expression) combination you use
   ```
3. Set the knob: `kkl.side_image_tag = "sylvie"`.

The avatar then appears whenever `sylvie ...` is shown and updates live as attributes change.

> The library cannot ship your art. If no matching `side ...` image exists, no avatar appears
> (this fails silently). The stock avatar sits flush bottom-left; to nudge it, edit your own `say`
> screen's `add SideImage()` line, e.g. `add SideImage() xalign 0.0 xoffset 20 yalign 1.0 yoffset -20`.

## Notes & caveats

- **History override:** `30_kirikirilike_history.rpy` replaces the stock `history` screen (at init 999).
  To disable it and restore the game-menu History, **delete that one file**.
- **Wheel nav in menus:** the wheel bindings live on an overlay screen (`kkl_wheelnav`), which Ren'Py
  suppresses inside menus. That's why the "wheel-down closes History" binding lives inside the History
  screen itself.
- **Rollback:** by default the lib captures wheel-up before the rollback binding, so History opens
  without disabling rollback — keyboard/PageUp rollback keeps working. Set `kkl.force_rollback_disabled`
  to go full KiriKiri.
- **Styles:** with `history_use_project_styles = True` (default) the History reuses your standard
  `history_*`/`game_menu_*` styles. Set it `False` for a non-standard GUI to use the bundled
  `kkl_history_*` fallbacks.

## Files

| File | Init | Purpose |
|---|---|---|
| `00_kirikirilike_config.rpy` | -100 / -1 | Declares the `kkl` knobs and defaults. |
| `10_kirikirilike_core.rpy` | 100 | Wires `config.side_image_tag` and optional rollback disable. |
| `20_kirikirilike_wheelnav.rpy` | 150 | The `kkl_wheelnav` overlay (captured wheel bindings). |
| `30_kirikirilike_history.rpy` | 999 | Self-contained nav-less History screen. |
