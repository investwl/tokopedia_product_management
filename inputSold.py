from time import strftime
import psycopg
from datetime import datetime
import pdb

#variable untuk show skrg saat user nginput
now = datetime.now()
month_now = now.strftime("%m")
year_now = now.strftime("%Y")

#ini file utk masukkin sebuah penjualan ke dalam psql
def format_printing(hold_info):
    print("{:<5} {:<70} {:<10} {:<10} {:<10}".format("No.", "Name", "Capital", "Price", "SKU"))
    list_number = 1
    for i in range(len(hold_info)):
        print("{:<5} {:<70} {:<10} {:<10} {:<10}".format(list_number, hold_info[i][1], hold_info[i][2], hold_info[i][3], hold_info[i][4]))
        list_number += 1

def input_sold():
    with psycopg.connect(conninfo="postgresql://postgres:angjaya08102005@127.0.0.1:5432/tokopedia") as connection:
        with connection.cursor() as cursors:
            #pdb.set_trace()
            hold_info = ""
            while True:
                #tanya dulu penjualan atau topads
                sold_input = input("Welcome, please choose if it's an item sold or topads.\n----------------------------------\nA. Item Sold            B. Topads\n(A / B) : ")
                #penjualan
                if sold_input.lower() == "a":
                    while True:
                        #minta nama / sku, type 'cancel' untuk keluar anytime, min 3 char
                        itemsold_input = input("Input name / sku the item that is sold with minimum of 3 characters.\n(Type in 'cancel' anytime to cancel the process)\nYour answer : ")
                        if itemsold_input.lower() == "cancel":
                            break
                        try:
                            itemsold_input = int(itemsold_input)
                            show_sku = cursors.execute("SELECT * FROM topeditem WHERE itemsku = %s;"%(itemsold_input))
                            hold_info = cursors.fetchall()
                            if len(hold_info) > 0:
                                format_printing(hold_info)
                            else:
                                print("No item found? Try again\n=======================")
                                continue
                        except:
                            if len(itemsold_input) < 3:
                                print("Min. 3 characters!")
                                continue
                            show_name = cursors.execute("SELECT * FROM topeditem WHERE itemname LIKE '%{}%';".format(itemsold_input))
                            hold_info = cursors.fetchall()
                            #jika len holdinfo diatas 0, baru bisa proceed
                            if len(hold_info) > 0:
                                format_printing(hold_info)
                                if len(hold_info) >= 2:
                                    print("=====================\nThere are more than one item detected, choose one item based on its SKU.")
                                    #input minta sku
                            else:
                                print("No item found? Try again\n=======================")
                                continue
                        while True:
                            ask_cancel = False
                            try:
                                ask_quantity = int(input("Input the quantity of item being sold (must be more than 0)\nQuantity : "))
                                if ask_quantity > 0:
                                    print("Successfully added !")
                                    cursors.execute("INSERT INTO topedsold(sold_name, sold_sku, sold_quantity, sold_date_month, sold_date_year) values('%s', %s, %s, %s, %s);"%(hold_info[0][1], hold_info[0][4], ask_quantity, int(month_now), int(year_now)))
                                    break
                            except:
                                if ask_quantity == "cancel":
                                    ask_cancel = True
                                    break
                        if ask_cancel == True:
                            continue
                        break
                #topads
                elif sold_input.lower() == "b":
                    #topads, berarti minta berapa ribu harga topadsnya, dalam format full angka
                    while True:
                        try:
                            ask_topads = input("How much money is used to pay topads?\nTopads : ")
                            if ask_topads.lower() == "cancel":
                                break
                            if int(ask_topads) > 0:
                                #ask for certainty
                                print("Topads : Rp. %s,-"%(ask_topads))
                                topads_verify = input("Are you sure with this amount of topads?\nYes / No : ")
                                if topads_verify.lower() == "yes":
                                    cursors.execute("INSERT INTO topedsold(sold_topads, sold_quantity, sold_date_month, sold_date_year) values(%s, %s, %s, %s);"%(ask_topads, 1, int(month_now), int(year_now)))
                                    break
                                elif topads_verify.lower() == "no":
                                    #masih benerin ini logic break continue thingynya
                                    continue
                        except:
                            pass
                    #input ke dalam bagian topads dan quantity
                else:
                    print("Wrong input! Try again")
                
                #user mau ngisi data lagi atau nggak, jika ya berarti continue, jika nggak ya break
                user_confirm_redo = False
                while True:
                    user_redo = input("Input more data ?\n(Yes / No) : ")
                    if user_redo.lower() == "yes":
                        user_confirm_redo = True
                        break
                    elif user_redo.lower() == "no":
                        break
                    else:
                        print("Yes or No only.")
                    
                if user_confirm_redo == True:
                    continue
                elif user_confirm_redo == False:
                    break

                break
            print("Returning to main menu...")