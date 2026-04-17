import random
import json
import os

# ===== DATA GAME =====
SENJATA = {
    "Keris": {"damage": 8, "harga": 0},
    "Tombak": {"damage": 12, "harga": 50},
    "Pedang Pusaka": {"damage": 18, "harga": 120}
}

MUSUH = [
    {"nama": "Buto Ijo", "hp": 30, "damage": 6, "gold": 15, "exp": 20},
    {"nama": "Leak Bali", "hp": 25, "damage": 8, "gold": 20, "exp": 25},
    {"nama": "Siluman Ular", "hp": 40, "damage": 10, "gold": 35, "exp": 40},
    {"nama": "Raksasa Penunggu Candi", "hp": 60, "damage": 14, "gold": 60, "exp": 70}
]

# ===== CLASS PEMAIN =====
class Pemain:
    def __init__(self, nama):
        self.nama = nama
        self.level = 1
        self.hp = 100
        self.max_hp = 100
        self.exp = 0
        self.exp_untuk_levelup = 50
        self.gold = 30
        self.senjata = "Keris"
        self.inventory = {"Ramuan": 2}

    def status(self):
        print("\n=== STATUS ===")
        print(f"Nama: {self.nama} | Level: {self.level}")
        print(f"HP: {self.hp}/{self.max_hp} | EXP: {self.exp}/{self.exp_untuk_levelup}")
        print(f"Gold: {self.gold} | Senjata: {self.senjata} (+{SENJATA[self.senjata]['damage']} dmg)")
        print("Inventory:", self.inventory)
        print("==============\n")

    def pakai_ramuan(self):
        if self.inventory.get("Ramuan", 0) > 0:
            heal = 30
            self.hp = min(self.max_hp, self.hp + heal)
            self.inventory["Ramuan"] -= 1
            print(f"Kamu minum ramuan. +{heal} HP. HP sekarang: {self.hp}/{self.max_hp}")
            return True
        else:
            print("Ramuan habis!")
            return False

    def tambah_exp(self, jumlah):
        self.exp += jumlah
        print(f"Dapat {jumlah} EXP!")
        while self.exp >= self.exp_untuk_levelup:
            self.level_up()

    def level_up(self):
        self.level += 1
        self.exp -= self.exp_untuk_levelup
        self.exp_untuk_levelup = int(self.exp_untuk_levelup * 1.5)
        self.max_hp += 20
        self.hp = self.max_hp
        print(f"\n*** LEVEL UP! Kamu sekarang level {self.level} ***")
        print(f"Max HP naik jadi {self.max_hp}. HP dipulihkan penuh!\n")

    def serang(self):
        base_dmg = SENJATA[self.senjata]["damage"]
        bonus = random.randint(0, self.level * 2)
        return base_dmg + bonus

    def simpan_data(self):
        data = {
            "nama": self.nama, "level": self.level, "hp": self.hp, "max_hp": self.max_hp,
            "exp": self.exp, "exp_untuk_levelup": self.exp_untuk_levelup, "gold": self.gold,
            "senjata": self.senjata, "inventory": self.inventory
        }
        with open("savegame.json", "w") as f:
            json.dump(data, f)
        print("Game berhasil disimpan!")

    def load_data(self):
        if os.path.exists("savegame.json"):
            with open("savegame.json", "r") as f:
                data = json.load(f)
            self.__dict__.update(data)
            print("Data game berhasil dimuat!")
            return True
        return False

# ===== FUNGSI BATTLE =====
def battle(pemain):
    musuh = random.choice(MUSUH).copy()
    print(f"\n!!! Kamu bertemu {musuh['nama']}!!!")
    print(f"HP Musuh: {musuh['hp']}, Damage: {musuh['damage']}\n")

    while musuh['hp'] > 0 and pemain.hp > 0:
        print(f"HP Kamu: {pemain.hp}/{pemain.max_hp} | HP {musuh['nama']}: {musuh['hp']}")
        aksi = input("Pilih aksi: [1] Serang [2] Pakai Ramuan [3] Lari: ")

        if aksi == "1":
            dmg = pemain.serang()
            musuh['hp'] -= dmg
            print(f"Kamu menyerang dengan {pemain.senjata}! {musuh['nama']} kena {dmg} damage.")

            if musuh['hp'] > 0:
                musuh_dmg = random.randint(musuh['damage']-2, musuh['damage']+2)
                pemain.hp -= musuh_dmg
                print(f"{musuh['nama']} menyerang balik! Kamu kena {musuh_dmg} damage.")

        elif aksi == "2":
            pemain.pakai_ramuan()
            musuh_dmg = random.randint(musuh['damage']-2, musuh['damage']+2)
            pemain.hp -= musuh_dmg
            print(f"Sambil minum ramuan, {musuh['nama']} menyerang! Kena {musuh_dmg} damage.")

        elif aksi == "3":
            if random.random() < 0.6:
                print("Kamu berhasil lari dari pertarungan!")
                return
            else:
                print("Gagal lari!")
                musuh_dmg = random.randint(musuh['damage']-2, musuh['damage']+2)
                pemain.hp -= musuh_dmg
                print(f"{musuh['nama']} menyerang! Kamu kena {musuh_dmg} damage.")
        else:
            print("Pilihan tidak valid!")

    if pemain.hp <= 0:
        print("\nKamu kalah... Game Over.")
        return False
    else:
        print(f"\nKamu mengalahkan {musuh['nama']}!")
        pemain.gold += musuh['gold']
        print(f"Dapat {musuh['gold']} gold.")
        pemain.tambah_exp(musuh['exp'])
        if random.random() < 0.3:
            pemain.inventory["Ramuan"] = pemain.inventory.get("Ramuan", 0) + 1
            print("Kamu menemukan 1 Ramuan!")
        return True

# ===== TOKO =====
def toko(pemain):
    while True:
        print("\n=== TOKO SENJATA CANDI ===")
        print(f"Gold kamu: {pemain.gold}")
        for i, (nama, data) in enumerate(SENJATA.items(), 1):
            print(f"{i}. {nama} - Damage: {data['damage']}, Harga: {data['harga']} gold")
        print(f"{len(SENJATA)+1}. Ramuan - Pulihkan 30 HP, Harga: 15 gold")
        print(f"{len(SENJATA)+2}. Keluar")

        pilih = input("Beli apa? ")
        try:
            pilih = int(pilih)
            if 1 <= pilih <= len(SENJATA):
                nama_senjata = list(SENJATA.keys())[pilih-1]
                harga = SENJATA[nama_senjata]['harga']
                if pemain.gold >= harga:
                    pemain.gold -= harga
                    pemain.senjata = nama_senjata
                    print(f"Kamu membeli {nama_senjata}!")
                else:
                    print("Gold tidak cukup!")
            elif pilih == len(SENJATA) + 1:
                if pemain.gold >= 15:
                    pemain.gold -= 15
                    pemain.inventory["Ramuan"] = pemain.inventory.get("Ramuan", 0) + 1
                    print("Kamu membeli 1 Ramuan!")
                else:
                    print("Gold tidak cukup!")
            elif pilih == len(SENJATA) + 2:
                break
            else:
                print("Pilihan salah!")
        except ValueError:
            print("Masukkan angka!")

# ===== MAIN GAME =====
def main():
    print("=== PETUALANGAN DI NUSANTARA ===")
    print("Game RPG teks bertema alkulturasi Hindu-Buddha")

    nama = input("Masukkan nama karaktermu: ")
    pemain = Pemain(nama)

    if os.path.exists("savegame.json"):
        muat = input("File save ditemukan. Muat game? y/n: ")
        if muat.lower() == 'y':
            pemain.load_data()

    while pemain.hp > 0:
        pemain.status()
        print("Pilih kegiatan:")
        print("1. Jelajah Hutan - cari musuh")
        print("2. Ke Candi - istirahat, pulihkan HP")
        print("3. Toko Senjata")
        print("4. Simpan Game")
        print("5. Keluar")

        aksi = input("Pilihan: ")

        if aksi == "1":
            hasil = battle(pemain)
            if hasil == False:
                break
        elif aksi == "2":
            print("Kamu bermeditasi di candi... HP pulih penuh.")
            pemain.hp = pemain.max_hp
        elif aksi == "3":
            toko(pemain)
        elif aksi == "4":
            pemain.simpan_data()
        elif aksi == "5":
            simpan = input("Simpan game sebelum keluar? y/n: ")
            if simpan.lower() == 'y':
                pemain.simpan_data()
            print("Terima kasih sudah bermain!")
            break
        else:
            print("Pilihan tidak ada.")

    if pemain.hp <= 0:
        print("Petualanganmu berakhir di sini, ksatria...")

if __name__ == "__main__":
    main()