import psycopg

#file untuk add items ke database topeditem

def add_new_item():
    with psycopg.connect(conninfo="postgresql://postgres:angjaya08102005@127.0.0.1:5432/tokopedia") as connection:
        with connection.cursor() as cursors:
            while True:
                #minta name
                user_add_name = input("Add items if there's a new product in Tokopedia Seller\n(type in 'cancel' if there's anything wrong, 'exit' to exit this menu.)\nName : ")
                if user_add_name.lower() == "cancel":
                    continue
                elif user_add_name.lower() == "exit":
                    break
                #minta modal
                user_add_cap = input("Capital (only numbers, no Rp.) : ")
                if user_add_cap.lower() == "cancel":
                    continue
                elif user_add_cap.lower() == "exit":
                    break
                else:
                    try:
                        user_add_capital = int(user_add_cap)
                    except:
                        print("Numbers only! No special characters or any words inside.\n")
                        continue
                #minta harga jual
                user_add_prc = input("Price you sell at Tokopedia (only numbers, no Rp.): ")
                if user_add_prc.lower() == "cancel":
                    continue
                elif user_add_prc.lower() == "exit":
                    break
                else:
                    try:
                        user_add_price = int(user_add_prc)
                    except:
                        print("Numbers only! No special characters or any words inside.\n")
                        continue
                #minta nomor seri barangnya di tokopedia atau SKU
                user_add_unit = input("Item SKU : ")
                if user_add_unit.lower() == "cancel":
                    continue
                elif user_add_unit.lower() == "exit":
                    break
                else:
                    try:
                        user_add_sku = int(user_add_unit)
                    except:
                        print("Numbers only! No special characters or any words inside.\n")
                        continue
                #pengecekan dulu apabila sudah benar
                print("=============================\nName : %s\nCapital : %s            Price for Sale : %s\nSKU : %s"%(user_add_name, user_add_capital, user_add_price, user_add_sku))
                isit_true = input("Does these seems correct?\nYes / No : ")
                if isit_true.lower() == "no":
                    continue
                #udh kelar minta2, ini sekarang nyoba untuk masukkin ke dalam databasenya.
                try:
                    cursors.execute("INSERT INTO topeditem(itemname, itemcapital, itemprice, itemsku) values('%s', '%s', '%s', '%s');"%(user_add_name, user_add_capital, user_add_price, user_add_sku))
                except:
                    print("There's a duplicate in either name / SKU, please re-enter the info.")
                    continue
                cursors.execute("SELECT * FROM topeditem order by itemid desc fetch first row only;")
                check_result = cursors.fetchall()
                if check_result == "" or check_result == None:
                    print("Something's wrong inside the code, may the developer fix it.")
                if isit_true.lower() == "yes":
                    print("New items added !")
                break
            print("Returning to main menu...")