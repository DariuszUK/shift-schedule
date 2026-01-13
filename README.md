# Shift Reminder - System Odliczeń

Aplikacja systemowa z zasobnikiem systemowym do zarządzania nieograniczoną liczbą odliczeń.

## Funkcje

### 1. Nieograniczone odliczenia
- Dynamiczne dodawanie/usuwanie odliczeń
- Każde odliczenie ma swoją indywidualną konfigurację
- Przechowywanie w pliku JSON

### 2. Typy odliczeń
- **TO (DO)** - odliczanie do konkretnej daty/godziny
- **FROM (OD)** - wyświetlanie czasu upływającego od konkretnej daty/godziny
- Obie opcje z systemem alertów

### 3. Historia odliczeń
- Lista wszystkich ukończonych odliczeń
- Data rozpoczęcia i zakończenia
- Czas trwania
- Status i notatki
- Filtrowanie i sortowanie
- Czyszczenie historii

### 4. Zarządzanie odliczeniami
- Dodawanie nowych odliczeń
- Edycja istniejących
- Usuwanie odliczeń
- Konfiguracja:
  - Nazwa
  - Data/czas rozpoczęcia (dla typu FROM)
  - Data/czas zakończenia (dla typu TO)
  - Typ odliczenia (TO/FROM)
  - Kolor wyświetlania
  - Alerty (włącz/wyłącz, czas, tryb, kolor)
  - Aktywowanie/dezaktywowanie

### 5. Menu kontekstowe (RMB)
- ⚙️ Ustawienia
- ⏱️ Zarządzaj odliczeniami
- 📋 Historia odliczeń
- 🔄 Odśwież dane
- 👁️ Widoczność
- 📅 Work Calendar
- 📊 Excel Export
- 🔧 Manage Shifts
- ❌ Zamknij

## Instalacja

```bash
pip install -r requirements.txt
```

## Uruchomienie

```bash
python shift_reminder.py
```

## Format danych

Dane są przechowywane w pliku `countdowns.json` w formacie:

```json
{
  "countdowns": [
    {
      "id": "unique_id",
      "name": "nazwa",
      "type": "TO",
      "start_datetime": "2026-01-15 10:00:00",
      "end_datetime": "2026-01-23 15:00:00",
      "enabled": true,
      "show": true,
      "color": "#00ffff",
      "alert_enabled": true,
      "alert_minutes": 60,
      "alert_mode": "pulse",
      "alert_color": "#ff0000"
    }
  ],
  "history": [
    {
      "id": "unique_id",
      "name": "nazwa",
      "type": "TO",
      "started_at": "2025-12-01 10:00:00",
      "ended_at": "2025-12-23 15:00:00",
      "duration_seconds": 1900800,
      "notes": "Zakończone pomyślnie"
    }
  ]
}
```

## Wymagania systemowe

- Python 3.7+
- Windows (dla ikony w zasobniku systemowym)
- Tkinter (zazwyczaj dołączony do Pythona)

## Struktura plików

- `shift_reminder.py` - główny plik aplikacji
- `models.py` - modele danych (Countdown, HistoryEntry)
- `storage.py` - moduł zarządzania przechowywaniem danych
- `dialogs.py` - okna dialogowe (zarządzanie, historia)
- `countdowns.json` - plik z danymi odliczeń
- `requirements.txt` - zależności Pythona