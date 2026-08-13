# Leroy Diamonds — Web Mockup

Statický jednostránkový (one-page) makéta webu pre klenotnícku spoločnosť
**Leroy Diamonds s. r. o.** (Bratislava). Luxusný, minimalistický dizajn
v čiernej farbe, dvojjazyčný obsah (SK / EN), pripravený na nasadenie
cez GitHub Pages.

## Štruktúra projektu

```
leroy-diamonds-site/
├── index.html          # celá stránka (HTML + CSS + JS v jednom súbore)
├── images/              # reálne fotografie šperkov Leroy Diamonds
│   ├── ring-marquise-halo.png
│   ├── ring-rose-1.png
│   ├── ring-rose-2.png
│   ├── ring-solitaire-twist.png
│   ├── ring-claddagh.png
│   └── bracelet-tennis.png
├── robots.txt           # povolenie indexovania pre vyhľadávače
├── sitemap.xml           # mapa stránky pre Google Search Console
├── .gitignore
└── README.md
```

## Ako spustiť lokálne

Stránka je čisté HTML/CSS/JS bez build procesu — stačí ju otvoriť
priamo v prehliadači, alebo spustiť jednoduchý lokálny server:

```bash
# z priečinka leroy-diamonds-site/
python3 -m http.server 8000
# potom otvoriť http://localhost:8000
```

## Nasadenie na GitHub Pages

1. Vytvorte nový repozitár na GitHub (napr. `leroy-diamonds-web`).
2. Obsah tohto priečinka nahrajte do repozitára (do `main` vetvy, do koreňa):
   ```bash
   git init
   git add .
   git commit -m "Initial site"
   git branch -M main
   git remote add origin https://github.com/<vas-ucet>/leroy-diamonds-web.git
   git push -u origin main
   ```
3. V repozitári choďte do **Settings → Pages**.
4. Pri **Source** vyberte vetvu `main` a priečinok `/ (root)`.
5. Uložte — GitHub vygeneruje URL v tvare:
   `https://<vas-ucet>.github.io/leroy-diamonds-web/`
6. Nasadenie trvá spravidla 1–2 minúty.

### Vlastná doména (napr. leroydiamonds.sk)

1. V **Settings → Pages → Custom domain** zadajte `leroydiamonds.sk`.
2. U registrátora domény pridajte DNS záznamy:
   - `A` záznamy na IP adresy GitHub Pages (185.199.108.153,
     185.199.109.153, 185.199.110.153, 185.199.111.153), alebo
   - `CNAME` záznam smerujúci na `<vas-ucet>.github.io`, ak používate
     subdoménu (napr. `www`).
3. GitHub automaticky vytvorí súbor `CNAME` v repozitári — nezmazať.
4. Zapnite **Enforce HTTPS** po tom, čo sa DNS overí (môže trvať pár hodín).

## SEO — čo je už pripravené

- `<title>`, `meta description`, `keywords` (SK, prepínajú sa aj pri EN)
- Open Graph a Twitter Card tagy (náhľad pri zdieľaní na FB/IG/LinkedIn/X)
- `canonical` URL
- Štruktúrované dáta **JSON-LD** typu `JewelryStore` (adresa, sociálne siete,
  cenová kategória) — pomáha Google pochopiť, o aký biznis ide
- `robots.txt` + `sitemap.xml` pre Google Search Console
- Sémantické `alt` texty pri všetkých fotografiách

### Čo je potrebné doplniť pred ostrým nasadením

- [ ] Nahradiť `https://leroydiamonds.sk/` v `index.html`, `robots.txt`,
      `sitemap.xml` a JSON-LD skutočnou finálnou doménou (ak bude iná)
- [ ] Doplniť reálny telefón a e-mail (v `index.html` sú označené
      `doplniť reálny kontakt` / `to be added`)
- [ ] Nahradiť `og:image` a favicon skutočným logom/brand vizuálom
      (aktuálne sa používa fotka prsteňa ako dočasný placeholder)
- [ ] Zaregistrovať doménu v Google Search Console a odoslať `sitemap.xml`
- [ ] Zvážiť samostatné URL pre EN verziu (napr. `/en/`) pre správne
      `hreflang` značky — aktuálne je prepínač jazyka riešený cez JS na
      jednej URL, čo je vizuálne v poriadku, ale Google indexuje primárne
      slovenskú verziu ako predvolenú

## Jazyky (SK / EN)

Prepínač jazyka je v hlavičke stránky (SK je predvolený). Celý text má
dvojicu atribútov `data-sk` / `data-en` priamo v HTML — úprava textu sa
robí v `index.html`, netreba samostatné súbory pre preklad.

## Fotografie

Fotografie v `images/` sú reálne práce Leroy Diamonds (s gravírovaním
značky). Pri pridávaní nových kúskov stačí nahrať súbor do `images/` a
odkázať naň v `index.html` (sekcie "Kolekcie" a "Naša tvorba").

## Poznámka

Toto je **maketa/prototyp** pripravená na schválenie pred plnou
implementáciou (napr. napojenie kontaktného formulára na reálny
backend/e-mail, prípadne e-shop funkcionalita).
