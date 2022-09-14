#file untuk delete item, show nama dan SKU saja untuk didelete
#kayaknya ganti sm html css pas udh bisa
#probably html css juga harus punya feature search, JS? probably gonna cry.
import psycopg

def show_full_info(found_user_input):
    print("{:<5} {:<70} {:<10} {:<10} {:<10} {:<10}".format("No.", "Name", "Capital", "Price", "SKU", "Date added"))
    found_number = 1
    for i in range(len(found_user_input)):
        print("{:<5} {:<70} {:<10} {:<10} {:<10} {}".format(found_number, found_user_input[i][1], found_user_input[i][2], found_user_input[i][3], found_user_input[i][4], found_user_input[i][5]))
        found_number += 1

def delete_item():
    with psycopg.connect(conninfo="postgresql://postgres:angjaya08102005@127.0.0.1:5432/tokopedia") as connection:
        with connection.cursor() as cursors:
            print("These are the list of items in Tokopedia Seller - iWL")
            #take all names and sku
            grab_data = cursors.execute("SELECT itemname, itemsku FROM topeditem ORDER BY itemsku ASC;")
            take_data = cursors.fetchall()
            print("{:<5} {:<70} {:<10}".format("No.", "Name", "SKU"))
            list_number = 1
            for i in range(len(take_data)):
                print("{:<5} {:<70} {:<10}".format(list_number, take_data[i][0], take_data[i][1]))
                list_number += 1
            print("----------------------------------------------------------------------------------------")
            while True:
                #minta nama barang / sku utk pilih item apa yang mau dibuang
                user_deleting = input("Input item name or SKU that you want to delete (Case sensitive)\nYour answer : ")
                #try utk kalo sku
                try:
                    user_delete = int(user_deleting)
                    find_user_input = cursors.execute("SELECT * FROM topeditem WHERE itemsku = %s"%(user_delete))
                    found_user_input = cursors.fetchall()
                    if found_user_input == []:
                        print("No SKU matches.")
                        continue
                    else:
                        show_full_info(found_user_input)
                #except kalo isinya itemname
                except:
                    find_user_input = cursors.execute("SELECT * FROM topeditem WHERE itemname LIKE '%{}%';".format(user_deleting))
                    found_user_input = cursors.fetchall()
                    if found_user_input == []:
                        print("No item name matches.")
                        continue
                    else:
                        show_full_info(found_user_input)
                print("-------------------------------------------------------------------------------------------")
                for a in range(len(found_user_input)):
                    while True:
                        make_sure = input("Are you sure to delete %s?\n(Yes / No) : "%(found_user_input[a][1]))
                        #jika ya, delete from topeditem where itemsku = <userinput>
                        if make_sure.lower() == "yes":
                            delete_confirm = cursors.execute("DELETE FROM topeditem WHERE itemsku = %s"%(found_user_input[a][4]))
                            print("Item deleted.")
                        break
                print("Returning to main menu...")
                break