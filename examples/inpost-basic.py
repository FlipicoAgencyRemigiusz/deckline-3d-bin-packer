from py3dbp import Packer, Bin, Item, Painter
import matplotlib.pyplot as plt
import random

# Locker prices (replace these with actual current prices if available)
locker_prices = {
    'A': 8.99,  # Price for locker size A
    'B': 10.99,  # Price for locker size B
    'C': 12.99  # Price for locker size C
}

# Define dimensions for InPost lockers [cm]
locker_dimensions = {
    'A': (8, 38, 64),
    'B': (19, 38, 64),
    'C': (41, 38, 64)
}


def get_dimensions(dimensions_str):
    """Parse dimension string and return a tuple of (width, height, depth)."""
    return tuple(map(int, dimensions_str.split('x')))


def get_random_color():
    """Generates a random color in hex format."""
    return "#{:06x}".format(random.randint(0, 0xFFFFFF))


def add_items_to_packer(packer, cart_items):
    """Add items to the packer from the cart with parsed dimensions."""
    for item in cart_items:
        width, height, depth = get_dimensions(item["dimensions"])
        color = get_random_color()  # Assign a random color to each item
        for _ in range(item["quantity"]):
            packer.addItem(Item(item["id"], item["name"], 'cube', (width, height, depth), 1, 1, 100, True, color))


def optimize_packing(cart_items):
    """Optimize packing of items into the smallest available locker."""
    best_solution = None
    best_price = float('inf')

    # Test each locker size
    for locker_size, dimensions in locker_dimensions.items():
        packer = Packer()
        packer.addBin(Bin(locker_size, dimensions, 25))
        add_items_to_packer(packer, cart_items)

        # Pack items and calculate costs
        packer.pack(bigger_first=True, fix_point=True, check_stable=True, support_surface_ratio=0.75,
                    number_of_decimals=0)
        bin_result = packer.bins[0]

        # Calculate space utilization and check if all items fit
        fitted_volume = sum(item.width * item.height * item.depth for item in bin_result.items)
        locker_volume = dimensions[0] * dimensions[1] * dimensions[2]
        space_utilization = round(fitted_volume / locker_volume * 100, 2)

        if not bin_result.unfitted_items and locker_prices[locker_size] < best_price:
            best_solution = (locker_size, bin_result, space_utilization)
            best_price = locker_prices[locker_size]

    return best_solution, best_price


def plot_solution(bin_result, locker_size):
    """Plot the items within the locker bin."""
    painter = Painter(bin_result)
    fig = painter.plotBoxAndItems(
        title=f"InPost Locker {locker_size} Packing",
        alpha=0.5,
        write_num=True,
        fontsize=5
    )
    fig.show()


# Example usage
if __name__ == "__main__":
    # Test items
    cart_items = [
        {"id": "item1", "name": "Large Item 1", "quantity": 7, "dimensions": "39x22x12"},
        {"id": "item2", "name": "Small Item 1", "quantity": 1, "dimensions": "22x10x5"},
        {"id": "item4", "name": "Small Item 2", "quantity": 1, "dimensions": "20x10x5"}
    ]

    # Find optimal locker size and cost
    solution, price = optimize_packing(cart_items)
    if solution:
        locker_size, bin_result, space_utilization = solution
        print(f"Optimal locker: {locker_size} with price: {price} PLN")
        print(f"Space utilization: {space_utilization}%")

        # Plot the solution
        plot_solution(bin_result, locker_size)
    else:
        print("No feasible solution found for packing.")