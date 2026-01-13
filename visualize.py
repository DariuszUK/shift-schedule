"""
Visualization script to display countdown data
"""
from datetime import datetime, timedelta
from storage import CountdownStorage
from models import Countdown, HistoryEntry


def format_duration(seconds):
    """Format duration in seconds to human-readable format"""
    days = seconds // 86400
    hours = (seconds % 86400) // 3600
    minutes = (seconds % 3600) // 60
    secs = seconds % 60
    
    parts = []
    if days > 0:
        parts.append(f"{days}d")
    if hours > 0:
        parts.append(f"{hours}h")
    if minutes > 0:
        parts.append(f"{minutes}m")
    if secs > 0 or not parts:
        parts.append(f"{secs}s")
    
    return " ".join(parts)


def calculate_countdown(countdown):
    """Calculate remaining/elapsed time for countdown"""
    now = datetime.now()
    
    if countdown.type == "TO" and countdown.end_datetime:
        end_dt = datetime.strptime(countdown.end_datetime, "%Y-%m-%d %H:%M:%S")
        delta = end_dt - now
        
        if delta.total_seconds() > 0:
            days = delta.days
            hours = delta.seconds // 3600
            minutes = (delta.seconds % 3600) // 60
            seconds = delta.seconds % 60
            return f"Pozostało: {days}d {hours}h {minutes}m {seconds}s", "active"
        else:
            return "ZAKOŃCZONE", "completed"
    
    elif countdown.type == "FROM" and countdown.start_datetime:
        start_dt = datetime.strptime(countdown.start_datetime, "%Y-%m-%d %H:%M:%S")
        delta = now - start_dt
        
        if delta.total_seconds() > 0:
            days = delta.days
            hours = delta.seconds // 3600
            minutes = (delta.seconds % 3600) // 60
            seconds = delta.seconds % 60
            return f"Upłynęło: {days}d {hours}h {minutes}m {seconds}s", "active"
        else:
            return "Jeszcze nie rozpoczęte", "pending"
    
    return "Brak danych", "unknown"


def display_countdowns(storage):
    """Display all countdowns"""
    print("\n" + "="*80)
    print("AKTYWNE ODLICZENIA")
    print("="*80)
    
    if not storage.countdowns:
        print("Brak odliczeń")
        return
    
    for i, countdown in enumerate(storage.countdowns, 1):
        time_info, status = calculate_countdown(countdown)
        
        print(f"\n[{i}] {countdown.name}")
        print(f"    Typ: {countdown.type}")
        print(f"    Status: {time_info}")
        print(f"    Włączone: {'Tak' if countdown.enabled else 'Nie'}")
        print(f"    Widoczne: {'Tak' if countdown.show else 'Nie'}")
        print(f"    Kolor: {countdown.color}")
        
        if countdown.type == "TO" and countdown.end_datetime:
            print(f"    Data zakończenia: {countdown.end_datetime}")
        elif countdown.type == "FROM" and countdown.start_datetime:
            print(f"    Data rozpoczęcia: {countdown.start_datetime}")
        
        if countdown.alert_enabled:
            print(f"    Alert: {countdown.alert_minutes} min przed, tryb: {countdown.alert_mode}, kolor: {countdown.alert_color}")
        else:
            print(f"    Alert: wyłączony")


def display_history(storage):
    """Display countdown history"""
    print("\n" + "="*80)
    print("HISTORIA ODLICZEŃ")
    print("="*80)
    
    if not storage.history:
        print("Brak wpisów w historii")
        return
    
    for i, entry in enumerate(storage.get_history(sort_by="ended_at", reverse=True), 1):
        print(f"\n[{i}] {entry.name}")
        print(f"    Typ: {entry.type}")
        print(f"    Rozpoczęto: {entry.started_at}")
        print(f"    Zakończono: {entry.ended_at}")
        print(f"    Czas trwania: {format_duration(entry.duration_seconds)}")
        if entry.notes:
            print(f"    Notatki: {entry.notes}")


def display_statistics(storage):
    """Display statistics"""
    print("\n" + "="*80)
    print("STATYSTYKI")
    print("="*80)
    
    total = len(storage.countdowns)
    active = len(storage.get_active_countdowns())
    visible = len(storage.get_visible_countdowns())
    
    type_to = len([c for c in storage.countdowns if c.type == "TO"])
    type_from = len([c for c in storage.countdowns if c.type == "FROM"])
    
    with_alerts = len([c for c in storage.countdowns if c.alert_enabled])
    
    print(f"Łącznie odliczeń: {total}")
    print(f"Aktywne: {active}")
    print(f"Widoczne: {visible}")
    print(f"Typ TO (do): {type_to}")
    print(f"Typ FROM (od): {type_from}")
    print(f"Z alertami: {with_alerts}")
    print(f"Wpisy w historii: {len(storage.history)}")


def create_sample_data():
    """Create sample countdown data"""
    storage = CountdownStorage("countdowns.json")
    
    # Clear existing data
    storage.countdowns = []
    storage.history = []
    
    # Add sample countdowns
    countdown1 = Countdown(
        name="Urodziny Jana",
        type="TO",
        end_datetime=(datetime.now() + timedelta(days=45)).strftime("%Y-%m-%d 18:00:00"),
        color="#00ffff",
        alert_enabled=True,
        alert_minutes=1440,  # 1 day before
        alert_mode="pulse",
        alert_color="#ff0000"
    )
    storage.add_countdown(countdown1)
    
    countdown2 = Countdown(
        name="Projekt XYZ - dni od startu",
        type="FROM",
        start_datetime=(datetime.now() - timedelta(days=12)).strftime("%Y-%m-%d 09:00:00"),
        color="#00ff00",
        alert_enabled=False
    )
    storage.add_countdown(countdown2)
    
    countdown3 = Countdown(
        name="Wakacje 2026",
        type="TO",
        end_datetime="2026-07-01 00:00:00",
        color="#ffff00",
        alert_enabled=True,
        alert_minutes=10080,  # 7 days before
        alert_mode="blink",
        alert_color="#ff8800"
    )
    storage.add_countdown(countdown3)
    
    countdown4 = Countdown(
        name="Sprint Review",
        type="TO",
        end_datetime=(datetime.now() + timedelta(days=3)).strftime("%Y-%m-%d 14:00:00"),
        color="#ff00ff",
        alert_enabled=True,
        alert_minutes=60,  # 1 hour before
        alert_mode="pulse",
        alert_color="#ff0000"
    )
    storage.add_countdown(countdown4)
    
    # Add sample history
    entry1 = HistoryEntry(
        name="Projekt ABC",
        type="TO",
        started_at=(datetime.now() - timedelta(days=60)).strftime("%Y-%m-%d 10:00:00"),
        ended_at=(datetime.now() - timedelta(days=30)).strftime("%Y-%m-%d 15:00:00"),
        duration_seconds=2592000,  # 30 days
        notes="Zakończone pomyślnie"
    )
    storage.add_history_entry(entry1)
    
    entry2 = HistoryEntry(
        name="Konferencja Q1",
        type="TO",
        started_at=(datetime.now() - timedelta(days=90)).strftime("%Y-%m-%d 08:00:00"),
        ended_at=(datetime.now() - timedelta(days=85)).strftime("%Y-%m-%d 17:00:00"),
        duration_seconds=432000,  # 5 days
        notes="Uczestniczono"
    )
    storage.add_history_entry(entry2)
    
    print("✅ Utworzono przykładowe dane w pliku countdowns.json")
    
    return storage


def main():
    """Main function"""
    print("""
╔══════════════════════════════════════════════════════════════════╗
║              Shift Reminder - Wizualizacja Odliczeń             ║
╚══════════════════════════════════════════════════════════════════╝
""")
    
    import sys
    import os
    
    if len(sys.argv) > 1 and sys.argv[1] == "--create-sample":
        storage = create_sample_data()
    else:
        if not os.path.exists("countdowns.json"):
            print("ℹ️  Plik countdowns.json nie istnieje. Używam countdowns_example.json")
            if os.path.exists("countdowns_example.json"):
                # Copy example to working file for display
                import shutil
                shutil.copy("countdowns_example.json", "countdowns.json")
            else:
                print("⚠️  Brak danych do wyświetlenia.")
                print("\nUżyj: python visualize.py --create-sample aby utworzyć przykładowe dane")
                return
        
        storage = CountdownStorage("countdowns.json")
    
    display_statistics(storage)
    display_countdowns(storage)
    display_history(storage)
    
    print("\n" + "="*80)
    print("💡 Wskazówki:")
    print("   - Uruchom 'python demo.py' aby interaktywnie zarządzać odliczeniami")
    print("   - Uruchom 'python shift_reminder.py' aby uruchomić aplikację (wymaga Windows)")
    print("   - Uruchom 'python visualize.py --create-sample' aby utworzyć przykładowe dane")
    print("="*80 + "\n")


if __name__ == "__main__":
    main()
