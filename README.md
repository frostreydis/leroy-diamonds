# Leroy Diamonds — Web Mockup

A static one-page website mockup for **Leroy Diamonds s. r. o.**, a jewelry
atelier based in Bratislava, Slovakia. Minimalist, luxury-oriented design in
black with bilingual content (SK / EN, each on its own crawlable URL),
ready for deployment via GitHub Pages.

## Project structure

```
leroy-diamonds-site/
├── index.html            # homepage — Slovak (default). HTML + CSS + JS in one file.
├── en/
│   └── index.html          # homepage — English. Auto-generated, don't hand-edit (see below).
├── build-en.py            # regenerates en/index.html from index.html
├── generate-manifests.py # regenerates images/*/manifest.json — see below
├── images/
│   ├── hero/             # hero background photo + manifest.json
│   ├── philosophy/        # "Our Philosophy" photo + manifest.json
│   ├── portfolio/           # "Selected Pieces" gallery + manifest.json
│   ├── instagram/            # "Follow Our Work" gallery + manifest.json
│   └── branding/               # og-image.jpg (social share preview)
├── favicon.svg, favicon.ico, favicon-*.png, apple-touch-icon.png
├── robots.txt           # crawler permissions
├── sitemap.xml           # sitemap for Google Search Console (lists both languages)
├── .gitignore
├── LICENSE
└── README.md
```

## Running locally

The site is plain HTML/CSS/JS with no build step for the browser — but it
does **require a local server**, not a direct `file://` open, because the
photo galleries load their `manifest.json` via `fetch()`, which browsers
block on `file://` for security reasons.

```bash
# from inside leroy-diamonds-site/
python3 -m http.server 8000
# then open http://localhost:8000        (Slovak)
# and       http://localhost:8000/en/    (English)
```

## Deploying to GitHub Pages

1. Create a new GitHub repository (e.g. `leroy-diamonds-web`).
2. Push the contents of this folder to the repository (`main` branch, root):
   ```bash
   git init
   git add .
   git commit -m "Initial site"
   git branch -M main
   git remote add origin https://github.com/<your-account>/leroy-diamonds-web.git
   git push -u origin main
   ```
3. In the repository, go to **Settings → Pages**.
4. Under **Source**, select the `main` branch and the `/ (root)` folder.
5. Save — GitHub will generate a URL like:
   `https://<your-account>.github.io/leroy-diamonds-web/`
6. Deployment usually takes 1–2 minutes.

All internal links and asset paths (favicon, image galleries, the SK/EN
switch, the remembered-language redirect) are written as **relative**
paths, not root-absolute ones — so this site works correctly out of the
box whether it's served from a domain root, a custom domain, **or** a
GitHub Pages *project* subpath like
`https://<account>.github.io/leroy-diamonds-web/`. You don't need a
special repo name or a custom domain just to preview it on
`github.io/<repo>/` — a plain project Pages site works fine.
(Only the `hreflang`/canonical/Open Graph `<meta>` tags hardcode the real
`https://leroydiamonds.sk/...` domain, since those tags are required by
spec to be absolute URLs — see the SEO section below for what to update
there once you know the final domain.)

### Custom domain (e.g. leroydiamonds.sk)

1. In **Settings → Pages → Custom domain**, enter `leroydiamonds.sk`.
2. At your domain registrar, add DNS records:
   - `A` records pointing to the GitHub Pages IPs (185.199.108.153,
     185.199.109.153, 185.199.110.153, 185.199.111.153), or
   - a `CNAME` record pointing to `<your-account>.github.io` if you're
     using a subdomain (e.g. `www`).
3. GitHub will automatically create a `CNAME` file in the repository —
   don't delete it.
4. Enable **Enforce HTTPS** once DNS has propagated (can take a few hours).

## Languages (SK / EN) — two real URLs

- **`/`** — Slovak, the default.
- **`/en/`** — English, a genuinely separate, fully English HTML file
  (not a JS-only text swap), so search engines can index and rank each
  language on its own URL. Both pages declare `hreflang` alternates
  pointing at each other, plus `x-default` → the Slovak version.

**`en/index.html` is generated, not hand-written.** All page text lives
once, in `index.html`, as a pair of attributes on every element:
`data-sk="…"` / `data-en="…"`. Whenever you edit copy in `index.html`
(Slovak text and/or the matching `data-en` attribute), regenerate the
English page:

```bash
pip install beautifulsoup4   # one-time, if not already installed
python3 build-en.py
```

This rewrites `en/index.html` from scratch — never edit that file
directly, your changes would be lost on the next run. Commit both files.

The header's SK/EN switch is now a real link (`<a href="/">` /
`<a href="/en/">`), not a same-page JS toggle — clicking it navigates to
the other URL. A returning visitor's last choice is still remembered (see
below), it just now takes them to the matching URL instead of swapping
text in place.

### Remembering the visitor's language

The chosen language is saved to `localStorage` when the visitor clicks
SK/EN. A small inline script at the very top of `<head>` checks that
saved value on every load and redirects immediately if the visitor is on
the "wrong" URL for their last choice (e.g. they bookmarked `/` but
last picked English) — this runs before the page paints, so there's no
visible flash. Search engine crawlers never carry a stored preference, so
this redirect does not affect what gets indexed at each URL.

## SEO — what's already in place

- `<title>`, `meta description`, `keywords` — Slovak on `/`, English on
  `/en/`
- `hreflang` alternates (`sk`, `en`, `x-default`) on both pages, and in
  `sitemap.xml`
- Open Graph and Twitter Card tags, each pointing at the correct URL
  and locale (`sk_SK` / `en_US`) per page — nice previews when shared on
  Facebook/Instagram/LinkedIn/X
- A dedicated **branded social-share image**
  (`images/branding/og-image.jpg` — the diamond mark + wordmark, not a
  product photo) used for `og:image` / `twitter:image`
- `canonical` URL on each page
- **JSON-LD** structured data of type `JewelryStore` (address, social
  profiles, price range) — helps Google understand what kind of business
  this is
- `robots.txt` + `sitemap.xml` (lists both `/` and `/en/`) for Google
  Search Console
- A `google-site-verification` meta tag placeholder — see next section
- Descriptive `alt` text on every image
- A custom favicon (see below) instead of a generic browser icon

### Setting up Google Search Console

1. Go to [search.google.com/search-console](https://search.google.com/search-console)
   and add `leroydiamonds.sk` as a property.
2. Choose the **HTML tag** verification method — it gives you a code
   like `content="abc123..."`.
3. Open `index.html`, find the line near the top of `<head>`:
   ```html
   <meta name="google-site-verification" content="REPLACE_WITH_YOUR_GOOGLE_SITE_VERIFICATION_CODE">
   ```
   and replace the placeholder with your real code. Run
   `python3 build-en.py` afterwards so `en/index.html` picks up the
   change too (it's copied verbatim from `index.html`, no per-language
   value needed here).
4. Deploy, then click "Verify" in Search Console.
5. Submit `sitemap.xml` under **Sitemaps** (`https://leroydiamonds.sk/sitemap.xml`).

### Still to do before going live

- [ ] Replace `https://leroydiamonds.sk/` throughout (`index.html`,
      `en/index.html` — via `build-en.py`, `robots.txt`, `sitemap.xml`,
      the JSON-LD block) with the final real domain, if different
- [ ] Add the real Google Search Console verification code (see above)
- [ ] Add a real phone number and email (currently marked as
      `doplniť reálny kontakt` / `to be added` in `index.html`)
- [ ] Add a real TikTok URL in the footer (currently a placeholder `#`
      link — no confirmed public TikTok account was found for the
      business)
- [ ] Register the domain in Google Search Console and submit
      `sitemap.xml` (see above)

## Photo galleries — folder structure, optimization & the manifest script

Photos are organized by where they appear on the site, one folder per
section under `images/`:

```
images/
├── hero/           # 1 photo — hero background
├── philosophy/      # 1 photo — "Our Philosophy" section
├── portfolio/         # up to 12 shown — "Selected Pieces" gallery
├── instagram/          # "Follow Our Work" — loads 10 at a time, "Load more" for the rest
└── branding/             # og-image.jpg — not a gallery, just the social-share asset
```

Each gallery folder has its own `manifest.json` (e.g.
`images/portfolio/manifest.json`) listing the images inside it, generated
by `generate-manifests.py`. The site's JavaScript reads these manifests
at runtime and builds each gallery dynamically — **no filename is
hardcoded anywhere in `index.html`**. That means you can name files
however you like (`IMG_4821.jpg`, `ring-final-v3.jpg`, whatever your
camera or export tool produces).

### How to add / remove photos

1. Drop the new image file(s) into the right folder (e.g. `images/portfolio/`).
   Remove a photo the same way — just delete the file from the folder.
2. From the project root, run:
   ```bash
   python3 generate-manifests.py
   ```
   This rewrites every `manifest.json` to match what's actually on disk.
   Filenames it already knew about keep their existing `alt` / `sk` / `en`
   captions — you only need to add captions for genuinely new files.
3. Commit and push. GitHub Pages will pick up the changes on the next
   deploy — no other step required.

The script scans **every subfolder** of `images/` automatically — it has
no hardcoded folder list, so creating an entirely new folder (e.g.
`images/press/`) and running the script will generate a manifest for it
too. To actually display a new folder as a gallery on the page, you'd
also add a small fetch/render call in the `<script>` section of
`index.html` (copy the pattern used for `renderPortfolio()`), then run
`python3 build-en.py` to carry the change over to the English page.

### What happens if a folder has more photos than the display limit?

**Nothing breaks, and no file is touched.** `generate-manifests.py`
always lists *every* image it finds — the limits below are applied only
at display time, in the browser:

- **`images/portfolio/`** (cap: 12) — if the manifest has more entries
  than the cap, only the first 12 (in manifest order — normally
  alphabetical by filename) are rendered on the page. The rest simply
  aren't shown; they stay in the folder and in `manifest.json`, so
  raising the cap later (or removing older photos) brings them back with
  no re-upload needed. Each time this happens, a note is logged to the
  browser console (`F12` → Console) naming the folder and how many
  photos were skipped, so it's never a silent surprise while you're
  working on the site — regular visitors never see this message.
- **`images/instagram/`** has no hard cap — it paginates instead. The
  first 10 show on load, and every click on "Load more" reveals the
  next 10, until the whole manifest has been shown.

To change any of these numbers, edit the three constants near the top of
the `<script>` section in `index.html`:
```js
const INSTAGRAM_PAGE_SIZE = 10;
const PORTFOLIO_MAX = 12;
```
then run `python3 build-en.py` to apply the same change to `en/index.html`.

### Image optimization

- Every image uses native lazy-loading (`loading="lazy"`) so photos
  outside the viewport aren't downloaded until the visitor scrolls
  near them.
- Source photos are pre-compressed to JPEG at a width appropriate to
  where they're used (1920px for the hero, 800px for portfolio, 400px
  for Instagram thumbnails, etc.) — keep new uploads in a similar range
  rather than dropping in multi-megabyte camera originals. A quick way
  to resize/compress before adding a file:
  ```bash
  python3 -c "from PIL import Image; im=Image.open('source.jpg').convert('RGB'); im.thumbnail((800,800)); im.save('images/portfolio/new-piece.jpg','JPEG',quality=80,optimize=True)"
  ```

## Favicon & social-share image

The favicon (`favicon.svg` + PNG/ICO fallbacks) is a custom minimalist
diamond mark designed for this site — not a generic default icon or a
cropped product photo. `images/branding/og-image.jpg` (1200×630, the
standard Open Graph size) pairs the same mark with the "Leroy Diamonds"
wordmark for link previews on social media. If the business has (or
commissions) an official logo later, swap `images/branding/og-image.jpg`
and the `favicon.*` files for the real assets, keeping the same
filenames and dimensions so nothing else needs to change.

## License

See [LICENSE](./LICENSE). This is proprietary client work — see that file
for what is and isn't permitted.

## Note

This is a **mockup/prototype** intended for approval before full
implementation (e.g. connecting a real contact/inquiry backend, or
adding e-commerce functionality).
