import psycopg
#list menghtiung modal per bulan

def month_output(month_number):
    if month_number == 1:
        return 'January'
    elif month_number == 2:
        return 'February'
    elif month_number == 3:
        return 'March'
    elif month_number == 4:
        return 'April'
    elif month_number == 5:
        return 'May'
    elif month_number == 6:
        return 'June'
    elif month_number == 7:
        return 'July'
    elif month_number == 8:
        return 'August'
    elif month_number == 9:
        return 'September'
    elif month_number == 10:
        return 'October'
    elif month_number == 11:
        return 'November'
    elif month_number == 12:
        return 'December'

def monthly_cashflow():
    with psycopg.connect(conninfo="postgresql://postgres:angjaya08102005@127.0.0.1:5432/tokopedia") as connection:
        with connection.cursor() as cursors:
            
            print("Welcome to Monthly Capital.")
            #perulangan karena siapa tau nanti user mau ngisi lagi
            while True:
                #variable untuk simpan sold id yang bulannya sesuai dengan pengecekan line 31
                save_sold_id = []
                total_monthly_capital = 0
                total_monthly_price = 0
                #minta dulu bulan dan tahun yang mau discan
                while True:
                    try:
                        user_input_month = int(input("Input month with numbers (1 : January, 12 : December) : "))
                    except:
                        print("Only input integers")
                        continue
                    if user_input_month < 0 and user_input_month > 13:
                        print("Can only accept 1 - 12, as of January -  December. Try again !")
                        continue
                    try:
                        user_input_year = int(input("Input year (yyyy format ex. 2022, starts from 2022): "))
                    except:
                        print("Only input integers")
                        continue
                    if user_input_year < 2022:
                        print("A year shall be greater than 2021, meaning it starts from 2022 because this data firstly created in 2022. Try again!")
                        continue
                    break
                #scan bulan tahun yg sesuai dengan yang ada di dalam database
                cursors.execute("SELECT * FROM topedsold;")
                take_date = cursors.fetchall()
                for i in range(len(take_date)):
                    if user_input_month == take_date[i][5] and user_input_year == take_date[i][6]:
                        #ini kumpulin semua id yang sama bulan dan tahun soldnya
                        save_sold_id.append(take_date[i][0])
                #jika isi save_sold_id kosong karena gak ad yg sama, maka outputnya none karena gak ada isi
                if save_sold_id == []:
                    print("No items or topads history on %s %s! Try another month and year!"%(month_output(user_input_month), user_input_year))
                    continue
                #sudah dapat id dari topedsold yg bulan tahunnya sama sesuai input user,
                #maka for loop untuk cari capital item sesuai id barang di topedsold
                for id in range(len(save_sold_id)):
                    #dari id yang topedsold, ambil dulu namanya dan simpan dlu namanya dlm var
                    #lalu carilah capital si item tersebut lalu dikalikan dengan amount
                    cursors.execute("SELECT sold_name, sold_quantity FROM topedsold WHERE sold_id = %s;"%(save_sold_id[id]))
                    name_from_id = cursors.fetchall()
                    if name_from_id[0][0] == '':
                        cursors.execute("SELECT sold_topads FROM topedsold WHERE sold_id = %s;"%(save_sold_id[id]))
                        obtain_topads_id = cursors.fetchone()
                        total_monthly_capital = total_monthly_capital + obtain_topads_id[0]
                    else:
                        cursors.execute("SELECT itemcapital, itemprice FROM topeditem WHERE itemname = '%s';"%(name_from_id[0][0]))
                        capital_from_name = cursors.fetchall()
                        print(capital_from_name)
                        total_monthly_capital = total_monthly_capital + (capital_from_name[0][0] * name_from_id[0][1])
                        total_monthly_price = total_monthly_price + (capital_from_name[0][1] * name_from_id[0][1])
                        #show result capital
                print("\nThe capital for %s %s is Rp. %s,-\nTotal profit from %s product = Rp. %s,-"%(month_output(user_input_month), user_input_year, total_monthly_capital, len(save_sold_id), (total_monthly_price - total_monthly_capital)))
                #input apabila masih mau cek capital month atau udahan dan kembali ke main menu
                repeating = False
                while True:
                    user_check_again = input("Do another check on monthly capital?\n(Yes / No) : ")
                    if user_check_again.lower() == "yes":
                        repeating = True
                        break
                    elif user_check_again.lower() == "no":
                        break
                    else:
                        print("Yes or No only!")
                        continue
                if repeating == True:
                    continue
                print("Returning to main menu..")
                break