import flask
from flask import request, jsonify
from flask_cors import CORS
from py3dbp import Item
from inpost.test_off import pack_items  # Import z podfolderu 'inpost'
import requests
import threading
import time
from datetime import datetime

# Inicjalizacja aplikacji Flask
app = flask.Flask(__name__)
CORS(app, origins=["https://www.deckline.pl"])  # Zezwalaj tylko na określony origin

# URL do pingowania
PING_URL = "https://deckline-3d-bin-packer.onrender.com"  # Zamień na swój URL
PING_INTERVAL = 30  # Interwał w sekundach (30 sekund)


# Funkcja pingująca URL
def reload_website():
    while True:
        try:
            response = requests.get(PING_URL)
            print(f"Reloaded at {datetime.now().isoformat()}: Status Code {response.status_code}")
        except requests.RequestException as error:
            print(f"Error reloading at {datetime.now().isoformat()}: {error}")

        time.sleep(PING_INTERVAL)


# Uruchomienie pingowania w tle
threading.Thread(target=reload_website, daemon=True).start()


# Trasa testowa
@app.route('/')
def hello():
    return "Welcome to 3D packing API!"

# Endpoint do uruchomienia procesu pakowania
@app.route('/runPacking', methods=["POST"])
def run_packing():
    # Pobranie danych z JSON
    data = request.json

    # Sprawdzenie, czy JSON zawiera klucz 'items'
    if not data or 'items' not in data:
        return jsonify({"success": False, "reason": "Missing items data"}), 400

    print('data: ', data)
    items_to_pack = data['items']

    # Konwersja przedmiotów z ilością na obiekty Item
    def expand_items(items_with_quantity):
        expanded_items = []
        for entry in items_with_quantity:
            item = Item(
                entry['name'], entry['type'], 'cube',
                (entry['width'], entry['height'], entry['depth']),
                entry['weight'], 1, 100, True, entry['color']
            )
            # Dodajemy `item` tyle razy, ile wynosi `quantity`
            expanded_items.extend([item] * entry['quantity'])
        return expanded_items

    expanded_items = expand_items(items_to_pack)

    # Proces pakowania
    iteration_count = 0
    remaining_items = expanded_items

    while remaining_items:
        iteration_count += 1
        remaining_items = pack_items(remaining_items)  # Funkcja powinna zwracać niezapakowane przedmioty

    # Zwrot odpowiedzi
    return jsonify({"success": True, "iteration_count": iteration_count})


# Uruchomienie serwera
if __name__ == "__main__":
    print("* Starting web service...")
    app.run(host='0.0.0.0', port=5050, debug=True)
