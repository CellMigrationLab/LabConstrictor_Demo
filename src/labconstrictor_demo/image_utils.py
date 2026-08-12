"""
Helpers for reading, validating, and summarizing image data.
"""

from __future__ import annotations

from dataclasses import dataclass
from io import BytesIO
from pathlib import Path
from typing import Iterable, List, Mapping, Sequence

from PIL import Image


class ImageReadError(RuntimeError):
    """Raised when an uploaded file cannot be converted to an image."""


@dataclass(slots=True)
class ImageInfo:
    """Container for a Pillow image plus lightweight metadata."""

    name: str
    image: Image.Image
    content_type: str | None = None

    @property
    def size(self) -> tuple[int, int]:
        return self.image.size

    @property
    def width(self) -> int:
        return self.image.size[0]

    @property
    def height(self) -> int:
        return self.image.size[1]

    @property
    def mode(self) -> str:
        return self.image.mode

    @property
    def format(self) -> str | None:
        return self.image.format


def _bytes_to_image(data: bytes, *, name: str, content_type: str | None = None) -> ImageInfo:
    try:
        img = Image.open(BytesIO(data))
        img.load()
    except Exception as exc:  # pragma: no cover - Pillow error text varies
        raise ImageReadError(f"Could not open {name!r} as an image") from exc
    return ImageInfo(name=name, image=img, content_type=content_type)


def load_image(path: str | Path) -> ImageInfo:
    """
    Load an image from disk into an ImageInfo structure.
    """

    file_path = Path(path).expanduser().resolve()
    data = file_path.read_bytes()
    return _bytes_to_image(data, name=file_path.name)


def _iter_upload_entries(
    upload_value: Sequence[Mapping[str, object]] | Mapping[str, object]
) -> Iterable[Mapping[str, object]]:
    if isinstance(upload_value, Mapping):
        if "content" in upload_value or "metadata" in upload_value:
            return [upload_value]
        values = upload_value.values()
        if values and isinstance(next(iter(values)), Mapping):
            return values  # type: ignore[return-value]
    return upload_value  # type: ignore[return-value]


def read_image_from_upload(
    upload_value: Sequence[Mapping[str, object]] | Mapping[str, object] | None,
    *,
    multiple: bool = False,
) -> ImageInfo | List[ImageInfo]:
    """
    Convert the value emitted by ipywidgets.FileUpload into ImageInfo objects.
    """

    if not upload_value:
        raise ValueError("No upload value was provided.")

    entries = []
    for entry in _iter_upload_entries(upload_value):
        content = entry.get("content")
        if content is None:
            raise ImageReadError("Upload payload is missing the raw bytes under 'content'.")
        metadata = entry.get("metadata")
        if isinstance(metadata, Mapping):
            name = str(metadata.get("name") or "uploaded-image")
            content_type = metadata.get("type")
        else:
            name = str(entry.get("name") or "uploaded-image")
            content_type = entry.get("type") if isinstance(entry.get("type"), str) else None
        info = _bytes_to_image(content, name=name, content_type=content_type)  # type: ignore[arg-type]
        entries.append(info)

    if not entries:
        raise ValueError("Upload collection did not contain any files.")

    if multiple:
        return entries

    if len(entries) > 1:
        raise ValueError("Multiple files uploaded but multiple=False.")

    return entries[0]
