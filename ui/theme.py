import customtkinter as ctk

# Configuration du thème global CustomTkinter
ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("blue")

class Theme:
    # Palette de couleurs Windows 11 Dark Mode Premium
    BG_DARK = "#0F172A"       # Slate 900
    CARD_BG = "#1E293B"       # Slate 800
    CARD_HOVER = "#334155"    # Slate 700
    ACCENT_INDIGO = "#6366F1" # Indigo Primary
    ACCENT_EMERALD = "#10B981"# Emerald Success
    ACCENT_AMBER = "#F59E0B"  # Amber Warning
    ACCENT_ROSE = "#EF4444"   # Rose Error
    
    TEXT_MAIN = "#F8FAFC"     # Slate 50
    TEXT_MUTED = "#94A3B8"    # Slate 400
    BORDER_COLOR = "#475569"  # Slate 600

    # Polices
    FONT_FAMILY = "Segoe UI"
    FONT_TITLE = (FONT_FAMILY, 18, "bold")
    FONT_SUBTITLE = (FONT_FAMILY, 14, "bold")
    FONT_BODY = (FONT_FAMILY, 12)
    FONT_MUTED = (FONT_FAMILY, 11)
    FONT_CODE = ("Consolas", 11)

    # Contraintes plateformes (Caractères max, etc.)
    PLATFORM_CONSTRAINTS = {
        "wordpress": {"name": "WordPress", "icon": "🌐", "max_chars": None, "requires_title": True, "requires_media": False},
        "facebook": {"name": "Facebook", "icon": "📘", "max_chars": 63206, "requires_title": False, "requires_media": False},
        "instagram": {"name": "Instagram", "icon": "📸", "max_chars": 2200, "requires_title": False, "requires_media": True},
        "twitter": {"name": "Twitter / X", "icon": "🐦", "max_chars": 280, "requires_title": False, "requires_media": False},
        "linkedin": {"name": "LinkedIn", "icon": "💼", "max_chars": 3000, "requires_title": False, "requires_media": False}
    }
