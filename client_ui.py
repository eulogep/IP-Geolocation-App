from nicegui import ui
import requests


def query_server():
    hostname = server_input.value.strip().rstrip("/")
    ip = ip_input.value.strip()

    if not hostname or not ip:
        ui.notify("Veuillez renseigner l'adresse du serveur et l'IP", type="negative")
        return

    # Validation basique de l'IP
    if not validate_ip(ip):
        ui.notify("Format d'IP invalide", type="negative")
        return

    if hostname.startswith("http://") or hostname.startswith("https://"):
        url = f"{hostname}/ip/{ip}"
    else:
        url = f"http://{hostname}/ip/{ip}"

    # Afficher le spinner
    spinner.set_visibility(True)
    result_card.set_visibility(False)

    try:
        print("DEBUG URL =", url)
        r = requests.get(url, timeout=5)
        r.raise_for_status()
        data = r.json()

        # Masquer le spinner
        spinner.set_visibility(False)

        # Afficher les résultats
        display_results(data)
        ui.notify("✓ Géolocalisation réussie", type="positive")

    except Exception as e:
        spinner.set_visibility(False)
        ui.notify(f"Erreur : {e}", type="negative")


def validate_ip(ip):
    """Validation basique d'une adresse IP"""
    parts = ip.split(".")
    if len(parts) != 4:
        return False
    try:
        return all(0 <= int(part) <= 255 for part in parts)
    except ValueError:
        return False


def display_results(data):
    """Affiche les résultats dans l'interface"""
    ip = data.get("ip", "N/A")
    country = data.get("country", "N/A")
    lat = data.get("latitude")
    lon = data.get("longitude")

    # Advanced fields
    country_code = data.get("country_code")
    flag = get_flag(country_code)
    country_display = f"{flag} {country}" if flag else f"🏳️ {country}"

    isp = data.get("isp")
    asn = data.get("asn")

    # Mettre à jour les labels
    ip_label.set_text(f"🌐 IP : {ip}")
    country_label.set_text(f"📍 Pays : {country_display}")
    coords_label.set_text(
        f"🌍 Coordonnées : {lat}, {lon}" if lat and lon else "🌍 Coordonnées : N/A"
    )

    if isp:
        isp_display = f"{isp} (AS{asn})" if asn else isp
        isp_label.set_text(f"🏢 FAI : {isp_display}")
        isp_label.set_visibility(True)
    else:
        isp_label.set_visibility(False)

    # Ajouter à l'historique
    add_to_history(ip, country_display)

    # Afficher la card de résultats
    result_card.set_visibility(True)

    # Mettre à jour la carte
    if lat is not None and lon is not None:
        map_container.set_visibility(True)
        # Utiliser JavaScript pour mettre à jour la carte Leaflet
        # Utiliser JavaScript pour mettre à jour la carte Leaflet
        update_map_script = f"""
        if (typeof window.map !== 'undefined') {{
            window.map.setView([{lat}, {lon}], 5);
            if (window.marker) {{
                window.map.removeLayer(window.marker);
            }}
            window.marker = L.marker([{lat}, {lon}]).addTo(window.map)
                .bindPopup('<b>{country}</b><br>IP: {ip}<br>Lat: {lat}<br>Lon: {lon}')
                .openPopup();
        }}
        """
        ui.run_javascript(update_map_script)


def get_my_ip():
    """Détecte automatiquement l'IP publique de l'utilisateur"""
    try:
        response = requests.get("https://api.ipify.org?format=json", timeout=3)
        my_ip = response.json().get("ip")
        if my_ip:
            ip_input.set_value(my_ip)
            ui.notify(f"IP détectée : {my_ip}", type="info")
    except Exception as e:
        ui.notify(f"Impossible de détecter l'IP : {e}", type="warning")


def get_flag(country_code):
    """Convertit un code pays (ex: 'US') en emoji drapeau"""
    if not country_code:
        return ""
    try:
        return "".join([chr(ord(c) + 127397) for c in country_code.upper()])
    except Exception:
        return ""


search_history = []


def add_to_history(ip, country):
    """Ajoute une recherche à l'historique"""
    # Éviter les doublons consécutifs
    if search_history and search_history[0]["ip"] == ip:
        return

    search_history.insert(0, {"ip": ip, "country": country, "time": "Just now"})
    # Garder seulement les 5 derniers
    if len(search_history) > 5:
        search_history.pop()

    update_history_ui()


def update_history_ui():
    """Met à jour l'affichage de l'historique"""
    history_container.clear()
    if not search_history:
        history_title.set_visibility(False)
        return

    history_title.set_visibility(True)
    with history_container:
        for item in search_history:
            with ui.row().classes(
                "w-full justify-between items-center p-2 hover:bg-white/10 rounded cursor-pointer"
            ) as row:
                ui.label(f"{item['ip']}").classes("font-mono")
                ui.label(item["country"])
                row.on("click", lambda e, ip=item["ip"]: ip_input.set_value(ip))


# ============================================================================
# INTERFACE UTILISATEUR PREMIUM
# ============================================================================

# Style CSS personnalisé pour un thème sombre premium
ui.add_head_html("""
<style>
    body {
        background: linear-gradient(135deg, #1a1a2e 0%, #16213e 100%);
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    }
    
    .main-container {
        max-width: 1200px;
        margin: 0 auto;
        padding: 2rem;
    }
    
    .header-title {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        font-size: 2.5rem;
        font-weight: bold;
        text-align: center;
        margin-bottom: 0.5rem;
    }
    
    .subtitle {
        color: #a0aec0;
        text-align: center;
        margin-bottom: 2rem;
    }
    
    .input-card {
        background: rgba(255, 255, 255, 0.05);
        backdrop-filter: blur(10px);
        border-radius: 16px;
        padding: 2rem;
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3);
        border: 1px solid rgba(255, 255, 255, 0.1);
        margin-bottom: 2rem;
    }
    
    .result-card {
        background: linear-gradient(135deg, rgba(102, 126, 234, 0.1) 0%, rgba(118, 75, 162, 0.1) 100%);
        backdrop-filter: blur(10px);
        border-radius: 16px;
        padding: 2rem;
        box-shadow: 0 8px 32px rgba(102, 126, 234, 0.2);
        border: 1px solid rgba(102, 126, 234, 0.3);
        margin-bottom: 2rem;
    }
    
    .map-container {
        border-radius: 16px;
        overflow: hidden;
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3);
        border: 1px solid rgba(255, 255, 255, 0.1);
    }
    
    .info-label {
        font-size: 1.2rem;
        color: #e2e8f0;
        margin: 0.5rem 0;
        padding: 0.5rem;
        background: rgba(255, 255, 255, 0.05);
        border-radius: 8px;
    }
</style>

<!-- Leaflet CSS -->
<link rel="stylesheet" href="https://unpkg.com/leaflet@1.9.4/dist/leaflet.css" />
<script src="https://unpkg.com/leaflet@1.9.4/dist/leaflet.js"></script>
""")

with ui.column().classes("main-container"):
    # En-tête
    ui.html(
        '<div class="header-title">🌍 Géolocalisation IP Premium</div>', sanitize=False
    )
    ui.html(
        '<div class="subtitle">Découvrez la localisation de n\'importe quelle adresse IP</div>',
        sanitize=False,
    )

    # Card d'entrée
    with ui.card().classes("input-card"):
        with ui.row().classes("w-full gap-4"):
            server_input = (
                ui.input(
                    label="🖥️ Adresse du serveur",
                    value="127.0.0.1:8000",
                    placeholder="127.0.0.1:8000",
                )
                .classes("flex-1")
                .on("keydown.enter", query_server)
            )

            ip_input = (
                ui.input(label="🌐 Adresse IP cible", placeholder="8.8.8.8")
                .classes("flex-1")
                .on("keydown.enter", query_server)
            )

        with ui.row().classes("w-full gap-4 mt-4"):
            ui.button("🔍 Localiser", on_click=query_server).props(
                "color=primary size=lg"
            ).classes("flex-1")

            ui.button("📍 Mon IP", on_click=get_my_ip).props(
                "color=secondary size=lg"
            ).classes("flex-1")

    # Spinner de chargement
    spinner = ui.spinner(size="lg", color="primary")
    spinner.set_visibility(False)

    # Card de résultats
    with ui.card().classes("result-card") as result_card:
        ui.label("📊 Résultats").classes("text-xl font-bold mb-4")

        ip_label = ui.label("🌐 IP : -").classes("info-label")
        country_label = ui.label("🏳️ Pays : -").classes("info-label")
        with ui.row().classes("items-center gap-2"):
            coords_label = ui.label("📍 Coordonnées : -").classes("info-label")
            ui.button(
                icon="content_copy",
                on_click=lambda: ui.clipboard.write(
                    coords_label.text.replace("🌍 Coordonnées : ", "")
                ),
            ).props("round flat size=sm").tooltip("Copier les coordonnées")
        isp_label = ui.label("🏢 FAI : -").classes("info-label")
        isp_label.set_visibility(False)

    result_card.set_visibility(False)

    # Historique
    history_title = ui.label("🕒 Historique récent").classes(
        "text-lg font-bold mt-4 mb-2"
    )
    history_title.set_visibility(False)
    history_container = ui.column().classes("w-full mb-4 bg-white/5 rounded-xl p-2")

    # Carte interactive intégrée
    with ui.card().classes("map-container") as map_container:
        ui.html(
            '<div id="map" style="height: 500px; width: 100%;"></div>', sanitize=False
        )

    # Initialisation de la carte après le chargement de la page
    def init_map():
        ui.run_javascript("""
            if (typeof window.map === 'undefined') {
                window.map = L.map('map').setView([20, 0], 2);
                L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
                    attribution: '© OpenStreetMap contributors',
                    maxZoom: 18
                }).addTo(window.map);
                window.marker = null;
            }
        """)

    # Appeler l'initialisation de la carte une fois que le client est connecté
    ui.timer(0.1, init_map, once=True)

    # Footer
    ui.html(
        '<div class="subtitle mt-8">Propulsé par CIRCL API • Développé avec ❤️</div>',
        sanitize=False,
    )

ui.run(title="Géolocalisation IP Premium", port=8080)
