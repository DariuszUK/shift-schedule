"""
Test script for Shift Reminder countdown system
"""
import unittest
from datetime import datetime, timedelta
import os
import json

from models import Countdown, HistoryEntry
from storage import CountdownStorage


class TestCountdown(unittest.TestCase):
    """Test Countdown model"""
    
    def test_countdown_creation(self):
        """Test creating a countdown"""
        countdown = Countdown(
            name="Test Countdown",
            type="TO",
            end_datetime="2026-01-23 15:00:00",
            color="#00ffff"
        )
        
        self.assertEqual(countdown.name, "Test Countdown")
        self.assertEqual(countdown.type, "TO")
        self.assertEqual(countdown.end_datetime, "2026-01-23 15:00:00")
        self.assertTrue(countdown.enabled)
        self.assertTrue(countdown.show)
    
    def test_countdown_to_dict(self):
        """Test countdown serialization"""
        countdown = Countdown(
            name="Test",
            type="FROM",
            start_datetime="2026-01-15 10:00:00"
        )
        
        data = countdown.to_dict()
        
        self.assertIn("id", data)
        self.assertEqual(data["name"], "Test")
        self.assertEqual(data["type"], "FROM")
        self.assertEqual(data["start_datetime"], "2026-01-15 10:00:00")
    
    def test_countdown_from_dict(self):
        """Test countdown deserialization"""
        data = {
            "id": "test-id",
            "name": "Test Countdown",
            "type": "TO",
            "end_datetime": "2026-01-23 15:00:00",
            "enabled": True,
            "show": True,
            "color": "#00ffff",
            "alert_enabled": False,
            "alert_minutes": 60,
            "alert_mode": "pulse",
            "alert_color": "#ff0000"
        }
        
        countdown = Countdown.from_dict(data)
        
        self.assertEqual(countdown.id, "test-id")
        self.assertEqual(countdown.name, "Test Countdown")
        self.assertEqual(countdown.type, "TO")


class TestHistoryEntry(unittest.TestCase):
    """Test HistoryEntry model"""
    
    def test_history_entry_creation(self):
        """Test creating a history entry"""
        entry = HistoryEntry(
            name="Completed Countdown",
            type="TO",
            started_at="2025-12-01 10:00:00",
            ended_at="2025-12-23 15:00:00",
            duration_seconds=1900800,
            notes="Completed successfully"
        )
        
        self.assertEqual(entry.name, "Completed Countdown")
        self.assertEqual(entry.type, "TO")
        self.assertEqual(entry.duration_seconds, 1900800)
    
    def test_history_entry_to_dict(self):
        """Test history entry serialization"""
        entry = HistoryEntry(
            name="Test",
            type="FROM",
            started_at="2025-12-01 10:00:00",
            ended_at="2025-12-23 15:00:00",
            duration_seconds=1900800
        )
        
        data = entry.to_dict()
        
        self.assertIn("id", data)
        self.assertEqual(data["name"], "Test")
        self.assertEqual(data["type"], "FROM")


class TestCountdownStorage(unittest.TestCase):
    """Test CountdownStorage"""
    
    def setUp(self):
        """Set up test storage"""
        self.test_file = "test_countdowns.json"
        self.storage = CountdownStorage(self.test_file)
    
    def tearDown(self):
        """Clean up test file"""
        if os.path.exists(self.test_file):
            os.remove(self.test_file)
    
    def test_add_countdown(self):
        """Test adding a countdown"""
        countdown = Countdown(
            name="Test Countdown",
            type="TO",
            end_datetime="2026-01-23 15:00:00"
        )
        
        self.storage.add_countdown(countdown)
        
        self.assertEqual(len(self.storage.countdowns), 1)
        self.assertEqual(self.storage.countdowns[0].name, "Test Countdown")
    
    def test_delete_countdown(self):
        """Test deleting a countdown"""
        countdown = Countdown(
            name="Test Countdown",
            type="TO",
            end_datetime="2026-01-23 15:00:00"
        )
        
        self.storage.add_countdown(countdown)
        countdown_id = self.storage.countdowns[0].id
        
        self.storage.delete_countdown(countdown_id)
        
        self.assertEqual(len(self.storage.countdowns), 0)
    
    def test_update_countdown(self):
        """Test updating a countdown"""
        countdown = Countdown(
            name="Original Name",
            type="TO",
            end_datetime="2026-01-23 15:00:00"
        )
        
        self.storage.add_countdown(countdown)
        countdown_id = self.storage.countdowns[0].id
        
        updated_countdown = Countdown(
            id=countdown_id,
            name="Updated Name",
            type="TO",
            end_datetime="2026-01-23 15:00:00"
        )
        
        self.storage.update_countdown(countdown_id, updated_countdown)
        
        self.assertEqual(self.storage.countdowns[0].name, "Updated Name")
    
    def test_get_active_countdowns(self):
        """Test getting active countdowns"""
        countdown1 = Countdown(name="Active", type="TO", end_datetime="2026-01-23 15:00:00", enabled=True)
        countdown2 = Countdown(name="Inactive", type="TO", end_datetime="2026-01-23 15:00:00", enabled=False)
        
        self.storage.add_countdown(countdown1)
        self.storage.add_countdown(countdown2)
        
        active = self.storage.get_active_countdowns()
        
        self.assertEqual(len(active), 1)
        self.assertEqual(active[0].name, "Active")
    
    def test_get_visible_countdowns(self):
        """Test getting visible countdowns"""
        countdown1 = Countdown(name="Visible", type="TO", end_datetime="2026-01-23 15:00:00", enabled=True, show=True)
        countdown2 = Countdown(name="Hidden", type="TO", end_datetime="2026-01-23 15:00:00", enabled=True, show=False)
        
        self.storage.add_countdown(countdown1)
        self.storage.add_countdown(countdown2)
        
        visible = self.storage.get_visible_countdowns()
        
        self.assertEqual(len(visible), 1)
        self.assertEqual(visible[0].name, "Visible")
    
    def test_add_history_entry(self):
        """Test adding history entry"""
        entry = HistoryEntry(
            name="Completed",
            type="TO",
            started_at="2025-12-01 10:00:00",
            ended_at="2025-12-23 15:00:00",
            duration_seconds=1900800
        )
        
        self.storage.add_history_entry(entry)
        
        self.assertEqual(len(self.storage.history), 1)
        self.assertEqual(self.storage.history[0].name, "Completed")
    
    def test_clear_history(self):
        """Test clearing history"""
        entry = HistoryEntry(
            name="Completed",
            type="TO",
            started_at="2025-12-01 10:00:00",
            ended_at="2025-12-23 15:00:00",
            duration_seconds=1900800
        )
        
        self.storage.add_history_entry(entry)
        self.storage.clear_history()
        
        self.assertEqual(len(self.storage.history), 0)
    
    def test_persistence(self):
        """Test data persistence"""
        countdown = Countdown(
            name="Persistent",
            type="TO",
            end_datetime="2026-01-23 15:00:00"
        )
        
        self.storage.add_countdown(countdown)
        
        # Create new storage instance
        new_storage = CountdownStorage(self.test_file)
        
        self.assertEqual(len(new_storage.countdowns), 1)
        self.assertEqual(new_storage.countdowns[0].name, "Persistent")


if __name__ == "__main__":
    unittest.main()
