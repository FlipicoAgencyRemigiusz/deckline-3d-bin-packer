import flask, json, random
from flask import request, jsonify
from flask_cors import cross_origin
from py3dbp import Packer, Bin, Item
from inpost.test_off import pack_items  # import z podfolderu 'inpost'

# init flask
app = flask.Flask(__name__)


# Example route to test the API
@app.route('/')
@cross_origin()
def hello():
    return "Welcome to 3D packing API!"


# Endpoint for running the packing script
@app.route('/runPacking', methods=["POST"])
@cross_origin()
def run_packing():
    data = request.json  # Oczekuje JSON z itemami

    if not data or 'items' not in data:
        return jsonify({"success": False, "reason": "Missing items data"}), 400

    items_to_pack = data['items']

    # Convert input items to py3dbp Item objects
    def expand_items(items_with_quantity):
        expanded_items = []
        for entry in items_with_quantity:
            item = Item(
                entry['name'], entry['type'], 'cube',
                (entry['width'], entry['height'], entry['depth']),
                entry['weight'], 1, 100, True, entry['color']
            )
            expanded_items.extend([item] * entry['quantity'])
        return expanded_items

    expanded_items = expand_items(items_to_pack)

    # Run the packing process
    iteration_count = 0
    remaining_items = expanded_items

    while remaining_items:
        iteration_count += 1
        remaining_items = pack_items(remaining_items)

    return jsonify({"success": True, "iteration_count": iteration_count})


if __name__ == "__main__":
    print("* Starting web service...")
    app.run(host='0.0.0.0', port=5050, debug=True)
