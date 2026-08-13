# Leroy Diamonds — Web Mockup

A static one-page website mockup for **Leroy Diamonds s. r. o.**, a jewelry
atelier based in Bratislava, Slovakia. Minimalist, luxury-oriented design in
black with bilingual content (SK / EN), ready for deployment via GitHub
Pages.

## Project structure

```
leroy-diamonds-site/
├── index.html          # the entire page (HTML + CSS + JS in one file)
├── images/              # real Leroy Diamonds jewelry photographs
│   ├── ring-marquise-halo.png
│   ├── ring-rose-1.png
│   ├── ring-rose-2.png
│   ├── ring-solitaire-twist.png
│   ├── ring-claddagh.png
│   └── bracelet-tennis.png
├── robots.txt           # crawler permissions
├── sitemap.xml           # sitemap for Google Search Console
├── .gitignore
├── LICENSE
└── README.md
```

## Running locally

The site is plain HTML/CSS/JS with no build step — open it directly in a
browser, or serve it with a simple local server:

```bash
# from inside leroy-diamonds-site/
python3 -m http.server 8000
# then open http://localhost:8000
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

## SEO — what's already in place

- `<title>`, `meta description`, `keywords` (Slovak by default, also
  switched when EN is active)
- Open Graph and Twitter Card tags (nice previews when shared on
  Facebook/Instagram/LinkedIn/X)
- `canonical` URL
- **JSON-LD** structured data of type `JewelryStore` (address, social
  profiles, price range) — helps Google understand what kind of business
  this is
- `robots.txt` + `sitemap.xml` for Google Search Console
- Descriptive `alt` text on every image

### Still to do before going live

- [ ] Replace `https://leroydiamonds.sk/` in `index.html`, `robots.txt`,
      `sitemap.xml` and the JSON-LD block with the final real domain (if
      different)
- [ ] Add a real phone number and email (currently marked as
      `doplniť reálny kontakt` / `to be added` in `index.html`)
- [ ] Replace the `og:image` and favicon with the actual logo/brand asset
      (a ring photo is currently used as a temporary placeholder)
- [ ] Register the domain in Google Search Console and submit
      `sitemap.xml`
- [ ] Consider a separate URL for the EN version (e.g. `/en/`) for proper
      `hreflang` tagging — the current language switch is handled via JS
      on a single URL, which works visually, but Google primarily indexes
      the Slovak version as the default

## Languages (SK / EN)

The language switch is in the site header (Slovak is the default). Every
piece of text carries a pair of `data-sk` / `data-en` attributes directly
in the HTML — edit the text in `index.html`, no separate translation
files are needed.

## Photography

The images in `images/` are real Leroy Diamonds pieces (with the brand
engraving visible). To add new pieces, drop the file into `images/` and
reference it in `index.html` (the "Collections" and "Our Work" sections).

## License

See [LICENSE](./LICENSE). This is proprietary client work — see that file
for what is and isn't permitted.

## Note

This is a **mockup/prototype** intended for approval before full
implementation (e.g. connecting the contact form to a real backend/email
service, or adding e-commerce functionality).
