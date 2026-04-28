tugas = []

while True:
    print(f"\n--- DAFTAR TUGAS ({len(tugas)}) ---")
    print("1. Tambah | 2. Lihat | 3. Keluar")
    
    pilihan = input("Pilih menu: ")

    if pilihan == "1":
        item = input("Masukkan tugas baru: ")
        tugas.append(item)
        print("Tersimpan!")
    elif pilihan == "2":
        print("\nTugas Kamu:")
        for i, isi in enumerate(tugas, 1):
            print(f"{i}. {isi}")
    elif pilihan == "3":
        print("Sampai jumpa!")
        break
    else:
        print("Pilihan salah!")