#!/usr/bin/env python
"""Layout variations for garage door sites.

Each site gets a unique layout rotation across:
- Hero styles (banner, split, overlay, minimal)
- Service card layouts (grid, carousel, list, featured)
- Testimonial displays (carousel, grid, sidebar, featured)
- CTA sections (horizontal, stacked, card, minimal)
- Footer styles (classic, minimal, compact)

This ensures all 10+ sites have distinct visual presentations while sharing core CSS.
"""

LAYOUT_STYLES = {
    "hero": [
        "banner",      # Full-width image with overlay text
        "split",       # Image left, text right
        "overlay",     # Text over top-left, minimal gradient
        "minimal",     # No background image, bold typography
    ],
    "services": [
        "grid",        # 3-column card grid
        "carousel",    # Horizontal scroll cards
        "list",        # Vertical list with icons
        "featured",    # Large featured card + smaller grid
    ],
    "testimonials": [
        "carousel",    # Horizontal rotating testimonials
        "grid",        # 2-3 column grid
        "sidebar",     # Quote left, byline right
        "featured",    # Large pull quote + smaller list
    ],
    "cta": [
        "horizontal",  # Side-by-side image + text
        "stacked",     # Vertical stack
        "card",        # Centered card with border
        "minimal",     # Text-only with link
    ],
    "footer": [
        "classic",     # Multi-column with logo + links
        "compact",     # Single column, minimal
        "minimal",     # Footer bar with links only
        "boutique",    # Large footer branding
    ],
}

def get_layout_for_site(site_index):
    """Rotate through layout combinations based on site index.
    
    Args:
        site_index: Integer (0-based) of the site in the list
        
    Returns:
        dict: Layout choice for each section
    """
    num_layouts = len(LAYOUT_STYLES["hero"])
    
    return {
        "hero": LAYOUT_STYLES["hero"][site_index % num_layouts],
        "services": LAYOUT_STYLES["services"][(site_index + 1) % len(LAYOUT_STYLES["services"])],
        "testimonials": LAYOUT_STYLES["testimonials"][(site_index + 2) % len(LAYOUT_STYLES["testimonials"])],
        "cta": LAYOUT_STYLES["cta"][(site_index + 3) % len(LAYOUT_STYLES["cta"])],
        "footer": LAYOUT_STYLES["footer"][(site_index + 4) % len(LAYOUT_STYLES["footer"])],
    }


# Hero layout CSS generators
def hero_banner(css_vars):
    """Full-width background image with overlay."""
    return f"""
.hero {{
    position: relative;
    min-height: 90vh;
    display: flex;
    align-items: center;
    justify-content: center;
    background: linear-gradient(135deg, var(--p), var(--pd));
    color: white;
    overflow: hidden;
}}
.hero img {{
    position: absolute;
    inset: 0;
    width: 100%;
    height: 100%;
    object-fit: cover;
    opacity: 0.7;
    z-index: -1;
}}
.hero::after {{
    content: '';
    position: absolute;
    inset: 0;
    background: rgba(0, 0, 0, 0.35);
    z-index: 0;
}}
.hero__content {{
    position: relative;
    z-index: 1;
    text-align: center;
    max-width: 800px;
    padding: 0 32px;
}}
.hero h1 {{
    font-size: clamp(2.2rem, 5vw, 4rem);
    margin-bottom: 20px;
    font-weight: 900;
}}
.hero p {{
    font-size: 1.1rem;
    margin-bottom: 30px;
    opacity: 0.95;
}}
"""

def hero_split(css_vars):
    """Image left, content right."""
    return f"""
.hero {{
    display: grid;
    grid-template-columns: 1fr 1fr;
    align-items: center;
    min-height: 85vh;
    gap: 0;
}}
.hero img {{
    width: 100%;
    height: 100%;
    object-fit: cover;
    order: -1;
}}
.hero__content {{
    padding: 60px;
    background: white;
}}
.hero h1 {{
    font-size: clamp(2rem, 4vw, 3.2rem);
    margin-bottom: 20px;
    color: var(--ink);
}}
.hero p {{
    color: #666;
    font-size: 1.05rem;
    margin-bottom: 30px;
}}
@media(max-width: 900px) {{
    .hero {{ grid-template-columns: 1fr; }}
    .hero img {{ order: 0; height: 40vh; }}
    .hero__content {{ padding: 40px; }}
}}
"""

def hero_overlay(css_vars):
    """Text overlay in top-left, minimal gradient."""
    return f"""
.hero {{
    position: relative;
    min-height: 85vh;
    display: flex;
    align-items: flex-start;
    padding-top: 100px;
    color: white;
    overflow: hidden;
}}
.hero img {{
    position: absolute;
    inset: 0;
    width: 100%;
    height: 100%;
    object-fit: cover;
    z-index: -1;
}}
.hero::after {{
    content: '';
    position: absolute;
    inset: 0;
    background: linear-gradient(135deg, rgba(0,0,0,0.4) 0%, transparent 50%);
    z-index: 0;
}}
.hero__content {{
    position: relative;
    z-index: 1;
    max-width: 600px;
    margin: 0 32px;
}}
.hero h1 {{
    font-size: clamp(2.2rem, 5vw, 3.8rem);
    margin-bottom: 16px;
    font-weight: 900;
}}
.hero p {{
    font-size: 1.08rem;
    margin-bottom: 30px;
    max-width: 500px;
}}
"""

def hero_minimal(css_vars):
    """Bold typography, no background image."""
    return f"""
.hero {{
    background: linear-gradient(135deg, var(--p) 0%, var(--pd) 100%);
    color: white;
    padding: 120px 32px;
    text-align: center;
}}
.hero__content {{
    max-width: 900px;
    margin: 0 auto;
}}
.hero h1 {{
    font-size: clamp(2.4rem, 6vw, 4.5rem);
    margin-bottom: 24px;
    font-weight: 900;
    letter-spacing: -0.02em;
}}
.hero p {{
    font-size: 1.2rem;
    margin-bottom: 40px;
    max-width: 700px;
    margin-left: auto;
    margin-right: auto;
    opacity: 0.95;
}}
"""


# Service cards layout CSS
def services_grid(css_vars):
    """3-column card grid."""
    return f"""
.services {{
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
    gap: 28px;
    padding: 80px 0;
}}
.service-card {{
    background: white;
    border-radius: 12px;
    overflow: hidden;
    box-shadow: 0 4px 12px rgba(0,0,0,0.08);
    transition: transform 0.3s, box-shadow 0.3s;
}}
.service-card:hover {{
    transform: translateY(-8px);
    box-shadow: 0 12px 24px rgba(0,0,0,0.15);
}}
.service-card img {{
    width: 100%;
    height: 200px;
    object-fit: cover;
}}
.service-card__content {{
    padding: 24px;
}}
.service-card h3 {{
    font-size: 1.25rem;
    margin-bottom: 12px;
    color: var(--p);
}}
.service-card p {{
    color: #666;
    font-size: 0.95rem;
    line-height: 1.6;
}}
"""

def services_list(css_vars):
    """Vertical list with icons."""
    return f"""
.services {{
    display: flex;
    flex-direction: column;
    gap: 24px;
    padding: 80px 0;
}}
.service-card {{
    display: grid;
    grid-template-columns: 80px 1fr;
    gap: 24px;
    align-items: center;
    padding: 30px;
    background: #f9f9f9;
    border-left: 4px solid var(--p);
    transition: background 0.3s;
}}
.service-card:hover {{
    background: #f0f0f0;
}}
.service-card__icon {{
    width: 80px;
    height: 80px;
    border-radius: 50%;
    background: var(--p);
    color: white;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 2.5rem;
}}
.service-card h3 {{
    font-size: 1.35rem;
    margin-bottom: 8px;
    color: #333;
}}
.service-card p {{
    color: #666;
    margin: 0;
}}
"""

def services_featured(css_vars):
    """One large featured card + smaller grid."""
    return f"""
.services {{
    padding: 80px 0;
}}
.services__featured {{
    background: linear-gradient(135deg, var(--p), var(--pd));
    color: white;
    border-radius: 16px;
    overflow: hidden;
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 0;
    margin-bottom: 60px;
}}
.services__featured img {{
    width: 100%;
    height: 100%;
    object-fit: cover;
    order: -1;
}}
.services__featured-content {{
    padding: 50px;
    display: flex;
    flex-direction: column;
    justify-content: center;
}}
.services__featured h3 {{
    font-size: 2.2rem;
    margin-bottom: 16px;
}}
.services__featured p {{
    font-size: 1.05rem;
    opacity: 0.95;
    margin-bottom: 24px;
}}
.services__grid {{
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: 24px;
}}
.service-card {{
    background: white;
    padding: 28px;
    border-radius: 8px;
    box-shadow: 0 2px 8px rgba(0,0,0,0.06);
}}
.service-card h3 {{
    color: var(--p);
    margin-bottom: 12px;
}}
@media(max-width: 1000px) {{
    .services__featured {{ grid-template-columns: 1fr; }}
    .services__grid {{ grid-template-columns: 1fr 1fr; }}
}}
"""

# Testimonial layouts
def testimonials_carousel(css_vars):
    """Horizontal rotating testimonials."""
    return f"""
.testimonials {{
    padding: 80px 0;
    background: #f9f9f9;
}}
.testimonials__carousel {{
    display: grid;
    gap: 32px;
    overflow-x: auto;
    padding-bottom: 16px;
}}
.testimonial {{
    background: white;
    padding: 32px;
    border-radius: 12px;
    min-width: 350px;
    box-shadow: 0 4px 12px rgba(0,0,0,0.08);
}}
.testimonial__stars {{
    color: var(--p);
    font-size: 1.4rem;
    margin-bottom: 16px;
}}
.testimonial__text {{
    font-size: 1.1rem;
    margin-bottom: 20px;
    color: #333;
    line-height: 1.6;
}}
.testimonial__author {{
    font-weight: 600;
    color: var(--p);
}}
"""

def testimonials_grid(css_vars):
    """2-column testimonial grid."""
    return f"""
.testimonials {{
    padding: 80px 0;
    background: white;
}}
.testimonials__grid {{
    display: grid;
    grid-template-columns: repeat(2, 1fr);
    gap: 40px;
}}
.testimonial {{
    padding: 32px;
    border: 1px solid #e0e0e0;
    border-radius: 8px;
}}
.testimonial__stars {{
    color: var(--p);
    margin-bottom: 16px;
}}
.testimonial__text {{
    font-style: italic;
    font-size: 1.05rem;
    margin-bottom: 20px;
}}
.testimonial__author {{
    font-weight: 700;
    color: #333;
}}
@media(max-width: 768px) {{
    .testimonials__grid {{ grid-template-columns: 1fr; }}
}}
"""


# CTA section layouts
def cta_horizontal(css_vars):
    """Side-by-side image + CTA text."""
    return f"""
.cta {{
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 0;
    align-items: center;
    background: white;
}}
.cta img {{
    width: 100%;
    height: 100%;
    object-fit: cover;
}}
.cta__content {{
    padding: 60px;
    background: var(--p);
    color: white;
}}
.cta h2 {{
    font-size: 2rem;
    margin-bottom: 16px;
}}
.cta p {{
    font-size: 1.05rem;
    margin-bottom: 30px;
}}
@media(max-width: 900px) {{
    .cta {{ grid-template-columns: 1fr; }}
    .cta img {{ height: 300px; }}
}}
"""

def cta_card(css_vars):
    """Centered card with border."""
    return f"""
.cta {{
    padding: 80px 32px;
    text-align: center;
    background: white;
}}
.cta__card {{
    max-width: 600px;
    margin: 0 auto;
    padding: 50px;
    border: 2px solid var(--p);
    border-radius: 12px;
    background: #f9f9f9;
}}
.cta h2 {{
    font-size: 2rem;
    margin-bottom: 20px;
    color: var(--p);
}}
.cta p {{
    font-size: 1.05rem;
    color: #666;
    margin-bottom: 30px;
}}
.cta__btn {{
    background: var(--p);
    color: white;
    padding: 16px 40px;
    border-radius: 8px;
    font-size: 1rem;
    font-weight: 600;
    border: none;
    cursor: pointer;
    transition: background 0.3s;
}}
.cta__btn:hover {{
    background: var(--pd);
}}
"""

def cta_minimal(css_vars):
    """Text-only CTA."""
    return f"""
.cta {{
    padding: 60px 32px;
    text-align: center;
    background: linear-gradient(135deg, var(--p), var(--pd));
    color: white;
}}
.cta__content {{
    max-width: 700px;
    margin: 0 auto;
}}
.cta h2 {{
    font-size: 2.2rem;
    margin-bottom: 16px;
}}
.cta p {{
    font-size: 1.1rem;
    margin-bottom: 32px;
    opacity: 0.95;
}}
"""


# Footer layouts
def footer_classic(css_vars):
    """Multi-column footer with branding."""
    return f"""
footer {{
    background: var(--ink, #1a1a1a);
    color: white;
    padding: 60px 32px 20px;
}}
.footer__cols {{
    display: grid;
    grid-template-columns: 2fr 1fr 1fr 1fr;
    gap: 40px;
    max-width: 1200px;
    margin: 0 auto 40px;
}}
.footer__col h4 {{
    font-size: 0.85rem;
    text-transform: uppercase;
    letter-spacing: 0.1em;
    margin-bottom: 16px;
    color: var(--p);
}}
.footer__col a {{
    display: block;
    padding: 6px 0;
    color: #aaa;
    text-decoration: none;
    font-size: 0.95rem;
}}
.footer__col a:hover {{
    color: white;
}}
.footer__bottom {{
    text-align: center;
    padding-top: 20px;
    border-top: 1px solid #333;
    font-size: 0.9rem;
    color: #777;
}}
"""

def footer_minimal(css_vars):
    """Compact footer bar."""
    return f"""
footer {{
    background: var(--ink, #1a1a1a);
    color: #aaa;
    padding: 30px 32px;
}}
.footer__content {{
    max-width: 1200px;
    margin: 0 auto;
    display: flex;
    justify-content: space-between;
    align-items: center;
    flex-wrap: wrap;
    gap: 20px;
}}
footer a {{
    color: #ccc;
    margin: 0 15px;
    font-size: 0.95rem;
    text-decoration: none;
}}
footer a:hover {{
    color: white;
}}
"""


def get_layout_css(layout_dict):
    """Generate CSS for all layout components.
    
    Args:
        layout_dict: dict from get_layout_for_site()
        
    Returns:
        dict: CSS strings for each section
    """
    css_vars = {}  # For future color variables
    
    hero_func = {
        "banner": hero_banner,
        "split": hero_split,
        "overlay": hero_overlay,
        "minimal": hero_minimal,
    }[layout_dict["hero"]]
    
    services_func = {
        "grid": services_grid,
        "list": services_list,
        "featured": services_featured,
        "carousel": services_grid,  # Fallback
    }[layout_dict["services"]]
    
    testimonials_func = {
        "carousel": testimonials_carousel,
        "grid": testimonials_grid,
        "sidebar": testimonials_grid,  # Simplified
        "featured": testimonials_carousel,
    }[layout_dict["testimonials"]]
    
    cta_func = {
        "horizontal": cta_horizontal,
        "stacked": cta_minimal,
        "card": cta_card,
        "minimal": cta_minimal,
    }[layout_dict["cta"]]
    
    footer_func = {
        "classic": footer_classic,
        "compact": footer_minimal,
        "minimal": footer_minimal,
        "boutique": footer_classic,
    }[layout_dict["footer"]]
    
    return {
        "hero": hero_func(css_vars),
        "services": services_func(css_vars),
        "testimonials": testimonials_func(css_vars),
        "cta": cta_func(css_vars),
        "footer": footer_func(css_vars),
    }
