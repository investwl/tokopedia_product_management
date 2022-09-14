#berurutan, import function sesuai urutan main menu.
from addItem import add_new_item
from showItem import show_item
from deleteItem import delete_item
from inputSold import input_sold
from monthlyCashflow import monthly_cashflow

while True:
    print("Tokopedia Seller - iWL -")
    print("Main menu Tokopedia Seller items - What to do ?\n========================")
    print("1. Show all items\n2. Add new items based on Tokopedia Seller manually (because no idea how to add it automatically)\n3. Delete existing item on Tokopedia Seller manually\n4. Input penjualan\n5. List modal per bulan\n6. Exit")

    user_input = int(input("Your choice : "))
    if user_input > 0 and user_input < 8:
        if user_input == 1:
            #file show all itemnya
            show_item()
        elif user_input == 2:
            #file add new items sesuai toped
            add_new_item()
        elif user_input == 3:
            #file delete items sesuai toped
            delete_item()
        elif user_input == 4:
            #ini untuk input barang apa aja yang dibeli orang, saat input bakal tertera datetime kedalam psql.
            input_sold()
        elif user_input == 5:
            #file modal total per bulan
            monthly_cashflow()
        elif user_input == 6:
            print("See you next time !")
            break
    else:
        print("Choose only the number that assigns its label. (e.g : 1, as of show all items)")