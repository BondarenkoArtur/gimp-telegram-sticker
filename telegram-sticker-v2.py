#!/usr/bin/env python
"""Telegram Sticker v2

@link      https://github.com/BondarenkoArtur/gimp-telegram-sticker
"""

from __future__ import division

from gimpfu import *

FULL_OPACITY = 100

REGULAR_LAYER = 28

STICKER_SIZE = 512


def python_telegram_sticker(image, drawable,
                            sticker_outline,
                            sticker_feather,
                            sticker_color,
                            shadow_offset_x, shadow_offset_y,
                            shadow_blur_radius,
                            shadow_color,
                            shadow_opacity,
                            merge_before_process,
                            auto_crop_image,
                            merge_in_end):
    image.undo_group_start()

    pdb.gimp_progress_init("Creating sticker...", None)

    pdb.gimp_progress_set_text("Removing previous selections")
    pdb.gimp_selection_none(image)

    if merge_before_process:
        pdb.gimp_progress_set_text("Merging layers")
        image_layer = pdb.gimp_image_merge_visible_layers(image, 0)
    else:
        image_layer = pdb.gimp_image_get_active_layer(image)

    if auto_crop_image:
        pdb.gimp_progress_set_text("Cropping and resizing")
        pdb.plug_in_autocrop(image, image_layer)
        additional_size_outline = sticker_outline * 2 + sticker_feather
        additional_size_full_x = additional_size_outline + \
                                 abs(shadow_offset_x) + \
                                 shadow_blur_radius
        additional_size_full_y = additional_size_outline + \
                                 abs(shadow_offset_y) + \
                                 shadow_blur_radius
        if shadow_offset_x < 0:
            additional_offset_x = additional_size_outline + \
                                  abs(shadow_offset_x)
        else:
            additional_offset_x = additional_size_outline

        if shadow_offset_y < 0:
            additional_offset_y = additional_size_outline + \
                                  abs(shadow_offset_y)
        else:
            additional_offset_y = additional_size_outline

        if image_layer.width < STICKER_SIZE \
                and image_layer.height < STICKER_SIZE:
            pdb.gimp_layer_resize(image_layer, STICKER_SIZE,
                                  image_layer.height + additional_size_full_y,
                                  (STICKER_SIZE - image_layer.width) / 2,
                                  additional_offset_y)
            pdb.gimp_image_resize_to_layers(image)
        else:
            size_x = STICKER_SIZE - additional_size_full_x
            size_y = STICKER_SIZE - additional_size_full_y
            width = (image_layer.width + additional_size_full_x) / size_x
            height = (image_layer.height + additional_size_full_y) / size_y

            if width > height:
                new_width = STICKER_SIZE - additional_size_full_x
                new_height = int(image_layer.height /
                                 (image_layer.width / float(new_width)))
            else:
                new_height = STICKER_SIZE - additional_size_full_y
                new_width = int(image_layer.width /
                                (image_layer.height / float(new_height)))

            pdb.gimp_image_scale(image, new_width, new_height)
            pdb.gimp_image_resize(image, new_width + additional_size_full_x,
                                  new_height + additional_size_full_y,
                                  additional_offset_x, additional_offset_y)
            pdb.gimp_layer_resize_to_image_size(image_layer)

    pdb.gimp_progress_set_text("Creating white outline")
    pdb.gimp_image_select_item(image, 0, image_layer)
    pdb.gimp_selection_sharpen(image)
    pdb.gimp_selection_grow(image, sticker_outline)
    pdb.gimp_selection_feather(image, sticker_feather)
    sticker_layer = pdb.gimp_layer_new(image, image_layer.width,
                                       image_layer.height, 1,
                                       "Sticker Background",
                                       FULL_OPACITY, REGULAR_LAYER)
    image.add_layer(sticker_layer, 1)
    pdb.gimp_context_set_background(sticker_color)

    pdb.gimp_edit_bucket_fill_full(sticker_layer, 1,
                                   REGULAR_LAYER, FULL_OPACITY,
                                   0, False, False, 0, 0, 0)

    pdb.gimp_progress_set_text("Creating drop shadow")
    pdb.script_fu_drop_shadow(image, sticker_layer,
                              shadow_offset_x, shadow_offset_y,
                              shadow_blur_radius, shadow_color,
                              shadow_opacity, 0)

    pdb.gimp_image_raise_item_to_top(image, sticker_layer)
    pdb.gimp_image_raise_item_to_top(image, image_layer)

    if merge_in_end:
        pdb.gimp_progress_set_text("Merging layers")
        pdb.gimp_image_merge_visible_layers(image, 0)

    pdb.gimp_progress_set_text("Finishing")
    pdb.gimp_selection_none(image)
    pdb.gimp_progress_end()

    image.undo_group_end()


register(
    "python_fu_telegram_sticker_v2",
    "Makes a telegram sticker out of the current image",
    "Makes a telegram sticker out of the current image",
    "uaBArt",
    "uaBArt",
    "2019",
    "<Image>/Filters/Custom/Telegram Sticker v2...",
    "RGB*",
    [
        (PF_SLIDER, "sticker_outline", "_Sticker outline", 5, (0, 50, 1)),
        (PF_SLIDER, "sticker_feather", "Sticker _feather", 2, (0, 10, 1)),
        (PF_COLOR, "sticker_color", "Sticker co_lor", (255, 255, 255)),
        (PF_SLIDER, "shadow_offset_x", "Shadow offset _X", 5, (-50, 50, 1)),
        (PF_SLIDER, "shadow_offset_y", "Shadow offset _Y", 5, (-50, 50, 1)),
        (PF_SLIDER, "shadow_blur_radius",
         "Shadow blur _radius", 10, (0, 50, 1)),
        (PF_COLOR, "shadow_color", "Sha_dow color", (0, 0, 0)),
        (PF_SLIDER, "shadow_opacity", "Shadow o_pacity", 25, (0, 100, 1)),
        (PF_BOOL, "merge_before_process",
         "Merge all layers _before doing everything", True),
        (PF_BOOL, "auto_crop_image", "Crop _Image", True),
        (PF_BOOL, "merge_in_end", "Merge in the _end", True),
    ],
    [],
    python_telegram_sticker)

main()
