import customtkinter as ctk
from ui.theme import Theme

class PreviewTab(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent, fg_color="transparent")
        self._build_ui()

    def _build_ui(self):
        self.grid_rowconfigure(1, weight=1)
        self.grid_columnconfigure(0, weight=1)

        # Entête
        lbl_header = ctk.CTkLabel(self, text="👁️ Aperçu WYSIWYG Réaliste des Publications", font=Theme.FONT_TITLE, text_color=Theme.TEXT_MAIN, anchor="w")
        lbl_header.grid(row=0, column=0, sticky="ew", padx=15, pady=(15, 5))

        # Tabview pour sélectionner la plateforme à prévisualiser
        self.tabview = ctk.CTkTabview(self, corner_radius=12)
        self.tabview.grid(row=1, column=0, sticky="nsew", padx=15, pady=(0, 15))

        self.tab_wp = self.tabview.add("🌐 Article WordPress")
        self.tab_insta = self.tabview.add("📸 Feed Instagram")
        self.tab_tw = self.tabview.add("🐦 Post Twitter / X")
        self.tab_li = self.tabview.add("💼 Post LinkedIn")
        self.tab_fb = self.tabview.add("📘 Post Facebook")

        # Initialiser la structure de chaque aperçu
        self._setup_wp_preview(self.tab_wp)
        self._setup_insta_preview(self.tab_insta)
        self._setup_tw_preview(self.tab_tw)
        self._setup_li_preview(self.tab_li)
        self._setup_fb_preview(self.tab_fb)

    def _setup_wp_preview(self, tab):
        tab.grid_columnconfigure(0, weight=1)
        tab.grid_rowconfigure(0, weight=1)

        # Card de style Article de Blog
        card = ctk.CTkScrollableFrame(tab, fg_color="#1E293B", corner_radius=10, border_color=Theme.BORDER_COLOR, border_width=1)
        card.grid(row=0, column=0, sticky="nsew", padx=20, pady=20)
        card.grid_columnconfigure(0, weight=1)

        self.wp_preview_title = ctk.CTkLabel(card, text="Titre de l'article de blog", font=("Segoe UI", 22, "bold"), text_color="#F8FAFC", anchor="w", justify="left")
        self.wp_preview_title.pack(fill="x", padx=20, pady=(20, 5))

        self.wp_preview_meta = ctk.CTkLabel(card, text="Publié par l'Auteur • Blog WordPress", font=Theme.FONT_MUTED, text_color=Theme.TEXT_MUTED, anchor="w")
        self.wp_preview_meta.pack(fill="x", padx=20, pady=(0, 15))

        self.wp_preview_image_lbl = ctk.CTkLabel(card, text="[Aucune image à la une]", font=Theme.FONT_MUTED, text_color=Theme.TEXT_MUTED, fg_color="#334155", corner_radius=6, height=120)
        self.wp_preview_image_lbl.pack(fill="x", padx=20, pady=(0, 15))

        self.wp_preview_body = ctk.CTkLabel(card, text="Le contenu de l'article apparaîtra ici...", font=("Segoe UI", 13), text_color="#E2E8F0", anchor="nw", justify="left", wraplength=700)
        self.wp_preview_body.pack(fill="both", expand=True, padx=20, pady=(0, 20))

    def _setup_insta_preview(self, tab):
        tab.grid_columnconfigure(0, weight=1)
        tab.grid_rowconfigure(0, weight=1)

        # Simulation d'un post Instagram Mobile
        card = ctk.CTkFrame(tab, fg_color="#000000", corner_radius=16, border_color="#334155", border_width=2, width=380)
        card.grid(row=0, column=0, pady=20)
        card.pack_propagate(False)

        # Header Insta
        inst_header = ctk.CTkFrame(card, fg_color="#121212", height=50)
        inst_header.pack(fill="x")
        lbl_avatar = ctk.CTkLabel(inst_header, text="📷  votre_compte_insta", font=("Segoe UI", 12, "bold"), text_color="#FFFFFF")
        lbl_avatar.pack(side="left", padx=15, pady=10)

        # Image box
        self.insta_preview_img = ctk.CTkLabel(card, text="📸 Format Carré 1:1 Instagram", font=Theme.FONT_MUTED, text_color="#999999", fg_color="#262626", height=240)
        self.insta_preview_img.pack(fill="x")

        # Icons Bar
        icons_bar = ctk.CTkLabel(card, text="❤️  💬  ✈️   🔖", font=("Segoe UI", 14), text_color="#FFFFFF", anchor="w")
        icons_bar.pack(fill="x", padx=15, pady=(8, 2))

        # Caption
        self.insta_preview_text = ctk.CTkLabel(card, text="Légende Instagram...", font=("Segoe UI", 11), text_color="#E5E5E5", anchor="nw", justify="left", wraplength=340)
        self.insta_preview_text.pack(fill="both", expand=True, padx=15, pady=(2, 10))

    def _setup_tw_preview(self, tab):
        tab.grid_columnconfigure(0, weight=1)
        tab.grid_rowconfigure(0, weight=1)

        card = ctk.CTkFrame(tab, fg_color="#15202B", corner_radius=12, border_color="#38444D", border_width=1, width=480)
        card.grid(row=0, column=0, pady=20)
        card.pack_propagate(False)

        # Header Tweet
        tw_header = ctk.CTkFrame(card, fg_color="transparent")
        tw_header.pack(fill="x", padx=15, pady=(15, 5))

        lbl_user = ctk.CTkLabel(tw_header, text="🐦 Mon Compte  @mon_handle_x", font=("Segoe UI", 13, "bold"), text_color="#FFFFFF")
        lbl_user.pack(side="left")

        self.tw_preview_text = ctk.CTkLabel(card, text="Contenu du tweet...", font=("Segoe UI", 13), text_color="#FFFFFF", anchor="nw", justify="left", wraplength=440)
        self.tw_preview_text.pack(fill="both", expand=True, padx=15, pady=10)

        # Tweet Actions Bar
        tw_actions = ctk.CTkLabel(card, text="💬 12   🔄 4   ❤️ 89   📊 1.2k", font=("Segoe UI", 11), text_color="#8899A6", anchor="w")
        tw_actions.pack(fill="x", padx=15, pady=(0, 15))

    def _setup_li_preview(self, tab):
        tab.grid_columnconfigure(0, weight=1)
        tab.grid_rowconfigure(0, weight=1)

        card = ctk.CTkFrame(tab, fg_color="#1D2226", corner_radius=8, border_color="#38434F", border_width=1, width=520)
        card.grid(row=0, column=0, pady=20)
        card.pack_propagate(False)

        # Header LinkedIn
        li_header = ctk.CTkFrame(card, fg_color="transparent")
        li_header.pack(fill="x", padx=15, pady=(15, 5))
        lbl_user = ctk.CTkLabel(li_header, text="💼 Mon Profil Professionnel • 1er", font=("Segoe UI", 13, "bold"), text_color="#FFFFFF")
        lbl_user.pack(side="left")

        self.li_preview_text = ctk.CTkLabel(card, text="Post LinkedIn...", font=("Segoe UI", 12), text_color="#E0E0E0", anchor="nw", justify="left", wraplength=480)
        self.li_preview_text.pack(fill="both", expand=True, padx=15, pady=10)

        # LinkedIn Actions
        li_actions = ctk.CTkLabel(card, text="👍 J'aime   💬 Commenter   🔄 Partager   📨 Envoyer", font=("Segoe UI", 11), text_color="#A0A0A0", anchor="w")
        li_actions.pack(fill="x", padx=15, pady=(0, 15))

    def _setup_fb_preview(self, tab):
        tab.grid_columnconfigure(0, weight=1)
        tab.grid_rowconfigure(0, weight=1)

        card = ctk.CTkFrame(tab, fg_color="#242526", corner_radius=8, border_color="#3E4042", border_width=1, width=500)
        card.grid(row=0, column=0, pady=20)
        card.pack_propagate(False)

        fb_header = ctk.CTkFrame(card, fg_color="transparent")
        fb_header.pack(fill="x", padx=15, pady=(15, 5))
        lbl_user = ctk.CTkLabel(fb_header, text="📘 Ma Page Facebook", font=("Segoe UI", 13, "bold"), text_color="#E4E6EB")
        lbl_user.pack(side="left")

        self.fb_preview_text = ctk.CTkLabel(card, text="Post Facebook...", font=("Segoe UI", 13), text_color="#E4E6EB", anchor="nw", justify="left", wraplength=460)
        self.fb_preview_text.pack(fill="both", expand=True, padx=15, pady=10)

        fb_actions = ctk.CTkLabel(card, text="👍 J'aime   💬 Commenter   ➡️ Partager", font=("Segoe UI", 12), text_color="#B0B3B8", anchor="w")
        fb_actions.pack(fill="x", padx=15, pady=(0, 15))

    def update_previews(self, contents):
        """Met à jour instantanément les aperçus à partir du contenu transmis."""
        wp_title = contents.get("wordpress_title") or "Titre de votre article"
        wp_body = contents.get("wordpress") or contents.get("base") or "Le contenu de votre article apparaîtra ici..."
        
        self.wp_preview_title.configure(text=wp_title)
        self.wp_preview_body.configure(text=wp_body)

        img_path = contents.get("featured_image")
        if img_path:
            filename = img_path.split("/")[-1].split("\\")[-1]
            self.wp_preview_image_lbl.configure(text=f"🖼️ Image sélectionnée : {filename}")
            self.insta_preview_img.configure(text=f"🖼️ {filename}")
        else:
            self.wp_preview_image_lbl.configure(text="[Aucune image à la une]")
            self.insta_preview_img.configure(text="📸 Format Carré 1:1 Instagram")

        # Mettre à jour les aperçus sociaux avec le contenu décliné ou de base
        fb_t = contents.get("facebook") or contents.get("base") or "Votre post Facebook apparaîtra ici..."
        insta_t = contents.get("instagram") or contents.get("base") or "Votre légende Instagram apparaîtra ici..."
        tw_t = contents.get("twitter") or contents.get("base") or "Votre tweet apparaîtra ici..."
        li_t = contents.get("linkedin") or contents.get("base") or "Votre post LinkedIn apparaîtra ici..."

        self.fb_preview_text.configure(text=fb_t)
        self.insta_preview_text.configure(text=insta_t)
        self.tw_preview_text.configure(text=tw_t)
        self.li_preview_text.configure(text=li_t)
