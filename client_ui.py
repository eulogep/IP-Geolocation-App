from nicegui import ui
import requests
from datetime import datetime

# ----------------------------
# STATE
# ----------------------------
history = []  # list of dicts: {ip, country, isp, asn, time, lat, lon}


# ----------------------------
# HELPERS
# ----------------------------
def safe_get(d: dict, *keys, default=None):
    for k in keys:
        if isinstance(d, dict) and k in d and d[k] is not None:
            return d[k]
    return default


def notify_error(msg: str):
    ui.notify(msg, color="negative", position="top-right")


def notify_ok(msg: str):
    ui.notify(msg, color="positive", position="top-right")


# ----------------------------
# CORE ACTIONS
# ----------------------------
def query_geolocation(ip: str, hostname: str) -> dict:
    # hostname expected like: 127.0.0.1:8000
    hostname = (hostname or "").strip()
    ip = (ip or "").strip()

    if not hostname or not ip:
        raise ValueError("Adresse du serveur et IP cible sont obligatoires.")

    # IMPORTANT: do NOT call 8080 here (NiceGUI). Must call FastAPI (8000).
    url = f"http://{hostname}/ip/{ip}"
    print("DEBUG URL =", url)  # keep during dev

    r = requests.get(url, timeout=5)
    r.raise_for_status()
    return r.json()


def on_locate_clicked():
    try:
        data = query_geolocation(ip_input.value, server_input.value)

        ip = safe_get(data, "ip", default=ip_input.value)
        country = safe_get(data, "country", default="Unknown")
        lat = safe_get(data, "latitude", default=None)
        lon = safe_get(data, "longitude", default=None)

        # Optional fields if your backend provides them later
        isp = safe_get(data, "isp", "provider", default="—")
        asn = safe_get(data, "asn", default="—")

        # Update result card
        ip_value.set_text(ip)
        country_value.set_text(f"{country}")
        isp_value.set_text(f"{isp}")
        asn_value.set_text(f"{asn}")

        if lat is not None and lon is not None:
            coords_value.set_text(f"{float(lat):.4f}, {float(lon):.4f}")
            # Update Leaflet Map
            map_frame.set_center((float(lat), float(lon)))
            map_frame.set_zoom(13)
            map_frame.clear_layers()
            map_frame.marker(latlng=(float(lat), float(lon)))
        else:
            coords_value.set_text("—")
            map_frame.set_center((38.0, -97.0))
            map_frame.set_zoom(4)

        # Update history
        history.insert(
            0,
            {
                "ip": ip,
                "country": country,
                "isp": isp,
                "asn": asn,
                "time": datetime.now().strftime("%H:%M"),
                "lat": lat,
                "lon": lon,
            },
        )
        del history[8:]  # keep last 8

        refresh_history()
        notify_ok("Localisation effectuée.")
    except requests.exceptions.Timeout:
        notify_error("Timeout: le serveur n'a pas répondu (vérifie FastAPI sur 8000).")
    except requests.exceptions.ConnectionError:
        notify_error("Connexion impossible: vérifie que FastAPI tourne sur 8000.")
    except requests.HTTPError as e:
        notify_error(f"Erreur HTTP: {e}")
    except Exception as e:
        notify_error(f"Erreur: {e}")


def on_my_ip_clicked():
    try:
        # Fetch public IP from an external service
        ui.notify(
            "Détection de votre IP en cours...", color="info", position="top-right"
        )
        response = requests.get("https://api.ipify.org?format=json", timeout=5)
        response.raise_for_status()
        my_ip = response.json().get("ip")

        if my_ip:
            ip_input.value = my_ip
            notify_ok(f"Votre IP publique est : {my_ip}")
            on_locate_clicked()  # Auto-locate
        else:
            notify_error("Impossible de récupérer votre IP.")

    except Exception as e:
        notify_error(f"Erreur lors de la récupération de l'IP : {e}")


def refresh_history():
    history_col.clear()
    if not history:
        with history_col:
            ui.label("Aucun historique pour l’instant.").classes(
                "text-sm text-gray-300"
            )
        return

    with history_col:
        for item in history:
            with (
                ui.card()
                .classes(
                    "w-full p-3 rounded-xl border border-white/10 bg-white/5 backdrop-blur-xl cursor-pointer"
                )
                .on(
                    "click",
                    lambda e, ip=item["ip"]: (
                        ip_input.set_value(ip),
                        on_locate_clicked(),
                    ),
                )
            ):
                with ui.row().classes("items-center justify-between w-full"):
                    ui.label(item["ip"]).classes("font-semibold text-white")
                    ui.label(item["time"]).classes("text-xs text-gray-300")
                ui.label(f"{item['country']} • {item['isp']}").classes(
                    "text-xs text-gray-200"
                )


# ----------------------------
# PREMIUM STYLES (CSS)
# ----------------------------
ui.add_head_html("""
<style>
:root {
  --bg1: #050B1A;
  --bg2: #0B1A3A;
  --bg3: #2A0D52;
  --glass: rgba(255,255,255,0.06);
  --glass2: rgba(255,255,255,0.10);
  --stroke: rgba(255,255,255,0.14);
  --glow: rgba(59,130,246,0.35);
}

body {
  background: radial-gradient(1200px 600px at 20% 10%, rgba(59,130,246,0.22), transparent 60%),
              radial-gradient(900px 500px at 80% 20%, rgba(168,85,247,0.18), transparent 55%),
              linear-gradient(135deg, var(--bg1), var(--bg2), var(--bg3));
  color: white;
}

/* Subtle tech pattern */
body:before {
  content: "";
  position: fixed;
  inset: 0;
  pointer-events: none;
  opacity: 0.12;
  background-image:
    linear-gradient(rgba(255,255,255,0.08) 1px, transparent 1px),
    linear-gradient(90deg, rgba(255,255,255,0.06) 1px, transparent 1px);
  background-size: 42px 42px;
  mask-image: radial-gradient(circle at 40% 20%, black 0%, transparent 65%);
}

/* Glass cards */
.glass {
  background: var(--glass);
  border: 1px solid var(--stroke);
  backdrop-filter: blur(18px);
  border-radius: 18px;
  box-shadow: 0 10px 30px rgba(0,0,0,0.35);
}

.glass-strong {
  background: var(--glass2);
  border: 1px solid rgba(255,255,255,0.18);
  backdrop-filter: blur(22px);
  border-radius: 18px;
  box-shadow: 0 12px 40px rgba(0,0,0,0.40);
}

/* Title gradient */
.title-gradient {
  font-weight: 800;
  font-size: 34px;
  letter-spacing: 0.3px;
  background: linear-gradient(90deg, #22D3EE, #60A5FA, #A78BFA);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  text-shadow: 0 0 20px rgba(96,165,250,0.25);
}

/* Buttons */
.btn-primary .q-btn {
  background: linear-gradient(90deg, #2563EB, #38BDF8);
  color: white !important;
  border-radius: 14px;
  box-shadow: 0 10px 28px rgba(37,99,235,0.25);
}
.btn-secondary .q-btn {
  background: linear-gradient(90deg, #7C3AED, #A855F7);
  color: white !important;
  border-radius: 14px;
  box-shadow: 0 10px 28px rgba(168,85,247,0.22);
}

/* Inputs */
.q-field--outlined .q-field__control:before {
  border-color: rgba(255,255,255,0.18) !important;
}
.q-field--outlined .q-field__control {
  border-radius: 14px !important;
}

/* Map frame */
.map-frame {
  border: 1px solid rgba(255,255,255,0.12);
  border-radius: 18px;
  overflow: hidden;
  box-shadow: 0 18px 50px rgba(0,0,0,0.45);
}
.leaflet-container {
    background-color: transparent !important;
}
</style>
""")


# ----------------------------
# UI LAYOUT
# ----------------------------
with ui.column().classes("w-full items-center"):
    ui.html(
        '<div class="mt-10 title-gradient">🌍 Géolocalisation IP Premium</div>',
        sanitize=False,
    )

    with ui.row().classes("w-[1200px] max-w-[95vw] gap-6 mt-8"):
        # LEFT MAIN COLUMN
        with ui.column().classes("flex-1 gap-5"):
            # Top input bar (glass)
            with ui.card().classes("glass-strong w-full p-5"):
                with ui.row().classes("w-full items-end gap-4"):
                    server_input = (
                        ui.input("Adresse du serveur", placeholder="127.0.0.1:8000")
                        .props("outlined dense")
                        .classes("flex-1")
                    )
                    server_input.value = "127.0.0.1:8000"

                    ip_input = (
                        ui.input("Adresse IP cible", placeholder="8.8.8.8")
                        .props("outlined dense")
                        .classes("flex-1")
                    )
                    ip_input.value = "8.8.8.8"

                    ui.button("🔍 Localiser", on_click=on_locate_clicked).classes(
                        "btn-primary"
                    )
                    ui.button("📍 Mon IP", on_click=on_my_ip_clicked).classes(
                        "btn-secondary"
                    )

            # Results card
            with ui.card().classes("glass w-full p-6"):
                ui.label("📊 Résultats").classes("text-lg font-semibold text-white/90")

                with ui.row().classes("w-full mt-4 gap-6 items-center"):
                    # Big IP block
                    with ui.column().classes("min-w-[220px]"):
                        ui.label("IP").classes("text-xs text-gray-300")
                        ip_value = ui.label("—").classes(
                            "text-3xl font-extrabold text-white"
                        )

                    # Country / coords
                    with ui.column().classes("flex-1"):
                        ui.label("Pays").classes("text-xs text-gray-300")
                        country_value = ui.label("—").classes("text-lg font-semibold")

                        ui.label("Coordonnées").classes("text-xs text-gray-300 mt-3")
                        coords_value = ui.label("—").classes("text-base text-white/90")

                    # ISP / ASN
                    with ui.column().classes("flex-1"):
                        ui.label("FAI (ISP)").classes("text-xs text-gray-300")
                        isp_value = ui.label("—").classes("text-base font-semibold")

                        ui.label("ASN").classes("text-xs text-gray-300 mt-3")
                        asn_value = ui.label("—").classes("text-base text-white/90")

            # Map section
            with ui.card().classes("glass w-full p-4"):
                ui.label("🗺️ Carte").classes("text-lg font-semibold text-white/90 mb-3")
                # Using native ui.leaflet instead of iframe for better control and dark mode
                map_frame = ui.leaflet(center=(38.0, -97.0), zoom=4).classes(
                    "map-frame w-full h-[380px]"
                )
                map_frame.tile_layer = (
                    "https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
                )
                # Default attribution is sufficient

        # RIGHT HISTORY PANEL
        with ui.column().classes("w-[340px] max-w-[92vw]"):
            with ui.card().classes("glass-strong w-full p-5"):
                ui.label("🕘 Historique récent").classes(
                    "text-lg font-semibold text-white/90 mb-3"
                )
                history_col = ui.column().classes("w-full gap-3")
                refresh_history()


ui.run(title="IP Geolocation Premium", port=8080, dark=True)
