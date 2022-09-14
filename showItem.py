from xml.dom import UserDataHandler
import psycopg
#jika sudah mau bikin versi html nya, maka printnya akan pakai cara html / sepikirannya nanti.
#belajar html css for better output.

def show_item():
    with psycopg.connect(conninfo="postgresql://postgres:angjaya08102005@127.0.0.1:5432/tokopedia") as connection:
        with connection.cursor() as cursors:
            show_them_all = cursors.execute("SELECT itemname, itemcapital, itemprice, itemsku, itemdate FROM topeditem ORDER BY itemsku ASC;")
            show_them = cursors.fetchall()
            #ini untuk struktur outputnya
            print("{:<5} {:<70} {:<10} {:<10} {:<10} {:<10}".format("No.", "Name", "Capital", "Price", "SKU", "Date added"))
            list_number = 1
            for i in range(len(show_them)):
                print("{:<5} {:<70} {:<10} {:<10} {:<10} {}".format(list_number, show_them[i][0], show_them[i][1], show_them[i][2], show_them[i][3], show_them[i][4]))
                list_number = list_number + 1
            while True:
                user_done = input("Done?\n(Put 'Yes' if so) : ")
                if user_done.lower() == "yes":
                    break
            print("Returning to main menu...")