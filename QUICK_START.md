# Garage Door Sites Generator - Quick Reference

**Build unlimited professional garage door websites with one command.**  
Works the same for 10 sites or 1,000 sites.

## One-Page Cheat Sheet

### Setup (First Time - Any Number of Sites)
```bash
cd engine/
# Register all sites from domains.csv (scales to any number)
python engine.py bulk --sheet ../domains.csv

# Build all registered sites (all of them at once)
python engine.py build

# Preview all sites locally
python engine.py serve
# Visit http://localhost:8000/
```

### Add New Cities (Scales to Any Number)
1. Add rows to `domains.csv` (one or one hundred):
   ```csv
   105,newcity1garagedoor.com,New City 1 Garage Door,New City 1,ST,#COLORCODE,
   106,newcity2garagedoor.com,New City 2 Garage Door,New City 2,ST,#COLORCODE,
   107,newcity3garagedoor.com,New City 3 Garage Door,New City 3,ST,#COLORCODE,
   ```

2. Register and build:
   ```bash
   python engine.py bulk --sheet ../domains.csv
   python engine.py build
   ```

3. Preview:
   ```bash
   python engine.py serve
   ```

### Customize a Site

**Change color:**
```csv
# domains.csv
...,domain.com,...,#FF6B35,     # Update hex color
```
Then rebuild: `python engine.py bulk && python engine.py build`

**Change layout:**
Edit `config/layouts.json`:
```json
{
  "domain": "...",
  "hero": "split",           // "banner", "split", "overlay", "minimal"
  "services": "list",        // "grid", "list", "featured", "carousel"
  "testimonials": "grid",    // "carousel", "grid", "sidebar", "featured"
  "cta": "card",             // "horizontal", "stacked", "card", "minimal"
  "footer": "compact"        // "classic", "compact", "minimal", "boutique"
}
```
Then rebuild: `python engine.py build`

### Image Management

All images in `brand/photos/gd-1.jpg` through `gd-9.jpg`

Each site automatically uses them. To replace:
```bash
cp new-photos/* brand/photos/
python engine.py build
```

### View Built Sites

```bash
# All sites portal
http://localhost:8000/

# Individual sites (when serving)
http://localhost:8201/  # First site
http://localhost:8202/  # Second site
http://localhost:8203/  # Third site
# ... etc
```

### Common Paths

| Path | Purpose |
|------|---------|
| `engine/config/sites.json` | Site registry |
| `engine/config/themes.json` | Color themes |
| `engine/config/layouts.json` | Layout assignments |
| `brand/logos/` | Brand logos (200+) |
| `brand/photos/` | Photography (9 images) |
| `dist/` | Built websites (to deploy) |

### File Structure for New City Content

If you need to add custom content:
```bash
mkdir -p engine/content/<city>-<state>/
cat > engine/content/<city>-<state>/<city>-home.json << 'EOF'
{
  "title": "Garage Door ...",
  "meta": "...",
  "h1": "Garage Door Repair ...",
  "sections": [
    {"h2": "Section Title", "body": "Content here..."},
  ],
  "faq": [
    ["Question?", "Answer."],
  ]
}
EOF
```

### Deploy

```bash
# Copy built sites to hosting
scp -r dist/* user@host:/var/www/html/

# Or use FTP/rsync/GitHub Actions, etc.
```

---

## Layout Choices at a Glance

### Hero Styles
1. **banner** (default) - Full-width image, centered text overlay
2. **split** - Image left, content right (responsive)
3. **overlay** - Text over top-left, minimal gradient
4. **minimal** - No image, bold typography, gradient background

### Services Display
1. **grid** - 3-column card grid (most common)
2. **featured** - Large hero card + smaller grid
3. **list** - Vertical with large icons
4. **carousel** - Horizontal scroll (desktop only)

### Testimonials
1. **carousel** - Horizontal scrolling cards
2. **grid** - 2-column grid
3. **sidebar** - Quote left, byline right
4. **featured** - Large pull quote + list

### CTA Section
1. **horizontal** - Image left, text right
2. **card** - Centered bordered box
3. **minimal** - Text-only, gradient background
4. **stacked** - Vertical stack (same as minimal)

### Footer
1. **classic** - Multi-column with branding
2. **compact** - Minimal footer bar
3. **minimal** - Links only
4. **boutique** - Large branding (like classic)

---

## Color Theme Breakdown

When you add a Primary Color (e.g., `#2563EB`) to domains.csv:

**Generated automatically:**
- Primary (`--p`): `#2563EB` - Main brand color
- Primary Dark (`--pd`): `#1D4ED8` - Hover/pressed state
- Accent: `#F59E0B` - Complementary color (buttons, highlights)
- Text on Accent: `#FFFFFF` - White text (guaranteed readable)

**WCAG contrast:**
- 5.0+ on primary (white text readable)
- 3.4+ on accent (white text readable)

**No manual color picking needed!**

---

## Tips & Tricks

### Fastest site generation (for 10 cities):
```bash
# 1. Update domains.csv with all 10 entries
# 2. Run bulk registration
python engine.py bulk

# 3. Content auto-fills from template if folder exists
# 4. Build all
python engine.py build

# Done! All 10 sites in dist/
```

### Preview a single site:
```bash
# Edit one site in dist/ manually
cd dist/yourdomain.com/
python -m http.server 8888

# Visit http://localhost:8888/
```

### Change theme without rebuilding all sites:
1. Edit `config/themes.json` directly
2. Run only `python engine.py build`

### Duplicate a site's layout for another:
```bash
# Copy layout from site A to site B in layouts.json
{
  "domain": "site-b.com",
  ...same layout as site-a...
}
```

### Disable a site (don't build it):
Remove from `config/sites.json` temporarily, rebuild, add back

### Test a new layout locally before deploying:
1. Update `config/layouts.json`
2. Run `python engine.py build`
3. Preview on http://localhost:8000/ (while serving)
4. If happy, no need to rebuild—already deployed in `dist/`

---

## Troubleshooting Quick Fixes

| Problem | Solution |
|---------|----------|
| Site not building | Check `content/<city>-<state>/<city>-home.json` exists |
| Images missing | Run `python engine.py build` (copies images to dist/) |
| Old colors showing | Delete `config/themes.json`, run `python engine.py bulk` |
| Layout not applying | Check domain in `config/layouts.json`, run `python engine.py build` |
| Port already in use | Change port in `config/sites.json` for that site, rebuild |

---

## What's Included (10 Sites, As Built)

| # | Domain | City | State | Logos | Layout |
|---|--------|------|-------|-------|--------|
| 1 | chicopeegaragedoorpros.com | Chicopee | MA | ✓ | banner + featured |
| 2 | mesagaragedoorco.com | Mesa | AZ | ✓ | split + list |
| 3 | napervillegaragedoorpros.com | Naperville | IL | ✓ | overlay + grid |
| 4 | glendalegaragedoorco.com | Glendale | AZ | ✓ | minimal + carousel |
| 5 | temeculagaragedoorpros.com | Temecula | CA | ✓ | banner + featured |
| 6 | auroragaragedoorpros.com | Aurora | CO | ✓ | split + list |
| 7 | wheatongaragedoorpros.com | Wheaton | IL | ✓ | overlay + grid |
| 8 | saginawgaragedoorpros.com | Saginaw | MI | ✓ | minimal + carousel |
| 9 | arlingtonheightsgaragedoorpros.com | Arlington Heights | IL | ✓ | banner + featured |
| 10 | rochestergaragedoorpros.com | Rochester | NY | ✓ | split + list |

---

## Next Steps

1. ✅ All 10 sites registered in `config/sites.json`
2. ✅ Color themes auto-generated in `config/themes.json`
3. ✅ Layout variations assigned in `config/layouts.json`
4. ✅ Logos available in `brand/logos/`
5. ✅ Images organized in `brand/photos/`
6. 🔲 Add custom content for each city (if needed)
7. 🔲 Run final build: `python engine.py build`
8. 🔲 Deploy `dist/` to hosting

---

**Total setup time:** ~5 minutes
**Build time:** ~30 seconds
**Deploy time:** Depends on hosting method

See `ENGINE_GUIDE.md` for detailed documentation.
