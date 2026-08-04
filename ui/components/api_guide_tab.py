import customtkinter as ctk
import webbrowser
from ui.theme import Theme
from core.api_docs_guide import APIDocsGuide

class APIGuideTab(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent, fg_color="transparent")
        self._build_ui()

    def _build_ui(self):
        self.grid_rowconfigure(1, weight=1)
        self.grid_columnconfigure(0, weight=1)

        # En-tête
        lbl_title = ctk.CTkLabel(self, text="📚 Assistant Documentation & Obtention des Clés API (US 4.4)", font=Theme.FONT_TITLE, text_color=Theme.TEXT_MAIN, anchor="w")
        lbl_title.grid(row=0, column=0, sticky="ew", padx=15, pady=(15, 10))

        # Zone scrollable
        scroll_box = ctk.CTkScrollableFrame(self, fg_color=Theme.CARD_BG, corner_radius=12)
        scroll_box.grid(row=1, column=0, sticky="nsew", padx=15, pady=(0, 15))
        scroll_box.grid_columnconfigure(0, weight=1)

        intro_lbl = ctk.CTkLabel(
            scroll_box,
            text="Retrouvez ci-dessous les instructions pas-à-pas et les liens officiels pour configurer facilement les identifiants de vos comptes sans vous perdre dans la documentation.",
            font=Theme.FONT_BODY,
            text_color=Theme.TEXT_MUTED,
            anchor="w",
            justify="left",
            wraplength=700
        )
        intro_lbl.pack(fill="x", padx=15, pady=(15, 15))

        # Affichage des cartes de guides
        all_guides = APIDocsGuide.get_all_guides()
        for key, guide in all_guides.items():
            self._render_guide_card(scroll_box, guide)

    def _render_guide_card(self, parent, guide):
        card = ctk.CTkFrame(parent, fg_color="#0F172A", corner_radius=10, border_color=Theme.BORDER_COLOR, border_width=1)
        card.pack(fill="x", padx=15, pady=8)
        card.grid_columnconfigure(0, weight=1)

        # Header Carte
        h_frame = ctk.CTkFrame(card, fg_color="transparent")
        h_frame.pack(fill="x", padx=15, pady=(12, 5))

        lbl_icon_title = ctk.CTkLabel(h_frame, text=f"{guide['icon']} {guide['title']}", font=Theme.FONT_SUBTITLE, text_color=Theme.TEXT_MAIN)
        lbl_icon_title.pack(side="left")

        btn_link = ctk.CTkButton(
            h_frame,
            text="🌐 Consulter Portail Officiel",
            font=Theme.FONT_MUTED,
            fg_color=Theme.ACCENT_INDIGO,
            hover_color="#4F46E5",
            height=28,
            command=lambda u=guide['official_url']: webbrowser.open(u)
        )
        btn_link.pack(side="right")

        # Résumé
        lbl_sum = ctk.CTkLabel(card, text=guide['summary'], font=Theme.FONT_MUTED, text_color="#CBD5E1", anchor="w", justify="left")
        lbl_sum.pack(fill="x", padx=15, pady=(0, 10))

        # Étapes pas-à-pas
        steps_frame = ctk.CTkFrame(card, fg_color="#1E293B", corner_radius=6)
        steps_frame.pack(fill="x", padx=15, pady=(0, 12))

        for step in guide['steps']:
            lbl_step = ctk.CTkLabel(steps_frame, text=step, font=Theme.FONT_BODY, text_color=Theme.TEXT_MAIN, anchor="w", justify="left", wraplength=650)
            lbl_step.pack(fill="x", padx=12, pady=4)
