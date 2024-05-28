import argparse
import threading
import time
from dataclasses import dataclass

import dearpygui.dearpygui as dpg
import numpy as np
import PIL.Image as Image

IMG_HEIGHT = 512
IMG_WIDTH = 512
MENU_HEIGHT = 64
MENU_WIDTH = 512

VP_WIDTH = IMG_WIDTH
VP_HEIGHT = IMG_HEIGHT + MENU_HEIGHT

# GENERATE_BUTTON_WIDTH = 128
# PROGRESS_BAR_WIDTH = MENU_WIDTH - GENERATE_BUTTON_WIDTH - dpg.mvStyleVar_ItemSpacing


@dataclass
class State:
    prompt: str = ""
    running: bool = False


# This is just used to update the texture.
def update_image(sender):
    data = np.random.random((IMG_HEIGHT * IMG_WIDTH * 4)) # 4 since RGBA.
    # update the texture by setting a new value of the dynamic texture.
    # dynamic texture is in RGBA format.
    dpg.set_value("texture", data)


def generate_image_thread(sender):
    print("Generating image with prompt:", STATE.prompt)

    for i in range(100):
        time.sleep(0.01)
    update_image(sender)
    STATE.running = False

    # re-enable the generate button and revert its label.
    dpg.enable_item(sender)
    dpg.set_item_label(sender, "generate")

    print("Image generated.")


def prompt_update(sender, app_data):
    STATE.prompt = app_data


def generate(sender, app_data):
    if STATE.running:
        return
    else:
        # disable the generate button and change its label.
        dpg.disable_item(sender)
        dpg.set_item_label(sender, "generating...")
        # update state and start thread
        STATE.running = True
        thread = threading.Thread(
            target=generate_image_thread, args=(sender,), daemon=True
        )
        thread.start()


def create_app():
    with dpg.window(
        tag="app window",
        width=VP_WIDTH,
        height=VP_HEIGHT,
        no_move=True,
        no_resize=True,
        no_title_bar=True,
        pos=(0, 0),
    ):
        # Image window
        with dpg.child_window(tag="img", width=IMG_WIDTH, height=IMG_HEIGHT):
            # Create random texture as default.
            # It is dynamic so we can update it in the callback.
            with dpg.texture_registry(tag="texreg"):
                # add dynamic texture, this is in RGBA format.
                dpg.add_dynamic_texture(
                    width=IMG_HEIGHT,
                    height=IMG_WIDTH,
                    default_value=np.random.random((IMG_HEIGHT * IMG_WIDTH * 4)),
                    tag="texture",
                )
            # add image with the dynamic texture.
            dpg.add_image(
                texture_tag="texture", height=IMG_HEIGHT, width=IMG_WIDTH, tag="image"
            )

        # Menu window
        with dpg.child_window(tag="menu", width=MENU_WIDTH, height=MENU_HEIGHT):
            dpg.add_input_text(
                hint="Prompt",
                width=-1,
                height=16,
                callback=prompt_update,
            )
            with dpg.group(horizontal=True):
                #     progress_bar = dpg.add_progress_bar(
                #         default_value=0, overlay="0%", height=32, width=PROGRESS_BAR_WIDTH
                #     )
                dpg.add_button(
                    label="generate",
                    callback=generate,
                    height=32,
                    width=-1,
                )

        # Theme stuff
        with dpg.theme() as global_theme:
            with dpg.theme_component(dpg.mvAll):
                dpg.add_theme_style(
                    dpg.mvStyleVar_WindowPadding, 0, category=dpg.mvThemeCat_Core
                )
        dpg.bind_theme(global_theme)


def main(args):
    # must create a context.
    dpg.create_context()

    # create global state.
    global STATE
    STATE = State()
    STATE.running = False

    # set global font scale.
    dpg.set_global_font_scale(1.25)

    # show item registry if needed.
    if args.item_registry:
        dpg.show_item_registry()
    if args.style_editor:
        dpg.show_style_editor()
    if args.debug:
        dpg.show_debug()

    # we may need to resize the viewport when using any of the above.
    resizeable = args.resizable or args.style_editor or args.item_registry or args.debug

    # Create app
    create_app()

    # must create and show viewport.
    dpg.create_viewport(
        title="Image Generator",
        width=VP_WIDTH + 8,
        # max_width=VP_WIDTH + 1,
        height=VP_HEIGHT + 8,
        # max_height=VP_HEIGHT + 1,
        resizable=resizeable,
    )
    dpg.show_viewport()
    dpg.set_primary_window("app window", True)

    # must setup and start dpg
    dpg.setup_dearpygui()
    dpg.start_dearpygui()

    # must destroy the context.
    dpg.destroy_context()


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("--debug", action="store_true", default=False)
    parser.add_argument("--item-registry", action="store_true", default=False)
    parser.add_argument("--style-editor", action="store_true", default=False)
    parser.add_argument("--resizable", action="store_true", default=False)
    return parser.parse_args()


if __name__ == "__main__":
    args = parse_args()
    main(args)
