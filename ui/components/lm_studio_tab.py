import customtkinter as ctk
from tkinter import messagebox
from ui.theme import Theme

class LMStudioTab(ctk.CTkFrame):
    def __init__(self, parent, lm_client, config_mgr):
        super().__init__(parent, fg_color="transparent")
        self.lm_client = lm_client
        self.config_mgr = config_mgr
        self._build_ui()
        self._load_current_config()

    def _build_ui(self):
        self.grid_rowconfigure(1, weight=1)
        self.grid_columnconfigure(0, weight=1)

        # En-tête
        lbl_title = ctk.CTkLabel(self, text="🤖 Configuration LM Studio (IA Locale)", font=Theme.FONT_TITLE, text_color=Theme.TEXT_MAIN, anchor="w")
        lbl_title.grid(row=0, column=0, sticky="ew", padx=15, pady=(15, 10))

        # Conteneur principal
        main_box = ctk.CTkScrollableFrame(self, fg_color=Theme.CARD_BG, corner_radius=12)
        main_box.grid(row=1, column=0, sticky="nsew", padx=15, pady=(0, 15))
        main_box.grid_columnconfigure(0, weight=1)

        # --- SECTION 1 : CONNEXION SERVEUR ---
        lbl_s1 = ctk.CTkLabel(main_box, text="1. Paramètres de Connexion au Serveur Local", font=Theme.FONT_SUBTITLE, text_color=Theme.TEXT_MAIN, anchor="w")
        lbl_s1.pack(fill="x", padx=15, pady=(15, 5))

        url_frame = ctk.CTkFrame(main_box, fg_color="transparent")
        url_frame.pack(fill="x", padx=15, pady=5)
        
        lbl_url = ctk.CTkLabel(url_frame, text="URL API LM Studio :", font=Theme.FONT_BODY, width=150, anchor="w")
        lbl_url.pack(side="left")

        self.entry_url = ctk.CTkEntry(url_frame, font=Theme.FONT_BODY, placeholder_text="http://localhost:1234/v1", border_color=Theme.BORDER_COLOR)
        self.entry_url.pack(side="left", fill="x", expand=True, padx=(0, 10))

        btn_test = ctk.CTkButton(url_frame, text="🔌 Tester Connexion", fg_color=Theme.ACCENT_INDIGO, hover_color="#4F46E5", command=self._test_connection)
        btn_test.pack(side="right")

        # Badge de Statut Connection
        self.lbl_status_badge = ctk.CTkLabel(main_box, text="⚪ Non testé", font=Theme.FONT_BODY, text_color=Theme.TEXT_MUTED, anchor="w")
        self.lbl_status_badge.pack(fill="x", padx=15, pady=(2, 10))

        # --- SECTION 2 : CHOIX DU MODÈLE ET HYPERPARAMÈTRES ---
        lbl_s2 = ctk.CTkLabel(main_box, text="2. Modèle chargé & Hyperparamètres", font=Theme.FONT_SUBTITLE, text_color=Theme.TEXT_MAIN, anchor="w")
        lbl_s2.pack(fill="x", padx=15, pady=(15, 5))

        model_frame = ctk.CTkFrame(main_box, fg_color="transparent")
        model_frame.pack(fill="x", padx=15, pady=5)

        lbl_m = ctk.CTkLabel(model_frame, text="Modèle actif :", font=Theme.FONT_BODY, width=150, anchor="w")
        lbl_m.pack(side="left")

        self.option_models = ctk.CTkOptionMenu(model_frame, values=["Aucun modèle détecté"], font=Theme.FONT_BODY)
        self.option_models.pack(side="left", fill="x", expand=True)

        # Temperature Slider
        temp_frame = ctk.CTkFrame(main_box, fg_color="transparent")
        temp_frame.pack(fill="x", padx=15, pady=5)

        lbl_t = ctk.CTkLabel(temp_frame, text="Température (Créativité) :", font=Theme.FONT_BODY, width=170, anchor="w")
        lbl_t.pack(side="left")

        self.slider_temp = ctk.CTkSlider(temp_frame, from_=0.0, to=1.0, number_of_steps=20, command=self._on_temp_slider_change)
        self.slider_temp.pack(side="left", fill="x", expand=True, padx=10)

        self.lbl_temp_val = ctk.CTkLabel(temp_frame, text="0.7", font=Theme.FONT_BODY, width=40)
        self.lbl_temp_val.pack(side="right")

        # Bouton Sauvegarder Config
        btn_save = ctk.CTkButton(main_box, text="💾 Sauvegarder les paramètres LM Studio", fg_color=Theme.ACCENT_EMERALD, hover_color="#059669", command=self._save_config)
        btn_save.pack(padx=15, pady=15, anchor="w")

        # --- SECTION 3 : BAC À SABLE / TEST PROMPT ---
        ctk.CTkFrame(main_box, height=2, fg_color=Theme.BORDER_COLOR).pack(fill="x", padx=15, pady=10)

        lbl_s3 = ctk.CTkLabel(main_box, text="3. Bac à Sable (Test de prompt direct)", font=Theme.FONT_SUBTITLE, text_color=Theme.TEXT_MAIN, anchor="w")
        lbl_s3.pack(fill="x", padx=15, pady=(5, 5))

        self.entry_test_prompt = ctk.CTkEntry(main_box, font=Theme.FONT_BODY, placeholder_text="Tapez une question ou une instruction de test pour LM Studio...")
        self.entry_test_prompt.pack(fill="x", padx=15, pady=5)

        btn_run_prompt = ctk.CTkButton(main_box, text="▶️ Exécuter le test IA", fg_color="#334155", hover_color="#475569", command=self._run_test_prompt)
        btn_run_prompt.pack(padx=15, pady=5, anchor="w")

        self.txt_test_response = ctk.CTkTextbox(main_box, height=120, font=Theme.FONT_BODY, corner_radius=6)
        self.txt_test_response.pack(fill="x", padx=15, pady=(5, 15))

    def _load_current_config(self):
        lm_cfg = self.config_mgr.get("lm_studio")
        self.entry_url.insert(0, lm_cfg.get("url", "http://localhost:1234/v1"))
        temp = lm_cfg.get("temperature", 0.7)
        self.slider_temp.set(temp)
        self.lbl_temp_val.configure(text=f"{temp:.1f}")

    def _on_temp_slider_change(self, value):
        self.lbl_temp_val.configure(text=f"{value:.1f}")

    def _test_connection(self):
        url = self.entry_url.get().strip()
        self.lm_client.base_url = url.rstrip("/")
        
        res = self.lm_client.check_connection()
        if res["connected"]:
            models = res["models"]
            self.lbl_status_badge.configure(text=f"🟢 {res['message']}", text_color=Theme.ACCENT_EMERALD)
            if models:
                self.option_models.configure(values=models)
                self.option_models.set(models[0])
            else:
                self.option_models.configure(values=["Modèle générique LM Studio"])
                self.option_models.set("Modèle générique LM Studio")
        else:
            self.lbl_status_badge.configure(text=f"🔴 {res['message']}", text_color=Theme.ACCENT_ROSE)

    def _save_config(self):
        url = self.entry_url.get().strip()
        model = self.option_models.get()
        temp = float(self.slider_temp.get())

        self.config_mgr.set("lm_studio", "url", url)
        self.config_mgr.set("lm_studio", "selected_model", model)
        self.config_mgr.set("lm_studio", "temperature", temp)

        self.lm_client.base_url = url.rstrip("/")
        messagebox.showinfo("Configuration sauvegardée", "Les paramètres LM Studio ont été enregistrés avec succès !")

    def _run_test_prompt(self):
        prompt = self.entry_test_prompt.get().strip()
        if not prompt:
            return
        
        self.txt_test_response.delete("1.0", "end")
        self.txt_test_response.insert("1.0", "Génération en cours avec LM Studio...")

        selected_model = self.option_models.get()
        temp = float(self.slider_temp.get())

        res = self.lm_client.generate(prompt, model=selected_model, temperature=temp)
        self.txt_test_response.delete("1.0", "end")
        if res["success"]:
            self.txt_test_response.insert("1.0", res["text"])
        else:
            self.txt_test_response.insert("1.0", f"Erreur : {res['error']}")
