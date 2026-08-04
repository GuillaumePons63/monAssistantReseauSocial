import customtkinter as ctk
from tkinter import filedialog, messagebox
from ui.theme import Theme

class EditorTab(ctk.CTkFrame):
    def __init__(self, parent, lm_client, wp_client, config_mgr, on_content_change_cb=None):
        super().__init__(parent, fg_color="transparent")
        self.lm_client = lm_client
        self.wp_client = wp_client
        self.config_mgr = config_mgr
        self.on_content_change_cb = on_content_change_cb

        # Dictionnaire pour stocker les contenus par plateforme
        self.content_by_platform = {
            "base": "",
            "wordpress_title": "",
            "wordpress": "",
            "facebook": "",
            "instagram": "",
            "twitter": "",
            "linkedin": ""
        }
        self.featured_image_path = None

        self._build_ui()

    def _build_ui(self):
        # Grille principale : 2 colonnes (Gauche: Éditeur direct, Droite: Actions IA & Métadonnées)
        self.grid_columnconfigure(0, weight=3)
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        # --- COLONNE GAUCHE : ÉDITEUR DIRECT AVEC ONGLETS ---
        left_frame = ctk.CTkFrame(self, fg_color=Theme.CARD_BG, corner_radius=12)
        left_frame.grid(row=0, column=0, sticky="nsew", padx=(0, 10), pady=10)
        left_frame.grid_rowconfigure(1, weight=1)
        left_frame.grid_columnconfigure(0, weight=1)

        # En-tête avec titre
        header_frame = ctk.CTkFrame(left_frame, fg_color="transparent")
        header_frame.grid(row=0, column=0, sticky="ew", padx=15, pady=(15, 5))
        
        lbl_title = ctk.CTkLabel(header_frame, text="✍️ Éditeur Direct de Publications", font=Theme.FONT_TITLE, text_color=Theme.TEXT_MAIN)
        lbl_title.pack(side="left")

        # Tabview pour basculer entre Base et les déclinaisons par réseau (US 2.1)
        self.tabview = ctk.CTkTabview(left_frame, corner_radius=8, command=self._on_tab_change)
        self.tabview.grid(row=1, column=0, sticky="nsew", padx=15, pady=(0, 10))

        self.tab_base = self.tabview.add("📝 Message de base")
        self.tab_wp = self.tabview.add("🌐 WordPress")
        self.tab_fb = self.tabview.add("📘 Facebook")
        self.tab_insta = self.tabview.add("📸 Instagram")
        self.tab_tw = self.tabview.add("🐦 Twitter / X")
        self.tab_li = self.tabview.add("💼 LinkedIn")

        # Contenu Onglet Base
        self._setup_base_tab(self.tab_base)

        # Contenu Onglet WordPress
        self._setup_wordpress_tab(self.tab_wp)

        # Contenu Onglets Réseaux Sociaux
        self.platform_editors = {}
        self._setup_platform_tab(self.tab_fb, "facebook")
        self._setup_platform_tab(self.tab_insta, "instagram")
        self._setup_platform_tab(self.tab_tw, "twitter")
        self._setup_platform_tab(self.tab_li, "linkedin")

        # --- COLONNE DROITE : PANNEAU ACTIONS IA & CONTRAINTES ---
        right_frame = ctk.CTkFrame(self, fg_color=Theme.CARD_BG, corner_radius=12)
        right_frame.grid(row=0, column=1, sticky="nsew", padx=(0, 0), pady=10)
        right_frame.grid_columnconfigure(0, weight=1)

        # Titre Panneau IA
        lbl_ia = ctk.CTkLabel(right_frame, text="🤖 Actions IA (LM Studio)", font=Theme.FONT_SUBTITLE, text_color=Theme.TEXT_MAIN)
        lbl_ia.pack(padx=15, pady=(15, 10), anchor="w")

        # Bouton Principal Générer Déclinaisons
        btn_generate_all = ctk.CTkButton(
            right_frame,
            text="✨ Décliner sur tous les réseaux",
            font=(Theme.FONT_FAMILY, 12, "bold"),
            fg_color=Theme.ACCENT_INDIGO,
            hover_color="#4F46E5",
            height=40,
            command=self._generate_all_adaptations
        )
        btn_generate_all.pack(padx=15, pady=5, fill="x")

        # Petits boutons d'actions IA rapides (US 1.3, US 1.4)
        ia_actions_frame = ctk.CTkFrame(right_frame, fg_color="transparent")
        ia_actions_frame.pack(padx=15, pady=10, fill="x")

        btn_shorten = ctk.CTkButton(ia_actions_frame, text="⚡ Raccourcir", fg_color="#334155", hover_color="#475569", command=lambda: self._apply_ia_action("shorten"))
        btn_shorten.pack(pady=3, fill="x")

        btn_pro = ctk.CTkButton(ia_actions_frame, text="💼 Ton Professionnel", fg_color="#334155", hover_color="#475569", command=lambda: self._apply_ia_action("tone_pro"))
        btn_pro.pack(pady=3, fill="x")

        btn_correct = ctk.CTkButton(ia_actions_frame, text="✏️ Corriger l'orthographe", fg_color="#334155", hover_color="#475569", command=lambda: self._apply_ia_action("correct"))
        btn_correct.pack(pady=3, fill="x")

        btn_hashtags = ctk.CTkButton(ia_actions_frame, text="🏷️ Suggérer Hashtags", fg_color="#334155", hover_color="#475569", command=lambda: self._apply_ia_action("hashtags"))
        btn_hashtags.pack(pady=3, fill="x")

        # Séparateur
        ctk.CTkFrame(right_frame, height=2, fg_color=Theme.BORDER_COLOR).pack(fill="x", padx=15, pady=15)

        # Section Media WordPress / Publication
        lbl_wp_action = ctk.CTkLabel(right_frame, text="🌐 Actions WordPress", font=Theme.FONT_SUBTITLE, text_color=Theme.TEXT_MAIN)
        lbl_wp_action.pack(padx=15, pady=(0, 10), anchor="w")

        self.btn_select_media = ctk.CTkButton(
            right_frame,
            text="🖼️ Image à la une",
            fg_color="#334155",
            hover_color="#475569",
            command=self._select_featured_image
        )
        self.btn_select_media.pack(padx=15, pady=5, fill="x")

        self.lbl_media_status = ctk.CTkLabel(right_frame, text="Aucune image sélectionnée", font=Theme.FONT_MUTED, text_color=Theme.TEXT_MUTED)
        self.lbl_media_status.pack(padx=15, pady=(0, 10))

        # Bouton Publier WordPress (Priorité n°1)
        btn_publish_wp = ctk.CTkButton(
            right_frame,
            text="🚀 Publier sur WordPress",
            font=(Theme.FONT_FAMILY, 13, "bold"),
            fg_color=Theme.ACCENT_EMERALD,
            hover_color="#059669",
            height=42,
            command=lambda: self._publish_to_wordpress(status="publish")
        )
        btn_publish_wp.pack(padx=15, pady=5, fill="x")

        btn_draft_wp = ctk.CTkButton(
            right_frame,
            text="📝 Enregistrer Brouillon WP",
            font=Theme.FONT_BODY,
            fg_color="#475569",
            hover_color="#64748B",
            command=lambda: self._publish_to_wordpress(status="draft")
        )
        btn_draft_wp.pack(padx=15, pady=5, fill="x")

    def _setup_base_tab(self, tab):
        tab.grid_rowconfigure(1, weight=1)
        tab.grid_columnconfigure(0, weight=1)

        lbl_desc = ctk.CTkLabel(tab, text="Saisissez ici le texte source ou le sujet principal à partir duquel l'IA générera les versions déclinées :", font=Theme.FONT_MUTED, text_color=Theme.TEXT_MUTED, anchor="w")
        lbl_desc.grid(row=0, column=0, sticky="ew", pady=(5, 5))

        self.txt_base = ctk.CTkTextbox(tab, font=Theme.FONT_BODY, corner_radius=6, border_color=Theme.BORDER_COLOR, border_width=1)
        self.txt_base.grid(row=1, column=0, sticky="nsew")
        self.txt_base.bind("<KeyRelease>", self._on_text_change)

    def _setup_wordpress_tab(self, tab):
        tab.grid_rowconfigure(3, weight=1)
        tab.grid_columnconfigure(0, weight=1)

        lbl_t = ctk.CTkLabel(tab, text="Titre de l'article WordPress :", font=Theme.FONT_BODY, text_color=Theme.TEXT_MAIN, anchor="w")
        lbl_t.grid(row=0, column=0, sticky="ew", pady=(5, 2))

        self.entry_wp_title = ctk.CTkEntry(tab, font=Theme.FONT_SUBTITLE, placeholder_text="Titre de votre article...", border_color=Theme.BORDER_COLOR)
        self.entry_wp_title.grid(row=1, column=0, sticky="ew", pady=(0, 10))

        lbl_c = ctk.CTkLabel(tab, text="Contenu de l'article (Markdown / HTML) :", font=Theme.FONT_BODY, text_color=Theme.TEXT_MAIN, anchor="w")
        lbl_c.grid(row=2, column=0, sticky="ew", pady=(5, 2))

        self.txt_wp_content = ctk.CTkTextbox(tab, font=Theme.FONT_BODY, corner_radius=6, border_color=Theme.BORDER_COLOR, border_width=1)
        self.txt_wp_content.grid(row=3, column=0, sticky="nsew")
        self.txt_wp_content.bind("<KeyRelease>", self._on_text_change)

    def _setup_platform_tab(self, tab, platform_key):
        tab.grid_rowconfigure(1, weight=1)
        tab.grid_columnconfigure(0, weight=1)

        constraint = Theme.PLATFORM_CONSTRAINTS[platform_key]
        
        status_frame = ctk.CTkFrame(tab, fg_color="transparent")
        status_frame.grid(row=0, column=0, sticky="ew", pady=(5, 5))

        lbl_info = ctk.CTkLabel(status_frame, text=f"Post décliné pour {constraint['name']} {constraint['icon']}", font=Theme.FONT_MUTED, text_color=Theme.TEXT_MUTED)
        lbl_info.pack(side="left")

        lbl_counter = ctk.CTkLabel(status_frame, text="0 char", font=Theme.FONT_MUTED, text_color=Theme.ACCENT_EMERALD)
        lbl_counter.pack(side="right")

        txt_editor = ctk.CTkTextbox(tab, font=Theme.FONT_BODY, corner_radius=6, border_color=Theme.BORDER_COLOR, border_width=1)
        txt_editor.grid(row=1, column=0, sticky="nsew")
        txt_editor.bind("<KeyRelease>", lambda e, key=platform_key: self._update_char_counter(key))

        self.platform_editors[platform_key] = {
            "textbox": txt_editor,
            "counter_label": lbl_counter,
            "max_chars": constraint["max_chars"]
        }

    def _on_tab_change(self):
        self._notify_content_change()

    def _on_text_change(self, event=None):
        self._notify_content_change()

    def _notify_content_change(self):
        if self.on_content_change_cb:
            current_data = self.get_all_contents()
            self.on_content_change_cb(current_data)

    def _update_char_counter(self, platform_key):
        editor_info = self.platform_editors.get(platform_key)
        if not editor_info:
            return
        
        text = editor_info["textbox"].get("1.0", "end-1c")
        count = len(text)
        max_c = editor_info["max_chars"]

        if max_c:
            label_text = f"{count} / {max_c} chars"
            if count > max_c:
                color = Theme.ACCENT_ROSE
            elif count > max_c * 0.85:
                color = Theme.ACCENT_AMBER
            else:
                color = Theme.ACCENT_EMERALD
        else:
            label_text = f"{count} chars"
            color = Theme.ACCENT_EMERALD

        editor_info["counter_label"].configure(text=label_text, text_color=color)
        self._notify_content_change()

    def get_all_contents(self):
        """Retourne un dictionnaire avec le texte actuel de chaque onglet."""
        wp_raw = self.txt_wp_content.get("1.0", "end-1c").strip()
        wp_title = self.entry_wp_title.get().strip()

        # Si le titre WP n'est pas rempli explicitement mais commence par '# Titre', l'extraire
        if not wp_title and wp_raw.startswith("# "):
            lines = wp_raw.split("\n")
            wp_title = lines[0].replace("# ", "").strip()

        data = {
            "base": self.txt_base.get("1.0", "end-1c").strip(),
            "wordpress_title": wp_title,
            "wordpress": wp_raw,
            "facebook": self.platform_editors["facebook"]["textbox"].get("1.0", "end-1c").strip(),
            "instagram": self.platform_editors["instagram"]["textbox"].get("1.0", "end-1c").strip(),
            "twitter": self.platform_editors["twitter"]["textbox"].get("1.0", "end-1c").strip(),
            "linkedin": self.platform_editors["linkedin"]["textbox"].get("1.0", "end-1c").strip(),
            "featured_image": self.featured_image_path
        }
        return data

    def set_base_content(self, text):
        """Remplace le texte de base et active l'onglet Base."""
        self.txt_base.delete("1.0", "end")
        self.txt_base.insert("1.0", text)
        self.tabview.set("📝 Message de base")
        self._notify_content_change()

    def _select_featured_image(self):
        file_path = filedialog.askopenfilename(
            title="Sélectionner l'image à la une pour WordPress",
            filetypes=[("Images", "*.jpg *.jpeg *.png *.webp *.gif")]
        )
        if file_path:
            self.featured_image_path = file_path
            filename = file_path.split("/")[-1].split("\\")[-1]
            self.lbl_media_status.configure(text=f"🖼️ {filename[:20]}...", text_color=Theme.ACCENT_EMERALD)
            self._notify_content_change()

    def _generate_all_adaptations(self):
        """Génère automatiquement les versions adaptées via LM Studio pour toutes les plateformes."""
        base_text = self.txt_base.get("1.0", "end-1c").strip()
        if not base_text:
            messagebox.showwarning("Texte vide", "Veuillez d'abord saisir un texte dans l'onglet '📝 Message de base'.")
            return

        conn = self.lm_client.check_connection()
        if not conn["connected"]:
            messagebox.showerror("LM Studio déconnecté", f"Impossible de contacter LM Studio : {conn['message']}\n\nVérifiez que LM Studio est lancé sur http://localhost:1234")
            return

        selected_model = self.config_mgr.get("lm_studio", "selected_model", "")

        # 1. Génération WordPress
        res_wp = self.lm_client.adapt_for_platform(base_text, "wordpress", model=selected_model)
        if res_wp["success"]:
            wp_text = res_wp["text"]
            self.txt_wp_content.delete("1.0", "end")
            self.txt_wp_content.insert("1.0", wp_text)
            
            # Auto-extraction du titre
            if wp_text.startswith("# "):
                lines = wp_text.split("\n")
                extracted_title = lines[0].replace("# ", "").strip()
                self.entry_wp_title.delete(0, "end")
                self.entry_wp_title.insert(0, extracted_title)

        # 2. Génération pour chaque réseau social
        for p_key in ["facebook", "instagram", "twitter", "linkedin"]:
            res_p = self.lm_client.adapt_for_platform(base_text, p_key, model=selected_model)
            if res_p["success"]:
                tb = self.platform_editors[p_key]["textbox"]
                tb.delete("1.0", "end")
                tb.insert("1.0", res_p["text"])
                self._update_char_counter(p_key)

        messagebox.showinfo("Génération terminée", "L'IA a généré avec succès l'ensemble des déclinaisons pour vos réseaux et votre blog !")
        self._notify_content_change()

    def _apply_ia_action(self, action_key):
        """Applique une action IA sur l'onglet actif."""
        current_tab_name = self.tabview.get()
        
        # Récupérer l'éditeur de l'onglet actif
        if current_tab_name == "📝 Message de base":
            tb = self.txt_base
        elif current_tab_name == "🌐 WordPress":
            tb = self.txt_wp_content
        else:
            p_map = {"📘 Facebook": "facebook", "📸 Instagram": "instagram", "🐦 Twitter / X": "twitter", "💼 LinkedIn": "linkedin"}
            pk = p_map.get(current_tab_name)
            tb = self.platform_editors[pk]["textbox"] if pk else None

        if not tb:
            return

        text = tb.get("1.0", "end-1c").strip()
        if not text:
            messagebox.showwarning("Texte vide", "Il n'y a aucun texte à traiter dans l'onglet actif.")
            return

        selected_model = self.config_mgr.get("lm_studio", "selected_model", "")

        if action_key == "hashtags":
            res = self.lm_client.extract_hashtags(text, model=selected_model)
            if res["success"]:
                tb.insert("end", f"\n\n{res['text']}")
        else:
            res = self.lm_client.rewrite_action(text, action_key, model=selected_model)
            if res["success"]:
                tb.delete("1.0", "end")
                tb.insert("1.0", res["text"])

        self._notify_content_change()

    def _publish_to_wordpress(self, status="draft"):
        """Publie ou sauvegarde en brouillon sur WordPress."""
        contents = self.get_all_contents()
        wp_title = contents["wordpress_title"]
        wp_body = contents["wordpress"]

        if not wp_title:
            messagebox.showwarning("Titre manquant", "Veuillez renseigner un titre pour l'article WordPress.")
            return
        if not wp_body:
            messagebox.showwarning("Contenu manquant", "Veuillez ajouter du contenu dans l'onglet WordPress.")
            return

        if not self.wp_client.is_configured():
            messagebox.showerror("Configuration WordPress manquante", "Veuillez d'abord configurer vos identifiants WordPress dans l'onglet '⚙️ Comptes & API'.")
            return

        # S'il y a une image à la une, la téléverser d'abord
        media_id = None
        if self.featured_image_path:
            res_m = self.wp_client.upload_media(self.featured_image_path)
            if res_m["success"]:
                media_id = res_m["media_id"]
            else:
                messagebox.showwarning("Avertissement Média", f"Impossible d'envoyer l'image à la une : {res_m['message']}\n\nLa publication continue sans image.")

        # Publication
        res = self.wp_client.publish_post(
            title=wp_title,
            content=wp_body,
            status=status,
            featured_media_id=media_id
        )

        if res["success"]:
            messagebox.showinfo("Succès WordPress", res["message"] + (f"\n\nLien: {res['link']}" if res.get('link') else ""))
        else:
            messagebox.showerror("Erreur WordPress", res["message"])
