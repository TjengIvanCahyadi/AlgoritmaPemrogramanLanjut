# Import date untuk tanggal di program
from datetime import date

# Import time untuk waktu di program
import time

# Import OS untuk clear screen
import os

# Import string untuk penggunaan ascii
import string

# Import random untuk randomize no faktur penjualan
import random

# Import pandas untuk csv
import pandas as pd

# Untuk fungsi pyssword
import sys
from msvcrt import getch


# Fungsi Clear Screen
def cs():
    os.system("cls" if os.name == "nt" else "clear")


# Membuat huruf random untuk nomor faktur
def membuat_huruf(banyak_huruf):
    return random.sample(string.ascii_letters, banyak_huruf)


# Membuat angka random untuk nomor faktur
def membuat_angka(banyak_angka):
    angka_random = []
    for i in range(banyak_angka):
        angka_random.append(str(random.randint(0, 9)))
    return angka_random


# Fungsi Masking Password Menjadi Bintang-BIntang
def pyssword(prompt="< Masukan PIN: "):
    pwd = ""
    sys.stdout.write(prompt)
    sys.stdout.flush()
    while True:
        key = ord(getch())
        if key == 13:  # Return Key
            sys.stdout.write("\n")
            return pwd
            break
        if key == 8:  # Backspace key
            if len(pwd) > 0:
                # Erases previous character
                sys.stdout.write("\b" + " " + "\b")
                sys.stdout.flush()
                pwd = pwd[:-1]
        else:
            # Masks user input
            char = chr(key)
            sys.stdout.write("*")
            sys.stdout.flush()
            pwd = pwd + char


def tanggal_dan_waktu():
    # Assign tanggal dan waktu
    today = date.today()
    waktu = time.localtime()
    tanggal = "%02d-%02d-%04d" % (today.day, today.month, today.year)
    jam = "%02d:%02d:%02d" % (waktu.tm_hour, waktu.tm_min, waktu.tm_sec)
    return tanggal,jam


# Write riwayat transaksi to file csv
def riwayat_transaksi_to_csv():

    tanggals = []
    jams = []
    nomor_fakturs = []
    merks = []
    jenis_barangs = []
    quantities = []
    hargas = []
    subtotals = []
    totals = []
    bayars = []
    kembalians = []

    for sublist in riwayat:
        for merk in sublist[3]:
            for jenis_barang in sublist[3][merk]:
                tanggals.append(sublist[0])
                jams.append(sublist[1])
                nomor_fakturs.append(sublist[2])
                totals.append(sublist[4])
                bayars.append(sublist[5])
                kembalians.append(sublist[6])

    for sublist in riwayat:
        for merk in sublist[3]:
            for jenis_barang in sublist[3][merk]:
                merks.append(merk)
                jenis_barangs.append(jenis_barang)
                quantities.append(sublist[3][merk][jenis_barang]['quantity'])
                hargas.append(sublist[3][merk][jenis_barang]['harga'])
                subtotals.append(sublist[3][merk][jenis_barang]['subtotal'])

    data = {
            "tanggal": tanggals,
            "jam": jams,
            "nomor faktur": nomor_fakturs,
            "merk": merks,
            "jenis barang": jenis_barangs,
            "quantity": quantities,
            "harga": hargas,
            "subtotal": subtotals,
            "total": totals,
            "bayar": bayars,
            "kembalian": kembalians
            }
    
    data_riwayat = pd.DataFrame.from_dict(data)

    data_riwayat.to_csv('Data Riwayat Transaksi.csv', index=False)


# Write barang rusak to file csv
def barang_rusak_to_csv():
  
    merk = []
    jenis_barang = []
    tanggal_lapor = []
    jam_lapor = []
    status = []

    for barang in barang_rusak:
        merk.append(barang[0])
        jenis_barang.append(barang[1])
        tanggal_lapor.append(barang[2])
        jam_lapor.append(barang[3])
        status.append(barang[4])
  
    data = {
            "merk": merk,
            "jenis barang": jenis_barang,
            "tanggal lapor": tanggal_lapor,
            "jam_lapor": jam_lapor,
            "status": status
            }

    data_rusak = pd.DataFrame.from_dict(data)

    data_rusak.to_csv('Data Rusak.csv', index=False)


# Write barang to file csv
def barang_to_csv():
    merks = []
    jenis_barangs = []
    quantities = []
    hargas = []

    for merk in barang:
        for jenis_barang in barang[merk]:
            merks.append(merk)
            jenis_barangs.append(jenis_barang)
            quantities.append(barang[merk][jenis_barang]['quantity'])
            hargas.append(barang[merk][jenis_barang]['harga'])

    data = {
            "merk": merks,
            "jenis barang": jenis_barangs,
            "quantity": quantities,
            "harga": hargas
            }

    data_barang = pd.DataFrame.from_dict(data)
    data_barang.to_csv('Data Barang.csv', index=False)


# Read File csv riwayat transaksi
def read_riwayat_transaksi():

    data_transaksi = pd.read_csv('Data Riwayat Transaksi.csv')

    data_trx_groupped = data_transaksi.groupby(["nomor faktur"])

    kode_trx = data_trx_groupped.groups

    riwayats = []

    for nmr_faktur in list(kode_trx.keys()):

        trx_bds_faktur = data_trx_groupped.get_group(nmr_faktur)

        data_trx = trx_bds_faktur.iloc[0]

        data_faktur_skrg = [data_trx['tanggal'], data_trx['jam'], data_trx['nomor faktur'],
                            {}, data_trx['total'], data_trx['bayar'], data_trx['kembalian']]

        barang_skrg = {}

        trx_groupped_by_merk = trx_bds_faktur.groupby(["merk"])

        merk2 = trx_groupped_by_merk.groups

        for merk in list(merk2.keys()):

            ### Siapkan variabel untuk simpan barang
            barang_skrg[merk] = {}

            ### Ambil row yang punya barang dengan merk tsb
            barang2 = trx_groupped_by_merk.get_group(merk)

            ### Loop over row tsb
            for index, row in barang2.iterrows():

                ### Ambil data2nya
                jenis_barang = row['jenis barang']
                quantity = row['quantity']
                harga = row['harga']
                subtotal = row['subtotal']
                
                ### Input ke variabel di line 17
                barang_skrg[merk][jenis_barang] = {
                    'quantity': quantity, 
                    'harga': harga, 
                    'subtotal': subtotal
                }

        ### Timpa data
        data_faktur_skrg[3] = barang_skrg

        ### Append ke riwayat
        riwayats.append(data_faktur_skrg)
    
    return riwayats


# Read File csv barang rusak
def read_rusak():
    barang_rusak = pd.read_csv("Data Rusak.csv")
    barang_rusak = barang_rusak.values.tolist()
    return barang_rusak


# Read file csv barang
def read_barang():
    data_barang = pd.read_csv("Data Barang.csv")
    data_barang = data_barang.values.tolist()

    kumpulan_barang = {}

    for barang in data_barang:
        nama_merk = barang[0]
        jenis_barang = barang[1]
        kuantitas = barang[2]
        harga = barang[3]

        # KALAU MERK BELUM TERDAFTAR/ADA DI KUMPULAN BARANG
        # MAKA KITA BUAT/DAFTARKAN MERKNYA
        if nama_merk not in kumpulan_barang.keys():
            kumpulan_barang[nama_merk] = {}

        # TAMBAHKAN BARANG KE MERK TERSEBUT
        kumpulan_barang[nama_merk][jenis_barang] = {
            "quantity": kuantitas,
            "harga": harga,
        }

    return kumpulan_barang


# Dictionary stock barang
barang = read_barang()

# List barang rusak
barang_rusak = read_rusak()

# List riwayat transaksi
riwayat = read_riwayat_transaksi()

# dictionary untuk menampung belanjaan
belanjaan = {}

# List untuk menampung hasil search barang rusak
ditemukan = []

# Identifier / pengenal
identifier = 0


def hapus_riwayat():

    # Menampilkan seluruh data riwayat transaki
    print(f"|{'-'*263}|")
    print(
        f"|\tNo\t|\tTanggal\t\t|\tJam\t\t|\tNomor Faktur\t\t|\tMerk\t\t|\tJenis Barang\t|\tQuantity\t|\tHarga\t\t|\tSubTotal\t|\tTotal\t|\tBayar\t|   Kembalian   |"
    )
    print(f"|{'-'*263}|")

    for i in range(len(riwayat)):

        print(f"|\t{i+1}\t|", end="")

        for j in range(len(riwayat[i])):

            if j == 3:

                for key1, value1 in riwayat[i][j].items():
                    if len(key1) >= 8:
                        print(f"\t{key1}\t|", end="")
                    else:
                        print(f"\t{key1}\t\t|", end="")

                    for key2, value2 in value1.items():

                        if len(str(key2)) >= 8:
                            print(f"\t{key2}\t|", end="")
                        else:
                            print(f"\t{key2}\t\t|", end="")

                        for key3, value3 in value2.items():
                            if len(str(value3)) >= 8:
                                print(f"\t{value3}\t|", end="")
                            else:
                                print(f"\t{value3}\t\t|", end="")

            else:
                if len(str(riwayat[i][j])) <= 13:
                    print(f"\t{riwayat[i][j]}\t|", end="")
                else:
                    print(f"\t{riwayat[i][j]}\t|", end="")

        print()
    print(f"|{'-'*263}|")

    while True:
        
        pilihan = input("Masukkan nomor: ")

        if pilihan.isnumeric() == True:
            
            pilihan = int(pilihan)

            if pilihan >= 1 and pilihan <= len(riwayat):

                break

            else:

                print ("Pilihan Tidak Ada !")
        
        else:

            print ("Tolong Masukkan Angka !")

    del riwayat[pilihan-1]

    riwayat_transaksi_to_csv()

    # Jika ingin kembali ke menu tampilkan barang rusak tekan enter
    input("Tekan enter untuk kembali...")

    # Memanggil fungsi clear screen
    cs()

    riwayat_transaksi()


def tampil_riwayat():

    # Menampilkan seluruh data riwayat transaki
    print(f"|{'-'*263}|")
    print(
        f"|\tNo\t|\tTanggal\t\t|\tJam\t\t|\tNomor Faktur\t\t|\tMerk\t\t|\tJenis Barang\t|\tQuantity\t|\tHarga\t\t|\tSubTotal\t|\tTotal\t|\tBayar\t|   Kembalian   |"
    )
    print(f"|{'-'*263}|")

    for i in range(len(riwayat)):

        print(f"|\t{i+1}\t|", end="")

        for j in range(len(riwayat[i])):

            if j == 3:

                for key1, value1 in riwayat[i][j].items():
                    if len(key1) >= 8:
                        print(f"\t{key1}\t|", end="")
                    else:
                        print(f"\t{key1}\t\t|", end="")

                    for key2, value2 in value1.items():

                        if len(str(key2)) >= 8:
                            print(f"\t{key2}\t|", end="")
                        else:
                            print(f"\t{key2}\t\t|", end="")

                        for key3, value3 in value2.items():
                            if len(str(value3)) >= 8:
                                print(f"\t{value3}\t|", end="")
                            else:
                                print(f"\t{value3}\t\t|", end="")

            else:
                if len(str(riwayat[i][j])) <= 13:
                    print(f"\t{riwayat[i][j]}\t|", end="")
                else:
                    print(f"\t{riwayat[i][j]}\t|", end="")

        print()
    print(f"|{'-'*263}|")

    # Jika ingin kembali, tekan enter
    input("Tekan enter untuk kembali...")

    # Memanggil fungsi clear screen
    cs()

    if identifier == "admin":
        riwayat_transaksi()
    else:
        kasir()


def riwayat_transaksi():
    
    while True:

        print (f"<{'-'*100}>")
        print (f"< Riwayat Transaksi >")
        print (f"<{'-'*100}>")
        print (f"< [1] Tampilkan Riwayat Transaksi >")
        print (f"< [2] Hapus Riwayat Transaksi >")
        print (f"< [3] Kembali >")
        print (f"<{'-'*100}>")
        
        try:
            pilihan = int(input("< Masukkan pilihan: "))

            cs()

            if pilihan >= 1 and pilihan <= 3:

                if pilihan == 1:
                    tampil_riwayat()
                elif pilihan == 2:
                    hapus_riwayat()
                elif pilihan == 3:
                    admin()

                break

            else:

                print ("Pilihan Tidak Tersedia !")

        except ValueError:

            cs()
            print(f"{' '*7}Tolong Masukkan Angka !{' '*7}")


def bubble_sort_rusak(pilih_urutan, pilih_urutkan_sesuai):

    # Ascending
    if pilih_urutan == 1:
        urut = False

        while not urut:
            urut = True

            for i in range(0, len(barang_rusak) - 1):
                if (
                    barang_rusak[i][pilih_urutkan_sesuai - 1]
                    > barang_rusak[i + 1][pilih_urutkan_sesuai - 1]
                ):
                    urut = False
                    barang_rusak[i], barang_rusak[i + 1] = (
                        barang_rusak[i + 1],
                        barang_rusak[i],
                    )

    # Descending
    elif pilih_urutan == 2:
        urut = False

        while not urut:
            urut = True

            for i in range(0, len(barang_rusak) - 1):
                if (
                    barang_rusak[i][pilih_urutkan_sesuai - 1]
                    < barang_rusak[i + 1][pilih_urutkan_sesuai - 1]
                ):
                    urut = False
                    barang_rusak[i], barang_rusak[i + 1] = (
                        barang_rusak[i + 1],
                        barang_rusak[i],
                    )


def sequential_search_rusak(pilih_cari_sesuai, dicari):

    for i in range(len(barang_rusak)):
        if barang_rusak[i][pilih_cari_sesuai] == dicari:
            ditemukan.append(barang_rusak[i])

    # Menampilkan seluruh data barang rusak
    print(f"||{'='*134}||")
    print(
        f"||\tNo\t||\tMerk\t\t||\tJenis Barang\t||\tTanggal\t\t||\tWaktu\t\t||\tStatus\t\t||"
    )
    print(f"||{'='*134}||")
    for i in range(len(ditemukan)):
        print(f"||\t{i+1}\t||", end="")
        for j in range(len(ditemukan[i])):
            if len(ditemukan[i][j]) <= 7:
                print(f"\t{ditemukan[i][j]}\t\t||", end="")
            else:
                print(f"\t{ditemukan[i][j]}\t||", end="")
        print()
    print(f"||{'='*134}||")

    # Jika ingin kembali ke menu tampilkan barang rusak tekan enter
    input("Tekan enter untuk kembali...")

    cs()

    ditemukan.clear()


def cari_rusak():

    while True:

        print(f"<---------------------->")
        print(f"<      Cari Sesuai     >")
        print(f"<---------------------->")
        print(f"< [1] Merk             >")
        print(f"< [2] Jenis Barang     >")
        print(f"< [3] Tanggal          >")
        print(f"< [4] Jam              >")
        print(f"< [5] Status           >")
        print(f"< [6] Kembali          >")
        print(f"<---------------------->")

        try:

            cari_sesuai = int(input("< Masukkan pilihan: "))

            cs()

            if cari_sesuai == 1:
                
                cari = str(input("< Masukkan Merk yang Dicari: "))

                cs()

                sequential_search_rusak(0, cari)

            elif cari_sesuai == 2:

                cari = str(input("< Masukkan Jenis Barang yang Dicari: "))

                cs()

                sequential_search_rusak(1, cari)

            elif cari_sesuai == 3:

                cari = str(input("< Masukkan Tanggal yang Dicari (09-02-2021): "))

                cs()

                sequential_search_rusak(2, cari)

            elif cari_sesuai == 4:

                cari = str(input("< Masukkan Jam yang Dicari (23:22:00): "))

                cs()

                sequential_search_rusak(3, cari)

            elif cari_sesuai == 5:

                cari = str(input("< Masukkan Status yang Dicari: "))

                cs()

                sequential_search_rusak(4, cari)

            elif cari_sesuai == 6:

                cs()
                if identifier == "admin":
                    barang_rusak_admin()
                else:
                    barang_rusak_kasir()
                break

            else:

                cs()
                print(f"{' '*11}Pilihan tidak ada!{' '*11}")

        except ValueError:

            cs()
            print(f"{' '*7}Tolong Masukkan Angka !{' '*7}")


def hapus_rusak():

    print(f"||{'='*134}||")
    print(
        f"||\tNo\t||\tMerk\t\t||\tJenis Barang\t||\tTanggal\t\t||\tWaktu\t\t||\tStatus\t\t||"
    )
    print(f"||{'='*134}||")
    for i in range(len(barang_rusak)):
        print(f"||\t{i+1}\t||", end="")
        for j in range(len(barang_rusak[i])):
            if len(barang_rusak[i][j]) <= 7:
                print(f"\t{barang_rusak[i][j]}\t\t||", end="")
            else:
                print(f"\t{barang_rusak[i][j]}\t||", end="")
        print()
    print(f"||{'='*134}||")

    while True:

        index = input("Masukkan nomor: ")

        if index.isnumeric() == True:
            
            index = int(index)

            if index >= 1 and index <= len(barang_rusak):

                break

            else:

                print ("Pilihan Tidak Ada !")
        
        else:

            print ("Tolong Masukkan Angka !")

    del barang_rusak[index - 1]

    barang_rusak_to_csv()

    cs()

    barang_rusak_admin()


def perbarui_rusak():

    print(f"||{'='*134}||")
    print(
        f"||\tNo\t||\tMerk\t\t||\tJenis Barang\t||\tTanggal\t\t||\tWaktu\t\t||\tStatus\t\t||"
    )
    print(f"||{'='*134}||")
    for i in range(len(barang_rusak)):
        print(f"||\t{i+1}\t||", end="")
        for j in range(len(barang_rusak[i])):
            if len(barang_rusak[i][j]) <= 7:
                print(f"\t{barang_rusak[i][j]}\t\t||", end="")
            else:
                print(f"\t{barang_rusak[i][j]}\t||", end="")
        print()
    print(f"||{'='*134}||")

    while True:

        index = input("Masukkan nomor: ")

        if index.isnumeric() == True:
            
            index = int(index)

            if index >= 1 and index <= len(barang_rusak):

                break

            else:

                print ("Pilihan Tidak Ada !")
        
        else:

            print ("Tolong Masukkan Angka !")

    status = str(input("Masukkan status baru: "))

    barang_rusak[index - 1][4] = status.strip().lower()

    barang_rusak_to_csv()

    cs()

    barang_rusak_admin()


def tambah_rusak():

    tanggal,jam = tanggal_dan_waktu()

    key = str(input("Masukkan merk barang: "))
    jenis_barang = str(input("Masukkan jenis barang: "))
    barang_rusak.append([key, jenis_barang, tanggal, jam, "belum"])
    barang_rusak_to_csv()
    print("Berhasil Menambahkan Barang Rusak")
    input("Tekan enter untuk kembali...")

    if identifier == "admin":
        barang_rusak_admin()
    else:
        barang_rusak_kasir()


def tampil_rusak():

    while True:

        print ("<----------------->")
        print ("<  Metode Tampil  >")
        print ("<----------------->")
        print ("< [1] Ascending   >")
        print ("< [2] Descending  >")
        print ("<----------------->")

        pilih_urutan = str(input("< Masukkan pilihan: >"))

        if pilih_urutan == "1" or pilih_urutan == "2":

            pilih_urutan = int(pilih_urutan)
            cs()
            break
        
        else:

            cs()
            print ("Pilihan Tidak Ditemukan !")
    
    while True:

        print(f"<-------------------->")
        print(f"<     Urut Sesuai    >")
        print(f"<-------------------->")
        print(f"< [1] Merk           >")
        print(f"< [2] Jenis Barang   >")
        print(f"< [3] Tanggal        >")
        print(f"< [4] Jam            >")
        print(f"< [5] Status         >")
        print(f"<-------------------->")

        pilih_urutkan_sesuai = str(input("< Masukkan pilihan: "))

        if pilih_urutkan_sesuai >= "1" and pilih_urutkan_sesuai <= "5":
            
            pilih_urutkan_sesuai = int(pilih_urutkan_sesuai)
            cs()
            break

        else:

          cs()
          print ("Pilihan Tidak Ditemukan !")

    bubble_sort_rusak(pilih_urutan, pilih_urutkan_sesuai)

    # Menampilkan seluruh data barang rusak
    print(f"||{'='*134}||")
    print(
        f"||\tNo\t||\tMerk\t\t||\tJenis Barang\t||\tTanggal\t\t||\tWaktu\t\t||\tStatus\t\t||"
    )
    print(f"||{'='*134}||")
    for i in range(len(barang_rusak)):
        print(f"||\t{i+1}\t||", end="")
        for j in range(len(barang_rusak[i])):
            if len(barang_rusak[i][j]) <= 7:
                print(f"\t{barang_rusak[i][j]}\t\t||", end="")
            else:
                print(f"\t{barang_rusak[i][j]}\t||", end="")
        print()
    print(f"||{'='*134}||")

    # Jika ingin kembali ke menu tampilkan barang rusak tekan enter
    input("Tekan enter untuk kembali...")

    # Memanggil fungsi clear screen
    cs()

    if identifier == "admin":
        barang_rusak_admin()
    else:
        barang_rusak_kasir()


def barang_rusak_admin():

    while True:

        # Menampilkan isi menu barang rusak
        print(f"<{'-'*34}>")
        print(f"<{' '*11}Barang Rusak{' '*11}>")
        print(f"<{'-'*34}>")
        print(f"< [1] Tampilkan Barang Rusak{' '*7}>")
        print(f"< [2] Tambahkan Barang Rusak{' '*7}>")
        print(f"< [3] Perbarui Status Barang Rusak >")
        print(f"< [4] Hapus Barang Rusak{' '*11}>")
        print(f"< [5] Cari{' '*25}>")
        print(f"< [6] Kembali{' '*22}>")
        print(f"<{'-'*34}>")

        try:

            pilihan = int(input("< Masukkan pilihan: "))

            cs()

            if pilihan >= 1 and pilihan <= 6:

                if pilihan == 1:
                    tampil_rusak()
                elif pilihan == 2:
                    tambah_rusak()
                elif pilihan == 3:
                    perbarui_rusak()
                elif pilihan == 4:
                    hapus_rusak()
                elif pilihan == 5:
                    cari_rusak()
                elif pilihan == 6:
                    admin()
                
                break

            else:

                print (f"{' '*6}Pilihan Tidak Tersedia !{' '*6}")

        except ValueError:

            cs()
            print(f"{' '*7}Tolong Masukkan Angka !{' '*7}")


def Sequential_Search(barang, cari_sesuai, cari):

    global belanjaan

    if cari_sesuai == 1:
        
        list_merk = list(barang.keys())

        if cari in list_merk:

            belanjaan[cari] = barang[cari]

            print(f"|{'-'*151}|")
            print(f"|\t\tMerk\t\t|\t\tJenis Barang\t\t|\t\tJumlah Barang\t\t|\t\tHarga Barang\t\t|")
            print(f"|{'-'*151}|")
            for key1, value1 in belanjaan[cari].items():

                if len(cari) >= 8:
                    print (f"|\t\t{cari}\t|", end="")
                else:
                    print (f"|\t\t{cari}\t\t|", end="")

                if len(key1) >= 8:
                    print(f"\t\t{key1}\t\t|", end="")
                else:
                    print(f"\t\t{key1}\t\t\t|", end="")
                for value2 in value1.values():
                    if len(str(value2)) >= 8:
                        print(f"\t\t{value2}\t\t|", end="")
                    else:
                        print(f"\t\t{value2}\t\t\t|", end="")
                print()
            print(f"|{'-'*151}|")

            input("Tekan Enter untuk Kembali ...")

            cs()
        
        else:

            cs()
            print (" Merk Tidak Ditemukan !")

    elif cari_sesuai == 2:

        for merk in barang:

            for jenis_barang in barang[merk]:

                if cari == jenis_barang:

                    belanjaan[merk] = barang[merk][jenis_barang]

        if belanjaan == {}:

            cs()

            print ("Jenis Barang Tidak Ditemukan !")
        
        else:

            print(f"|{'-'*151}|")
            print(f"|\t\tMerk\t\t|\t\tJenis Barang\t\t|\t\tJumlah Barang\t\t|\t\tHarga Barang\t\t|")
            print(f"|{'-'*151}|")
            for key1, value1 in belanjaan.items():

                if len(key1) >= 8:
                    print (f"|\t\t{key1}\t|", end="")
                else:
                    print (f"|\t\t{key1}\t\t|", end="")

                if len(cari) >= 8:
                    print(f"\t\t{cari}\t\t|", end="")
                else:
                    print(f"\t\t{cari}\t\t\t|", end="")

                for value2 in value1.values():

                    if len(str(value2)) >= 8:
                        print(f"\t\t{value2}\t\t|", end="")
                    else:
                        print(f"\t\t{value2}\t\t\t|", end="")
                print()
            print(f"|{'-'*151}|")

            input("Tekan Enter untuk Kembali ...")

            cs()
    
    belanjaan = {}


def cari():

    while True:

        # Menampilkan menu cari sesuai
        print(f"<--------------------->")
        print(f"<         Cari        >")
        print(f"<--------------------->")
        print(f"< [1] Merk            >")
        print(f"< [2] Jenis Barang    >")
        print(f"< [3] Kembali         >")
        print(f"<--------------------->")

        try:

            cari_sesuai = int(input("< Masukkan pilihan: "))

            cs()

            if cari_sesuai == 1:
                
                cari = str(input("< Masukkan Merk yang Dicari: "))

                cs()

                Sequential_Search(barang, cari_sesuai, cari)

            elif cari_sesuai == 2:

                cari = str(input("< Masukkan Jenis Barang yang Dicari: "))

                cs()

                Sequential_Search(barang, cari_sesuai, cari)

            elif cari_sesuai == 3:

                cs()
                if identifier == "admin":
                    stock_barang_admin()
                else:
                    stock_barang_kasir()
                break

            else:

                cs()
                print(f"{' '*11}Pilihan tidak ada!{' '*11}")

        except ValueError:

            cs()
            print(f"Tolong Masukkan Angka !")


def hapus():

    while True:

        # Menampilkan semua merk yang ada
        i = 0
        print(f"<{'-'*23}>")
        for a in barang.keys():
            i += 1
            if len(a) >= 7:
                print(f"< [{i}]\t {a[0].upper()}{a[1:len(a)]}\t>")
            else:
                print(f"< [{i}]\t {a[0].upper()}{a[1:len(a)]}\t\t>")
        print(f"< [{i+1}]\t Kembali\t>")
        print(f"<{'-'*23}>")

        try:

            # Meminta inputan merk
            pilihan = int(input("< Masukkan merk yang ingin diperbarui stock dan harganya: "))

            list_merk = []

            for key in barang.keys():

                list_merk.append(key)

            if (pilihan >= 1 and pilihan <= 9):

                # Memanggil fungsi clear screen
                cs()

                # Memberi info tidak adanya barang
                if len(barang[list_merk[int(pilihan) - 1]]) == 0:
                    print(f"{' '*4}Tidak ada barang!{' '*4}")

                # Menampilkan stock barang
                else:

                    # Menampilkan stock barang
                    print(f"|{'-'*119}|")
                    print(f"|{' '*56} {list_merk[int(pilihan)-1]} {' '*56}|")
                    print(f"|{'-'*119}|")
                    print(f"|\t\tJenis Barang\t\t|\t\tJumlah Barang\t\t|\t\tHarga Barang\t\t|")
                    print(f"|{'-'*119}|")
                    for key1, value1 in barang[list_merk[int(pilihan) - 1]].items():
                        if len(key1) >= 8:
                            print(f"|\t\t{key1}\t\t|", end="")
                        else:
                            print(f"|\t\t{key1}\t\t\t|", end="")
                        for value2 in value1.values():
                            if len(str(value2)) >= 8:
                                print(f"\t\t{value2}\t\t|", end="")
                            else:
                                print(f"\t\t{value2}\t\t\t|", end="")
                        print()
                    print(f"|{'-'*119}|")

                    # Meminta inputan jenis barang yang ingin dihapus
                    hapus_jenisbarang = str(input("Masukkan jenis barang yang ingin dihapus: "))

                    # Pemberitahuan jenis barang yang diinput belum ada
                    barang_distock = list(barang[list_merk[int(pilihan) - 1]].keys())
                    if barang_distock.count(hapus_jenisbarang) == 0:
                        cs()
                        print(f"{hapus_jenisbarang} tidak ditemukan!")

                    # Menghapus jenis barang
                    else:

                        del barang[list_merk[int(pilihan) - 1]][hapus_jenisbarang]

                        barang_to_csv()

                        # Memanggil fungsi clear screen
                        cs()

                        # Pemberitahuan janis barang berhasil dihpaus
                        print(f"{hapus_jenisbarang} berhasil dihapus!")

            elif pilihan == 10:

                cs()
                if identifier == "admin":
                    stock_barang_admin()
                else:
                    stock_barang_kasir()
                break

            else:

                cs()
                print(" Pilihan tidak ditemukan!")

        except ValueError:

            cs()
            print(f" Tolong Masukkan Angka !")


def perbarui():

    while True:

        # Menampilkan semua merk yang ada
        i = 0
        print(f"<{'-'*23}>")
        for a in barang.keys():
            i += 1
            if len(a) >= 7:
                print(f"< [{i}]\t {a[0].upper()}{a[1:len(a)]}\t>")
            else:
                print(f"< [{i}]\t {a[0].upper()}{a[1:len(a)]}\t\t>")
        print(f"< [{i+1}]\t Kembali\t>")
        print(f"<{'-'*23}>")

        try:

            # Meminta inputan merk
            pilihan = int(input("< Masukkan merk yang ingin diperbarui stock dan harganya: "))

            list_merk = []

            for key in barang.keys():

                list_merk.append(key)

            if (pilihan >= 1 and pilihan <= 9):

                # Memanggil fungsi clear screen
                cs()

                # Memberi info tidak adanya barang
                if len(barang[list_merk[int(pilihan) - 1]]) == 0:
                    cs()
                    print("Tidak ada barang")

                else:

                    # Menampilkan stock barang
                    print(f"|{'-'*119}|")
                    print(f"|{' '*56} {list_merk[int(pilihan)-1]} {' '*56}|")
                    print(f"|{'-'*119}|")
                    print(f"|\t\tJenis Barang\t\t|\t\tJumlah Barang\t\t|\t\tHarga Barang\t\t|")
                    print(f"|{'-'*119}|")
                    for key1, value1 in barang[list_merk[int(pilihan) - 1]].items():
                        if len(key1) >= 8:
                            print(f"|\t\t{key1}\t\t|", end="")
                        else:
                            print(f"|\t\t{key1}\t\t\t|", end="")
                        for value2 in value1.values():
                            if len(str(value2)) >= 8:
                                print(f"\t\t{value2}\t\t|", end="")
                            else:
                                print(f"\t\t{value2}\t\t\t|", end="")
                        print()
                    print(f"|{'-'*119}|")

                # Meminta inputan jenis barang yang ingin diperbarui
                update_jenisbarang = str(
                    input(
                        "Masukkan jenis barang yang ingin diperbarui quantity atau harganya: "
                    )
                )

                # Pemberitahuan jenis barang yang diinput belum ada
                barang_distock = list(barang[list_merk[int(pilihan) - 1]].keys())
                if barang_distock.count(" ".join(update_jenisbarang.split()).lower()) == 0:
                    cs()
                    print(
                        f"{update_jenisbarang} tidak ditemukan! Silahkan pergi ke menu tambah jika ingin menambahkan jenis barang baru!"
                    )

                # Mengupdate dictionary
                else:

                    while True:

                        print(f"<--------------->")
                        print(f"< [1] Quantity\t>")
                        print(f"< [2] Harga\t>")
                        print(f"< [3] Keduanya\t>")
                        print(f"<--------------->")

                        # Meminta inputan apa yang ingin diupdate
                        tanya = str(input("< Mau perbarui apa? "))

                        cs()

                        if int(tanya) >= 1 and int(tanya) <= 3:

                            # Hanya perbarui quantity
                            if tanya == "1":

                                while True:

                                    # Meminta inputan quantity baru
                                    quantity = input("< Masukkan jumlah barang baru (berupa angka): ")

                                    if quantity.isnumeric() == True:

                                        quantity = int(quantity)

                                        break

                                    else:

                                        print ("Masukkan Berupa Angka !")

                                # Mengupdate dictionary
                                barang[list_merk[int(pilihan) - 1]][update_jenisbarang]["quantity"] = quantity

                            # Hanya perbarui harga
                            elif tanya == "2":

                                while True:

                                    # Meminta inputan harga
                                    harga = input("< Masukkan harga barang (Tidak Menggunakan Rp dan Titik): ")

                                    if harga.isnumeric() == True:

                                        harga = int(harga)

                                        break

                                # Mengupdate dictionary
                                barang[list_merk[int(pilihan) - 1]][update_jenisbarang]["harga"] = harga

                            # Perbarui quantity dan harga
                            elif tanya == "3":

                                while True:

                                    # Meminta inputan jumlah barang / quantity
                                    quantity = input("< Masukkan jumlah barang: ")

                                    if quantity.isnumeric() == True:

                                        quantity = int(quantity)

                                        while True:

                                            # Meminta inputan harga
                                            harga = input("< Masukkan harga barang (Tidak Menggunakan Rp dan Titik): ")

                                            if harga.isnumeric() == True:

                                                harga = int(harga)

                                                break

                                            else:

                                                print ("Masukkan Angka Tanpa Titik !")

                                        break

                                    else:

                                        print ("Masukkan Berupa Angka !")

                                # Mengupdate dictionary
                                barang[list_merk[int(pilihan) - 1]][update_jenisbarang] = {"quantity": quantity,"harga": harga}

                            break

                        else:

                            cs()
                            print("Pilihan tidak ditemukan!")

                    barang_to_csv()

                    # Memanggil fungsi clear screen
                    cs()

                    # Pemberitahuan data berhasil ditambahkan
                    print(f"{update_jenisbarang} berhasil diperbarui!")

            elif pilihan == 10:

                cs()
                if identifier == "admin":
                    stock_barang_admin()
                else:
                    stock_barang_kasir()
                break

            else:

                cs()
                print("Pilihan tidak ditemukan!")

        except ValueError:

            cs()
            print(f" Tolong Masukkan Angka !")


def tambah():

    while True:

        # Menampilkan semua merk yang ada
        i = 0
        print(f"<{'-'*23}>")
        for a in barang.keys():
            i += 1
            if len(a) >= 7:
                print(f"< [{i}]\t {a[0].upper()}{a[1:len(a)]}\t>")
            else:
                print(f"< [{i}]\t {a[0].upper()}{a[1:len(a)]}\t\t>")
        print(f"< [{i+1}]\t Kembali\t>")
        print(f"<{'-'*23}>")

        try:

            # Meminta inputan merk
            pilihan = int(input("< Masukkan merk yang ingin ditambahkan jenis barangnya: "))

            list_merk = []

            for key in barang.keys():

                list_merk.append(key)

            if (pilihan >= 1 and pilihan <= 9):

                # Memanggil fungsi clear screen
                cs()

                # tampilan
                print(f"<------------------->")
                print(f"\t{list_merk[int(pilihan)-1]}\t")
                print(f" Tambah Jenis Barang ")
                print(f"<------------------->")

                # Meminta inputan jenis barang baru
                jenisbarang = str(input("< Masukkan jenis barang baru: "))

                barang_distock = list(barang[list_merk[int(pilihan) - 1]].keys())

                # Pemberitahuan jenis barang yang diinput belum ada
                if barang_distock.count(jenisbarang) == 1:
                    cs()
                    print(
                        f"{jenisbarang} sudah tersedia! Silahkan pergi ke menu perbarui jika ingin memperbarui quantity dan harga barang!"
                    )

                # Mengupdate dictionary
                else:

                    while True:

                        # Meminta inputan jumlah barang / quantity
                        quantity = input("< Masukkan jumlah barang: ")

                        if quantity.isnumeric() == True:

                            quantity = int(quantity)

                            while True:

                                # Meminta inputan harga
                                harga = input("< Masukkan harga barang (Tidak Menggunakan Rp dan Titik): ")

                                if harga.isnumeric() == True:

                                    harga = int(harga)

                                    break

                                else:

                                    print ("Masukkan Angka Tanpa Titik !")

                            break

                        else:

                            print ("Masukkan Berupa Angka !")
                        
                    # Menambahkan ke dalam dictionary
                    barang[list_merk[int(pilihan) - 1]][jenisbarang.lower()] = {
                        "quantity": quantity,
                        "harga": harga,
                    }
                    barang_to_csv()
                    # Memanggil fungsi clear screen
                    cs()
                    # Pemberitahuan data berhasil ditambahkan
                    print(
                        f"{jenisbarang[0].upper()}{jenisbarang[1:999]} berhasil ditambahkan!"
                    )

            elif pilihan == 10:

                cs()
                if identifier == "admin":
                    stock_barang_admin()
                else:
                    stock_barang_kasir()
                break

            else:

                cs()
                print("Pilihan tidak ditemukan!")

        except ValueError:

            cs()
            print(f" Tolong Masukkan Angka !")


def bubbleSort(ar, metodeurut):
    n = len(ar)
    if metodeurut == "1":
        # Traverse through all array elements
        for i in range(n):
            # Last i elements are already in correct position
            for j in range(0, n - i - 1):
                # Swap if the element found is greater than the next element
                if ar[j] > ar[j + 1]:
                    ar[j], ar[j + 1] = ar[j + 1], ar[j]
    else:
        # Traverse through all array elements
        for i in range(n):
            # Last i elements are already in correct position
            for j in range(0, n - i - 1):
                # Swap if the element found is greater than the next element
                if ar[j] < ar[j + 1]:
                    ar[j], ar[j + 1] = ar[j + 1], ar[j]

    return ar


def urut(metodeurut):

    global barang

    # Menyimpan list key (merk) dari dictionary barang --> variabel keynya
    keynya = list(barang.keys())

    # Menyorting list keynya
    key_tersort = bubbleSort(keynya, metodeurut)

    # Membuat dictionary kosong untuk menyimpan hasil pengurutan
    barang_baru = {}

    # Menyimpan isi (key dan value) dari dictionary barang ke dalam barang baru dengan kondisi keynya (merknya) sudah terurut
    for x in key_tersort:
        barang_baru[x] = barang[x]

    # Mengurutkan dan Menyimpan sub-key (jenis barang) yang sudah terurut ke dalam variabel barang_baru | mereplace value di variabel barang_baru dengan kondisi sudah terurut
    for key, value in barang_baru.items():

        # Menaruh key dari value dari barang_baru ke dalam variabel key_di_dalam
        key_di_dalam = list(value.keys())

        # Mengurutkan key dari value di variabel key_di_dalam
        key_di_dalam_tersort = bubbleSort(key_di_dalam, metodeurut)

        # dictionary kosong untuk menampung value yang sudah terurut
        barang_di_dalam_baru = {}

        # Menaruh value dari key yang sudah tersort ke dalam
        for x in key_di_dalam_tersort:
            barang_di_dalam_baru[x] = value[x]

        barang_baru[key] = barang_di_dalam_baru

    barang = barang_baru


def tampil():

    while True:

        print ("<----------------->")
        print ("<  Metode Tampil  >")
        print ("<----------------->")
        print ("< [1] Ascending   >")
        print ("< [2] Descending  >")
        print ("<----------------->")

        metodeurut = str(input("< Masukkan pilihan: "))

        cs()

        if metodeurut == "1" or metodeurut == "2":
            break
        else:
            print("Masukkan pilihan yang benar!")

    urut(metodeurut)

    while True:

        # Menampilkan semua merk yang ada
        i = 0
        print(f"<{'-'*23}>")
        for a in barang.keys():
            i += 1
            if len(a) >= 7:
                print(f"< [{i}]\t {a[0].upper()}{a[1:len(a)]}\t>")
            else:
                print(f"< [{i}]\t {a[0].upper()}{a[1:len(a)]}\t\t>")
        print(f"< [{i+1}]\t Semua\t\t>")
        print(f"< [{i+2}]\t Kembali\t>")
        print(f"<{'-'*23}>")

        try:
            # Meminta inputan merk
            pilihan = int(input("< Masukkan merk yang ingin ditampilkan: "))

            list_merk = []
            for key in barang.keys():
                list_merk.append(key)

            if (pilihan >= 1 and pilihan <= 9):

    
                # Memanggil fungsi clear screen
                cs()

                # Memberi info tidak adanya barang
                if len(barang[list_merk[int(pilihan) - 1]]) == 0:
                    print("Tidak ada barang")

                # Menampilkan stock barang
                else:

                    print(f"|{'-'*119}|")
                    print(f"|{' '*56} {list_merk[int(pilihan)-1]} {' '*56}|")
                    print(f"|{'-'*119}|")
                    print(f"|\t\tJenis Barang\t\t|\t\tJumlah Barang\t\t|\t\tHarga Barang\t\t|")
                    print(f"|{'-'*119}|")
                    for key1, value1 in barang[list_merk[int(pilihan) - 1]].items():
                        if len(key1) >= 8:
                            print(f"|\t\t{key1}\t\t|", end="")
                        else:
                            print(f"|\t\t{key1}\t\t\t|", end="")
                        for value2 in value1.values():
                            if len(str(value2)) >= 8:
                                print(f"\t\t{value2}\t\t|", end="")
                            else:
                                print(f"\t\t{value2}\t\t\t|", end="")
                        print()
                    print(f"|{'-'*119}|")

                print()
                input("Tekan enter untuk kembali...")
                cs()

            elif pilihan == 10:

                # Memanggil fungsi clear screen
                cs()

                # Memberi info tidak adanya barang
                if len(barang) == 0:
                    print("Tidak ada barang")

                # Menampilkan semua stock barang
                else:
                    print(f"|{'-'*160}|")
                    print(
                        f"|\t\tMerk\t\t\t|\t\tJenis Barang\t\t|\t\tJumlah Barang\t\t|\t\tHarga Barang\t\t|"
                    )
                    print(f"|{'-'*160}|")
                    for key, value in barang.items():
                        for key1, value1 in value.items():
                            if len(key) >= 8:
                                print(f"|\t\t{key}\t\t|", end="")
                            else:
                                print(f"|\t\t{key}\t\t\t|", end="")
                            if len(key1) >= 8:
                                print(f"\t\t{key1}\t\t|", end="")
                            else:
                                print(f"\t\t{key1}\t\t\t|", end="")
                            for value2 in value1.values():
                                if len(str(value2)) >= 8:
                                    print(f"\t\t{value2}\t\t|", end="")
                                else:
                                    print(f"\t\t{value2}\t\t\t|", end="")
                            print()
                    print(f"|{'-'*160}|")

                print()
                input("Tekan enter untuk kembali...")
                cs()

            elif pilihan == 11:

                cs()

                if identifier == "admin":
                    stock_barang_admin()
                else:
                    stock_barang_kasir()

                break

            else:

                cs()
                print(" Pilihan tidak ditemukan!")

        except ValueError:

            cs()
            print(f" Tolong Masukkan Angka !")


def stock_barang_admin():

    while True:

        # Menampilkan menu user
        print(f"<{'-'*24}>")
        print(f"<{' '*6}Stock Barang{' '*6}>")
        print(f"<{'-'*24}>")
        print(f"< [1] Tampilkan Barang{' '*2} >")
        print(f"< [2] Tambahkan Barang{' '*2} >")
        print(f"< [3] Perbarui Barang{' '*3} >")
        print(f"< [4] Hapus Barang{' '*6} >")
        print(f"< [5] Cari Barang{' '*7} >")
        print(f"< [6] Kembali{' '*11} >")
        print(f"<{'-'*24}>")

        try:
            # meminta inputan pilihan menu
            pilihan = int(input("< Masukkan pilihan: "))

            # Memanggil fungsi clear screen
            cs()

            if pilihan >= 1 and pilihan <= 6:

                if pilihan == 1:
                    tampil()
                elif pilihan == 2:
                    tambah()
                elif pilihan == 3:
                    perbarui()
                elif pilihan == 4:
                    hapus()
                elif pilihan == 5:
                    cari()
                elif pilihan == 6:
                    admin()
                
                break

            else:

                print(f"{' '*6}Menu tidak ada!{' '*5}")

        except ValueError:

            cs()
            print(f"  Tolong Masukkan Angka !")


def admin():

    global identifier

    identifier = "admin"

    while True:

        # Menampilkan Menu Admin
        print(f"<{'-'*35}>")
        print(f"<{' '*15}Admin{' '*15}>")
        print(f"<{'-'*35}>")
        print(f"< [1] Stock Barang{' '*17} >")
        print(f"< [2] Barang Rusak{' '*17} >")
        print(f"< [3] Riwayat Transaksi{' '*12} >")
        print(f"< [4] Kembali{' '*22} >")
        print(f"<{'-'*35}>")

        try:

            pilihan = int(input("< Masukkan pilihan: "))

            # Memanggil fungsi clear screen
            cs()

            if pilihan >= 1 and pilihan <= 4:
            
                if pilihan == 1:
                    stock_barang_admin()
                elif pilihan == 2:
                    barang_rusak_admin()
                elif pilihan == 3:
                    riwayat_transaksi()
                elif pilihan == 4:
                    main()
                
                break

            else:

                print(f"{' '*11}Menu tidak ada!{' '*11}")

        except ValueError:

            cs()
            print(f"{' '*7}Tolong Masukkan Angka !{' '*7}")


def login():

    # PIN masuk menu admin
    for i in range(3):
        pin = pyssword()
        cs()
        if pin == "09042021":
            break
        elif i == 2:
            print(f"{' '*6}Silahkan Coba Lagi Nanti!{' '*6}")
            main()
        print("PIN yang Anda Masukkan Salah!")


def barang_rusak_kasir():

    while True:

        # Menampilkan menu barang rusak user
        print(f"<{'-'*30}>")
        print(f"<{' '*9}Barang Rusak{' '*9}>")
        print(f"<{'-'*30}>")
        print(f"< [1] Tampilkan Barang Rusak   >")
        print(f"< [2] Tambahkann Barang Rusak  >")
        print(f"< [3] Kembali{' '*17} >")
        print(f"<{'-'*30}>")

        try:

            # meminta inputan pilihan menu
            pilihan = int(input("< Masukkan pilihan: "))

            # Memanggil fungsi clear screen
            cs()

            if pilihan >= 1 and pilihan <= 3:

                if pilihan == 1:
                    tampil_rusak()
                elif pilihan == 2:
                    tambah_rusak()
                elif pilihan == 3:
                    kasir()
                
                break

            else:

                print(f"{' '*9}Menu tidak ada!{' '*8}")

        except ValueError:

            cs()
            print(f"{' '*7}Tolong Masukkan Angka !{' '*7}")


def stock_barang_kasir():

    while True:

        # Menampilkan menu user
        print(f"<{'-'*24}>")
        print(f"<{' '*6}Stock Barang{' '*6}>")
        print(f"<{'-'*24}>")
        print(f"< [1] Cari Barang{' '*7} >")
        print(f"< [2] Tampilkan Barang{' '*2} >")
        print(f"< [3] Kembali{' '*11} >")
        print(f"<{'-'*24}>")

        try:
            # meminta inputan pilihan menu
            pilihan = int(input("< Masukkan pilihan: "))

            # Memanggil fungsi clear screen
            cs()

            if pilihan >= 1 and pilihan <= 3:

                if pilihan == 1:
                    cari()
                elif pilihan == 2:
                    tampil()
                elif pilihan == 3:
                    kasir()
                
                break

            else:

                print(f"{' '*6}Menu tidak ada!{' '*5}")

        except ValueError:

            cs()
            print(f"{' '*7}Tolong Masukkan Angka !{' '*7}")


def bill():

    global belanjaan

    # Menjumlahkan semua isi pada list belanjaan
    total = 0
    for key1, value1 in belanjaan.items():
        for key2 in value1.keys():
            total += belanjaan[key1][key2]["subtotal"]

    # Menampilkan total untuk memberi informasi ke kasir, kasir akan memberi informasi ke pembeli total harganya
    print(f"Total: Rp{total}")

    # Meminta inputan uang yang dibayarkan pembeli
    while True:

        bayar = input("Masukkan tunai (angka saja tanpa titik): ")

        if bayar.isnumeric() == True:
            bayar = int(bayar)
            if bayar >= total:
                tanggal,jam = tanggal_dan_waktu()
                break
            else:
                print ("Uang tidak cukup!")
        else:
            print ("Tolong masukkan angka saja :)")

    # Memanggil fungsi clear screen
    cs()

    # Variabel pemanggil fungsi pembuat angka dan huruf
    digit_awal = membuat_huruf(int(3)) + membuat_angka(int(8))
    digit_terakhir = membuat_angka(int(4))
    no_faktur = f"{''.join(digit_awal).upper()}-{''.join(digit_terakhir)}"

    # Menampilkan struck
    print(
        f"EKLEKTRONIK\t\t\t\t\t\t\t\t\t\t\tFAKTUR No: {no_faktur}"
    )
    print(f"Jl. Kakarot Nomor 57\t\t\t\t\t\t\t\t\t\t{tanggal} {jam}")
    print(f"Namek")
    print(f"Telp. 112233")
    print(f"{'-'*129}")
    print(f"Merk\t\t\tJenis Barang\t\t\tQuantity\t\t\tHarga\t\t\t\tSub Total")
    print(f"{'-'*129}")
    for key, value in belanjaan.items():
        for key1, value1 in value.items():
            if len(key) >= 8:
                print(f"{key}\t\t", end="")
            else:
                print(f"{key}\t\t\t", end="")
            if len(key1) >= 8:
                print(f"{key1}\t\t", end="")
            else:
                print(f"{key1}\t\t\t", end="")
            for value2 in value1.values():
                if len(str(value2)) >= 8:
                    print(f"\t{value2}\t\t", end="")
                else:
                    print(f"\t{value2}\t\t\t", end="")
            print()
    print(f"{'-'*129}")
    print(f"\t\t\t\t\t\t\t\t\t\t\t\t\t\tTotal: Rp{total}")
    print(f"\t\t\t\t\t\t\t\t\t\t\t\t\t\tTunai: Rp{bayar}")
    print(f"\t\t\t\t\t\t\t\t\t\t\t\t\t\tKembali: Rp{bayar-total}")
    print()
    print(f"Terima Kasih atas Kunjungan Anda")
    input("Tekan enter untuk kembali ke menu kasir...")

    riwayat.append([tanggal,jam,no_faktur,belanjaan,total,bayar,bayar-total])

    riwayat_transaksi_to_csv()

    # Membersihkan dictionary belanjaan
    belanjaan = {}

    cs()

    kasir()


def update_kasir(barang, merk, jenisbarang, qty):

    # Update list belanjaan untuk diproses di fungsi struck
    if merk in belanjaan:
        if jenisbarang.strip().lower() in belanjaan[merk.replace(" ", "").lower()]:
            belanjaan[merk.replace(" ", "").lower()][jenisbarang.strip().lower()][
                "quantity"
            ] += qty
            belanjaan[merk.replace(" ", "").lower()][jenisbarang.strip().lower()][
                "subtotal"
            ] = belanjaan[merk.replace(" ", "").lower()][jenisbarang.strip().lower()]["quantity"] * barang[merk.replace(" ", "").lower()][jenisbarang.strip().lower()]["harga"]
        else:
            belanjaan[merk.replace(" ", "").lower()][jenisbarang.strip().lower()] = {
                "quantity": qty,
                "harga": barang[merk.replace(" ", "").lower()][
                    jenisbarang.strip().lower()
                ]["harga"],
                "subtotal": qty * barang[merk.replace(" ", "").lower()][
                    jenisbarang.strip().lower()
                ]["harga"]
            }
    else:
        belanjaan[merk.replace(" ", "").lower()] = {
            jenisbarang.strip().lower(): {
                "quantity": qty,
                "harga": barang[merk.replace(" ", "").lower()][
                    jenisbarang.strip().lower()
                ]["harga"],
                "subtotal": qty * barang[merk.replace(" ", "").lower()][
                    jenisbarang.strip().lower()
                ]["harga"]
            }
        }

    # Update stock karena adanya pembelian
    barang[merk.replace(" ", "").lower()][jenisbarang.strip().lower()][
        "quantity"
    ] -= qty

    while True:

        # Tambah barang lagi?
        lagi = str(input("< Tambah Barang (y/ya | t/tidak)? "))

        cs()

        # Ya
        if lagi.replace(" ", "").lower() == "ya" or lagi.replace(" ", "").lower() == "y":
            # Memanggil fungsi kasir
            transaksi()
            break

        # Tidak
        elif (
            lagi.replace(" ", "").lower() == "tidak" or lagi.replace(" ", "").lower() == "t"
        ):
            # Memanggil fungsi struck
            bill()
            break

        # Input Sembarang
        else:
            print("Tidak ditemukan!")


def transaksi():

    # Memanggil fungsi clear screen
    cs()

    # Memberi info tidak adanya barang
    if len(barang) == 0:
        print("Tidak ada barang")
        input("Tekan enter untuk kembali...")
        main()

    # Menampilkan semua stock barang
    else:
        while True:
            merk = str(input("< Masukkan merk: "))
            # Ngecek apakah merknya ada di dalam dictionary
            if list(barang.keys()).count(merk.replace(" ", "").lower()) == 1:
                cs()
                print(f"|{'-'*119}|")
                print(f"|{' '*56} {merk.lower().capitalize()} {' '*56}|")
                print(f"|{'-'*119}|")
                print(f"|\t\tJenis Barang\t\t|\t\tJumlah Barang\t\t|\t\tHarga Barang\t\t|")
                print(f"|{'-'*119}|")
                for key1, value1 in barang[merk].items():
                    if len(key1) >= 8:
                        print(f"|\t\t{key1}\t\t|", end="")
                    else:
                        print(f"|\t\t{key1}\t\t\t|", end="")
                    for value2 in value1.values():
                        if len(str(value2)) >= 8:
                            print(f"\t\t{value2}\t\t|", end="")
                        else:
                            print(f"\t\t{value2}\t\t\t|", end="")
                    print()
                print(f"|{'-'*119}|")

                # Meminta inputan jenis barang
                while True:
                    jenisbarang = str(input("< Masukkan jenis barang: "))
                    if (list(barang[merk.replace(" ", "").lower()].keys()).count(jenisbarang.strip().lower()) == 1):
                        while True:
                            try:
                                # Meminta inputan jumlah barang yang ingin dibeli
                                qty = int(input("< Masukkan jumlah barang: "))
                                if (qty <= barang[merk.replace(" ", "").lower()][jenisbarang.strip().lower()]["quantity"]):
                                    break
                                else:
                                    print(f"Stock tidak mencukupi! Stock tersedia: {barang[merk.replace(' ','').lower()][jenisbarang.strip().lower()]['quantity']}")
                            except:
                                    print ("Masukkan jumlah barang berupa angka!")
                        break
                    else:
                        print(f"{jenisbarang.capitalize()} tidak ditemukan!")
                update_kasir(barang, merk, jenisbarang, qty)
                break
            else:
                print(f"{merk.capitalize()} tidak ditemukan!")


def kasir():

    global identifier

    identifier = "kasir"

    while True:

        # Menampilkan menu user
        print(f"<{'-'*37}>")
        print(f"<{' '*16}Kasir{' '*16}>")
        print(f"<{'-'*37}>")
        print(f"< [1] Transaksi{' '*22} >")
        print(f"< [2] Tampilkan Riwayat Transaksi     >")
        print(f"< [3] Stock Barang{' '*19} >")
        print(f"< [4] Barang Rusak{' '*19} >")
        print(f"< [5] Kembali{' '*24} >")
        print(f"<{'-'*37}>")

        try:

            # meminta inputan pilihan menu
            pilihan = int(input("< Masukkan pilihan: "))

            # Memangggil fungsi clear screen
            cs()

            if pilihan >= 1 and pilihan <= 5:

                if pilihan == 1:
                    transaksi()
                elif pilihan == 2:
                    tampil_riwayat()
                elif pilihan == 3:
                    stock_barang_kasir()
                elif pilihan == 4:
                    barang_rusak_kasir()
                elif pilihan == 5:
                    main()

                break

            else:

                print(f"{' '*12}Menu tidak ada!{' '*12}")

        except ValueError:

            cs()
            print(f"{' '*7}Tolong Masukkan Angka !{' '*7}")


def main():

    while True:

        tanggal,jam = tanggal_dan_waktu()

        # Menampilkan Menu Utama
        print(f"<{'-'*35}>")
        print(f"<{' '*10}Toko Elektronik{' '*10}>")
        print(f"<{' '*13}Since 2021{' '*12}>")
        print(f"<{' '*13}{tanggal}{' '*12}>")
        print(f"<{' '*14}{jam}{' '*13}>")
        print(f"<{'-'*35}>")
        print(f"< [1] Admin{' '*24} >")
        print(f"< [2] Kasir{' '*24} >")
        print(f"< [3] Keluar{' '*23} >")
        print(f"<{'-'*35}>")

        try:

            pilihan = int(input("< Masukkan pilihan: "))

            # Memanggil fungsi clear screen
            cs()

            if pilihan >= 1 and pilihan <= 3:

                if pilihan == 1:

                    login()
                    admin()

                elif pilihan == 2:

                    kasir()

                elif pilihan == 3:

                    print(
                    """
                    d888888b d88888b d8888b. d888888b .88b  d88.  .d8b.         db   dD  .d8b.  .d8888. d888888b db   db 
                    `~~88~~' 88'     88  `8D   `88'   88'YbdP`88 d8' `8b        88 ,8P' d8' `8b 88'  YP   `88'   88   88 
                       88    88ooooo 88oobY'    88    88  88  88 88ooo88        88,8P   88ooo88 `8bo.      88    88ooo88 
                       88    88~~~~~ 88`8b      88    88  88  88 88~~~88        88`8b   88~~~88   `Y8b.    88    88~~~88 
                       88    88.     88 `88.   .88.   88  88  88 88   88        88 `88. 88   88 db   8D   .88.   88   88 
                       YP    Y88888P 88   YD Y888888P YP  YP  YP YP   YP        YP   YD YP   YP `8888Y' Y888888P YP   YP
                    """
                    )

                break

            else:

                print(f"{' '*11}Menu tidak ada!{' '*11}")

        except ValueError:

            cs()
            print(f"{' '*7}Tolong Masukkan Angka !{' '*7}")


if __name__ == "__main__":
    main()