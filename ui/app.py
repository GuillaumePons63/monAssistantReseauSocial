import customtkinter as ctk
from ui.theme import Theme
from ui.components.editor_tab import EditorTab
from ui.components.preview_tab import PreviewTab
from ui.components.trends_tab import TrendsTab
from ui.components.lm_studio_tab import LMStudioTab
from ui.components.api_guide_tab import APIGuideTab
from ui.components.accounts_tab import AccountsTab

class MainApp(ctk.CTk):
    def __init__(self, config_mgr, lm_client, wp_client, trend_watcher):
        super().__init__()

        self.config_mgr = config_mgr
        self.lm_client = lm_client
        self.wp_client = wp_client
        self.trend_watcher = trend_watcher

        # Window Settings
        self.title("Assistant de Publication Réseaux Sociaux & WordPress (IA Locale LM Studio)")
        self.geometry("1280x800")
        self.minsize(1024, 680)

        self._configure_grid()
        self._build_sidebar()
        self._build_status_bar()
        self._build_main_views()

        # Afficher la vue initiale
        self._select_view("editor")
        self._update_status_bar()

    def _configure_grid(self):
        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=0)  # Status Bar
        self.grid_columnconfigure(0, weight=0)  # Sidebar
        self.grid_columnconfigure(1, weight=1)  # Main View Container

    def _build_sidebar(self):
        sidebar = ctk.CTkFrame(self, width=220, corner_radius=0, fg_color="#090D16")
        sidebar.grid(row=0, column=0, sticky="nsew")
        sidebar.grid_rowconfigure(7, weight=1)

        # App Logo & Title
        lbl_logo = ctk.CTkLabel(
            sidebar,
            text="🚀 SocialAI Studio",
            font=(Theme.FONT_FAMILY, 18, "bold"),
            text_color=Theme.ACCENT_INDIGO
        )
        lbl_logo.grid(row=0, column=0, padx=20, pady=(20, 20), sticky="w")

        # Sidebar Buttons
        self.sidebar_btns = {}
        
        nav_items = [
            ("editor", "✍️  Éditeur & Déclinaisons"),
            ("preview", "👁️  Aperçu WYSIWYG"),
            ("trends", "🔥  Veille & Tendances"),
            ("lm_studio", "🤖  LM Studio (IA)"),
            ("api_guide", "📚  Assistant Clés API"),
            ("accounts", "⚙️  Comptes & WordPress")
        ]

        for idx, (key, text) in enumerate(nav_items, start=1):
            btn = ctk.CTkButton(
                sidebar,
                text=text,
                font=(Theme.FONT_FAMILY, 13),
                anchor="w",
                fg_color="transparent",
                text_color=Theme.TEXT_MUTED,
                hover_color="#1E293B",
                height=40,
                command=lambda k=key: self._select_view(k)
            )
            btn.grid(row=idx, column=0, padx=10, pady=4, sticky="ew")
            self.sidebar_btns[key] = btn

    def _build_main_views(self):
        self.container = ctk.CTkFrame(self, fg_color=Theme.BG_DARK, corner_radius=0)
        self.container.grid(row=0, column=1, sticky="nsew")
        self.container.grid_rowconfigure(0, weight=1)
        self.container.grid_columnconfigure(0, weight=1)

        # Instanciation des vues
        self.views = {}

        # 1. Preview Tab
        self.views["preview"] = PreviewTab(self.container)
        
        # 2. Editor Tab (Rappels de callback vers la Preview)
        self.views["editor"] = EditorTab(
            self.container,
            self.lm_client,
            self.wp_client,
            self.config_mgr,
            on_content_change_cb=self._on_editor_content_changed
        )

        # 3. Trends Tab
        self.views["trends"] = TrendsTab(
            self.container,
            self.trend_watcher,
            self.config_mgr,
            on_use_topic_cb=self._on_use_topic_from_trends
        )

        # 4. LM Studio Tab
        self.views["lm_studio"] = LMStudioTab(self.container, self.lm_client, self.config_mgr)

        # 5. API Guide Tab
        self.views["api_guide"] = APIGuideTab(self.container)

        # 6. Accounts Tab
        self.views["accounts"] = AccountsTab(
            self.container,
            self.wp_client,
            self.config_mgr,
            on_import_post_cb=self._on_import_post_to_editor
        )

        for view in self.views.values():
            view.grid(row=0, column=0, sticky="nsew")

    def _build_status_bar(self):
        status_bar = ctk.CTkFrame(self, height=32, corner_radius=0, fg_color="#0F172A", border_color=Theme.BORDER_COLOR, border_width=1)
        status_bar.grid(row=1, column=0, columnspan=2, sticky="ew")

        self.lbl_status_lm = ctk.CTkLabel(status_bar, text="🤖 LM Studio : Verification...", font=Theme.FONT_MUTED, text_color=Theme.TEXT_MUTED)
        self.lbl_status_lm.pack(side="left", padx=15)

        self.lbl_status_wp = ctk.CTkLabel(status_bar, text="🌐 WordPress : Verification...", font=Theme.FONT_MUTED, text_color=Theme.TEXT_MUTED)
        self.lbl_status_wp.pack(side="left", padx=15)

    def _select_view(self, key):
        for k, btn in self.sidebar_btns.items():
            if k == key:
                btn.configure(fg_color="#1E293B", text_color=Theme.TEXT_MAIN)
            else:
                btn.configure(fg_color="transparent", text_color=Theme.TEXT_MUTED)

        for k, view in self.views.items():
            if k == key:
                view.tkraise()

    def _on_editor_content_changed(self, contents):
        # Mettre à jour l'aperçu WYSIWYG
        if "preview" in self.views:
            self.views["preview"].update_previews(contents)

    def _on_use_topic_from_trends(self, topic_text):
        if "editor" in self.views:
            self.views["editor"].set_base_content(topic_text)
            self._select_view("editor")

    def _on_import_post_to_editor(self, post_content):
        if "editor" in self.views:
            self.views["editor"].set_base_content(post_content)
            self._select_view("editor")

    def _update_status_bar(self):
        # Vérification asynchrone / rapide du statut
        lm_res = self.lm_client.check_connection()
        if lm_res["connected"]:
            self.lbl_status_lm.configure(text="🤖 LM Studio : 🟢 Connecté", text_color=Theme.ACCENT_EMERALD)
        else:
            self.lbl_status_lm.configure(text="🤖 LM Studio : 🔴 Déconnecté", text_color=Theme.ACCENT_ROSE)

        if self.wp_client.is_configured():
            wp_res = self.wp_client.verify_connection()
            if wp_res["success"]:
                self.lbl_status_wp.configure(text="🌐 WordPress : 🟢 Connecté", text_color=Theme.ACCENT_EMERALD)
            else:
                self.lbl_status_wp.configure(text="🌐 WordPress : 🔴 Erreur auth", text_color=Theme.ACCENT_ROSE)
        else:
            self.lbl_status_wp.configure(text="🌐 WordPress : ⚪ Non configuré", text_color=Theme.TEXT_MUTED)
