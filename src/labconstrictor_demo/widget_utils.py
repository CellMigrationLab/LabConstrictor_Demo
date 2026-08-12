"""
Composable ipywidgets helpers for notebook front-ends.
"""

from __future__ import annotations

from typing import Callable, Iterable, Literal

import ipywidgets as widgets
from IPython.display import display

UploadCallback = Callable[[tuple[dict, ...]], None]
Level = Literal["info", "success", "warning", "error"]


def create_image_uploader(
    *,
    description: str = "Pick an image",
    multiple: bool = False,
    tooltip: str | None = None,
) -> widgets.FileUpload:
    """
    Build a styled FileUpload widget restricted to images.
    """

    button_style = "primary" if not multiple else ""
    uploader = widgets.FileUpload(
        accept="image/*",
        multiple=multiple,
        description=description,
        style={"button_color": "#4d8bf5"},
        tooltip=tooltip,
        layout=widgets.Layout(width="auto"),
        button_style=button_style,
    )
    return uploader


def wire_upload_handler(uploader: widgets.FileUpload, handler: UploadCallback) -> None:
    """
    Attach a handler that fires whenever at least one file is uploaded.
    """

    def _wrapped(change):
        if change["name"] == "value" and change["new"]:
            handler(change["new"])

    uploader.observe(_wrapped, names="value")


def notify(message: str, level: Level = "info") -> widgets.HTML:
    """
    Render a lightweight status banner using HTML widget.
    """

    palette = {
        "info": "#005a9c",
        "success": "#237804",
        "warning": "#a15c00",
        "error": "#b03060",
    }
    bg_palette = {
        "info": "#e5f1fb",
        "success": "#edf7ed",
        "warning": "#fff8e1",
        "error": "#fde7ef",
    }
    fg = palette.get(level, palette["info"])
    bg = bg_palette.get(level, bg_palette["info"])
    html = widgets.HTML(
        value=(
            f"<div style='padding:8px 12px;border-radius:6px;"
            f"color:{fg};background:{bg};border:1px solid {fg}33;'>"
            f"{message}</div>"
        )
    )
    display(html)
    return html
