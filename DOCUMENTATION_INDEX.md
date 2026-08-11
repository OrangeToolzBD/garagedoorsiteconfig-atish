# 📚 Documentation Index - Garage Door Sites Platform

## Quick Navigation

**Start here based on your need:**

### 🚀 Just Want to Build the Sites?
→ Read: **QUICK_START.md** (5 minutes)
- One-page workflow
- Essential commands only
- Paths reference
- Troubleshooting quick fixes

### 📖 Want to Understand Everything?
→ Read: **ENGINE_GUIDE.md** (30 minutes)
- Complete architecture
- Color theme system explained
- Layout variations explained
- Configuration deep dive
- Customization guide
- Full troubleshooting

### 🎨 Want to See How Sites Look?
→ Read: **LAYOUT_VISUAL_GUIDE.md** (15 minutes)
- ASCII diagrams for each section
- Site-by-site layout examples
- Hero styles visualized
- Services options visualized
- Customization examples

### 📊 What Changed Since Last Time?
→ Read: **ENGINE_UPDATE_SUMMARY.md** (10 minutes)
- What's new (layouts.py, layouts.json)
- Technical details
- Usage examples
- Configuration examples
- Testing checklist

### ✅ What Am I Getting?
→ Read: **DELIVERABLES.md** (10 minutes)
- Complete list of 10 sites
- Features included
- Quality metrics
- What's ready to deploy
- Common tasks reference

### 📋 Project Overview?
→ Read: **PROJECT_SUMMARY.md** (5 minutes)
- 10-site lineup table
- Color scheme per site
- Layout combination per site
- Easy reference

---

## File Organization

### 📄 Documentation Files (You Are Here)
```
DOCUMENTATION_INDEX.md           ← You are here
ENGINE_GUIDE.md                  ← Complete reference (2000+ lines)
QUICK_START.md                   ← Quick cheat sheet (400+ lines)
LAYOUT_VISUAL_GUIDE.md           ← Visual diagrams (600+ lines)
ENGINE_UPDATE_SUMMARY.md         ← What changed (500+ lines)
DELIVERABLES.md                  ← What you got (600+ lines)
PROJECT_SUMMARY.md               ← Site lineup (300+ lines)
```

### 💻 Engine Files
```
engine/
├── engine.py                    ← Main CLI (bulk, build, serve, audit, new)
├── build.py                     ← Build system
├── templates.py                 ← HTML/CSS templates
├── serve.py                     ← Development server
├── audit_seo.py                 ← SEO audit tool
├── logo_gen.py                  ← Logo generation
├── scaffold.py                  ← Site scaffolding
├── make_demo_content.py          ← Demo content
├── layouts.py                   ← Layout variation system (NEW - 600+ lines)
├── config/
│   ├── sites.json               ← Site registry
│   ├── themes.json              ← Color themes (auto-generated)
│   ├── layouts.json             ← Layout assignments (auto-generated)
│   └── layouts.json
└── README.md                    ← Original engine docs
```

### 📊 Configuration Files
```
domains.csv                      ← Master registry (200 cities, Primary Color column)
config/
├── sites.json                   ← 10 site entries
├── themes.json                  ← 10 color themes (auto-generated)
└── layouts.json                 ← 10 layout assignments (auto-generated)
```

### 🏗️ Brand Assets
```
brand/
├── logos/                       ← 200+ city logos (NN_city_garage_door_*.png)
├── photos/                      ← Centralized images (gd-1.jpg through gd-9.jpg)
└── ...                          ← Other brand assets
```

### 📝 Content Structure
```
engine/content/
├── chicopee-ma/                 ← Content for Chicopee site
├── mesa-az/                     ← Content for Mesa site
├── naperville-il/               ← Content for Naperville site
└── ... (8 more cities)
```

### 🌐 Output (After Build)
```
dist/
├── chicopeegaragedoorpros.com/
├── mesagaragedoorco.com/
├── naperville-gd.com/
├── ... (7 more sites)
└── [10 complete websites ready to deploy]
```

---

## Reading Order (Recommended)

### For Quick Start (20 minutes)
1. **QUICK_START.md** - Understand workflow
2. Run: `python engine.py bulk --sheet ../domains.csv`
3. Run: `python engine.py build`
4. Run: `python engine.py serve` (preview)
5. Reference: **QUICK_START.md** "Common Commands" if needed

### For Complete Understanding (1 hour)
1. **DELIVERABLES.md** - What you have
2. **ENGINE_GUIDE.md** - How it all works
3. **LAYOUT_VISUAL_GUIDE.md** - How sites look
4. **ENGINE_UPDATE_SUMMARY.md** - Technical details
5. **PROJECT_SUMMARY.md** - Quick reference

### For Customization (30 minutes)
1. **ENGINE_GUIDE.md** "Customization" section
2. **LAYOUT_VISUAL_GUIDE.md** "How to Customize"
3. Edit `config/layouts.json` or `domains.csv`
4. Run: `python engine.py build`

### For Troubleshooting (10 minutes)
1. **QUICK_START.md** "Troubleshooting Quick Fixes"
2. **ENGINE_GUIDE.md** "Troubleshooting" section
3. Check `engine.py build` output for errors
4. Verify paths (brand/photos/, content/ folders, etc.)

---

## Key Concepts at a Glance

### Color Theming
```
domains.csv (Primary Color: #2563EB)
    ↓ Automatic Generation
config/themes.json
{
  "p": "#2563EB",              // Primary
  "pd": "#1D4ED8",             // Dark variant
  "accent": "#F59E0B",         // Complementary
  "on_accent": "#FFFFFF"       // Text (WCAG guaranteed)
}
    ↓ Applied During Build
dist/<domain>/assets/site.css   // All colors applied
```

**Key File**: ENGINE_GUIDE.md → "Color Theme System"

### Layout Variations
```
get_layout_for_site(index)  // Deterministic rotation
    ↓
config/layouts.json         // Stores assignments
{
  "hero": "banner",
  "services": "featured",
  "testimonials": "carousel",
  "cta": "horizontal",
  "footer": "classic"
}
    ↓ Applied During Build
dist/<domain>/index.html    // Layout applied
```

**Key File**: LAYOUT_VISUAL_GUIDE.md → "Pattern Summary"

### Image Management
```
brand/photos/gd-*.jpg       // Single source
    ↓ Copied During Build
dist/<domain>/assets/photos// Used by all sites
```

**Key File**: ENGINE_GUIDE.md → "Image Management"

### Build Pipeline
```
python engine.py bulk           // Register & generate configs
    ↓
config/sites.json, themes.json, layouts.json created
    ↓
python engine.py build          // Build all sites
    ↓
dist/<domain>/*                 // Sites ready to deploy
```

**Key File**: QUICK_START.md → "One-Command Setup"

---

## Configuration File Reference

### domains.csv
**Format**: CSV with header row
**Columns**: #, Domain, Business Name, City, State, Primary Color
**Example**: 
```
1,chicopeegaragedoorpros.com,Chicopee Garage Door Pros,Chicopee,MA,#0F172A
```
**Where**: Root workspace folder
**Key Section**: ENGINE_GUIDE.md → "Domain Registry"

### config/sites.json
**Format**: JSON array
**Fields**: domain, city, st, brand, theme, layout, port, content, phone, tagline
**Example**:
```json
{
  "domain": "chicopeegaragedoorpros.com",
  "city": "Chicopee",
  "st": "MA",
  "brand": "Chicopee Garage Door Pros",
  "theme": "chicopeegaragedoorpros",
  "port": 8202
}
```
**Where**: engine/config/
**Key Section**: ENGINE_GUIDE.md → "Configuration Reference"

### config/themes.json
**Format**: JSON object with theme entries
**Fields**: p, pd, accent, on_accent, display, body, fonts
**Auto-Generated**: During `python engine.py bulk`
**Where**: engine/config/
**Key Section**: ENGINE_GUIDE.md → "Color Themes"

### config/layouts.json
**Format**: JSON with layouts array
**Fields**: domain, hero, services, testimonials, cta, footer
**Auto-Generated**: During `python engine.py bulk`
**Where**: engine/config/
**Key Section**: LAYOUT_VISUAL_GUIDE.md → "How to Customize"

---

## Common Questions Answered

### Q: How do I build all 10 sites?
**A**: See QUICK_START.md → "One-Command Setup"

### Q: How do I understand the color system?
**A**: See ENGINE_GUIDE.md → "Color Theme System"

### Q: How do I see what the layouts look like?
**A**: See LAYOUT_VISUAL_GUIDE.md → "Site-by-Site Layouts"

### Q: How do I customize a site's layout?
**A**: See LAYOUT_VISUAL_GUIDE.md → "How to Customize"

### Q: How do I change a site's colors?
**A**: See ENGINE_GUIDE.md → "Customization Guide"

### Q: Where are the images stored?
**A**: See DELIVERABLES.md → "Image Centralization"

### Q: How do I deploy to production?
**A**: See QUICK_START.md → "Common Commands" or ENGINE_GUIDE.md → "Deployment"

### Q: What if the build fails?
**A**: See QUICK_START.md → "Troubleshooting" or ENGINE_GUIDE.md → "Troubleshooting"

### Q: What's new in this version?
**A**: See ENGINE_UPDATE_SUMMARY.md → "What's Been Updated"

### Q: Can I use the same layout for all sites?
**A**: Yes, edit config/layouts.json. See LAYOUT_VISUAL_GUIDE.md → "How to Customize"

---

## Command Reference

### Essential Commands
```bash
# Register all 10 sites
python engine.py bulk --sheet ../domains.csv

# Build all sites
python engine.py build

# Preview locally
python engine.py serve
```

**Full Reference**: QUICK_START.md → "Essential Commands" or ENGINE_GUIDE.md → "CLI Reference"

---

## File Sizes & Scope

| File | Lines | Read Time | Purpose |
|------|-------|-----------|---------|
| ENGINE_GUIDE.md | 2000+ | 30 min | Complete reference |
| QUICK_START.md | 400+ | 5 min | Quick cheat sheet |
| LAYOUT_VISUAL_GUIDE.md | 600+ | 15 min | Visual diagrams |
| ENGINE_UPDATE_SUMMARY.md | 500+ | 10 min | Technical summary |
| DELIVERABLES.md | 600+ | 10 min | Project overview |
| PROJECT_SUMMARY.md | 300+ | 5 min | Site lineup |
| **Total** | 5,000+ | 75 min | Complete docs |

---

## Next Steps

1. **Pick your path** (see "Reading Order" section above)
2. **Read the relevant docs** (start with QUICK_START.md)
3. **Run the commands** (bulk → build → serve)
4. **Customize as needed** (colors, layouts, content)
5. **Deploy to production** (copy dist/ to server)

---

## Support Resources

**Still have questions?**

1. **QUICK_START.md** - Fastest answers
2. **ENGINE_GUIDE.md** - Most complete
3. **LAYOUT_VISUAL_GUIDE.md** - Most visual
4. **ENGINE_UPDATE_SUMMARY.md** - Most technical

Each file has:
- Table of contents
- Examples
- Code snippets
- Troubleshooting section

---

## Document Summary Table

| Document | Best For | Length | Time |
|----------|----------|--------|------|
| **QUICK_START.md** | Fast setup & reference | 400 lines | 5 min |
| **ENGINE_GUIDE.md** | Deep understanding | 2000 lines | 30 min |
| **LAYOUT_VISUAL_GUIDE.md** | Visual learners | 600 lines | 15 min |
| **ENGINE_UPDATE_SUMMARY.md** | Technical details | 500 lines | 10 min |
| **DELIVERABLES.md** | Project overview | 600 lines | 10 min |
| **PROJECT_SUMMARY.md** | Quick lookup | 300 lines | 5 min |
| **DOCUMENTATION_INDEX.md** | Navigation | 300 lines | 5 min |

---

## File Map (Visual)

```
garagedoorsites/
│
├── 📚 DOCUMENTATION (What You're Reading)
│   ├── QUICK_START.md              ← Start here (5 min)
│   ├── ENGINE_GUIDE.md             ← Complete guide (30 min)
│   ├── LAYOUT_VISUAL_GUIDE.md       ← Visual reference (15 min)
│   ├── ENGINE_UPDATE_SUMMARY.md     ← What changed (10 min)
│   ├── DELIVERABLES.md             ← What you got (10 min)
│   ├── PROJECT_SUMMARY.md           ← Site lineup (5 min)
│   └── DOCUMENTATION_INDEX.md       ← This file
│
├── 💻 ENGINE (Build System)
│   ├── engine.py                   ← Main CLI
│   ├── layouts.py                  ← Layout system (NEW)
│   ├── build.py, templates.py, serve.py, audit_seo.py
│   ├── config/
│   │   ├── sites.json              ← 10 sites
│   │   ├── themes.json             ← 10 themes (auto)
│   │   └── layouts.json            ← 10 layouts (auto)
│   └── content/                    ← Source content
│
├── 🏗️ BRAND (Assets)
│   ├── logos/                      ← 200+ city logos
│   └── photos/                     ← gd-1.jpg...gd-9.jpg
│
├── 📊 CONFIGURATION
│   └── domains.csv                 ← Master registry
│
└── 🌐 OUTPUT (After Build)
    └── dist/                       ← 10 websites
        ├── chicopeegaragedoorpros.com/
        ├── mesagaragedoorco.com/
        └── ... (8 more)

```

---

## Summary

You have:
- ✅ 10 production-ready sites
- ✅ Automated color theming
- ✅ Layout variations
- ✅ 5,000+ lines of documentation
- ✅ Everything you need to build & deploy

**Start**: Read QUICK_START.md (5 minutes)
**Understand**: Read ENGINE_GUIDE.md (30 minutes)
**Customize**: Follow examples in LAYOUT_VISUAL_GUIDE.md
**Deploy**: Instructions in ENGINE_GUIDE.md

All documentation is here. Everything you need is covered.

**Ready to build? Start with QUICK_START.md →**
