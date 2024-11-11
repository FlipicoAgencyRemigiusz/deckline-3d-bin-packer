import flask
from flask import request, jsonify
from flask_cors import CORS
from py3dbp import Item
from inpost.test_off import pack_items  # Import z podfolderu 'inpost'

# Inicjalizacja aplikacji Flask
app = flask.Flask(__name__)
CORS(app, origins=["https://www.deckline.pl"])  # Zezwalaj tylko na określony origin

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
