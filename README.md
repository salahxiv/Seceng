# Verwundbare API

## Voraussetzungen
- Python 3.x
- Flask
- Requests

## Installation
1. Abhängigkeiten installieren:
   ```sh
   pip install Flask requests
   ```

2. API starten:
   ```sh
   python app.py
   ```

3. Die API läuft dann auf `http://localhost:5000`.

## Endpunkte

### `/calculate`
- **Methode**: `GET`
- **Beschreibung**: Führt eine Berechnung aus, die den Ressourcenverbrauch erhöhen kann, da die Anzahl der Iterationen unbegrenzt ist.
- **Parameter**:
  - `n` (optional): Anzahl der Iterationen (Standard ist `1000000`).

### `/fetchData`
- **Methode**: `POST`
- **Beschreibung**: Führt eine Anfrage zu einer angegebenen URL aus, anfällig für Server Side Request Forgery (SSRF).
- **Body**:
  ```json
  {
    "url": "<URL>"
  }
  ```

### `/debug`
- **Methode**: `GET`
- **Beschreibung**: Gibt Debug-Informationen aus. Dies zeigt an, dass die Anwendung möglicherweise im Debug-Modus läuft, was ein Sicherheitsrisiko darstellt.

### `/importData`
- **Methode**: `POST`
- **Beschreibung**: Fügt Daten in die Datenbank ein, anfällig für SQL-Injection.
- **Body**:
  ```json
  {
    "data": "<Daten>"
  }
  ```

## Sicherheitsprobleme
Diese API wurde absichtlich entwickelt, um gegen mehrere OWASP API Top 10 Kategorien zu verstoßen:

1. **Unrestricted Resource Consumption**: Die `/calculate`-Route erlaubt eine große Anzahl von Iterationen, was die Ressourcen des Servers erschöpfen kann.
2. **Server Side Request Forgery (SSRF)**: Die `/fetchData`-Route akzeptiert beliebige URLs, was es einem Angreifer ermöglicht, interne Server zu scannen.
3. **Security Misconfiguration**: Die Anwendung läuft im Debug-Modus, was Sicherheitsinformationen preisgeben kann.
4. **Unsafe Consumption of APIs**: Die `/importData`-Route ist anfällig für SQL-Injection, da die Benutzereingabe direkt in die Datenbankabfrage eingefügt wird.

## Hinweise
Diese API ist nur zu Demonstrationszwecken und sollte nicht in einer Produktionsumgebung verwendet werden, da sie erhebliche Sicherheitslücken enthält.

## Testen der API
Um die API zu testen, können verschiedene Tools wie `curl`, Postman oder ein Browser verwendet werden. Nachfolgend sind einige Beispiele aufgeführt, wie die einzelnen Endpunkte getestet werden können:

### `/calculate` testen
- **Postman**:
  - **Methode**: `GET`
  - **URL**: `http://localhost:5000/calculate?n=1000000`
  - **Erwartete Ausgabe**: Eine JSON-Antwort mit dem Berechnungsergebnis (`{"result": 499999500000}` bei `n=1000000`).

### `/fetchData` testen
- **Postman**:
  - **Methode**: `POST`
  - **URL**: `http://localhost:5000/fetchData`
  - **Body** (RAW, JSON):
    ```json
    {
      "url": "http://example.com"
    }
    ```
  - **Erwartete Ausgabe**: Der Inhalt der angegebenen URL, z. B. HTML-Code der Seite `http://example.com`. Wenn eine interne URL angegeben wird, könnte das eine Sicherheitslücke offenbaren.

### `/debug` testen
- **Postman**:
  - **Methode**: `GET`
  - **URL**: `http://localhost:5000/debug`
  - **Erwartete Ausgabe**: Eine Nachricht, dass der Debug-Modus aktiviert ist (`"Debug mode is on!"`). Dies zeigt an, dass die Anwendung möglicherweise im unsicheren Debug-Modus läuft.

### `/importData` testen
- **Postman**:
  - **Methode**: `POST`
  - **URL**: `http://localhost:5000/importData`
  - **Body** (RAW, JSON):
    ```json
    {
    "data": "testdata'); DROP TABLE data; --"
    }

    ```
  - **Erwartete Ausgabe**: Eine Bestätigung, dass die Daten eingefügt wurden (`"Data inserted!"`). Bei Verwendung von schädlichen Daten, wie oben gezeigt, könnte dies zu einer SQL-Injection führen, die die Datenbank manipuliert (z. B. Löschen der Tabelle `data`).

## Zusammenfassung der erwarteten Ausgaben
- **`/calculate`**: JSON mit dem Ergebnis der Berechnung.
- **`/fetchData`**: Inhalt der angegebenen URL, als JSON zurückgegeben.
- **`/debug`**: Eine einfache Textnachricht, die den Debug-Modus bestätigt.
- **`/importData`**: Bestätigungsnachricht, dass die Daten eingefügt wurden, was bei schädlichen Eingaben zu einer SQL-Injection führen könnte.
