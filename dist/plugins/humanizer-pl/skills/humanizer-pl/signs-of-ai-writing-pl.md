# Oznaki pisania AI w języku polskim

Katalog manier, fraz i błędów typowych dla polszczyzny generowanej przez duże modele
językowe (ChatGPT, Claude, Gemini i inne) — polski odpowiednik wikipediowego przewodnika
[Signs of AI writing](https://en.wikipedia.org/wiki/Wikipedia:Signs_of_AI_writing).
Część markerów to adaptacja obserwacji z angielskiego pierwowzoru (struktura dokumentu
i markery uniwersalne — CC BY-SA 4.0, WikiProject AI Cleanup), ale trzon zebrano
z polskich źródeł: dyskusji polskich wikipedystów, badań językoznawczych nad polszczyzną
LLM-ów, polskich poradników copywriterskich i SEO, opisów detektorów, obserwacji
nauczycieli i egzaminatorów oraz polskich mediów społecznościowych. Pełna lista źródeł
znajduje się na końcu.

Ta lista jest **opisowa, nie normatywna** — to katalog obserwacji, nie zbiór zakazów.
Żaden pojedynczy marker niczego nie dowodzi: modele uczyły się na ludzkim piśmie, więc
każdą z tych manier można znaleźć także u ludzi (copywriterzy SEO pisali „w dzisiejszych
czasach" na długo przed ChatGPT). Znaczenie ma **nagromadzenie** — jedna fraza to nic,
pięć w jednym akapicie to czerwona flaga. Najmocniejsze są markery „twarde" (zmyślone
źródła, ślady interfejsu czatu, `utm_source=chatgpt.com`), najsłabsze — pojedyncze słowa.

Uwaga praktyczna: automatyczne detektory AI radzą sobie z polszczyzną **gorzej niż
z angielskim** (osobna sekcja niżej) i bywają rażąco niezgodne między sobą. Zanim
oskarżysz kogoś o użycie AI, przeczytaj sekcję „Nieskuteczne wskaźniki".

---

## 1. Regresja do średniej: co model robi z treścią

LLM przewiduje statystycznie najbardziej prawdopodobny ciąg dalszy — wynik dąży do
środka rozkładu: ogólnikowy, wygładzony, pasujący do możliwie wielu tematów naraz.
Konkretny fakt („konstruktor pierwszego sprzęgu wagonowego") zamienia się w generyczny
panegiryk („wizjoner, który odcisnął trwałe piętno na branży"). Temat robi się
jednocześnie **mniej konkretny i bardziej doniosły**.

### 1.1. Pompowanie ważności i „szerszego kontekstu"

**Frazy do obserwacji:** _odgrywa kluczową rolę_, _ma kluczowe znaczenie_, _stanowi
istotny element_, _podkreśla znaczenie_, _wpisuje się w szerszy kontekst/trend_,
_odzwierciedla szersze zjawisko_, _pozostawił trwały ślad/dziedzictwo_, _świadczy
o bogatej historii_, _cieszy się dużym zainteresowaniem_, _stanowi ważny punkt na
mapie_...

Model dokleja do najzwyklejszych faktów deklaracje ich doniosłości i związki
z „szerszym obrazem" — nawet przy tematach tak przyziemnych jak etymologia nazwy wsi
albo dane demograficzne gminy.

> Założenie zakładu w 1962 roku stanowiło przełomowy moment w rozwoju regionu,
> odzwierciedlając szersze procesy industrializacji Polski. Fabryka odgrywała kluczową
> rolę w kształtowaniu lokalnej tożsamości, a jej dziedzictwo pozostaje żywe do dziś.

Po ludzku: fabryka produkowała meble, zatrudniała 400 osób, zamknięto ją w 1994 roku.

### 1.2. Powierzchowne analizy doklejane imiesłowem

**Frazy do obserwacji:** _podkreślając…_, _ukazując…_, _odzwierciedlając…_,
_przyczyniając się do…_, _wzmacniając…_, _budując…_, _co podkreśla…_, _co świadczy o…_,
_co czyni go…_

Ulubiony ruch modelu: do zdania z faktem dokleić na końcu frazę imiesłowową („-ąc")
z pseudownioskiem. Badanie gramatyki LLM-ów ([Reinhart i in., PNAS
2025](https://www.pnas.org/doi/10.1073/pnas.2422455122)) pokazuje, że modele używają
konstrukcji imiesłowowych **2–5 razy częściej niż ludzie**. Sygnał jest najmocniejszy,
gdy podmiotem „podkreślania" jest rzecz lub fakt — fakt niczego nie podkreśla, to
narrator dopisuje mu intencję.

> Rynek otaczają kamienice z XVIII wieku, odzwierciedlając bogatą historię miasta
> i podkreślając jego wyjątkowy charakter na tle regionu.

### 1.3. Ton promocyjny i reklamowy

**Frazy do obserwacji:** _tętniący życiem_, _malowniczo położony_, _w sercu…_,
_urzekający_, _wyjątkowy_, _niepowtarzalny klimat_, _bogata oferta_, _szeroki wachlarz_,
_zapierający dech w piersiach_, _prawdziwa perła_, _raj dla…_

Model z trudem utrzymuje neutralny ton, zwłaszcza przy tematach „dziedzictwa
kulturowego", turystyki i firm — tekst informacyjny zjeżdża w stronę folderu
reklamowego. Badania korpusowe potwierdzają pozytywny bias afektywny tekstu LLM
(więcej „radości", mniej emocji negatywnych — [Muñoz-Ortiz i in.
2024](https://arxiv.org/abs/2308.09067)).

> Kazimierz Dolny to prawdziwa perła renesansu, malowniczo położona w sercu Małopolskiego
> Przełomu Wisły. To wyjątkowe miasteczko urzeka niepowtarzalnym klimatem i tętni życiem
> przez cały rok, oferując odwiedzającym szeroki wachlarz atrakcji.

### 1.4. Dydaktyczne wtręty i disclaimery

**Frazy do obserwacji:** _warto pamiętać, że…_, _należy jednak zauważyć…_, _co istotne…_,
_ważne jest, aby zrozumieć…_, _nie można zapominać…_, _może się różnić w zależności od…_

Model poucza czytelnika, o czym „warto pamiętać", i asekuruje się zastrzeżeniami — także
tam, gdzie nikt o poradę nie prosił.

> Warto jednak pamiętać, że każda sytuacja jest inna i przed podjęciem decyzji należy
> skonsultować się ze specjalistą. Ważne jest, aby zrozumieć, że opisane zasady mogą
> się różnić w zależności od konkretnego przypadku.

### 1.5. Obowiązkowe podsumowania

**Frazy do obserwacji:** _Podsumowując…_, _Reasumując…_, _Konkludując…_, _W skrócie…_,
_Ogólnie rzecz biorąc…_, _Na zakończenie warto…_, _Podsumowując, można stwierdzić, że…_

Dłuższy tekst niemal zawsze dostaje sekcję „Podsumowanie", a akapity — zdania zamykające,
które przeformułowują to, co już padło („Dzięki temu…", „Co ostatecznie prowadzi do…").
Zakończenie zwykle nie wnosi żadnej nowej informacji: to parafraza środka tekstu, często
zwieńczona okrągłym frazesem o przyszłości, współpracy albo „potrzebie dalszej refleksji".

> Podsumowując, wybór odpowiedniego rozwiązania zależy od indywidualnych potrzeb.
> Warto więc dokładnie przeanalizować dostępne opcje, aby podjąć świadomą decyzję,
> która przyniesie wymierne korzyści w dłuższej perspektywie.

### 1.6. Sekcja „Wyzwania i perspektywy"

Schemat rodem z wypracowania: „Mimo licznych sukcesów X stoi przed wyzwaniami, takimi
jak…", po czym następuje zwrot optymistyczny („Mimo tych wyzwań… dalszy dynamiczny
rozwój"). Sygnałem jest sztywna formuła, nie samo wspominanie o problemach.

> Mimo dynamicznego rozwoju gmina stoi przed wyzwaniami typowymi dla obszarów wiejskich,
> takimi jak odpływ młodych mieszkańców i starzenie się społeczeństwa. Mimo tych wyzwań,
> dzięki strategicznemu położeniu i planowanym inwestycjom, gmina ma szansę na dalszy
> zrównoważony rozwój.

---

## 2. Leksyka: polski słownik AI

Najlepiej udokumentowana warstwa. Polskie poradniki, skanery fraz i detektory zgodnie
wskazują powtarzalny repertuar — poniższe frazy pojawiają się na wielu niezależnych
listach (m.in. [skaner ~120 fraz Jacka
Wolniewicza](https://jacekwolniewicz.pl/skaner-po-polsku-ktory-lapie-120-fraz-naduzywanych-przez-ai/),
[detektor KrupińskiAI](https://krupinskiai.pl/apps/ai-detektor) z bazą 50+ zwrotów,
[przewodnik po „GPT-izmach"](https://dbest-content.com/jak-rozpoznac-tekst-z-ai-kompletny-przewodnik-po-gpt-izmach/),
[poradnik Fundacji Orange](https://pracownieorange.pl/inspiration/jak-rozpoznac-tekst-napisany-przez-ai-praktyczny-przewodnik/)).
Pojedyncze wystąpienie nie znaczy nic; liczy się zagęszczenie i współwystępowanie.

### 2.1. Frazy otwierające

Najbardziej rozpoznawalna sygnatura polskiego tekstu AI — wariacje „w dzisiejszym…
świecie":

- **W dzisiejszym dynamicznie zmieniającym się świecie…** (i warianty: _w dzisiejszym
  dynamicznym świecie_, _w dynamicznie zmieniającym się krajobrazie cyfrowym_)
- **W dzisiejszych czasach…** / _W obecnych czasach…_ / _W obecnej rzeczywistości…_
- **W erze cyfrowej…** / _W dobie cyfryzacji…_ / _w dobie pędzącej technologii…_
- **W tym artykule przyjrzymy się…** / _W poniższym artykule omówimy…_
- **Nie sposób nie zauważyć, że…** / _Nie jest tajemnicą, że…_
- **Czy zastanawiałeś się kiedyś, …?** / _Wiele osób zadaje sobie pytanie…_
- **Zanurzmy się…** / _Zagłębmy się w temat…_ / _Przyjrzyjmy się bliżej…_ /
  _Witamy w świecie…_ (polskie wcielenia angielskiego „let's delve into")

> W dzisiejszym dynamicznie zmieniającym się świecie kluczowe jest wdrożenie
> odpowiednich strategii, które pozwolą na optymalizację procesów.

Zdanie jak wyżej mogłoby otwierać tekst o księgowości, ogrodnictwie i hodowli alpak —
i to jest jego cecha rozpoznawcza.

### 2.2. Wypełniacze „warto–należy"

Najczęściej cytowana pojedyncza fraza polskiego tekstu AI: **„Warto zauważyć, że…"**.
Rodzina jest liczna:

- _warto zauważyć / podkreślić / zaznaczyć / pamiętać / wspomnieć / rozważyć_
- _należy zauważyć / podkreślić / pamiętać / mieć na uwadze_
- _trzeba pamiętać, że…_, _nie można zapominać, że…_, _nie sposób pominąć faktu, że…_
- _ważne jest, aby pamiętać…_, _kluczowym aspektem jest…_, _istotnym elementem jest…_
- _w praktyce oznacza to, że…_, _mając na uwadze powyższe…_

Samo „warto" bywa nazywane słowem-wydmuszką: pozwala nic nie stwierdzić wprost
i uniknąć odpowiedzialności za tezę.

### 2.3. Łączniki międzyzdaniowe

_Co więcej…_, _Ponadto…_, _Dodatkowo, …_ (z kalkowym przecinkiem — patrz sekcja 4.4),
_Co ciekawe…_, _W istocie…_, _W kontekście…_, _Na podstawie dostępnych danych…_,
_To prowadzi nas do wniosku, że…_, _Oto…_ („Oto kilka kluczowych aspektów związanych
z…" — samo „oto" potrafi wystąpić kilkanaście razy w jednym tekście).

Charakterystyczny jest nie pojedynczy łącznik, lecz ich **mechaniczna regularność**:
przejścia formalnie są, ale nie niosą faktycznego mostu logicznego między akapitami.

### 2.4. Przymiotniki-wytrychy

Polskie odpowiedniki angielskich „AI words" (crucial, comprehensive, robust, seamless…):

- **kluczowy** — najczęściej wymieniane pojedyncze słowo-marker polszczyzny AI
  (_kluczowy element/aspekt_, _kluczowe znaczenie_, _odgrywa kluczową rolę_)
- **kompleksowy** (_kompleksowe podejście/rozwiązanie_), **holistyczny** (_holistyczne
  podejście_, _holistyczna perspektywa_)
- **innowacyjny**, **dynamiczny**, **rewolucyjny**, **przełomowy**, **transformacyjny**
- **istotny**, _niezwykle istotny_, **fundamentalny**, **wielowymiarowy**,
  **wieloaspektowy**
- **bezproblemowy** (kalka „seamless"), **solidny** (kalka „robust"), **szyty na miarę**
  (kalka „tailor-made"), **dedykowany** (kalka „dedicated" — patrz 3.1)
- **niezawodny**, **wyjątkowy**, **fascynujący**, **niezwykły**, _tętniący życiem_
  (kalka „vibrant")
- nadużywane przysłówki: _niezwykle_, _niesamowicie_, _skrupulatnie_ (kalka
  „meticulously"), _realnie_ („To realnie wpływa na wyniki")

W badaniach anglojęzycznych ta warstwa jest twardo policzona: po 2023 roku częstość słów
typu „delves" wzrosła kilkudziesięciokrotnie, a nadwyżkowe słownictwo w abstraktach
naukowych to niemal wyłącznie „słowa stylu" ([Kobak i in., Science Advances
2025](https://www.science.org/doi/10.1126/sciadv.adt3813); [Juzek & Ward, COLING
2025](https://aclanthology.org/2025.coling-main.426/)). Modele piszące po polsku kalkują
ten sam repertuar.

### 2.5. Rzeczowniki-buzzwordy i metafory

_synergia_, _krajobraz_ (cyfrowy, biznesowy, medialny — kalka „landscape"), _era
cyfrowa_, _ekosystem_ (poza biologią), _potencjał_ (zwłaszcza „ukryty" i „pełny"),
_game-changer_ (żywcem z angielskiego), _fundament każdego biznesu_.

### 2.6. Czasowniki marketingowo-entuzjastyczne

_rewolucjonizuje branżę_, _transformuje_, _odblokuj / uwolnij (potencjał)_, _odkryj…_,
_zapomnij o…_, _zmienia zasady gry_, _otwiera drzwi do nowych możliwości_,
_turbodoładuj…_, _dzięki zaawansowanej technologii…_, przedrostek _ultra-_.

### 2.7. Coachingowa nowomowa

_Uwolnij swój wewnętrzny potencjał_, _Odkryj autentyczną wersję siebie_, _Wyrusz
w podróż transformacji_, _Przepracuj limitujące przekonania_, _Wejdź na wyższy poziom_,
_Zbuduj abundance mindset_.

### 2.8. Fałszywa autentyczność

Coraz częstszy artefakt „humanizowanych" promptów — frazy symulujące osobiste
doświadczenie, których nie popiera żaden konkret:

_Ostatnio coraz częściej słyszę, że…_, _Ostatnio rozmawiałem z klientem i…_, _Często
widzę, że ludzie popełniają…_, _Moi klienci pytają mnie ostatnio o…_, _W rozmowach
z klientami pojawia się…_, _Wiele osób zmaga się z…_, _I szczerze?_, _Najciekawsze jest
jednak coś innego._

Po deklaracji „rozmowy z klientem" nie następuje żadna historia: ani kto, ani kiedy,
ani co z niej wynikło. To odróżnia symulację od anegdoty.

### 2.9. Hedging i statystyki-widma

**Frazy do obserwacji:** _wydaje się, że…_, _można przypuszczać…_, _potencjalnie mogło
dojść do…_, _w niektórych przypadkach…_, _eksperci twierdzą…_, _niektóre badania
pokazują…_, _wiele osób…_, _prawdopodobnie…_

Model przypisuje opinie mgławicowym autorytetom bez wskazania źródła, a obok potrafi
postawić podejrzanie okrągłą liczbę:

> Według badań aż 78% konsumentów ufa markom, które stawiają na autentyczność.

Jakich badań? Czyich? Z którego roku? Statystyka bez źródła — zwłaszcza „procentowa" —
to klasyczna halucynacja. Badania porównawcze esejów pokazują przy tym paradoks: model
hedguje **frazami**, ale unika prawdziwej modalności epistemicznej — u ludzi „moim
zdaniem", „chyba", „raczej" występują wielokrotnie częściej ([Herbold i in., Scientific
Reports 2023](https://www.nature.com/articles/s41598-023-45644-9)).

### 2.10. Mapa kalk: angielskie AI-words → polskie odpowiedniki

| Angielski marker | Polskie wcielenie |
|---|---|
| delve / dive into | zanurzmy się, zagłębmy się w temat, zgłębić |
| crucial / pivotal / key | kluczowy |
| comprehensive | kompleksowy |
| holistic | holistyczny |
| robust | solidny |
| seamless | bezproblemowy, płynny |
| vibrant | tętniący życiem |
| landscape | krajobraz (cyfrowy/biznesowy) |
| leverage | wykorzystać potencjał, lewarować |
| unlock / unleash | odblokować, uwolnić (potencjał) |
| game-changer | game-changer (bez tłumaczenia) |
| tailor-made / dedicated | szyty na miarę, dedykowany |
| it's important to note | warto zauważyć, że / należy pamiętać |
| moreover / furthermore | co więcej / ponadto |
| in conclusion | podsumowując / reasumując / konkludując |
| meticulous | skrupulatny, drobiazgowy |
| commendable | godny pochwały |
| significant / notable | znaczący, istotny, godny uwagi |

---

## 3. Składnia i gramatyka

### 3.1. Kalki składniowe z angielskiego

Model „myśli" strukturami angielskimi i kalkuje je do polszczyzny — tekst „pachnie
tłumaczeniem". Najczęstsze konstrukcje (status normatywny za poradnią PWN):

- **zaadresować problem / adresować potrzeby** (to address a problem) — po polsku
  problemy się rozwiązuje, dostrzega, zajmuje się nimi
- **dedykowany dla / dedykowany do** (dedicated to) — poprawnie: przeznaczony dla,
  służący do; tradycyjnie dedykuje się _coś komuś_ (książkę)
- **w oparciu o** dane/algorytmy/badania — z abstraktami poprawnie „na podstawie",
  „opierając się na"
- **wydaje się być** (seems to be) — po polsku „być" jest zbędne: _wydaje się dobry_
- **na końcu dnia** (at the end of the day) — po polsku „ostatecznie", „w gruncie rzeczy"
- **podjąć akcję** (take action), **dostarczać rezultaty/wartość** (deliver
  results/value), **robić różnicę** (make a difference)
- **„Jako X, …" z anakolutem** (As an X, …): „Jako model językowy, moim celem jest…" —
  podmiot zdania nie jest nosicielem roli; po polsku zgrzyt
- anglosaskie realia w polskim tekście: Thanksgiving, 4th of July, stopy w przepisach

### 3.2. „To nie X, to Y" i krewni

Konstrukcje przeciwstawne — polskie wcielenie angielskiego „It's not X, it's Y":

> To nie jest kolejny kurs. To system. / To nie tylko narzędzie — to filozofia. /
> Samorozwój to nie trend, to zmiana stylu życia. / To coś więcej niż…

Oraz negatywne paralelizmy: **nie tylko…, ale także/przede wszystkim…** — jedna
z najbardziej ulubionych figur modeli. Konstrukcja jest o tyle zdradliwa, że przeniknęła
już do ludzkiej polszczyzny (media opisują ją jako frazę, która „jest już wszędzie") —
markerem jest jej **zagęszczenie**, nie pojedyncze użycie.

### 3.3. Reguła trzech, triady i anafory

Model kompulsywnie wylicza **dokładnie trzy** elementy:

> Oferujemy rozwiązania innowacyjne, kompleksowe i skalowalne. Działamy szybko,
> skutecznie i efektywnie.

Pokrewne figury: anafora (trzy zdania pod rząd o identycznym początku) i staccato
„**Bez X. Bez Y. Tylko Z.**" („Bez stresu. Bez wysiłku. Bez ryzyka."), a także puste
„fałszywe zakresy" — „od strategii po egzekucję, od wizji po rezultaty" — w których
nie sposób wskazać żadnej skali.

### 3.4. Strona bierna, bezosobowość, nominalizacje

Styl urzędowo-akademicki tam, gdzie człowiek napisałby wprost:

- formy bezosobowe i bierne: _zostało przeprowadzone badanie_, _należy wdrożyć_,
  _zaleca się stosowanie_, _dokonano analizy_
- **nominalizacje** — rzeczowniki odczasownikowe zamiast czasowników:
  „Zidentyfikowanie kluczowych czynników sukcesu jest niezbędne" zamiast „Trzeba
  ustalić, co decyduje o sukcesie"; nagłówki list w stylu „Zapewnienie…", „Budowanie…",
  „Angażowanie…" (badania: nominalizacje 1,5–2 razy częstsze niż u ludzi)
- napuszone piętrowe zbitki: „realizacja procesu implementacji rozwiązania" zamiast
  „wdrożył system"

### 3.5. Monotonny rytm (niska „burstiness")

Ludzie piszą falami: krótkie zdanie, potem długie, wtrącenie, pytanie, urwana myśl.
Model maszeruje równym krokiem — zdania o zbliżonej długości i identycznej budowie,
akapity jak od linijki, zero pytań retorycznych, zero wykrzyknień, zero ryzyka. To
właśnie mierzy „burstiness" w detektorach; po polsku obserwacja potwierdzona zarówno
przez praktyków („hipnotyczny rytm"), jak i badawczo — teksty generowane mają
konsekwentnie niższą perpleksję i węższe rozkłady konstrukcji gramatycznych niż ludzkie
([PolEval 2025 „Śmigiel"](https://aclanthology.org/2025.poleval-main.2/);
[stylometria UJ](https://arxiv.org/abs/2507.00838)).

### 3.6. Powtórzenia leksykalne

Dwa przeciwstawne warianty, oba maszynowe:

- **powtarzanie tego samego rzeczownika** co drugie zdanie zamiast zaimka lub elipsy —
  w polskim korpusie badawczym „najłatwiej wykrywalne" teksty maszynowe zawierały
  powtórzenia głównego rzeczownika, fraz i wzorców gramatycznych (Śmigiel); to samo
  wskazało badanie wypracowań maturalnych ChatGPT (Mazur: „nieuzasadnione powtórzenia"
  jako główne wykolejenie stylistyczne)
- **przesadna wariacja synonimiczna** („elegant variation"): bohater → protagonista →
  główna postać → tytułowy bohater w czterech kolejnych zdaniach — artefakt kary za
  powtórzenia w dekodowaniu

### 3.7. Błędy gramatyczne typowe dla polszczyzny LLM

Badanie wypracowań maturalnych generowanych przez ChatGPT ([R. Mazur, „LingVaria"
1(37)/2024](https://journals.akademicka.pl/lv/article/view/5756)) daje twardy profil
błędów: **składnia 35%**, leksyka 24%, interpunkcja (niemal wyłącznie **dodane** zbędne
znaki), ortografia — prawie bezbłędna. To odwrotność profilu słabego pisarza-człowieka
(u ludzi: literówki i ortografia tak, składnia względnie sprawna).

Konkretne typy z przykładami z badań:

- **zerwana zgoda w zdaniach złożonych**: „Wielu pisarzy i poetów _starali się_ zgłębić…"
  (poprawnie: _starało się_); „poezja Mickiewicza… _przedstawiają_"
- **błędy łączliwości (kolokacji)**: Makbet „_popada w mroczne czyny_", „staje się
  _namiętnie ambitny_", Hiob „zachowuje _wiarę w Boga i cierpienie_"
- **mylony aspekt czasownika**: _popełnić_ zamiast _popełniać_ przy czynności
  powtarzalnej
- **nieodmienione lub źle odmienione nazwiska i nazwy własne**: „praca Jana Kowalski",
  brak odmiany nazwiska, które odmieniać trzeba — fleksja nazw własnych to słaby punkt
  modeli testowany wprost w polskich benchmarkach
- **mieszanie rejestrów**: niemotywowane archaizmy obok kolokwializmów w tekście
  neutralnym
- osobliwe zniekształcenia zamiast zwykłych literówek: „tyranozaurus" zamiast „tyran",
  „z poza" zamiast „spoza"

---

## 4. Typografia i interpunkcja

Warstwa najłatwiej sprawdzalna — znaki są binarne: albo są, albo ich nie ma. Dla
polszczyzny działa dodatkowy filtr: model często stosuje **konwencje angielskie**,
których polska ręka na polskiej klawiaturze nie produkuje.

| Element | Norma polska | Typowy tekst LLM |
|---|---|---|
| Myślnik | półpauza „–" ze spacjami (internet, prasa); pauza „—" w składzie książkowym | pauza „—" gęsto i regularnie, zamiast przecinków i dwukropków |
| Zakresy | 2010–2020 (półpauza bez spacji) | 2010-2020 (dywiz) albo 2010—2020 |
| Cudzysłów | „…" (dolny-górny) | "…" angielskie typograficzne lub "..." proste |
| Kropka a cudzysłów | „cytat". — kropka po zamknięciu | "cytat." — kropka w środku (wzór amerykański) |
| Nagłówki | Tylko pierwsze słowo wielką literą | Title Case: Każde Słowo Wielką Literą |
| Po dwukropku | mała litera (wyjątek: cytat) | Wielka litera |
| Punkty listy | konsekwentna interpunkcja | brak znaków albo niekonsekwencja |
| Wyróżnienia | oszczędnie | **pogrubienia** „kluczowych fraz" w co drugim zdaniu |
| Hasztagi | #malymiliterami | #CamelCaseKażdeSłowoWielką |

### 4.1. Pauza „—" jako podpis AI

Najgłośniejszy pojedynczy marker w polskim internecie. W polskiej praktyce wydawniczej
standardowym myślnikiem — zwłaszcza w tekstach internetowych — jest **półpauza „–" ze
spacjami**; przeciętny użytkownik pisze wręcz zwykły dywiz „-". ChatGPT domyślnie sypie
**długą pauzą „—"**, i to w miejscach, gdzie człowiek postawiłby przecinek, dwukropek
albo nawias — „zbyt regularnie i schematycznie". Charakterystyczne jest rytmiczne
„dopowiedzenie po myślniku" na końcu zdania:

> To nie jest kwestia narzędzi — to kwestia nawyków. Warto zacząć od małych kroków —
> nawet pięć minut dziennie robi różnicę — i systematycznie budować rutynę.

Zastrzeżenia: pauza jest poprawna w składzie książkowym i bywa świadomym wyborem
redakcyjnym; OpenAI ogłosiło w 2025 r. „naprawę" nadużywania em dashy, a ludzie zaczęli
ten znak naśladować — marker traci moc z czasem i działa tylko w połączeniu z innymi.

### 4.2. Cudzysłowy nie-po-polsku

Polski cudzysłów podstawowy to „…" (otwierający dolny, zamykający górny). Modele
domyślnie dają cudzysłowy angielskie — typograficzne "…" (ChatGPT) albo proste "..."
(częste u Claude/Gemini). Żaden z nich nie jest polską normą, więc **oba warianty są
markerem** w starannym polskim tekście. Sygnałem bywa też niekonsekwencja: „…" obok "…"
w jednym tekście (fragmenty pisane ręcznie kontra wklejone z czatu).

### 4.3. Kropka przed cudzysłowem

Po polsku kropka kończąca zdanie stoi **po** cudzysłowie zamykającym („taki przykład").
Wzorzec amerykański — kropka wewnątrz ("taki przykład.") — jest kalką, której polska
ręka odruchowo nie produkuje. Subtelny, ale mocny sygnał.

### 4.4. Przecinek po okoliczniku na początku zdania

Angielska reguła („Additionally, …", „In this context, …") przeniesiona do polszczyzny:

> Dodatkowo, warto zwrócić uwagę na koszty. W kontekście tych zmian, kluczowe jest
> odpowiednie przygotowanie. Jednakże, nie każdy przypadek jest taki sam.

Po polsku po „Dodatkowo", „Jednakże" czy frazie okolicznikowej przecinka się nie stawia.
W badaniu wypracowań ChatGPT **45 z 48 błędów interpunkcyjnych** polegało właśnie na
dodaniu zbędnego znaku — to marker o wysokiej czułości.

### 4.5. Title Case i CamelCase

„Jak Skutecznie Budować Markę Osobistą w 2026 Roku" — w polskim tytule wielką literą
pisze się tylko pierwsze słowo (i nazwy własne). Model kalkuje angielską konwencję
tytułów, czasem razem z jej wyjątkami (małe „i", „w"). To samo w hasztagach:
#TworzenieTreściSEO #ZautomatyzowanyMarketing — „hasztagi zapisane jak nazwy klas
w Javie".

### 4.6. Listy: wielka litera po dwukropku, brak interpunkcji

Po dwukropku wprowadzającym wyliczenie po polsku pisze się małą literą; punkty listy
kończy się konsekwentnie (przecinki/średniki albo kropki przy pełnych zdaniach). Modele
dają wielką literę po dwukropku i punkty bez żadnego znaku na końcu — albo
niekonsekwentnie, część z kropką, część bez.

### 4.7. Nadużycie pogrubień

Model wytłuszcza „kluczowe frazy" mechanicznie, w co drugim zdaniu, w funkcji
pseudonagłówków — maniera odziedziczona po poradnikach i pitch-deckach. Na polskiej
Wikipedii „zbędne boldy" są wymieniane wprost jako częsty błąd LLM. Pochodny ślad
twardy: surowe gwiazdki `**tekst**` w gotowej publikacji — znak, że tekst szedł z czatu
przez edytor, który Markdownu nie sparsował.

### 4.8. Emoji jako ozdobniki struktury

🚀 ✅ 💡 🔑 📌 przy punktach list, nagłówki obudowane emoji z obu stron („🌸 PROMOCJA 🌸"),
zdania zaczynane od emoji, ✅ jako punktor. W tekstach „profesjonalnych" — silny sygnał;
w luźnej komunikacji prywatnej — żaden.

---

## 5. Struktura i formatowanie

### 5.1. Listy „Hasło: zdanie"

Najbardziej charakterystyczna struktura formatowania AI — wyliczenie, w którym każdy
punkt zaczyna się pogrubionym hasłem z dwukropkiem:

> Oto najważniejsze korzyści:
>
> - **Oszczędność czasu:** automatyzacja pozwala skrócić proces o połowę.
> - **Większa wydajność:** zespół może skupić się na zadaniach strategicznych.
> - **Skalowalność:** rozwiązanie rośnie razem z organizacją.

Do kompletu: prawie każdy akapit kończy się zdaniem-zapowiedzią z dwukropkiem, nawet
gdy lista ma dwie pozycje, a tekst „składa się wyłącznie z punktów" i przypomina
notatki ze studiów zamiast narracji.

### 5.2. Szablon kompozycyjny i równe akapity

Sztywny szkielet: wstęp → trzy punkty → podsumowanie (wariant dłuższy: nagłówek, wstęp,
dokładnie pięć sekcji H2, podsumowanie). Każdy rozdział podobnej długości, każdy akapit
pełni tę samą funkcję i liczy tyle samo zdań. Ludzie piszą asymetrycznie — jeden wątek
na całą stronę, inny zbywają zdaniem.

### 5.3. Wtórne podsumowania w środku tekstu

„W skrócie…" w połowie wywodu, mini-podsumowanie po każdym akapicie, przymus domykania
każdej myśli. Tekst przypomina serię zamkniętych kapsuł zamiast ciągłej narracji.

### 5.4. Ślady Markdownu i kopiowania z czatu

Twarde artefakty transferu czat → publikacja:

- `##` przed nagłówkami, `**gwiazdki**`, `---` jako separator w systemach, które
  Markdownu nie renderują (Word, CMS-y, wikikod)
- na Wikipedii: nagłówki hashami, gwiazdkowe pogrubienia w wikikodzie, formatowanie
  i szablony w konwencji en.wiki zamiast polskiej
- brakujące pierwsze litery akapitów (błąd zaznaczania przy kopiowaniu), doklejone tło
  aplikacji czatu przy wklejaniu z formatowaniem, brak łamania wierszy
- nadmiarowe spacje (podwójne, na początku akapitu) — artefakt niektórych modeli

---

## 6. Treść i fakty

### 6.1. Halucynacje podawane tonem pewności

Model „z niezwykłą pewnością siebie pisze totalne bzdury" — argumentuje, podaje
przykłady, brzmi ekspercko. Udokumentowane polskie przypadki: „Katowice na północy
Polski", pięcioro polskich noblistów (zamiast siedmiorga), przeniesienie włoskiego
newsa na polski grunt z wymyśloną podstawą prawną i przewalutowaniem „z 42 euro
powstało 500 zł", zmyślona polska nazwa gatunku rośliny, nieaktualny stan prawny
opisany jako obowiązujący. Charakterystyczne: **ogólniki wyglądają prawdopodobnie,
szczegóły to fantazje** — im bardziej specjalistyczny temat, tym więcej konfabulacji.

### 6.2. Zmyślone źródła i bibliografia

Najsilniejszy pojedynczy marker według praktyki polskiej Wikipedii (przesłanka
kasowania artykułów) i promotorów prac dyplomowych:

- pozycje bibliograficzne, które „się nie googlują" — książka o wiarygodnym tytule,
  której nie ma w żadnym katalogu
- **DOI prowadzący do innej pracy**, nieistniejące ISBN, realne czasopismo + zmyślony
  tytuł artykułu
- **przekręcone imię przy prawdziwym nazwisku** (albo odwrotnie): „Micah Gonzales"
  zamiast Micah Zenko — ISBN, rok i wydawca się zgadzają, autor nie
- przypis „całą książką" bez numerów stron; źródło, które istnieje, ale nie zawiera
  przypisywanej mu informacji (source–text mismatch)
- cytaty przypisane niewłaściwym osobom; wypowiedzi osób, które nie mogły ich
  wypowiedzieć
- martwe linki od dnia publikacji (model pamięta stare URL-e) połączone z bieżącą,
  hurtowo identyczną datą dostępu we wszystkich przypisach

### 6.3. Ogólniki zamiast konkretów

Tekst długi, „nieostry", z małą liczbą faktów: zero nazw firm, miejscowości, dat,
liczb, nazwisk. Badania stylometryczne potwierdzają: teksty ludzkie tego samego gatunku
mają istotnie **więcej nazw własnych, dat i liczebników**. Pokrewne sygnały: truizmy
(„SEO jest ważne dla widoczności w Google"), „pozorna konkretność" („eksperci",
„najnowsze badania", „wiele przedsiębiorstw" — bez ani jednego nazwiska czy tytułu),
zdania, które „brzmią mądrze, ale nie mówią nic konkretnego".

### 6.4. Brak osobistej perspektywy i przesadne wyważenie

Zero wspomnień, porażek, emocji, ironii; encyklopedyczny dystans w gatunkach, które
żyją osobistym głosem (blog, felieton, post). Model przedstawia „argumenty obu stron"
i unika jednoznacznego rozstrzygnięcia — kończy tam, gdzie wypada, a nie tam, dokąd
doprowadził go wywód. W liczbach: markery pierwszoosobowej postawy („moim zdaniem")
w esejach GPT-4 spadają praktycznie do zera.

### 6.5. Brak polskiego kontekstu

Odniesienia do Thanksgiving i 4th of July w tekście dla polskiego czytelnika, ceny
w dolarach, amerykańskie ramy prawne opisane jak polskie, anglojęzyczne odniesienia
kulturowe bez adaptacji. W tłumaczeniach maszynowo-AI: nazwy i tytuły pozostawione po
angielsku tam, gdzie istnieją polskie odpowiedniki.

### 6.6. Slop społecznościowy (Facebook/LinkedIn)

Rozpoznawalne polskie schematy treści generowanych masowo:

- **Facebook („boomertrapy")**: „Dzisiaj są moje urodziny! Nikt nie złożył mi życzeń,
  bo jestem ze wsi", „to mój pierwszy tort zrobiony samemu", „Polub, jeśli kochasz
  Jezusa" — chwytająca za serce historia + wyrzut + prośba o reakcję
- **LinkedIn**: sztywny szablon hook → rozwinięcie → CTA („Nie czekaj – skorzystaj już
  dziś"), otwarcia typu „Właśnie odkryłem coś, co zmieniło moje myślenie
  o przywództwie", „pionowa" konstrukcja (jedno zdanie = jedna linia), morał biznesowy
  wyciągnięty z banalnej czynności, automatyczne komentarze „Świetny post! Dziękuję za
  podzielenie się"
- **farmy treści**: dziesiątki artykułów dziennie na jednej domenie (często przejętej
  po lokalnej firmie lub parafii), fikcyjni autorzy ze stockowymi zdjęciami, brak
  danych kontaktowych redakcji, „podejrzanie szeroki zakres tematów bez specjalizacji"

---

## 7. Komunikacja przeznaczona dla użytkownika

Twarde dowody: fragmenty rozmowy z chatbotem wklejone do publikacji. Badanie
[A. Strzeleckiego (UE Katowice)](https://onlinelibrary.wiley.com/doi/10.1002/leap.1650)
znalazło takie artefakty w 89 artykułach naukowych z czasopism Q1/Q2 — przeszły pełną
recenzję.

**Frazy do obserwacji (wersje polskie i angielskie):**

- _Oczywiście! Oto…_, _Jasne, poniżej znajdziesz…_, _Mam nadzieję, że to pomoże!_,
  _Cieszę się, że mogę pomóc!_, _Daj znać, jeśli chcesz, żebym coś rozwinął_,
  _Czy chcesz, żebym…?_
- _Jako model językowy / jako sztuczna inteligencja nie mogę…_ (odmowa wykonania
  polecenia wklejona do tekstu)
- _Według mojej wiedzy na dzień ostatniej aktualizacji…_, _Nie mam dostępu do danych
  w czasie rzeczywistym…_, _Na dzień [data] brak doniesień o…_ (disclaimery o cezurze
  wiedzy)
- _Regenerate response_ / _Wygeneruj odpowiedź ponownie_ (skopiowany przycisk
  interfejsu)
- pozostawione **placeholdery**: „[Wstaw nazwę firmy]", „[Opisz konkretny przypadek]",
  „[Nazwisko posła lub senatora] (np. Jan Kowalski)" — model podał szablon, użytkownik
  nie uzupełnił
- pytanie użytkownika (prompt) wklejone razem z odpowiedzią
- **podwójne formy grzecznościowo-rodzajowe w tekście ciągłym**: „jako poseł/posłanka
  uważam…", „Niech Pan/Pani przestanie…" — u ludzi w prozie ciągłej praktycznie
  niespotykane

---

## 8. Ślady techniczne

Markery „śledcze" — wymagają zajrzenia w kod/linki, ale są niemal rozstrzygające:

- **`utm_source=chatgpt.com`** lub `utm_source=openai` doklejone do URL-i źródeł
  (dowodzi użycia ChatGPT do wyszukania linków; na pl.wiki dwukrotnie zdemaskowało
  autorów)
- resztki markupu specyficznego dla chatbotów: `citeturn0search0`,
  `:contentReference[oaicite:0]{index=0}`, `oai_citation`, `[attached_file:1]`,
  `({"attribution":{"attributableIndex":"…"}})`, znak ↩ przy przypisach
- Markdown w systemach, które go nie używają (patrz 5.4); na wiki dodatkowo: zmyślone
  kategorie, szablony i skróty zasad (np. odsyłacz do nieistniejącego „WP:ENCYFIRMY")
- **metadane i tempo**: pięć artykułów zapisanych w jednej minucie, 34 hasła i 530 tys.
  bajtów jednego dnia, komentarze publikowane co dwie sekundy przez API — żaden człowiek
  tak nie pisze
- identyczna data dostępu we wszystkich przypisach + część linków martwa od początku

---

## 9. Maniery konkretnych modeli i data ważności markerów

„AI" nie jest monolitem — klasyfikator rozpoznaje autora tekstu spośród pięciu czołowych
chatbotów z 97% skutecznością, a sygnatura modelu **przeżywa nawet tłumaczenie na inny
język** ([Sun i in., „Idiosyncrasies in Large Language
Models"](https://arxiv.org/abs/2502.12150)). Większość polskich list fraz opisuje de facto
ChatGPT; inne modele zdradzają się inaczej. Do tego markery mają **datę ważności**:
angielski pierwowzór tego katalogu datuje słownictwo per generacja modelu („delve" to
sygnatura ery GPT-4, wygasła w 2025 r.), a OpenAI od listopada 2025 r. pozwala wyłączyć
em dashe. Poniższa tabela to synteza polskich testów porównawczych i badań — traktować
jako przybliżenie, które starzeje się w cyklu ~12 miesięcy:

| Generator | Typowe ślady w polszczyźnie | Uwagi czasowe |
|---|---|---|
| ChatGPT (era GPT-3.5/4, 2023–2024) | „w dzisiejszym dynamicznym świecie", „zagłębmy się", „kluczowy", „holistyczny", listy z boldem, równe akapity | „zagłębmy się"/delve wygasa od 2025 |
| ChatGPT (era GPT-4o, 2024–2025) | „Świetne pytanie!", entuzjazm („rewelacyjny, niesamowity"), emoji 🚀✨, „to nie X, to Y", gęste pauzy „—" | szczyt sykofancji: IV 2025 (wycofany); em dash wyłączalny od XI 2025 |
| ChatGPT (era GPT-5, od 2025) | suchszy, rzeczowy ton; mniej ozdobników; nadal „podkreślając", listy | markery ery 4o słabną w nowych tekstach |
| Claude | poprawna fleksja (najmniej błędów odmiany w polskich testach), mało boldów i list, płynne akapity; za to asekuranctwo („to zależy od kontekstu"), „szczerze mówiąc", „Masz absolutną rację!" | opinie testerów zgodne: „pisze najbardziej po polsku" |
| Gemini | ton „sprawnego urzędnika", kalki i dosłowne idiomy, dryf rejestru w długich tekstach, **kursywa** na pojedynczych słowach, „niezwykle/niesamowicie", częste „ponadto/co więcej" | polszczyzna wyraźnie poprawiła się w nowszych wersjach — oceny źródeł rozbieżne |
| DeepSeek | pisze „jak ChatGPT" (74% tekstów mylonych z OpenAI); dodatkowo: pojedyncze chińskie znaki lub nagłe angielskie zdania w polskim tekście | mieszanie języków najsilniejsze w R1 |
| Bielik / PLLuM | prawie bez frazesów rodem z ChatGPT; za to ogólnikowość, sprzeczności wewnętrzne, kancelaryjna sztywność (PLLuM), anglojęzyczne odmowy w polskiej rozmowie (Bielik) | polskie modele, wdrażane m.in. w administracji |

Praktyczny wniosek: brak frazesów „w dzisiejszym świecie" nie oznacza, że tekst nie jest
generowany — mógł wyjść z modelu o innym profilu. I odwrotnie: flagowanie tekstu z 2026 r.
po markerach ery GPT-4 to prosty sposób na pomyłkę.

---

## 10. Generowanie czy tłumaczenie? Cztery profile tekstu

Katalog byłby krzywdzący bez tego rozróżnienia. „Nienaturalna polszczyzna z kalkami" ma
co najmniej cztery różne źródła — a tylko część z nich to „tekst AI":

| Profil | Co to jest | Dominujące artefakty |
|---|---|---|
| A. Generacja natywna (LLM po polsku) | tekst wygenerowany od zera po polsku | frazesy, struktura, markery z sekcji 1–8 |
| B. Generacja EN → tłumaczenie | tekst wygenerowany po angielsku i przetłumaczony | podwójny profil: markery A **plus** ślady tłumaczenia |
| C. Człowiek → DeepL/Google Translate | ludzki tekst przepuszczony przez translator | czyste „machine translationese" — **bez** markerów treściowych AI |
| D. Postedycja | tłumaczenie maszynowe poprawione przez człowieka | profil pośredni: prostszy i bardziej „znormalizowany" niż przekład ludzki |

**Na tłumaczenie (B/C), a nie generację natywną, wskazują** (za polskimi badaniami
przekładoznawczymi — [Biel, Lingua Legis
29/2021](https://lingualegis.ils.uw.edu.pl/index.php/lingualegis/article/view/63);
[Boralewska i in., tamże](https://lingualegis.ils.uw.edu.pl/index.php/lingualegis/article/view/66);
[Szczęsny, Rocznik Przekładoznawczy 20/2025](https://apcz.umk.pl/RP/article/view/66328)):

- **niekonsekwencja terminologiczna w obrębie akapitu** — „government contractor" raz jako
  „kontrahent rządowy", raz „wykonawca rządowy"; NMT tłumaczy segment po segmencie, LLM
  generujący natywnie pilnuje spójności terminu
- **błędy zgody rodzaju i przypadka, zwłaszcza w wyliczeniach** („Osoba… zobowiązany…
  uprawnione…"), wyliczenia po dwukropku w mianowniku zamiast wymaganego przypadka —
  duże LLM-y piszące po polsku dziś prawie tego nie robią
- interpunkcja i wielkie litery **skopiowane ze źródła** (angielskie cudzysłowy, wyrywkowy
  Title Case), powtórzone segmenty na granicach wierszy, urwane zdania
- idiomy przełożone dosłownie, utrwalone polskie ekwiwalenty „przetłumaczone na świeżo",
  skróty rozwiązane błędnie
- gęste kalki **jednego** języka źródłowego przy braku frazesów i metastruktury AI

**Kluczowe ostrzeżenie:** profil C to człowiek. Tekst napisany przez człowieka
i przetłumaczony maszynowo ma obniżoną różnorodność leksykalną — dokładnie tę cechę,
którą detektory czytają jako „AI". To ten sam mechanizm, przez który detektory
dyskryminują osoby piszące w języku obcym. Naprawą profilu C jest postedycja
(ujednolicenie terminologii, polska typografia, scalenie segmentów), a nie „odAIowanie".

---

## 11. Co mierzą badania i detektory

Warstwa ilościowa — dla porządku, bo to na niej stoją wszystkie automaty:

- **Perpleksja** (przewidywalność tekstu): teksty generowane mają konsekwentnie niższą
  perpleksję niż ludzkie — potwierdzone dla polszczyzny na korpusie 64 tys. próbek
  ([PolEval 2025 „Śmigiel"](https://aclanthology.org/2025.poleval-main.2/)). Na tej
  mierze opiera się państwowy Jednolity System Antyplagiatowy
  ([JSA](https://jsa-cp.opi.org.pl/baza-wiedzy-skroty/uzycie-sztucznej-inteligencji/)):
  fragment poniżej progu = „podejrzany". JSA uczciwie zastrzega, że definicje i przepisy
  prawne mają naturalnie niską perpleksję (fałszywe alarmy).
- **Burstiness** (zmienność długości/struktury zdań): u modeli niska — patrz 3.5.
- **Bogactwo leksykalne** (type-token ratio, hapaksy): u modeli niższe; to najodporniejszy
  sygnał między domenami według badań porównawczych.
- **Standaryzacja gramatyczna**: wąskie rozkłady konstrukcji składniowych, mało inwersji,
  mniej interpunkcji w tokenach ogółem (przy jednoczesnym dodawaniu zbędnych przecinków
  po polsku — te dwa fakty nie są sprzeczne: mniej znaków, ale w bardziej schematycznych
  miejscach).

**Dlaczego nie ufać detektorom przy polszczyźnie:**

- vendor plagiat.pl podaje dla polskiego **ponad dwukrotnie wyższy** odsetek fałszywych
  pozytywów niż dla angielskiego (4,5% vs 2%); praktycy szacują margines błędu na 10–15%
- ten sam tekst potrafi dostać 92% AI w jednym narzędziu i „100% człowiek" w drugim
  (test Sempai); ZeroGPT oznaczał fragmenty Biblii jako 98% AI
- benchmark [CEAID](https://arxiv.org/abs/2509.26051) dla języków środkowoeuropejskich:
  dla polskiego przyzwoicie działają tylko detektory dotrenowane na polskich danych
  (~0,96–0,98 AUC); uniwersalne metody statystyczne ~0,78, zero-shot ~0,65
- detektory nadzorowane załamują się na nowej domenie + nowym modelu (spadek do ~61%)
- teksty współtworzone (człowiek + AI, po redakcji) rozjeżdżają wyniki najbardziej;
  poniżej ~200 słów wyniki są niewiarygodne
- konsensus polskiej Wikipedii: „Nie mamy metod wykrywania AI. Mamy za to metody
  wykrywania braku czy błędnych źródeł. I tego się trzymajmy."

---

## 12. Sygnały pisania ludzkiego

- **Data**: tekst opublikowany przed 30 listopada 2022 r. (premiera ChatGPT) niemal na
  pewno nie jest tekstem LLM.
- **Zdolność wyjaśnienia własnych decyzji**: autor umie opowiedzieć, skąd wziął
  informację, dlaczego tak sformułował zdanie, co jest na stronie 34 cytowanej książki.
  W szkole i na uczelni rozmowa o pracy jest skuteczniejsza niż każdy detektor
  (najczęściej wskazywana metoda w ankiecie wśród nauczycieli akademickich).
- **Konkret biograficzny, który model musiałby zmyślić**: własna liczba, zrzut ekranu,
  szczegół z lokalnego kontekstu, historia z puentą nie do wygenerowania.
- **Naturalna nierówność**: literówki, urwane zdania, asymetryczne akapity, prawdziwe
  emocje — choć uwaga, to sygnał pomocniczy, nie dowód (patrz niżej).

---

## 13. Nieskuteczne wskaźniki (jak nie oskarżać)

Fałszywe oskarżenie o użycie AI krzywdzi realne osoby. Czego **nie** traktować jako
dowodu:

- **Nienaganna polszczyzna sama w sobie.** Wielu ludzi po prostu pisze poprawnie.
  Hiperpoprawność nabiera znaczenia dopiero w zderzeniu z kontekstem (uczeń, który
  dotąd pisał inaczej; nagła zmiana idiolektu w połowie tekstu).
- **Prostota i przewidywalność stylu.** Detektory oparte na perpleksji dyskryminują
  osoby piszące w języku dla nich obcym — w głośnym badaniu 61% esejów TOEFL pisanych
  przez ludzi oznaczono jako AI ([Liang i in., Patterns
  2023](https://arxiv.org/abs/2304.02819)). Ubogi repertuar leksykalny ≠ maszyna.
- **Pojedyncze słowa i znaki.** Jedno „kluczowy", jedna pauza „—", jedno „warto
  zauważyć" — to statystyczny szum. Em dash bywa świadomym wyborem typograficznym,
  a „smart quotes" wstawia Word.
- **Osobisty ton jako dowód człowieczeństwa** — heurystyka odwrotnie skorelowana
  z prawdą: modele bez trudu generują „ja", rodzinę i wyznania (patrz 2.8), a badania
  pokazują, że tekst AI bywa oceniany jako „bardziej ludzki niż ludzki"
  ([Jakesch i in., PNAS 2023](https://www.pnas.org/doi/10.1073/pnas.2208839120)).
- **Wynik pojedynczego detektora.** Zawsze wskaźnik ryzyka, nigdy wyrocznia — tym
  bardziej po polsku.
- **Formalny, listowy układ wypowiedzi.** Ludzie też piszą maile z „Szanowni Państwo"
  i punktami.
- **Kalki i „obca" polszczyzna sama w sobie.** To równie dobrze ludzki tekst
  przetłumaczony DeepL-em albo autor nienatywny (patrz sekcja 10 — profile B/C/D).
  Kalki nabierają znaczenia dopiero w połączeniu z markerami treściowymi
  i strukturalnymi AI.

Do tego dochodzi **pętla zwrotna**: maniery AI przenikają do ludzkiej polszczyzny
(konstrukcja „to nie X, to Y" jest już wszędzie, em dash bywa modny), a modele są
korygowane (OpenAI „naprawiło" em dashe, częstość „delve" spadła po 2024 r.). Każda
lista fraz się starzeje — nagromadzenie i markery twarde starzeją się najwolniej.

---

## Źródła

### Badania naukowe (polszczyzna)

- R. Mazur, [„O poprawności językowej tekstów generowanych przez SI na przykładzie
  ChatuGPT"](https://journals.akademicka.pl/lv/article/view/5756), LingVaria 1(37)/2024 —
  typologia błędów ChatGPT w polskich wypracowaniach
- A. Urzędowska, [„Sztuczna inteligencja a inteligencja językowa. Eksperyment
  walidacyjny czatu GPT-4"](https://studiadecultura.uken.krakow.pl/article/view/11305),
  Studia de Cultura — błędy interpunkcyjne i stylistyczne GPT-4 po polsku
- P. Przybyła, J. Strebeyko, A. Wróblewska, [PolEval 2025 Task 1 „Śmigiel": Spotting
  Machine-Generated Text from LLMs for
  Polish](https://aclanthology.org/2025.poleval-main.2/) — pierwszy polski shared task
  detekcji; perpleksja, powtórzenia, placeholdery
- [CEAID: Benchmark of Multilingual Machine-Generated Text Detection Methods for
  Central European Languages](https://arxiv.org/abs/2509.26051) — skuteczność detektorów
  dla polskiego
- K. Przystalski, J. K. Argasiński, I. Grabska-Gradzińska, J. K. Ochab, [„Stylometry
  recognizes human and LLM-generated texts in short
  samples"](https://arxiv.org/abs/2507.00838), ESWA 2026 — standaryzacja gramatyczna,
  TTR, nasycenie faktami
- A. Strzelecki, [„'As of my last knowledge update': How is content generated by ChatGPT
  infiltrating scientific papers…"](https://onlinelibrary.wiley.com/doi/10.1002/leap.1650),
  Learned Publishing 2025 — artefakty czatu w publikacjach naukowych
- [StyloMetrix (NASK)](https://github.com/NASK-NLP/StyloMetrix) — interpretowalne cechy
  stylometryczne z pełnym wsparciem polskiego
- [JSA — baza wiedzy: użycie sztucznej
  inteligencji](https://jsa-cp.opi.org.pl/baza-wiedzy-skroty/uzycie-sztucznej-inteligencji/) —
  metoda perpleksji w systemie antyplagiatowym polskich uczelni

### Badania naukowe (międzynarodowe, markery uniwersalne)

- D. Kobak i in., [„Delving into LLM-assisted writing in biomedical publications through
  excess vocabulary"](https://www.science.org/doi/10.1126/sciadv.adt3813), Science
  Advances 2025 — „słowa stylu"
- T. Juzek, Z. Ward, [„Why Does ChatGPT 'Delve' So
  Much?"](https://aclanthology.org/2025.coling-main.426/), COLING 2025
- A. Reinhart i in., [„Do LLMs write like humans? Variation in grammatical and
  rhetorical styles"](https://www.pnas.org/doi/10.1073/pnas.2422455122), PNAS 2025 —
  imiesłowy, nominalizacje
- S. Herbold i in., [„A large-scale comparison of human-written versus
  ChatGPT-generated essays"](https://www.nature.com/articles/s41598-023-45644-9),
  Scientific Reports 2023 — modalność, hedging
- W. Liang i in., [„GPT detectors are biased against non-native English
  writers"](https://arxiv.org/abs/2304.02819), Patterns 2023
- M. Jakesch i in., [„Human heuristics for AI-generated language are
  flawed"](https://www.pnas.org/doi/10.1073/pnas.2208839120), PNAS 2023
- C. Shaib i in., [„Measuring AI 'Slop' in Text"](https://arxiv.org/abs/2509.19163) —
  taksonomia slopu
- M. Sun i in., [„Idiosyncrasies in Large Language
  Models"](https://arxiv.org/abs/2502.12150) — sygnatury per model przeżywają tłumaczenie
- Ł. Biel, [„Postedycja tłumaczeń maszynowych"](https://lingualegis.ils.uw.edu.pl/index.php/lingualegis/article/view/63),
  Lingua Legis 29/2021; M. Boralewska, P. Gil, A. Macko, [„DeepL czy Google
  Tłumacz?"](https://lingualegis.ils.uw.edu.pl/index.php/lingualegis/article/view/66),
  tamże; A. Szczęsny, [„Z czym (jeszcze) nie radzi sobie sztuczna inteligencja
  w tłumaczeniu?"](https://apcz.umk.pl/RP/article/view/66328), Rocznik Przekładoznawczy
  20/2025 — profile błędów tłumaczenia maszynowego w polszczyźnie
- Wang i in., [„Real, Fake, or Manipulated? (HERO)"](https://arxiv.org/abs/2509.15350) —
  tekst tłumaczony maszynowo jest odróżnialny od generowanego
- [Wikipedia: Signs of AI writing](https://en.wikipedia.org/wiki/Wikipedia:Signs_of_AI_writing) —
  pierwowzór tego katalogu (WikiProject AI Cleanup)

### Polska Wikipedia (praktyka społeczności)

- [Wikipedia:Zalecenia zastosowania narzędzi SI w polskiej
  Wikipedii](https://pl.wikipedia.org/wiki/Wikipedia:Zalecenia_zastosowania_narz%C4%99dzi_SI_w_polskiej_Wikipedii)
- Dyskusje Kawiarenki i Poczekalni (2025–2026): zmyślone przypisy jako główny marker,
  przekręceni autorzy, hurtowe daty dostępu, `utm_source=chatgpt.com`, tempo edycji;
  m.in. [DNU Cymodoceowate](https://pl.wikipedia.org/wiki/Wikipedia:Poczekalnia/artyku%C5%82y/2025:08:04:Cymodoceowate)

### Poradniki, detektory i praktycy (frazy polskie)

- [Skaner ~120 polskich fraz AI — Jacek
  Wolniewicz](https://jacekwolniewicz.pl/skaner-po-polsku-ktory-lapie-120-fraz-naduzywanych-przez-ai/)
- [Detektor AI KrupińskiAI — 19 metryk + baza fraz](https://krupinskiai.pl/apps/ai-detektor)
- [DBest Content — „GPT-izmy": kompletny przewodnik](https://dbest-content.com/jak-rozpoznac-tekst-z-ai-kompletny-przewodnik-po-gpt-izmach/)
- [Katsin — „To pisało AI: 15 sposobów"](https://katsin.pl/jak-rozpoznac-tekst-z-chatagpt/)
- [Fundacja Orange — praktyczny przewodnik](https://pracownieorange.pl/inspiration/jak-rozpoznac-tekst-napisany-przez-ai-praktyczny-przewodnik/)
- [Senuto](https://www.senuto.com/pl/blog/jak-sprawdzic-czy-tekst-zostal-napisany-przez-ai/),
  [Top Online](https://toponline.pl/blog/jak-rozpoznac-tekst-napisany-przez-ai),
  [Widoczni](https://widoczni.com/blog/ai-copywriting-poradnik/),
  [chcesztresc.pl](https://www.chcesztresc.pl/jak-sprawdzic-czy-tekst-zostal-napisany-przez-ai/),
  [WhitePress — test detektorów](https://www.whitepress.com/pl/baza-wiedzy/828/detektory-tresci-ai),
  [Sempai — test detektorów](https://sempai.pl/blog/czy-detektory-ai-klamia-test-najpopularniejszych-narzedzi/)
- [„Wszystko co Najważniejsze" — 10 sygnałów](https://wszystkoconajwazniejsze.pl/pepites/jak-rozpoznac-tekst-napisany-przez-ai/)
- Poradnik MEiN/IBE [„Chat GPT w szkole. Szanse
  i zagrożenia"](https://zpe.gov.pl/a/jak-sprawdzic-kto-napisal-prace/D1GzsAmYe)

### Typografia (normy polskie)

- [Poradnia PWN: dywiz, myślnik i półpauza](https://sjp.pwn.pl/poradnia/haslo/dywiz-myslnik-i-polpauza;1528.html)
- [typografia.info: cudzysłowy](https://typografia.info/podstawy/cudzyslowy)
- [fontnieczcionka.pl: „Pauza jako podpis AI"](https://fontnieczcionka.pl/artykuly/pauza-jako-podpis-ai-jak-uzywac-dywizu-polpauzy-i-pauzy)
- Poradnia PWN: [„zaadresować problem"](https://sjp.pwn.pl/poradnia/haslo/Nowe-zapozyczenie-zaadresowac-problem;18224.html),
  [„w oparciu o"](https://sjp.pwn.pl/poradnia/haslo/w-oparciu-o;8458.html),
  [„dedykowany"](https://sjp.pwn.pl/poradnia/haslo/dedykowany-komputer;5725.html)

### Media i społeczności

- [Zwierciadło — em dash zdradza ChatGPT](https://zwierciadlo.pl/lifestyle/550236,1,ten-jeden-element-zdradza-ze-tekst-zostal-napisany-przez-chatgpt-zdemaskowaly-go-dziennikarki-z-pokolenia-z.read)
- [Wirtualne Media — przycisk „AI slop" na LinkedInie](https://www.wirtualnemedia.pl/miarka-sie-przebrala-na-linkedin-mozna-zglaszac-slabe-posty-napisane-przez-ai,7313339813955584a)
- [GeekWeek — „To nie X, to Y" jest już wszędzie](https://geekweek.interia.pl/technologia/sztuczna-inteligencja/news-to-nie-x-to-y-ulubiona-fraza-chatgpt-jest-juz-wszedzie-i-to,nId,23504553)
- [Spider's Web — „boomertrapy"](https://spidersweb.pl/2024/07/ai-slopy-boomertrapy-poradnik-co-to.html)
- [mycompanypolska — farmy AI w Google Discover](https://mycompanypolska.pl/artykul/farmy-ai-w-polsce-jak-sztuczna-inteligencja-zalewa-google-discover-/20561)
- Wykop: [afera WP Kreator](https://wykop.pl/link/7985603/wp-kpi-z-czytelnikow-od-msc-masowo-promuje-ai-slop-i-halucynacje-w-tonie-porad),
  [tag #aislop](https://wykop.pl/tag/aislop)
