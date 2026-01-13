"""
Shift Reminder - System Tray Application with Countdown Management
"""
import tkinter as tk
from tkinter import messagebox
import pystray
from PIL import Image, ImageDraw, ImageFont
import threading
from datetime import datetime, timedelta
from dateutil import parser
import time
import sys
import os

from storage import CountdownStorage
from dialogs import CountdownDialog, HistoryDialog, ManageCountdownsDialog
from models import HistoryEntry


class ShiftReminder:
    """Main application class"""
    
    def __init__(self):
        self.storage = CountdownStorage()
        self.icon = None
        self.running = True
        self.alert_active = {}  # Track active alerts by countdown ID
        
        # Create system tray icon
        self.create_icon()
        
        # Start countdown update thread
        self.update_thread = threading.Thread(target=self.update_countdowns, daemon=True)
        self.update_thread.start()
    
    def create_icon(self):
        """Create system tray icon"""
        # Create icon image
        image = self.create_icon_image()
        
        # Create menu
        menu = pystray.Menu(
            pystray.MenuItem("⚙️ Ustawienia", self.show_settings),
            pystray.MenuItem("⏱️ Zarządzaj odliczeniami", self.manage_countdowns),
            pystray.MenuItem("📋 Historia odliczeń", self.show_history),
            pystray.Menu.SEPARATOR,
            pystray.MenuItem("🔄 Odśwież dane", self.refresh_data),
            pystray.MenuItem("👁️ Widoczność", self.toggle_visibility),
            pystray.Menu.SEPARATOR,
            pystray.MenuItem("📅 Work Calendar", self.show_work_calendar),
            pystray.MenuItem("📊 Excel Export", self.excel_export),
            pystray.MenuItem("🔧 Manage Shifts", self.manage_shifts),
            pystray.Menu.SEPARATOR,
            pystray.MenuItem("❌ Zamknij", self.quit_app)
        )
        
        # Create icon
        self.icon = pystray.Icon("shift_reminder", image, "Shift Reminder", menu)
    
    def create_icon_image(self, text="SR", color="cyan"):
        """Create icon image with text"""
        # Create image
        width = 64
        height = 64
        image = Image.new('RGB', (width, height), color=(0, 0, 0))
        draw = ImageDraw.Draw(image)
        
        # Draw circle
        if color == "cyan":
            fill_color = (0, 255, 255)
        elif color == "red":
            fill_color = (255, 0, 0)
        elif color == "yellow":
            fill_color = (255, 255, 0)
        else:
            fill_color = (0, 255, 255)
        
        draw.ellipse([4, 4, width-4, height-4], fill=fill_color, outline=(255, 255, 255), width=2)
        
        # Draw text
        try:
            font = ImageFont.truetype("arial.ttf", 24)
        except:
            font = ImageFont.load_default()
        
        # Calculate text position
        bbox = draw.textbbox((0, 0), text, font=font)
        text_width = bbox[2] - bbox[0]
        text_height = bbox[3] - bbox[1]
        position = ((width - text_width) // 2, (height - text_height) // 2 - 2)
        
        draw.text(position, text, fill=(0, 0, 0), font=font)
        
        return image
    
    def update_icon(self, text="SR", color="cyan"):
        """Update icon image"""
        if self.icon:
            self.icon.icon = self.create_icon_image(text, color)
    
    def run(self):
        """Run the application"""
        self.icon.run()
    
    def update_countdowns(self):
        """Update countdowns in background thread"""
        while self.running:
            try:
                now = datetime.now()
                active_countdowns = self.storage.get_active_countdowns()
                
                # Check for completed countdowns
                for countdown in active_countdowns:
                    if countdown.type == "TO" and countdown.end_datetime:
                        end_dt = datetime.strptime(countdown.end_datetime, "%Y-%m-%d %H:%M:%S")
                        
                        # Check if countdown is complete
                        if now >= end_dt:
                            # Move to history
                            start_dt = datetime.strptime(countdown.start_datetime, "%Y-%m-%d %H:%M:%S") if countdown.start_datetime else end_dt - timedelta(days=1)
                            duration = int((end_dt - start_dt).total_seconds())
                            
                            entry = HistoryEntry(
                                id=countdown.id,
                                name=countdown.name,
                                type=countdown.type,
                                started_at=start_dt.strftime("%Y-%m-%d %H:%M:%S"),
                                ended_at=end_dt.strftime("%Y-%m-%d %H:%M:%S"),
                                duration_seconds=duration,
                                notes="Zakończone pomyślnie"
                            )
                            self.storage.add_history_entry(entry)
                            self.storage.delete_countdown(countdown.id)
                            continue
                        
                        # Check for alerts
                        if countdown.alert_enabled and countdown.id not in self.alert_active:
                            alert_time = end_dt - timedelta(minutes=countdown.alert_minutes)
                            if now >= alert_time:
                                self.trigger_alert(countdown)
                
                # Update icon with countdown info
                visible_countdowns = self.storage.get_visible_countdowns()
                if visible_countdowns:
                    # Find nearest countdown
                    nearest = None
                    nearest_delta = None
                    
                    for countdown in visible_countdowns:
                        if countdown.type == "TO" and countdown.end_datetime:
                            end_dt = datetime.strptime(countdown.end_datetime, "%Y-%m-%d %H:%M:%S")
                            delta = end_dt - now
                            if delta.total_seconds() > 0 and (nearest_delta is None or delta < nearest_delta):
                                nearest = countdown
                                nearest_delta = delta
                    
                    if nearest and nearest_delta:
                        # Update icon with countdown
                        days = nearest_delta.days
                        if days > 0:
                            self.update_icon(f"{days}d", "cyan")
                        else:
                            hours = int(nearest_delta.seconds // 3600)
                            if hours > 0:
                                self.update_icon(f"{hours}h", "yellow")
                            else:
                                minutes = int((nearest_delta.seconds % 3600) // 60)
                                self.update_icon(f"{minutes}m", "red")
                    else:
                        self.update_icon("SR", "cyan")
                else:
                    self.update_icon("SR", "cyan")
                
            except Exception as e:
                print(f"Error updating countdowns: {e}")
            
            time.sleep(60)  # Update every minute
    
    def trigger_alert(self, countdown):
        """Trigger alert for countdown"""
        self.alert_active[countdown.id] = True
        
        # Create notification
        try:
            if self.icon:
                self.icon.notify(
                    f"⏰ Alert: {countdown.name}",
                    f"Pozostało {countdown.alert_minutes} minut!"
                )
        except Exception as e:
            print(f"Error showing notification: {e}")
        
        # Update icon color based on alert
        if countdown.alert_mode == "pulse" or countdown.alert_mode == "blink":
            # Simple color change for alert
            self.update_icon("!", "red")
    
    def show_settings(self):
        """Show settings dialog"""
        def show():
            root = tk.Tk()
            root.withdraw()
            messagebox.showinfo("Ustawienia", "Dialog ustawień w przygotowaniu")
            root.destroy()
        
        threading.Thread(target=show, daemon=True).start()
    
    def manage_countdowns(self):
        """Show countdown management dialog"""
        def show():
            root = tk.Tk()
            root.withdraw()
            dialog = ManageCountdownsDialog(None, self.storage, on_refresh=self.refresh_data)
            root.wait_window(dialog.window)
            root.destroy()
        
        threading.Thread(target=show, daemon=True).start()
    
    def show_history(self):
        """Show history dialog"""
        def show():
            root = tk.Tk()
            root.withdraw()
            dialog = HistoryDialog(None, self.storage.history, on_clear=self.clear_history)
            root.wait_window(dialog.window)
            root.destroy()
        
        threading.Thread(target=show, daemon=True).start()
    
    def refresh_data(self):
        """Refresh data from storage"""
        self.storage.load()
        self.alert_active.clear()
        
        def show():
            root = tk.Tk()
            root.withdraw()
            messagebox.showinfo("Odświeżanie", "Dane zostały odświeżone")
            root.destroy()
        
        threading.Thread(target=show, daemon=True).start()
    
    def toggle_visibility(self):
        """Toggle countdown visibility"""
        def show():
            root = tk.Tk()
            root.withdraw()
            messagebox.showinfo("Widoczność", "Dialog widoczności w przygotowaniu")
            root.destroy()
        
        threading.Thread(target=show, daemon=True).start()
    
    def show_work_calendar(self):
        """Show work calendar"""
        def show():
            root = tk.Tk()
            root.withdraw()
            messagebox.showinfo("Work Calendar", "Kalendarz pracy w przygotowaniu")
            root.destroy()
        
        threading.Thread(target=show, daemon=True).start()
    
    def excel_export(self):
        """Export to Excel"""
        def show():
            root = tk.Tk()
            root.withdraw()
            messagebox.showinfo("Excel Export", "Eksport do Excel w przygotowaniu")
            root.destroy()
        
        threading.Thread(target=show, daemon=True).start()
    
    def manage_shifts(self):
        """Manage shifts"""
        def show():
            root = tk.Tk()
            root.withdraw()
            messagebox.showinfo("Manage Shifts", "Zarządzanie zmianami w przygotowaniu")
            root.destroy()
        
        threading.Thread(target=show, daemon=True).start()
    
    def clear_history(self):
        """Clear countdown history"""
        self.storage.clear_history()
    
    def quit_app(self):
        """Quit application"""
        self.running = False
        if self.icon:
            self.icon.stop()


def main():
    """Main entry point"""
    app = ShiftReminder()
    app.run()


if __name__ == "__main__":
    main()
