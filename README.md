Projekt - Porównywarka Cen Gier

Aplikacja webowa stworzona we Flasku, umożliwiająca porównywanie cen cyfrowych gier komputerowych z różnych sklepów internetowych. 
Projekt zawiera system kont użytkowników, historię wyszukiwań oraz ulubione gry.

* Technologie:

  - Python + Flask
  - HTML + CSS
  - SQLite-baza danych
  - CheapShark API
  - API Narodowego Banku Polskiego

* Działanie aplikacji

1. Strona główna
  - Użytkownik wpisuje tytuł gry i klika "Szukaj".
  - Aplikacja wyświetla listę wyników zawierających:
    - miniaturę gry,
    - najniższą cenę w USD i przeliczoną na PLN według kursu na dany dzień,
    - przycisk "Zobacz szczegóły"

2. Szczegóły gry
  - Pokazywane są wszystkie dostępne oferty gry z różnych sklepów.
  - Najtańsza oferta jest podświetlona na zielono.
  - Oferty zawierają:
    - cenę w USD i PLN,
    - nazwę sklepu i logo,
    - link przekierowujący do zakupu gry

3. Rejestracja i logowanie
  - Po rejestracji użytkownik może się zalogować.
  - Po zalogowaniu:
    - na stronie pojawia się komunikat "Jesteś zalogowany",
    - użytkownik może zapisywać ulubione gry,
    - zapisywana jest historia jego wyszukiwań

4. Ulubione gry
  - Zalogowani użytkownicy mogą dodawać gry do listy ulubionych.
  - Lista jest dostępna z poziomu menu

5. Historia wyszukiwań
  - Aplikacja zapisuje historię zapytań użytkownika wraz z datą (użytkownicy zalogowani)

* Obsługiwane sklepy (CheapShark API)

  - Steam
  - Epic Games Store
  - GOG
  - GreenManGaming
  - Humble Store
  - Fanatical
  - EA (dawniej Origin)
  - Uplay
  - Blizzard Shop
  - GamesPlanet
  - GamersGate
  - Amazon
  - Direct2Drive
  - GameBillet
  - 2Game
  - WinGameStore
  - Voidu
  - AllYouPlay
  - Gamesload

* Przelicznik cen do PLN

  CheapShark API zwraca ceny w USD. Aby przeliczyć ceny na polskie złote:
  - Aplikacja korzysta z oficjalnego API NBP:
  https://api.nbp.pl/api/exchangerates/rates/A/USD/?format=json

  - Dzięki temu każda cena ma przybliżoną wartość w PLN.
  - Ceny przeliczane mogą różnić się od tych w sklepach (bo sklepy stosują własne przeliczniki lub lokalne promocje).

* Niestety nie mogłam użyć bezpośrednio API Steam/GOG/Epic itp.

  - Sklepy te nie udostępniają publicznego API lub mają bardzo ograniczony dostęp.
  - Steam wymaga ID gry (AppID) i dodatkowej konfiguracji.
  - Epic Games i GOG nie oferują otwartego API do porównywania cen.

* By rozwiązać ten problem użyłam CheapShark API, które:

  - gromadzi dane z wielu sklepów,
  - jest darmowe,
  - nie wymaga autoryzacji,
  - jest łatwe w użyciu
