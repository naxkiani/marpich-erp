"""Physical vault location — current custody of a paper document."""
from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class PhysicalLocation:
    site_code: str
    room: str = ""
    cabinet: str = ""
    shelf: str = ""
    box: str = ""
    file_ref: str = ""

    def __post_init__(self) -> None:
        site = self.site_code.strip()
        if not site:
            raise ValueError("documents.errors.physical_site_required")
        if len(site) > 64:
            raise ValueError("documents.errors.physical_site_too_long")
        object.__setattr__(self, "site_code", site)
        object.__setattr__(self, "room", self.room.strip()[:64])
        object.__setattr__(self, "cabinet", self.cabinet.strip()[:64])
        object.__setattr__(self, "shelf", self.shelf.strip()[:64])
        object.__setattr__(self, "box", self.box.strip()[:64])
        object.__setattr__(self, "file_ref", self.file_ref.strip()[:128])

    def to_dict(self) -> dict:
        return {
            "site_code": self.site_code,
            "room": self.room,
            "cabinet": self.cabinet,
            "shelf": self.shelf,
            "box": self.box,
            "file_ref": self.file_ref,
        }

    @classmethod
    def from_dict(cls, data: dict | None) -> PhysicalLocation | None:
        if not data or not isinstance(data, dict):
            return None
        site = str(data.get("site_code") or "").strip()
        if not site:
            return None
        return cls(
            site_code=site,
            room=str(data.get("room") or ""),
            cabinet=str(data.get("cabinet") or ""),
            shelf=str(data.get("shelf") or ""),
            box=str(data.get("box") or ""),
            file_ref=str(data.get("file_ref") or ""),
        )
