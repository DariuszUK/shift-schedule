# Shift Reminder - User Guide

## Przegląd

Shift Reminder to aplikacja systemowa (system tray application) do zarządzania nieograniczoną liczbą odliczeń czasu. Aplikacja obsługuje dwa typy odliczeń:
- **TO (DO)** - odliczanie do konkretnej daty/godziny
- **FROM (OD)** - wyświetlanie czasu upływającego od konkretnej daty/godziny

## Instalacja

### Wymagania
- Python 3.7 lub nowszy
- System Windows (dla ikony w zasobniku systemowym)

### Kroki instalacji

1. Sklonuj repozytorium:
```bash
git clone https://github.com/DariuszUK/shift-schedule.git
cd shift-schedule
```

2. Zainstaluj zależności:
```bash
pip install -r requirements.txt
```

3. Uruchom aplikację:
```bash
python shift_reminder.py
```

## Funkcje

### 1. Nieograniczone odliczenia

Aplikacja pozwala na utworzenie dowolnej liczby odliczeń. Każde odliczenie może być:
- Włączone lub wyłączone
- Widoczne lub ukryte
- Skonfigurowane z własnym kolorem
- Wyposażone w system alertów

### 2. Typy odliczeń

#### Typ TO (DO)
Odliczanie **do** konkretnej daty i godziny. Przykłady:
- Odliczanie do urodzin
- Czas do końca projektu
- Dni do wakacji

**Konfiguracja:**
- Typ: TO
- Data/czas zakończenia: np. "2026-07-01 00:00:00"
- Data/czas rozpoczęcia: opcjonalne

#### Typ FROM (OD)
Wyświetlanie czasu **od** konkretnej daty i godziny. Przykłady:
- Dni od rozpoczęcia projektu
- Czas od ważnego wydarzenia
- Wiek w dniach/godzinach

**Konfiguracja:**
- Typ: FROM
- Data/czas rozpoczęcia: np. "2026-01-01 09:00:00"
- Data/czas zakończenia: nie używane

### 3. System alertów

Każde odliczenie może mieć skonfigurowane alerty:
- **Włącz alerty**: włącz/wyłącz alerty dla tego odliczenia
- **Alert (minuty przed)**: ile minut przed zakończeniem pokazać alert (np. 60 = godzina przed)
- **Tryb alertu**: 
  - `pulse` - pulsujący alert
  - `blink` - migający alert
  - `static` - statyczny alert
- **Kolor alertu**: kolor wyświetlany podczas alertu (np. #ff0000 dla czerwonego)

### 4. Historia odliczeń

Wszystkie ukończone odliczenia są automatycznie zapisywane w historii. Historia zawiera:
- Nazwę odliczenia
- Typ (TO/FROM)
- Datę rozpoczęcia
- Datę zakończenia
- Całkowity czas trwania
- Notatki/status

**Funkcje historii:**
- Sortowanie według różnych kryteriów (data zakończenia, data rozpoczęcia, nazwa, czas trwania)
- Wyświetlanie szczegółowych informacji
- Czyszczenie całej historii

### 5. Zarządzanie odliczeniami

Dialog zarządzania odliczeniami pozwala na:
- **Dodawanie nowych odliczeń**: kliknij "➕ Dodaj nowe"
- **Edycję istniejących**: wybierz odliczenie i kliknij "✏️ Edytuj" lub kliknij dwukrotnie
- **Usuwanie odliczeń**: wybierz odliczenie i kliknij "🗑️ Usuń"
- **Odświeżanie listy**: kliknij "🔄 Odśwież"

## Menu kontekstowe (RMB)

Kliknięcie prawym przyciskiem myszy na ikonie w zasobniku systemowym pokazuje menu:

- **⚙️ Ustawienia** - ustawienia aplikacji (w przygotowaniu)
- **⏱️ Zarządzaj odliczeniami** - otwiera dialog zarządzania odliczeniami
- **📋 Historia odliczeń** - pokazuje historię zakończonych odliczeń
- **🔄 Odśwież dane** - przeładowuje dane z pliku JSON
- **👁️ Widoczność** - zarządzanie widocznością odliczeń (w przygotowaniu)
- **📅 Work Calendar** - kalendarz pracy (w przygotowaniu)
- **📊 Excel Export** - eksport danych do Excel (w przygotowaniu)
- **🔧 Manage Shifts** - zarządzanie zmianami (w przygotowaniu)
- **❌ Zamknij** - zamyka aplikację

## Format daty/czasu

Wszystkie daty i czasy muszą być w formacie:
```
YYYY-MM-DD HH:MM:SS
```

Przykłady:
- `2026-01-23 15:00:00` - 23 stycznia 2026, godzina 15:00
- `2026-07-01 00:00:00` - 1 lipca 2026, północ
- `2026-12-31 23:59:59` - 31 grudnia 2026, godzina 23:59:59

## Plik danych

Dane są przechowywane w pliku `countdowns.json` w tym samym katalogu co aplikacja.

### Struktura pliku:

```json
{
  "countdowns": [
    {
      "id": "unique_id",
      "name": "Nazwa odliczenia",
      "type": "TO",
      "start_datetime": null,
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
      "name": "Zakończone odliczenie",
      "type": "TO",
      "started_at": "2025-12-01 10:00:00",
      "ended_at": "2025-12-23 15:00:00",
      "duration_seconds": 1900800,
      "notes": "Zakończone pomyślnie"
    }
  ]
}
```

### Ręczna edycja

Możesz ręcznie edytować plik `countdowns.json`, ale **pamiętaj**:
1. Zachowaj poprawny format JSON
2. Użyj poprawnego formatu daty/czasu
3. Po edycji wybierz "🔄 Odśwież dane" w menu

## Przykładowe odliczenia

### Przykład 1: Odliczanie do urodzin
```json
{
  "name": "Urodziny Jana",
  "type": "TO",
  "end_datetime": "2026-03-15 18:00:00",
  "enabled": true,
  "show": true,
  "color": "#00ffff",
  "alert_enabled": true,
  "alert_minutes": 1440,
  "alert_mode": "pulse",
  "alert_color": "#ff0000"
}
```
Alert: 1440 minut (24 godziny) przed

### Przykład 2: Dni od rozpoczęcia projektu
```json
{
  "name": "Projekt ABC",
  "type": "FROM",
  "start_datetime": "2026-01-01 09:00:00",
  "enabled": true,
  "show": true,
  "color": "#00ff00",
  "alert_enabled": false
}
```

### Przykład 3: Odliczanie do wakacji
```json
{
  "name": "Wakacje 2026",
  "type": "TO",
  "end_datetime": "2026-07-01 00:00:00",
  "enabled": true,
  "show": true,
  "color": "#ffff00",
  "alert_enabled": true,
  "alert_minutes": 10080,
  "alert_mode": "blink",
  "alert_color": "#ff8800"
}
```
Alert: 10080 minut (7 dni) przed

## Testowanie aplikacji

### Uruchomienie demo
Zamiast uruchamiać pełną aplikację z ikoną systemową, możesz przetestować funkcjonalność za pomocą skryptu demo:

```bash
python demo.py
```

Demo pozwala na:
- Testowanie funkcji przechowywania danych
- Otwieranie dialogów dodawania/edycji odliczeń
- Przeglądanie dialogu zarządzania odliczeniami
- Wyświetlanie historii odliczeń

### Uruchomienie testów jednostkowych
```bash
python test_shift_reminder.py
```

## Rozwiązywanie problemów

### Aplikacja nie uruchamia się
1. Sprawdź czy masz zainstalowane wszystkie zależności: `pip install -r requirements.txt`
2. Sprawdź wersję Pythona: `python --version` (wymagane 3.7+)

### Odliczenia nie są zapisywane
1. Sprawdź uprawnienia do zapisu w katalogu aplikacji
2. Sprawdź czy plik `countdowns.json` nie jest otwarty w innym programie
3. Użyj "🔄 Odśwież dane" aby przeładować dane

### Błędy formatu daty
1. Użyj dokładnego formatu: `YYYY-MM-DD HH:MM:SS`
2. Upewnij się, że data jest poprawna (np. nie ma 32 stycznia)
3. Użyj 24-godzinnego formatu czasu (00:00 do 23:59)

### Ikona nie pojawia się w zasobniku systemowym
1. Aplikacja wymaga systemu Windows
2. Sprawdź czy zasobnik systemowy nie jest ukryty
3. Spróbuj uruchomić jako administrator

## Wsparcie

W razie problemów lub pytań:
1. Sprawdź ten przewodnik
2. Uruchom `python demo.py` aby przetestować funkcjonalność
3. Sprawdź logi aplikacji (wyświetlane w konsoli)
4. Utwórz issue na GitHubie

## Planowane funkcje

Funkcje obecnie w przygotowaniu:
- ⚙️ Rozszerzony dialog ustawień
- 👁️ Zaawansowane zarządzanie widocznością
- 📅 Integracja z kalendarzem pracy
- 📊 Eksport do Excel
- 🔧 Zarządzanie zmianami roboczymi
- 🔔 Rozszerzone opcje powiadomień
- 🎨 Dodatkowe motywy kolorystyczne
