from py3dbp import Packer, Bin, Item, Painter


def pack_items(items_to_pack):
    # Definiowanie bin'a InPost C
    bin_inpost_c = Bin(partno='InPost_C', WHD=(41, 38, 64), max_weight=25)

    # Inicjalizacja packera
    packer = Packer()
    packer.addBin(bin_inpost_c)

    # Dodanie itemów do packera w kolejności od największego do najmniejszego
    for item in sorted(items_to_pack, key=lambda x: x.getVolume(), reverse=True):
        packer.addItem(item)

    # Pakowanie do bin'a InPost C
    packer.pack(bigger_first=True, distribute_items=False)

    # Zbiera unfitted items
    unfitted_items = []

    # Wyświetlanie wyników i wizualizacja
    for b in packer.bins:
        print("Bin:", b.string())

        print("Fitted Items:")
        for item in b.items:
            print(" -", item.string())

        print("Unfitted Items:")
        for item in b.unfitted_items:
            print(" -", item.string())
            unfitted_items.append(item)  # Dodaj do listy elementów, które się nie zmieściły

        # Rysowanie wykresu 3D dla zawartości bin'a
        painter = Painter(b)
        fig = painter.plotBoxAndItems(
            title=b.partno,
            alpha=0.3,  # Ustawienie przezroczystości dla lepszej widoczności
            write_num=True,  # Wyświetlanie numerów części
            fontsize=8  # Rozmiar tekstu na wykresie
        )
        fig.savefig(f"plot_{b.partno}.png")  # Zapis wykresu do pliku PNG
        fig.show()

    return unfitted_items
