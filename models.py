"""
Data models for Shift Reminder countdown system
"""
from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional
import uuid


@dataclass
class Countdown:
    """Represents a countdown timer"""
    name: str
    type: str  # "TO" or "FROM"
    enabled: bool = True
    show: bool = True
    color: str = "#00ffff"
    alert_enabled: bool = False
    alert_minutes: int = 60
    alert_mode: str = "pulse"
    alert_color: str = "#ff0000"
    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    start_datetime: Optional[str] = None  # For FROM type
    end_datetime: Optional[str] = None  # For TO type
    
    def to_dict(self):
        """Convert to dictionary for JSON serialization"""
        return {
            "id": self.id,
            "name": self.name,
            "type": self.type,
            "start_datetime": self.start_datetime,
            "end_datetime": self.end_datetime,
            "enabled": self.enabled,
            "show": self.show,
            "color": self.color,
            "alert_enabled": self.alert_enabled,
            "alert_minutes": self.alert_minutes,
            "alert_mode": self.alert_mode,
            "alert_color": self.alert_color
        }
    
    @classmethod
    def from_dict(cls, data):
        """Create Countdown from dictionary"""
        return cls(
            id=data.get("id", str(uuid.uuid4())),
            name=data["name"],
            type=data["type"],
            start_datetime=data.get("start_datetime"),
            end_datetime=data.get("end_datetime"),
            enabled=data.get("enabled", True),
            show=data.get("show", True),
            color=data.get("color", "#00ffff"),
            alert_enabled=data.get("alert_enabled", False),
            alert_minutes=data.get("alert_minutes", 60),
            alert_mode=data.get("alert_mode", "pulse"),
            alert_color=data.get("alert_color", "#ff0000")
        )


@dataclass
class HistoryEntry:
    """Represents a completed countdown in history"""
    name: str
    type: str  # "TO" or "FROM"
    started_at: str
    ended_at: str
    duration_seconds: int
    notes: str = ""
    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    
    def to_dict(self):
        """Convert to dictionary for JSON serialization"""
        return {
            "id": self.id,
            "name": self.name,
            "type": self.type,
            "started_at": self.started_at,
            "ended_at": self.ended_at,
            "duration_seconds": self.duration_seconds,
            "notes": self.notes
        }
    
    @classmethod
    def from_dict(cls, data):
        """Create HistoryEntry from dictionary"""
        return cls(
            id=data.get("id", str(uuid.uuid4())),
            name=data["name"],
            type=data["type"],
            started_at=data["started_at"],
            ended_at=data["ended_at"],
            duration_seconds=data["duration_seconds"],
            notes=data.get("notes", "")
        )
