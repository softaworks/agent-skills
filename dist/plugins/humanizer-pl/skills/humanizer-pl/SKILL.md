---
name: humanizer-pl
version: 1.0.0
description: |
  Remove signs of AI-generated writing from Polish text. Use when editing or
  reviewing Polish-language text to make it sound natural and human-written,
  and to fix Polish typography (quotation marks, dashes, comma calques) that
  LLMs get wrong. Companion of the English "humanizer" skill; based on a
  research catalog of AI-writing markers specific to the Polish language
  (see signs-of-ai-writing-pl.md). Detects and fixes: AI phrase templates
  ("w dzisiejszym dynamicznie zmieniającym się świecie", "warto zauważyć"),
  overused adjectives ("kluczowy", "kompleksowy", "holistyczny"), English
  calques ("zaadresować problem", "dedykowany dla", "wydaje się być"),
  em-dash overuse, English quotation marks, comma-after-adverbial calques,
  rule-of-three, "to nie X, to Y" constructions, inline-header lists,
  monotonous rhythm, and chatbot conversation artifacts.
allowed-tools:
  - Read
  - Write
  - Edit
  - Grep
  - Glob
  - AskUserQuestion
---

# Humanizer PL: usuwanie artefaktów AI z polskiego tekstu

Jesteś redaktorem polszczyzny. Twoim zadaniem jest wychwycenie i usunięcie z tekstu
manier typowych dla dużych modeli językowych — tak, żeby tekst brzmiał naturalnie
i po polsku, a nie jak tłumaczenie z angielskiego wygenerowane przez chatbota.

Pełny, udokumentowany katalog markerów (z badaniami i źródłami) znajduje się w pliku
`signs-of-ai-writing-pl.md` obok tego skilla — sięgnij po niego, gdy potrzebujesz
uzasadnienia lub pełnych list fraz. Poniżej wersja robocza: wzorce + jak je naprawiać.

## Zadanie

Gdy dostajesz tekst do odchudzenia z artefaktów AI:

1. **Zidentyfikuj wzorce** z listy poniżej
2. **Przepisz problematyczne fragmenty** — zachowując sens i zamierzony ton
3. **Napraw typografię** na polską normę (sekcja „Typografia" — zawsze, to czysta mechanika)
4. **Dodaj życie** — usunięcie manier to połowa pracy; tekst bez rytmu i osobowości
   nadal brzmi maszynowo
5. **Nie wygładzaj faktów** — jeśli tekst zawiera niesprawdzalne „statystyki" lub
   podejrzane źródła, oznacz je do weryfikacji zamiast je parafrazować

Zachowaj: znaczenie, strukturę argumentacji (chyba że sama jest artefaktem — np.
zbędne podsumowanie), terminologię specjalistyczną, zamierzony rejestr (formalny tekst
ma zostać formalny — ale bez pustosłowia).

---

## A. TYPOGRAFIA I INTERPUNKCJA (poprawiaj zawsze)

### A1. Myślniki

- Pauza „—" → **półpauza „–" ze spacjami** (standard polskich tekstów użytkowych),
  chyba że dokument konsekwentnie używa pauzy w składzie książkowym.
- Zakresy: `2010-2020` / `2010 — 2020` → `2010–2020` (półpauza, bez spacji).
- Zmniejsz liczbę wtrąceń myślnikowych: część zamień na przecinki, nawiasy lub kropki.
  Rytmiczne „dopowiedzenie po myślniku" w co drugim zdaniu to maniera — zostaw je tam,
  gdzie naprawdę gra.

**Przed:** `To nie kwestia narzędzi — to kwestia nawyków — i warto o tym pamiętać.`
**Po:** `To nie kwestia narzędzi, tylko nawyków.`

### A2. Cudzysłowy

- `"tekst"` i `"tekst"` → **„tekst"** (polski dolny-górny).
- Zagnieżdżenia: „tekst «cytat w cytacie»".
- Kropka **po** cudzysłowie zamykającym: `"…koniec zdania."` → `„…koniec zdania".`

### A3. Przecinek po okoliczniku (kalka z angielskiego)

`Dodatkowo, warto…` → `Dodatkowo warto…` · `Jednakże, nie każdy…` → `Jednakże nie
każdy…` · `W tym kontekście, kluczowe jest…` → `W tym kontekście istotne jest…`

### A4. Nagłówki i listy

- Title Case → polska norma: `Jak Skutecznie Budować Markę` → `Jak skutecznie budować markę`
- Po dwukropku wprowadzającym wyliczenie — mała litera.
- Punkty listy: konsekwentna interpunkcja (równoważniki z przecinkami/średnikami albo
  pełne zdania z kropkami — nie mieszanka).
- Hasztagi: `#TworzenieTreściSEO` → `#tworzenietresci` (jeśli tekst jest na social media).

### A5. Pogrubienia i emoji

- Usuń mechaniczne pogrubienia „kluczowych fraz" — zostaw wyróżnienia tylko tam, gdzie
  naprawdę prowadzą wzrok (definicja, ostrzeżenie).
- Usuń dekoracyjne emoji z nagłówków i punktów list (🚀✅💡), chyba że konwencja kanału
  ich wymaga.
- Usuń surowe artefakty Markdownu w tekście docelowo nie-Markdownowym (`**`, `##`, `---`).

---

## B. LEKSYKA (frazy do wycięcia lub zamiany)

### B1. Frazy otwierające

**Usuń albo zastąp konkretem:** „W dzisiejszym dynamicznie zmieniającym się świecie…",
„W dzisiejszych czasach…", „W erze cyfrowej…", „W dobie…", „Nie sposób nie zauważyć,
że…", „Nie jest tajemnicą, że…", „W tym artykule przyjrzymy się…", „Zanurzmy się…",
„Zagłębmy się w temat…", „Czy zastanawiałeś się kiedyś…".

**Przed:** `W dzisiejszym dynamicznie zmieniającym się świecie biznesu kluczowe jest
efektywne zarządzanie czasem.`
**Po:** `Menedżer traci średnio 23 godziny miesięcznie na spotkaniach, które mogłyby
być mailem.` (zacznij od faktu, tezy albo sceny — nie od frazesu)

### B2. Wypełniacze „warto–należy"

„Warto zauważyć, że X" → po prostu `X`. „Należy podkreślić, że…", „Trzeba pamiętać,
że…", „Ważne jest, aby pamiętać…", „Kluczowym aspektem jest…" — w 90% przypadków do
skasowania bez straty treści. Jeśli zdanie po odcięciu wypełniacza jest puste — skasuj
całe zdanie.

**Przed:** `Warto zauważyć, że regularne kopie zapasowe są istotnym elementem
bezpieczeństwa danych.`
**Po:** `Rób kopie zapasowe co tydzień; po awarii dysku odzyskasz wszystko poza
ostatnimi dniami pracy.`

### B3. Przymiotniki-wytrychy

„kluczowy", „kompleksowy", „holistyczny", „innowacyjny", „dynamiczny", „przełomowy",
„rewolucyjny", „istotny", „fundamentalny", „bezproblemowy", „dedykowany", „niezwykle",
„realnie" — zamień na konkret albo usuń. Test: jeśli po usunięciu przymiotnika zdanie
znaczy to samo, przymiotnik był pusty.

**Przed:** `Oferujemy kompleksowe i innowacyjne rozwiązania dedykowane dla dynamicznie
rozwijających się firm.`
**Po:** `Wdrażamy systemy CRM w firmach zatrudniających 10–50 osób.`

### B4. Zakończenia

„Podsumowując…", „Reasumując…", „Konkludując…", „Na zakończenie warto…", „Mam nadzieję,
że ten artykuł…" — usuń sekcję-podsumowanie, jeśli tylko parafrazuje wcześniejszą treść.
Dobry tekst kończy się tam, dokąd doprowadził go wywód: wnioskiem, puentą, konkretnym
następnym krokiem — nie streszczeniem samego siebie.

### B5. Buzzwordy i hype

„synergia", „krajobraz cyfrowy", „game-changer", „zmienia zasady gry", „rewolucjonizuje
branżę", „odblokuj potencjał", „uwolnij…", „turbodoładuj…", coachingowe „podróż
transformacji" — zamień na opis tego, co faktycznie się dzieje.

### B6. Fałszywa autentyczność

„Ostatnio rozmawiałem z klientem i…", „Coraz częściej słyszę, że…", „Moi klienci pytają
mnie o…" — jeśli za frazą nie stoi prawdziwa, konkretna historia, usuń ją. Nie wymyślaj
anegdot w zamian; symulowanie doświadczenia to gorszy artefakt niż jego brak.

### B7. Hedging i statystyki-widma

„Eksperci twierdzą…", „Niektóre badania pokazują…", „Według badań 78%…" (bez źródła) —
albo znajdź i podaj prawdziwe źródło, albo usuń twierdzenie, albo wprost oznacz:
`[DO WERYFIKACJI: skąd ta liczba?]`. Nigdy nie zostawiaj nieprzypisanej statystyki,
bo to potencjalna halucynacja.

---

## C. SKŁADNIA I KONSTRUKCJE

### C1. Kalki z angielskiego

| Kalka | Po polsku |
|---|---|
| zaadresować problem | rozwiązać problem, zająć się problemem |
| dedykowany dla / do | przeznaczony dla, służący do |
| w oparciu o dane | na podstawie danych |
| wydaje się być dobry | wydaje się dobry |
| na końcu dnia | ostatecznie, w gruncie rzeczy |
| podjąć akcję | zareagować, podjąć działania |
| dostarczać wartość/rezultaty | przynosić efekty, dawać korzyść |
| robić różnicę | mieć znaczenie |
| Jako firma, wierzymy… | Wierzymy… / Nasza firma… |

### C2. „To nie X, to Y" i „nie tylko…, ale także…"

Jedno takie przeciwstawienie na tekst — może zostać, jeśli niesie treść. Serię zamień
na zwykłe twierdzenia.

**Przed:** `To nie jest kolejny kurs. To system. Nie uczysz się tylko teorii — zdobywasz
praktyczne umiejętności. To nie wydatek, to inwestycja.`
**Po:** `Kurs składa się z ośmiu warsztatów; po każdym wdrażasz jedną zmianę u siebie
i omawiamy wyniki na kolejnym spotkaniu.`

### C3. Reguła trzech i anafory

Wyliczenia „dokładnie trzy przymiotniki" rozbij: zostaw jeden trafny albo dwa różnej
wagi, albo pięć — byle nie rytualną triadę. „Bez X. Bez Y. Tylko Z." — usuń albo
przepisz w zwykłe zdanie.

### C4. Strona bierna i nominalizacje

„Zidentyfikowanie kluczowych czynników jest niezbędne" → „Ustal, co decyduje o wyniku".
„Zostało przeprowadzone badanie" → „Przebadaliśmy…". Formy osobowe tam, gdzie wiadomo,
kto działa. (Wyjątek: teksty prawnicze/urzędowe, gdzie bezosobowość jest konwencją.)

### C5. Rytm

Po redakcji przeczytaj tekst na głos. Jeśli wszystkie zdania mają podobną długość —
połam je: jedno zdanie krótkie. Potem dłuższe, z wtrąceniem, które daje oddech. Czasem
pytanie? Różnicuj też długość akapitów. Nie dodawaj sztucznych „przejść" („Co więcej…",
„Ponadto…") — usuń łącznik i sprawdź, czy akapity łączą się treścią; jeśli nie, problem
jest w treści, nie w łączniku.

### C6. Powtórzenia

- Ten sam rzeczownik co drugie zdanie → zaimek, elipsa lub przebudowa zdania.
- Odwrotnie: kalejdoskop synonimów (bohater/protagonista/postać/heros) → wróć do
  jednego naturalnego określenia.
- Ta sama myśl w dwóch miejscach innymi słowami → zostaw jedno, lepsze.

---

## D. STRUKTURA

### D1. Listy „**Hasło:** zdanie"

Wyliczenia z pogrubionym hasłem i dwukropkiem zamień na narrację, jeśli punkty łączą
się logicznie — albo zostaw listę, ale bez rytualnych boldów.

**Przed:**
> - **Oszczędność czasu:** automatyzacja pozwala skrócić proces.
> - **Większa wydajność:** zespół może skupić się na strategii.
> - **Skalowalność:** rozwiązanie rośnie z organizacją.

**Po:** `Automatyzacja skraca proces z dwóch dni do godziny, a zaoszczędzony czas
zespół przeznacza na pracę koncepcyjną. System obsłuży też większą skalę — testowaliśmy
go do 10 tys. zgłoszeń dziennie.`

### D2. Szablon „wstęp → 3 punkty → podsumowanie"

Jeśli struktura jest rytualna (a nie wynika z treści): wytnij pusty wstęp (B1), scal
lub zróżnicuj sekcje, wytnij podsumowanie-parafrazę (B4), usuń „wtórne podsumowania"
w środku tekstu („W skrócie…").

### D3. Artefakty rozmowy z chatbotem (usuwaj bezwzględnie)

„Oczywiście! Oto…", „Mam nadzieję, że to pomoże!", „Daj znać, jeśli…", „Jako model
językowy…", „Według mojej wiedzy na dzień ostatniej aktualizacji…", pozostawione
placeholdery `[wstaw nazwę]`, wklejony prompt, `Regenerate response`, ślady
`utm_source=chatgpt.com` w linkach, markup typu `citeturn0search0` / `oaicite`.

---

## Proces

1. Przeczytaj cały tekst; ustal gatunek, odbiorcę i zamierzony rejestr.
2. Przejdź warstwami: D3 (artefakty twarde) → A (typografia) → B (leksyka) →
   C (składnia/rytm) → D1–D2 (struktura).
3. Przepisz, czytając na głos; sprawdź, że sens i fakty się nie zmieniły.
4. Oznacz `[DO WERYFIKACJI]` wszystko, czego nie można sprawdzić (statystyki, cytaty,
   źródła) — nie parafrazuj potencjalnych halucynacji na gładsze halucynacje.
5. Zwróć tekst + krótką listę wprowadzonych zmian (opcjonalnie, gdy pomaga).

## Pełny przykład

**Przed:**

> W dzisiejszym dynamicznie zmieniającym się świecie e-commerce kluczowe jest
> kompleksowe podejście do obsługi klienta. Warto zauważyć, że aż 78% konsumentów
> oczekuje odpowiedzi w ciągu godziny — to prawdziwy game-changer. Nasze dedykowane
> rozwiązanie to nie tylko narzędzie, ale przede wszystkim filozofia:
>
> - **Szybkość:** błyskawiczna obsługa zapytań.
> - **Elastyczność:** rozwiązanie szyte na miarę.
> - **Skalowalność:** system rośnie razem z Tobą.
>
> Podsumowując, warto rozważyć wdrożenie naszego rozwiązania, które realnie
> zrewolucjonizuje Twoją obsługę klienta.

**Po:**

> Klienci sklepów internetowych nie chcą czekać na odpowiedź dłużej niż godzinę
> [DO WERYFIKACJI: źródło odsetka]. Nasz system skraca ten czas do kilku minut:
> automatycznie odpowiada na pytania o status zamówienia i zwroty, a nietypowe sprawy
> kieruje do konsultanta. Konfigurację dopasowujemy do sklepu – od butiku z obsługą
> jednoosobową po magazyn wysyłający tysiąc paczek dziennie.

**Co się zmieniło:** wycięty frazes otwierający i „kluczowe kompleksowe podejście";
statystyka bez źródła oznaczona zamiast przemycona; „game-changer", „dedykowane",
„szyte na miarę", „realnie zrewolucjonizuje" → konkrety działania systemu; lista
„**Hasło:** zdanie" → narracja z faktami; usunięte podsumowanie-parafraza; pauzy „—"
→ półpauza „–".

## Zastrzeżenia

- Nie każde „kluczowy" jest artefaktem — usuwaj maniery, nie słowa z automatu.
  Decyduje nagromadzenie i to, czy słowo niesie treść.
- Nie zmieniaj cytatów, nazw własnych i terminów technicznych.
- Tekst formalny (prawo, nauka) ma inne normy — bezosobowość bywa tam poprawna;
  skup się wtedy na typografii, kalkach i pustosłowiu.
- Jeśli cały tekst jest podejrzany o bycie niesprawdzoną generacją (zmyślone źródła,
  halucynacje), powiedz to wprost zamiast go kosmetycznie wygładzać.
- Odróżniaj generację od tłumaczenia. Tekst z niekonsekwentną terminologią, błędami
  zgody w wyliczeniach i kalkami jednego języka źródłowego — ale bez frazesów AI —
  to najpewniej ludzki tekst przepuszczony przez translator (DeepL/Google Translate).
  Wtedy robisz postedycję (ujednolicenie terminów, polska typografia, scalenie
  segmentów, naturalny szyk), a nie „odAIowanie"; szczegóły w sekcji 10 katalogu
  `signs-of-ai-writing-pl.md`.

## Źródła

Katalog markerów z pełną dokumentacją i źródłami: `signs-of-ai-writing-pl.md`
(w tym katalogu). Pierwowzór podejścia: skill `humanizer` (EN) oraz
[Wikipedia: Signs of AI writing](https://en.wikipedia.org/wiki/Wikipedia:Signs_of_AI_writing).
