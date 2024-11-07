from py3dbp import Packer, Bin, Item, Painter
import time
from decimal import Decimal

start = time.time()

# InPost "C" parcel size dimensions (adjust these to InPost's actual C size limits)
inpost_c_bin_dimensions = (Decimal(39), Decimal(22), Decimal(64))  # Adjust to InPost's actual size C limits
max_weight = Decimal(25)  # Example max weight limit, adjust accordingly

# Initialize the packing function
packer = Packer()

# Function to add a new InPost "C" size bin
def add_new_inpost_c_bin():
    return Bin('InPost_C_Bin', inpost_c_bin_dimensions, max_weight, corner=0, put_type=1)

# Initialize bin count
total_bins_used = 0  # Start counting from the first bin

# Define cart items with quantities
cart_items = [
    {"id": "item1", "name": "Large Item 1", "quantity": 6, "dimensions": "39x22x12"},
    {"id": "item2", "name": "Small Item 1", "quantity": 1, "dimensions": "22x10x5"},
    {"id": "item4", "name": "Small Item 2", "quantity": 1, "dimensions": "20x10x5"}
]

# Convert cart items to Item instances and add them to the packer
item_instances = []  # New list to keep track of items to be packed
for item_data in cart_items:
    width, height, depth = map(Decimal, item_data["dimensions"].split("x"))
    for _ in range(item_data["quantity"]):
        item_instances.append(
            Item(
                partno=item_data["id"],
                name=item_data["name"],
                typeof='cube',
                WHD=(width, height, depth),
                weight=Decimal(1),  # Set appropriate weight for each item
                level=1,
                loadbear=100,
                updown=True,
                color='blue'  # Optional color for differentiation
            )
        )

# Start packing process with a max attempt limit to prevent infinite loop
max_attempts = 10  # Set a reasonable limit for retries
attempt = 0

while item_instances and attempt < max_attempts:
    attempt += 1  # Increment the attempt counter
    current_bin = add_new_inpost_c_bin()
    packer.addBin(current_bin)

    # Przenieś przedmioty do packera na bieżąco
    for item in item_instances:
        packer.addItem(item)

    # Pack items into the bin
    packer.pack(
        bigger_first=True,
        distribute_items=True,
        fix_point=True,
        check_stable=True,
        support_surface_ratio=0.75,
        number_of_decimals=0
    )

    # Print packed results for the current bin
    print(f"** Bin: {current_bin.partno} **")
    print("Fitted items:")
    volume_t = Decimal(0)
    for item in current_bin.items:
        volume = item.width * item.height * item.depth
        volume_t += volume
        print(f"- {item.partno}, Pos: {item.position}, Volume: {volume}, Color: {item.color}")

    space_utilization = round(
        float(volume_t) / (float(current_bin.width) * float(current_bin.height) * float(current_bin.depth)) * 100, 2)
    print(f"Space utilization: {space_utilization}%")

    # Increment the bin count
    total_bins_used += 1

    # Remove only fitted items from item_instances
    for fitted_item in current_bin.items:
        for i, instance in enumerate(item_instances):
            if fitted_item.partno == instance.partno:
                del item_instances[i]
                break

    # Check if there are any unfitted items that cannot be packed and print a warning if max attempts reached
    if attempt == max_attempts and item_instances:
        print("Warning: Some items could not be packed within the maximum attempt limit.")
        break

    # Visualize the packing result
    painter = Painter(current_bin)
    fig = painter.plotBoxAndItems(title=current_bin.partno, alpha=0.8, write_num=False, fontsize=10)
    fig.show()

# Print the final number of bins used
print(f"Total bins used: {total_bins_used}")

stop = time.time()
print('Total time used:', stop - start)
