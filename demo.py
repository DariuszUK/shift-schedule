"""
Demo script for Shift Reminder countdown system
This script demonstrates the functionality without requiring the system tray
"""
import tkinter as tk
from tkinter import messagebox
from datetime import datetime, timedelta

from storage import CountdownStorage
from models import Countdown, HistoryEntry
from dialogs import CountdownDialog, HistoryDialog, ManageCountdownsDialog


def demo_countdown_storage():
    """Demo: Storage functionality"""
    print("\n=== Demo: Storage Functionality ===")
    
    storage = CountdownStorage("demo_countdowns.json")
    
    # Create sample countdowns
    countdown1 = Countdown(
        name="Urodziny Jana",
        type="TO",
        end_datetime=(datetime.now() + timedelta(days=30)).strftime("%Y-%m-%d %H:%M:%S"),
        color="#00ffff",
        alert_enabled=True,
        alert_minutes=1440
    )
    
    countdown2 = Countdown(
        name="Dni od rozpoczęcia projektu",
        type="FROM",
        start_datetime=(datetime.now() - timedelta(days=10)).strftime("%Y-%m-%d %H:%M:%S"),
        color="#00ff00"
    )
    
    # Add countdowns
    storage.add_countdown(countdown1)
    storage.add_countdown(countdown2)
    
    print(f"Added {len(storage.countdowns)} countdowns")
    print(f"Active countdowns: {len(storage.get_active_countdowns())}")
    print(f"Visible countdowns: {len(storage.get_visible_countdowns())}")
    
    # Add history entry
    entry = HistoryEntry(
        name="Completed Project",
        type="TO",
        started_at=(datetime.now() - timedelta(days=60)).strftime("%Y-%m-%d %H:%M:%S"),
        ended_at=(datetime.now() - timedelta(days=30)).strftime("%Y-%m-%d %H:%M:%S"),
        duration_seconds=2592000,  # 30 days
        notes="Zakończone pomyślnie"
    )
    
    storage.add_history_entry(entry)
    print(f"History entries: {len(storage.history)}")
    
    print("\nCountdowns:")
    for c in storage.countdowns:
        print(f"  - {c.name} ({c.type}): {'Enabled' if c.enabled else 'Disabled'}")
    
    print("\nHistory:")
    for h in storage.history:
        print(f"  - {h.name}: {h.duration_seconds} seconds")
    
    return storage


def demo_countdown_dialog():
    """Demo: Countdown dialog"""
    print("\n=== Demo: Countdown Dialog ===")
    
    root = tk.Tk()
    root.withdraw()
    
    def on_save(countdown):
        print(f"Countdown saved: {countdown.name} ({countdown.type})")
        print(f"  Start: {countdown.start_datetime}")
        print(f"  End: {countdown.end_datetime}")
        print(f"  Color: {countdown.color}")
        print(f"  Alert: {countdown.alert_enabled}")
    
    dialog = CountdownDialog(None, on_save=on_save)
    root.wait_window(dialog.window)
    root.destroy()


def demo_manage_countdowns():
    """Demo: Manage countdowns dialog"""
    print("\n=== Demo: Manage Countdowns Dialog ===")
    
    storage = demo_countdown_storage()
    
    root = tk.Tk()
    root.withdraw()
    
    def on_refresh():
        print("Countdowns refreshed")
    
    dialog = ManageCountdownsDialog(None, storage, on_refresh=on_refresh)
    root.wait_window(dialog.window)
    root.destroy()


def demo_history_dialog():
    """Demo: History dialog"""
    print("\n=== Demo: History Dialog ===")
    
    storage = demo_countdown_storage()
    
    root = tk.Tk()
    root.withdraw()
    
    def on_clear():
        storage.clear_history()
        print("History cleared")
    
    dialog = HistoryDialog(None, storage.history, on_clear=on_clear)
    root.wait_window(dialog.window)
    root.destroy()


def main_menu():
    """Show main menu"""
    print("\n" + "="*50)
    print("Shift Reminder - Demo Menu")
    print("="*50)
    print("1. Demo: Storage Functionality")
    print("2. Demo: Add/Edit Countdown Dialog")
    print("3. Demo: Manage Countdowns Dialog")
    print("4. Demo: History Dialog")
    print("5. Run All Demos")
    print("0. Exit")
    print("="*50)
    
    choice = input("\nSelect option: ").strip()
    
    if choice == "1":
        demo_countdown_storage()
        main_menu()
    elif choice == "2":
        demo_countdown_dialog()
        main_menu()
    elif choice == "3":
        demo_manage_countdowns()
        main_menu()
    elif choice == "4":
        demo_history_dialog()
        main_menu()
    elif choice == "5":
        demo_countdown_storage()
        input("\nPress Enter to continue to countdown dialog...")
        demo_countdown_dialog()
        input("\nPress Enter to continue to manage dialog...")
        demo_manage_countdowns()
        input("\nPress Enter to continue to history dialog...")
        demo_history_dialog()
        main_menu()
    elif choice == "0":
        print("\nExiting demo...")
        return
    else:
        print("\nInvalid option, try again.")
        main_menu()


if __name__ == "__main__":
    print("""
╔════════════════════════════════════════════════════════════════╗
║           Shift Reminder - Countdown System Demo              ║
║                                                                ║
║  This demo showcases the countdown management functionality   ║
║  without requiring the system tray to be running.             ║
╚════════════════════════════════════════════════════════════════╝
""")
    
    main_menu()
    print("\nThank you for trying Shift Reminder!")
