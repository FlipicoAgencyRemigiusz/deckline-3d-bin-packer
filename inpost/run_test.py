from test_off import pack_items
from py3dbp import Item

# Lista przedmiotów z użyciem parametru `quantity`
items_to_pack = [
    {"item": Item('Large_Item_1', 'large', 'cube', (35, 30, 25), 5, 1, 100, True, 'blue'), "quantity": 2},
    {"item": Item('Medium_Item_1', 'medium', 'cube', (20, 20, 20), 4, 1, 100, True, 'purple'), "quantity": 3},
    {"item": Item('Small_Item_1', 'small', 'cube', (10, 10, 10), 2, 1, 100, True, 'green'), "quantity": 5},
    {"item": Item('Tiny_Item_1', 'tiny', 'cube', (5, 5, 5), 0.5, 1, 100, True, 'pink'), "quantity": 10},
    # Dodaj więcej elementów według potrzeb, ustawiając ich `quantity`
]

# Funkcja do konwersji `quantity` na rzeczywistą listę przedmiotów
def expand_items(items_with_quantity):
    expanded_items = []
    for entry in items_with_quantity:
        expanded_items.extend([entry["item"]] * entry["quantity"])
    return expanded_items

# Inicjalizacja liczników
iteration_count = 0
remaining_items = expand_items(items_to_pack)  # Rozwiń listę na podstawie `quantity`

# Iteracja aż wszystkie przedmioty będą dopasowane
while remaining_items:
    iteration_count += 1
    print(f"\n--- Iteration {iteration_count} ---")
    remaining_items = pack_items(remaining_items)

print(f"Total number of iterations: {iteration_count}")
