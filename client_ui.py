from nicegui import ui
import requests


def query_server():
    hostname = server_input.value.strip().rstrip("/")
    ip = ip_input.value.strip()

    if not hostname or not ip:
        ui.notify("Hostname ou IP manquant", color="red")
        return

    if hostname.startswith("http://") or hostname.startswith("https://"):
        url = f"{hostname}/ip/{ip}"
    else:
        url = f"http://{hostname}/ip/{ip}"

    try:
        print("DEBUG URL =", url)
        r = requests.get(url, timeout=5)
        r.raise_for_status()
        data = r.json()
    except Exception as e:
        ui.notify(f"Erreur : {e}", color="red")
        return

    result_label.text = (
        f"IP : {data.get('ip')}\n"
        f"Pays : {data.get('country')}\n"
        f"Latitude : {data.get('latitude')}\n"
        f"Longitude : {data.get('longitude')}"
    )

    # Ouvrir la carte dans un nouvel onglet
    lat = data.get("latitude")
    lon = data.get("longitude")
    if lat is not None and lon is not None:
        map_url = (
            f"https://www.openstreetmap.org/?mlat={lat}&mlon={lon}#map=5/{lat}/{lon}"
        )
        ui.run_javascript(f'window.open("{map_url}", "_blank");')


# UI
ui.label("Géolocalisation d'IP").style("font-size: 24px; font-weight: bold")

server_input = ui.input(label="Adresse du serveur", value="127.0.0.1:8000")

ip_input = ui.input(label="IP cible (ex: 8.8.8.8)")

ui.button("Localiser", on_click=query_server)

result_label = ui.label("")

ui.run()
