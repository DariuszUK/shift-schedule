"""
Storage module for managing countdown data in JSON format
"""
import json
import os
from typing import List, Optional
from models import Countdown, HistoryEntry


class CountdownStorage:
    """Manages storage and retrieval of countdown data"""
    
    def __init__(self, filepath="countdowns.json"):
        self.filepath = filepath
        self.countdowns: List[Countdown] = []
        self.history: List[HistoryEntry] = []
        self.load()
    
    def load(self):
        """Load countdowns and history from JSON file"""
        if not os.path.exists(self.filepath):
            self.save()  # Create empty file
            return
        
        try:
            with open(self.filepath, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            self.countdowns = [Countdown.from_dict(c) for c in data.get("countdowns", [])]
            self.history = [HistoryEntry.from_dict(h) for h in data.get("history", [])]
        except Exception as e:
            print(f"Error loading data: {e}")
            self.countdowns = []
            self.history = []
    
    def save(self):
        """Save countdowns and history to JSON file"""
        data = {
            "countdowns": [c.to_dict() for c in self.countdowns],
            "history": [h.to_dict() for h in self.history]
        }
        
        try:
            with open(self.filepath, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
        except Exception as e:
            print(f"Error saving data: {e}")
    
    def add_countdown(self, countdown: Countdown):
        """Add a new countdown"""
        self.countdowns.append(countdown)
        self.save()
    
    def update_countdown(self, countdown_id: str, updated_countdown: Countdown):
        """Update an existing countdown"""
        for i, c in enumerate(self.countdowns):
            if c.id == countdown_id:
                self.countdowns[i] = updated_countdown
                self.save()
                return True
        return False
    
    def delete_countdown(self, countdown_id: str):
        """Delete a countdown"""
        self.countdowns = [c for c in self.countdowns if c.id != countdown_id]
        self.save()
    
    def get_countdown(self, countdown_id: str) -> Optional[Countdown]:
        """Get a countdown by ID"""
        for c in self.countdowns:
            if c.id == countdown_id:
                return c
        return None
    
    def get_active_countdowns(self) -> List[Countdown]:
        """Get all active countdowns"""
        return [c for c in self.countdowns if c.enabled]
    
    def get_visible_countdowns(self) -> List[Countdown]:
        """Get all visible countdowns"""
        return [c for c in self.countdowns if c.enabled and c.show]
    
    def add_history_entry(self, entry: HistoryEntry):
        """Add a new history entry"""
        self.history.append(entry)
        self.save()
    
    def clear_history(self):
        """Clear all history entries"""
        self.history = []
        self.save()
    
    def get_history(self, sort_by="ended_at", reverse=True) -> List[HistoryEntry]:
        """Get history entries, optionally sorted"""
        if sort_by:
            return sorted(self.history, key=lambda h: getattr(h, sort_by), reverse=reverse)
        return self.history
