# Shift Reminder - Quick Start Guide

## Szybki start

### 1. Instalacja (jednorazowo)

```bash
# Sklonuj repozytorium
git clone https://github.com/DariuszUK/shift-schedule.git
cd shift-schedule

# Zainstaluj zależności
pip install -r requirements.txt
```

### 2. Pierwsze uruchomienie

**Opcja A: Pełna aplikacja (Windows)**
```bash
python shift_reminder.py
```
Aplikacja pojawi się w zasobniku systemowym (system tray). Kliknij prawym przyciskiem myszy aby zobaczyć menu.

**Opcja B: Demo (wszystkie systemy)**
```bash
python demo.py
```
Interaktywne demo bez wymagania ikony systemowej.

**Opcja C: Wizualizacja (wszystkie systemy)**
```bash
# Utwórz przykładowe dane
python visualize.py --create-sample

# Wyświetl dane
python visualize.py
```

### 3. Dodaj pierwsze odliczenie

#### Przez aplikację:
1. Kliknij prawym przyciskiem myszy na ikonę w zasobniku
2. Wybierz "⏱️ Zarządzaj odliczeniami"
3. Kliknij "➕ Dodaj nowe"
4. Wypełnij formularz:
   - **Nazwa**: np. "Urodziny"
   - **Typ**: wybierz "DO" lub "OD"
   - **Data/czas**: np. "2026-06-15 18:00:00"
   - **Kolor**: wybierz kolor lub wpisz kod hex
   - **Alert**: włącz i ustaw minuty przed
5. Kliknij "Zapisz"

#### Przez plik JSON:
1. Utwórz/edytuj plik `countdowns.json`:
```json
{
  "countdowns": [
    {
      "id": "1",
      "name": "Moje pierwsze odliczenie",
      "type": "TO",
      "end_datetime": "2026-12-31 23:59:59",
      "enabled": true,
      "show": true,
      "color": "#00ffff",
      "alert_enabled": true,
      "alert_minutes": 60,
      "alert_mode": "pulse",
      "alert_color": "#ff0000"
    }
  ],
  "history": []
}
```
2. W menu wybierz "🔄 Odśwież dane"

### 4. Przykłady użycia

#### Odliczanie do urodzin (typ TO)
```json
{
  "name": "Urodziny Mamy",
  "type": "TO",
  "end_datetime": "2026-05-20 00:00:00",
  "alert_enabled": true,
  "alert_minutes": 1440
}
```
Alert: 24 godziny (1440 minut) przed

#### Dni od rozpoczęcia projektu (typ FROM)
```json
{
  "name": "Projekt Alpha",
  "type": "FROM",
  "start_datetime": "2026-01-01 09:00:00",
  "alert_enabled": false
}
```
Pokazuje ile czasu upłynęło od startu

#### Odliczanie do wakacji z alertem 7 dni przed
```json
{
  "name": "Wakacje 2026",
  "type": "TO",
  "end_datetime": "2026-07-01 00:00:00",
  "alert_enabled": true,
  "alert_minutes": 10080
}
```
Alert: 7 dni (10080 minut) przed

### 5. Najważniejsze funkcje

| Funkcja | Opis | Jak użyć |
|---------|------|----------|
| Dodaj odliczenie | Utwórz nowe odliczenie | RMB → Zarządzaj odliczeniami → Dodaj nowe |
| Edytuj odliczenie | Zmień istniejące odliczenie | RMB → Zarządzaj odliczeniami → Edytuj |
| Historia | Zobacz zakończone odliczenia | RMB → Historia odliczeń |
| Odśwież | Przeładuj dane z pliku | RMB → Odśwież dane |
| Usuń | Usuń odliczenie | RMB → Zarządzaj odliczeniami → Usuń |

### 6. Format daty/czasu

**ZAWSZE** używaj formatu: `YYYY-MM-DD HH:MM:SS`

✅ Poprawne:
- `2026-01-15 10:00:00`
- `2026-12-31 23:59:59`
- `2026-07-01 00:00:00`

❌ Niepoprawne:
- `15/01/2026 10:00:00`
- `2026-1-15 10:00:00`
- `2026-01-15 10:00`

### 7. Typy odliczeń

#### TO (DO) - odliczanie DO daty
- Używaj dla: urodzin, eventów, deadlinów
- Pokazuje: ile czasu **pozostało**
- Wymaga: `end_datetime`

#### FROM (OD) - odliczanie OD daty
- Używaj dla: wieku projektu, dni od wydarzenia
- Pokazuje: ile czasu **upłynęło**
- Wymaga: `start_datetime`

### 8. Kolory

Używaj kodów hex:
- `#00ffff` - cyan (domyślny)
- `#ff0000` - czerwony
- `#00ff00` - zielony
- `#ffff00` - żółty
- `#ff00ff` - magenta
- `#ffffff` - biały

### 9. Tryby alertu

- `pulse` - pulsujący (domyślny)
- `blink` - migający
- `static` - statyczny

### 10. Czas alertu (w minutach)

| Czas | Minuty |
|------|--------|
| 15 minut | 15 |
| 1 godzina | 60 |
| 6 godzin | 360 |
| 12 godzin | 720 |
| 24 godziny (1 dzień) | 1440 |
| 3 dni | 4320 |
| 7 dni | 10080 |
| 14 dni | 20160 |

### 11. Testowanie

```bash
# Uruchom testy
python test_shift_reminder.py

# Wszystkie testy powinny zakończyć się: OK
```

### 12. Rozwiązywanie problemów

**Problem**: Aplikacja nie uruchamia się
```bash
# Sprawdź zależności
pip install -r requirements.txt

# Sprawdź Pythona
python --version  # Wymagane: 3.7+
```

**Problem**: Błąd formatu daty
- Użyj dokładnego formatu: `YYYY-MM-DD HH:MM:SS`
- Sprawdź czy data jest poprawna (np. nie ma 32 stycznia)

**Problem**: Odliczenia nie są zapisywane
- Sprawdź uprawnienia do zapisu
- Sprawdź czy plik nie jest otwarty
- Użyj "🔄 Odśwież dane"

### 13. Wsparcie

- 📖 Pełna dokumentacja: `USER_GUIDE.md`
- 🐛 Zgłoś problem: GitHub Issues
- 💬 Pytania: GitHub Discussions

---

**Gratulacje!** Jesteś gotowy do użycia Shift Reminder! 🎉
