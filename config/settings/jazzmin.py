"""
Jazzmin Admin Theme Configuration.

Bu fayl Django admin panelni chiroyli va zamonaviy qiladi.
"""

JAZZMIN_SETTINGS = {
    # Title
    "site_title": "Medical MAS Admin",
    "site_header": "Medical MAS",
    "site_brand": "Multiagent Tibbiy Diagnostika",
    "site_logo": None,  # Logo qo'shish mumkin
    "login_logo": None,
    "login_logo_dark": None,
    "site_logo_classes": "img-circle",
    "site_icon": None,
    
    # Welcome text
    "welcome_sign": "Medical MAS Admin Paneliga Xush Kelibsiz",
    
    # Copyright
    "copyright": "Medical MAS © 2024",
    
    # Search model
    "search_model": ["auth.User", "patients.Patient"],
    
    # User avatar
    "user_avatar": None,
    
    ############
    # Top Menu #
    ############
    "topmenu_links": [
        {"name": "Bosh sahifa", "url": "admin:index", "permissions": ["auth.view_user"]},
        {"name": "Dashboard", "url": "dashboard:index", "permissions": ["auth.view_user"]},
        {"name": "API Docs", "url": "/api/docs/", "new_window": True},
        {"model": "auth.User"},
    ],
    
    #############
    # Side Menu #
    #############
    "show_sidebar": True,
    "navigation_expanded": True,
    "hide_apps": [],
    "hide_models": [],
    
    # Custom icons for models
    "icons": {
        "auth": "fas fa-users-cog",
        "auth.user": "fas fa-user",
        "auth.Group": "fas fa-users",
        
        "patients.Patient": "fas fa-user-injured",
        "patients.Symptom": "fas fa-thermometer-half",
        "patients.MedicalHistory": "fas fa-history",
        
        "diagnostics.DiseasePattern": "fas fa-disease",
        "diagnostics.DiagnosticSession": "fas fa-stethoscope",
        "diagnostics.DiagnosticResult": "fas fa-file-medical",
        
        "agents.AgentState": "fas fa-robot",
        
        "core.ACLMessage": "fas fa-envelope",
        "core.AgentLog": "fas fa-clipboard-list",
        
        "sites.Site": "fas fa-globe",
        "authtoken.Token": "fas fa-key",
        "authtoken.TokenProxy": "fas fa-key",
    },
    
    # Icons for default apps
    "default_icon_parents": "fas fa-chevron-circle-right",
    "default_icon_children": "fas fa-circle",
    
    #################
    # Related Modal #
    #################
    "related_modal_active": False,
    
    #############
    # UI Tweaks #
    #############
    "custom_css": None,
    "custom_js": None,
    "use_google_fonts_cdn": True,
    "show_ui_builder": False,
    
    ###############
    # Change view #
    ###############
    "changeform_format": "horizontal_tabs",
    "changeform_format_overrides": {
        "auth.user": "collapsible",
        "auth.group": "vertical_tabs",
    },
}

JAZZMIN_UI_TWEAKS = {
    "navbar_small_text": False,
    "footer_small_text": False,
    "body_small_text": False,
    "brand_small_text": False,
    "brand_colour": "navbar-primary",
    "accent": "accent-primary",
    "navbar": "navbar-white navbar-light",
    "no_navbar_border": False,
    "navbar_fixed": False,
    "layout_boxed": False,
    "footer_fixed": False,
    "sidebar_fixed": False,
    "sidebar": "sidebar-dark-primary",
    "sidebar_nav_small_text": False,
    "sidebar_disable_expand": False,
    "sidebar_nav_child_indent": False,
    "sidebar_nav_compact_style": False,
    "sidebar_nav_legacy_style": False,
    "sidebar_nav_flat_style": False,
    "theme": "default",
    "default_theme_mode": "auto",  # Changed from dark_mode_theme
    "button_classes": {
        "primary": "btn-primary",
        "secondary": "btn-secondary",
        "info": "btn-info",
        "warning": "btn-warning",
        "danger": "btn-danger",
        "success": "btn-success"
    }
}
