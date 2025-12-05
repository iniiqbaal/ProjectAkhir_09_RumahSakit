# ===================== DATA GLOBAL =====================
pasien = [] 
id_berikutnya = 1 
HARI_INI = "Monday" 
CURRENT_ADMIN = "" 

# Data Kamar (15 Kamar)
KAMAR = [
    {"nama": "C1", "kelas": "Kelas 3", "status": "Kosong", "biaya_harian": 100000},
    {"nama": "C2", "kelas": "Kelas 3", "status": "Kosong", "biaya_harian": 100000},
    {"nama": "C3", "kelas": "Kelas 3", "status": "Kosong", "biaya_harian": 100000},
    {"nama": "C4", "kelas": "Kelas 3", "status": "Kosong", "biaya_harian": 100000},
    {"nama": "C5", "kelas": "Kelas 3", "status": "Kosong", "biaya_harian": 100000},
    
    {"nama": "B1", "kelas": "Kelas 2", "status": "Kosong", "biaya_harian": 200000},
    {"nama": "B2", "kelas": "Kelas 2", "status": "Kosong", "biaya_harian": 200000},
    {"nama": "B3", "kelas": "Kelas 2", "status": "Kosong", "biaya_harian": 200000},
    {"nama": "B4", "kelas": "Kelas 2", "status": "Kosong", "biaya_harian": 200000},
    {"nama": "B5", "kelas": "Kelas 2", "status": "Kosong", "biaya_harian": 200000},

    {"nama": "A1", "kelas": "Kelas 1", "status": "Kosong", "biaya_harian": 300000},
    {"nama": "A2", "kelas": "Kelas 1", "status": "Kosong", "biaya_harian": 300000},
    {"nama": "A3", "kelas": "Kelas 1", "status": "Kosong", "biaya_harian": 300000},

    {"nama": "VIP1", "kelas": "VIP", "status": "Kosong", "biaya_harian": 500000},
    {"nama": "VIP2", "kelas": "VIP", "status": "Kosong", "biaya_harian": 500000}
] 

# Data Dokter & Biaya
jadwal_dokter = {
    "Monday": ["Dr. Ahmad (Kelamin)", "Dr. Budi (Jantung)"],
    "Tuesday": ["Dr. Citra (Mata)", "Dr. Dian (Kulit)"],
    "Wednesday": ["Dr. Eko (THT)", "Dr. Fani (Gigi)"],
    "Thursday": ["Dr. Gina (Anak)", "Dr. Hadi (Bedah)"],
    "Friday": ["Dr. Ika (Kandungan)", "Dr. Joko (Saraf)"],
    "Saturday": ["Dr. Kiki (Forensik)", "Dr. Lala (Psikiatri)"],
    "Sunday": ["Dr. Momo (Emergency)", "Dr. Nana (Radiologi)"]
}
dokter_tetap = ["Dr. Arya (Umum)", "Dr. Iqbal (Emergency)"]
biaya_konsultasi = 50000 

# Data Status Dokter dan Antrian
STATUS_DOKTER = {} 
ANTRIAN_DOKTER = {}

# Akun Admin
# Hanya "Super Admin" yang bisa akses menu CRUD Akun
AKUN_ADMIN = [
    {"username": "arya", "password": "password123", "role": "Super Admin"},
    {"username": "iqbal", "password": "password123", "role": "Super Admin"}
]
akun_non_admin = [] 

# ===================== FUNGSI UTILITY =====================
def clear_screen():
    print("\n" * 50) 

def validasi_nama(nama):
    if not nama or not nama.replace(" ", "").isalpha():
        return False, "Nama harus huruf dan tidak kosong."
    return True, ""

def validasi_telepon(telepon):
    if not telepon.isdigit():
        return False, "Nomor telepon harus berupa angka."
    panjang = len(telepon)
    if panjang < 10 or panjang > 13:
        return False, f"Nomor telepon harus antara 10 sampai 13 digit (Input Anda: {panjang})."
    return True, ""

def validasi_nilai_angka(nilai_str):
    try:
        n = int(nilai_str)
        if n < 0:
            return False, "Nilai tidak boleh negatif.", 0
        return True, "", n
    except ValueError:
        return False, "Input harus angka.", 0

def validasi_tanggal(tanggal_str):
    parts = tanggal_str.split('-')
    if len(parts) != 3:
        return False, "Format tanggal harus DD-MM-YYYY (misal: 01-12-2025)."
    if not (parts[0].isdigit() and parts[1].isdigit() and parts[2].isdigit()):
        return False, "Tanggal, bulan, dan tahun harus angka."
    if not (len(parts[0]) == 2 and len(parts[1]) == 2 and len(parts[2]) == 4):
        return False, "Format tanggal harus DD-MM-YYYY (2 digit hari, 2 digit bulan, 4 digit tahun)."
    return True, ""

def atur_hari_operasional():
    global HARI_INI
    print("\n=== ATUR HARI OPERASIONAL ===")
    print("Silakan masukkan hari ini untuk menyesuaikan jadwal dokter.")
    print("(Pilihan: Senin, Selasa, Rabu, Kamis, Jumat, Sabtu, Minggu)")
    
    while True:
        hari_input = input("Masukkan Hari Ini: ").lower()
        
        if hari_input == "senin":
            HARI_INI = "Monday"
            break
        elif hari_input == "selasa":
            HARI_INI = "Tuesday"
            break
        elif hari_input == "rabu":
            HARI_INI = "Wednesday"
            break
        elif hari_input == "kamis":
            HARI_INI = "Thursday"
            break
        elif hari_input == "jumat":
            HARI_INI = "Friday"
            break
        elif hari_input == "sabtu":
            HARI_INI = "Saturday"
            break
        elif hari_input == "minggu":
            HARI_INI = "Sunday"
            break
        else:
            print("Nama hari tidak valid. Gunakan Bahasa Indonesia (Contoh: Rabu).")
            
    print(f"✅ Sistem diatur untuk jadwal hari: {HARI_INI} ({hari_input.capitalize()})")

def dapatkan_dokter_tersedia(hari):
    terjadwal = jadwal_dokter.get(hari, [])
    semua_dokter = dokter_tetap + terjadwal
    dokter_unik = []
    for d in semua_dokter:
        if d not in dokter_unik:
            dokter_unik.append(d)
    return dokter_unik

# ===================== FUNGSI UTILITY KAMAR =====================
def dapatkan_kamar_tersedia():
    return [k for k in KAMAR if k['status'] == 'Kosong']

def set_status_kamar(nama_kamar, id_pasien):
    for kamar in KAMAR:
        if kamar['nama'] == nama_kamar:
            kamar['status'] = id_pasien if id_pasien is not None else "Kosong"
            break

def dapatkan_biaya_kamar(nama_kamar):
    for kamar in KAMAR:
        if kamar['nama'] == nama_kamar:
            return kamar['biaya_harian']
    return 0
    
def lihat_status_kamar():
    print("\n=== Status Kamar Rawat Inap ===")
    if not KAMAR:
        print("Tidak ada data kamar.")
        return
        
    print("| Nama Kamar | Kelas Kamar | Biaya Harian | Status                                         |")
    print("|------------|-------------|--------------|------------------------------------------------|")
    for k in KAMAR:
        status_info = f"ID Pasien: {k['status']}" if k['status'] != 'Kosong' else "Kosong"
        print(f"| {k['nama']:10} | {k['kelas']:11} | Rp{k['biaya_harian']:10} | {status_info:40} |")

# ===================== FUNGSI UTILITY DOKTER =====================

def inisialisasi_status_dokter():
    """Mengisi STATUS_DOKTER dan ANTRIAN_DOKTER dengan semua dokter yang ada"""
    semua_dokter_mingguan = []
    for hari in jadwal_dokter:
        semua_dokter_mingguan.extend(jadwal_dokter[hari])
    
    semua_dokter_mingguan.extend(dokter_tetap)
    
    dokter_unik = set(semua_dokter_mingguan)
    
    for dokter in dokter_unik:
        if dokter not in STATUS_DOKTER:
            STATUS_DOKTER[dokter] = None
        if dokter not in ANTRIAN_DOKTER:
            ANTRIAN_DOKTER[dokter] = []

def lihat_status_dokter():
    inisialisasi_status_dokter()
    dokter_bertugas = dapatkan_dokter_tersedia(HARI_INI)
    
    print(f"\n=== Status Layanan Dokter Hari Ini ({HARI_INI}) ===")
    if not dokter_bertugas:
        print("Tidak ada dokter bertugas hari ini.")
        return
        
    for dokter in sorted(dokter_bertugas):
        status = STATUS_DOKTER.get(dokter)
        antrian = ANTRIAN_DOKTER.get(dokter, [])
        
        info_status = ""
        if status is None:
            info_status = "Tersedia"
        else:
            pasien_dilayani = next((p['nama'] for p in pasien if p['id'] == status), f"ID:{status}")
            info_status = f"Sedang Melayani: {pasien_dilayani}"
            
        info_antrian = f"Antrian: {len(antrian)} pasien"
        if antrian:
            antrian_nama = ", ".join([str(id_p) for id_p in antrian])
            info_antrian += f" (ID: {antrian_nama})"
            
        print(f"**{dokter}** | {info_status:30} | {info_antrian}")

def set_dokter_melayani(nama_dokter, id_pasien):
    inisialisasi_status_dokter()
    if nama_dokter in STATUS_DOKTER:
        STATUS_DOKTER[nama_dokter] = id_pasien
        
def tambah_antrian_dokter(nama_dokter, id_pasien):
    inisialisasi_status_dokter()
    if nama_dokter in ANTRIAN_DOKTER:
        ANTRIAN_DOKTER[nama_dokter].append(id_pasien)

def hapus_pasien_dari_status(id_pasien):
    inisialisasi_status_dokter()
    for dokter, id_p in STATUS_DOKTER.items():
        if id_p == id_pasien:
            STATUS_DOKTER[dokter] = None 
            if ANTRIAN_DOKTER.get(dokter) and ANTRIAN_DOKTER[dokter]:
                id_pasien_berikutnya = ANTRIAN_DOKTER[dokter].pop(0)
                STATUS_DOKTER[dokter] = id_pasien_berikutnya
                for p in pasien:
                    if p['id'] == id_pasien_berikutnya:
                        p['status_layanan'] = "Dilayani Sekarang (dari antrian)"
                        break
                print(f"✅ Pasien ID {id_pasien_berikutnya} dari antrian kini dilayani oleh {dokter}.")
            return

    for dokter, antrian in ANTRIAN_DOKTER.items():
        if id_pasien in antrian:
            ANTRIAN_DOKTER[dokter].remove(id_pasien)
            return

# ===================== FUNGSI CRUD PASIEN & KAMAR =====================
def tambah_pasien():
    global id_berikutnya
    inisialisasi_status_dokter()
    print("\n--- Pendaftaran Pasien Baru (Umum/Rawat Jalan) ---")
    
    nama = input("Masukkan nama pasien: ")
    valid, pesan = validasi_nama(nama)
    if not valid:
        print(pesan)
        return
    
    asal = input("Masukkan asal (kota/daerah): ")
    
    while True:
        telepon = input("Masukkan nomor telepon: ")
        valid, pesan = validasi_telepon(telepon)
        if valid:
            break
        print(f"❌ {pesan} Silakan masukkan ulang.")
    
    while True:
        tanggal_konsultasi = input("Masukkan tanggal konsultasi (DD-MM-YYYY): ")
        valid, pesan = validasi_tanggal(tanggal_konsultasi)
        if valid:
            break
        print(pesan)

    for p in pasien:
        if (p["nama"].lower() == nama.lower() and 
            p["asal"].lower() == asal.lower() and 
            p["telepon"] == telepon):
            print("\n❌ Pasien dengan Nama, Asal, dan No. Telepon yang sama sudah terdaftar.")
            return

    keluhan = input("Masukkan keluhan: ")
    
    bpjs_q = input("Apakah pasien memiliki BPJS? (y/n): ").lower()
    memiliki_bpjs = bpjs_q == 'y'
    
    print("\nℹ️  Info: Pasien baru otomatis terdaftar sebagai 'Rawat Jalan'.")
    jenis_rawat = "Jalan"
    nama_kamar = "N/A"
    biaya_inap = 0
    lama_inap = 0
    
    dokter_tersedia = dapatkan_dokter_tersedia(HARI_INI)
    dokter_terpilih = "Belum Terpilih"
    status_layanan = "N/A" 

    if not dokter_tersedia:
        print(f"Tidak ada dokter tersedia hari ini ({HARI_INI}).")
    else:
        print(f"\nDokter tersedia hari ini ({HARI_INI}):")
        for i, dokter in enumerate(dokter_tersedia, 1):
            status_dilayani_id = STATUS_DOKTER.get(dokter)
            antrian = ANTRIAN_DOKTER.get(dokter, [])
            status_info = "Tersedia"
            if status_dilayani_id is not None:
                pasien_dilayani = next((p['nama'] for p in pasien if p['id'] == status_dilayani_id), f"ID:{status_dilayani_id}")
                status_info = f"Sedang Melayani {pasien_dilayani}"
            elif antrian:
                status_info = f"Menunggu Antrian ({len(antrian)} pasien)"

            print(f"{i}. {dokter} - Status: {status_info}")
        
        try:
            pilihan = input("Pilih dokter (nomor) atau tekan Enter untuk 'Belum Terpilih': ")
            if pilihan and 1 <= int(pilihan) <= len(dokter_tersedia):
                dokter_terpilih = dokter_tersedia[int(pilihan) - 1]
                
                if STATUS_DOKTER.get(dokter_terpilih) is None:
                    set_dokter_melayani(dokter_terpilih, id_berikutnya)
                    status_layanan = "Dilayani Sekarang"
                    print(f"✅ Pasien ID {id_berikutnya} langsung dilayani oleh {dokter_terpilih}.")
                else:
                    tambah_antrian_dokter(dokter_terpilih, id_berikutnya)
                    status_layanan = "Menunggu Antrian"
                    print(f"⚠️ {dokter_terpilih} sedang melayani. Pasien ID {id_berikutnya} masuk ke antrian.")

            else:
                dokter_terpilih = "Belum Terpilih" 
        except ValueError:
            print("Input tidak valid. Dokter diset 'Belum Terpilih'.")
            dokter_terpilih = "Belum Terpilih" 

    if memiliki_bpjs:
        total_biaya = 0
        print("\n✅ Pasien memiliki BPJS. Biaya Konsultasi GRATIS.")
    else:
        total_biaya = biaya_konsultasi
    
    data_pasien = {
        "id": id_berikutnya,
        "nama": nama,
        "asal": asal,
        "telepon": telepon,
        "keluhan": keluhan,
        "dokter": dokter_terpilih,
        "total_biaya": total_biaya,
        "tanggal_konsultasi": tanggal_konsultasi, 
        "jenis_rawat": jenis_rawat,
        "nama_kamar": nama_kamar,   
        "memiliki_bpjs": memiliki_bpjs,
        "lama_inap": lama_inap,
        "status_layanan": status_layanan
    }
    pasien.append(data_pasien)
    id_berikutnya += 1
    
    print(f"\nPasien berhasil ditambahkan dengan ID {data_pasien['id']}.")
    print(f"Total biaya awal: Rp{total_biaya}")

def proses_masuk_rawat_inap():
    if not pasien:
        print("Tidak ada data pasien.")
        return

    print("\n--- Proses Pemindahan ke Rawat Inap (Opname) ---")
    try:
        id_pasien = int(input("Masukkan ID Pasien yang disarankan Opname: "))
        target_pasien = None
        for p in pasien:
            if p['id'] == id_pasien:
                target_pasien = p
                break
        
        if not target_pasien:
            print("❌ ID Pasien tidak ditemukan.")
            return
            
        if target_pasien['jenis_rawat'] == 'inap':
            print(f"⚠️ Pasien {target_pasien['nama']} sudah berstatus Rawat Inap di kamar {target_pasien['nama_kamar']}.")
            return
            
        print(f"\nPasien ditemukan: {target_pasien['nama']} (Dokter: {target_pasien['dokter']})")
        konfirmasi = input("Apakah dokter menyarankan rawat inap? (y/n): ").lower()
        if konfirmasi != 'y':
            print("Proses dibatalkan.")
            return
            
        lama_inap = 1
        kamar_tersedia = dapatkan_kamar_tersedia()
        
        if target_pasien['memiliki_bpjs']:
            kamar_tersedia_final = [k for k in kamar_tersedia if k['kelas'] != 'VIP']
            print("\n⚠️ Pasien BPJS: Hanya kamar Kelas 1, 2, 3 yang tersedia (VIP tidak ditanggung).")
        else:
            kamar_tersedia_final = kamar_tersedia
        
        if not kamar_tersedia_final:
            print("❌ Maaf, Kamar Penuh/Tidak Tersedia. Pasien tidak bisa rawat inap saat ini.")
            return

        print("\nKamar Tersedia:")
        for i, k in enumerate(kamar_tersedia_final, 1):
            biaya_info = "(GRATIS/BPJS)" if target_pasien['memiliki_bpjs'] else f"(Rp{k['biaya_harian']}/hari)"
            print(f"{i}. {k['nama']} ({k['kelas']}) {biaya_info}")

        try:
            pilihan_kamar = int(input("Pilih kamar (nomor): "))
            if 1 <= pilihan_kamar <= len(kamar_tersedia_final):
                kamar_terpilih = kamar_tersedia_final[pilihan_kamar - 1]
                
                target_pasien['jenis_rawat'] = 'inap'
                target_pasien['nama_kamar'] = kamar_terpilih['nama']
                target_pasien['lama_inap'] = 1 
                
                set_status_kamar(kamar_terpilih['nama'], target_pasien['id'])
                
                if not target_pasien['memiliki_bpjs']:
                    biaya_tambahan = kamar_terpilih['biaya_harian']
                    target_pasien['total_biaya'] += biaya_tambahan
                    
                print(f"✅ Sukses! Pasien {target_pasien['nama']} kini dirawat di {kamar_terpilih['nama']}.")
            else:
                print("Pilihan kamar tidak valid.")
        except ValueError:
            print("Input harus angka.")

    except ValueError:
        print("ID harus angka.")

# ===================== FUNGSI LAINNYA =====================

def lihat_pasien():
    if not pasien:
        print("Tidak ada data pasien.")
        return
    
    print("\n" + "="*128)
    print(f"{'DAFTAR PASIEN':^128}")
    print("="*128)
    print(f"| {'ID':<3} | {'Nama':<20} | {'Asal':<12} | {'Telepon':<13} | {'Rawat/Kamar':<17} | {'Dokter':<12} | {'Status':<18} | {'Biaya':<10} |")
    print("-" * 128)
    
    for p in pasien:
        bpjs_info = " (BPJS)" if p.get('memiliki_bpjs', False) else ""
        lama_inap_info = f"({p.get('lama_inap', 0)}h)" if p.get('jenis_rawat') == 'inap' else ""
        
        nama_kamar_raw = p.get('nama_kamar', 'N/A')
        if "Checkout" in nama_kamar_raw:
             tampilan_kamar = "Selesai"
        else:
             tampilan_kamar = nama_kamar_raw

        rawat_kamar = f"{p.get('jenis_rawat', 'N/A')}/{tampilan_kamar}{lama_inap_info}"
        nama_data = f"{p['nama']}{bpjs_info}"
        
        dokter_singkat = p['dokter'].split(' ')[1] if len(p['dokter'].split(' ')) > 1 else p['dokter']
        
        nama_display = nama_data[:20]       
        asal_display = p['asal'][:12]       
        rawat_display = rawat_kamar[:17]    
        dokter_display = dokter_singkat[:12]
        status_display = p.get('status_layanan', 'N/A')[:18] 
        
        print(f"| {p['id']:<3} | {nama_display:<20} | {asal_display:<12} | {p['telepon']:<13} | {rawat_display:<17} | {dokter_display:<12} | {status_display:<18} | Rp{p['total_biaya']:<8} |")
    print("="*128)

def cari_pasien():
    kueri = input("Masukkan nama atau ID pasien untuk cari: ").lower()
    hasil = [p for p in pasien if kueri in str(p['id']).lower() or kueri in p['nama'].lower()]
    if hasil:
        print("\n--- Hasil Pencarian Lengkap ---")
        for p in hasil:
            bpjs_info = " (BPJS)" if p.get('memiliki_bpjs', False) else ""
            print("-" * 40)
            print(f"ID Pasien   : {p['id']}")
            print(f"Nama        : {p['nama']}{bpjs_info}")
            print(f"Asal        : {p['asal']}")
            print(f"Telepon     : {p['telepon']}") 
            print(f"Keluhan     : {p['keluhan']}")
            print(f"Dokter      : {p['dokter']}")
            print(f"Jenis Rawat : {p.get('jenis_rawat', 'N/A')}")
            print(f"Kamar       : {p.get('nama_kamar', 'N/A')}")
            print(f"Status      : {p.get('status_layanan', 'N/A')}")
            print(f"Total Biaya : Rp{p['total_biaya']}")
            print("-" * 40)
    else:
        print("Tidak ada pasien ditemukan.")

def perbarui_pasien():
    if not pasien:
        print("Tidak ada data pasien untuk diupdate.")
        return
    try:
        id_pasien = int(input("Masukkan ID pasien yang ingin diupdate: "))
        for p in pasien:
            if p["id"] == id_pasien:
                kamar_lama = p.get("nama_kamar", "N/A")
                print(f"--- Update Pasien: {p['nama']} ---")
                
                p["nama"] = input(f"Nama baru ({p['nama']}): ") or p["nama"]
                p["asal"] = input(f"Asal baru ({p['asal']}): ") or p["asal"]
                
                while True:
                    tel_baru = input(f"Telepon baru ({p['telepon']}): ")
                    if not tel_baru: 
                        break
                    valid, pesan = validasi_telepon(tel_baru)
                    if valid:
                        p["telepon"] = tel_baru
                        break
                    print(f"❌ {pesan}")

                p["keluhan"] = input(f"Keluhan baru ({p['keluhan']}): ") or p["keluhan"]
                tgl_kons_baru = input(f"Tanggal konsultasi baru ({p.get('tanggal_konsultasi', 'N/A')}): ")
                if tgl_kons_baru:
                    valid, pesan = validasi_tanggal(tgl_kons_baru)
                    if valid:
                        p["tanggal_konsultasi"] = tgl_kons_baru
                    else:
                        print(pesan)
                        return
                    
                bpjs_q = input(f"Ubah status BPJS? (y/n - Saat ini: {'Y' if p.get('memiliki_bpjs') else 'N'}): ").lower()
                if bpjs_q == 'y':
                    p['memiliki_bpjs'] = not p.get('memiliki_bpjs', False)
                    print(f"Status BPJS diubah menjadi: {'YA' if p['memiliki_bpjs'] else 'TIDAK'}")

                if kamar_lama != "N/A" and "Checkout" not in kamar_lama:
                    set_status_kamar(kamar_lama, None)
                
                update_dokter = input("Apakah ingin mengubah dokter? (y/n): ").lower()
                if update_dokter == 'y':
                    dokter_tersedia = dapatkan_dokter_tersedia(HARI_INI) 
                    if dokter_tersedia:
                        print(f"Dokter tersedia hari ini ({HARI_INI}):")
                        for i, dokter in enumerate(dokter_tersedia, 1):
                            print(f"{i}. {dokter}")
                        try:
                            pilihan = input("Pilih dokter baru (nomor): ")
                            if pilihan and 1 <= int(pilihan) <= len(dokter_tersedia):
                                p["dokter"] = dokter_tersedia[int(pilihan) - 1]
                            else:
                                print("Pilihan tidak valid.")
                        except ValueError:
                            print("Input harus berupa angka.")

                biaya_inap_total = 0
                if p.get("jenis_rawat") == 'inap' and p.get("nama_kamar") != "N/A" and "Checkout" not in p.get("nama_kamar"):
                    biaya_harian = dapatkan_biaya_kamar(p.get("nama_kamar"))
                    lama_inap_saat_ini = p.get("lama_inap", 1) 
                    biaya_inap_total = biaya_harian * lama_inap_saat_ini

                if p.get('memiliki_bpjs'):
                    p["total_biaya"] = 0
                else:
                    p["total_biaya"] = biaya_konsultasi + biaya_inap_total
                
                print("Data pasien berhasil diupdate.")
                print(f"Total Biaya Baru: Rp{p['total_biaya']}")
                return
        print("ID pasien tidak ditemukan.")
    except ValueError:
        print("ID harus berupa angka.")

def hapus_pasien():
    if not pasien:
        print("Tidak ada data pasien untuk dihapus.")
        return
    try:
        id_pasien = int(input("Masukkan ID pasien yang ingin dihapus: "))
        for i, p in enumerate(pasien):
            if p["id"] == id_pasien:
                kamar_pasien = p.get("nama_kamar")
                if p.get("jenis_rawat") == "inap" and kamar_pasien != "N/A" and "Checkout" not in kamar_pasien:
                    set_status_kamar(kamar_pasien, None)
                    print(f"Kamar {kamar_pasien} dikosongkan.")
                hapus_pasien_dari_status(id_pasien)
                del pasien[i]
                print("Pasien berhasil dihapus.")
                return
        print("ID pasien tidak ditemukan.")
    except ValueError:
        print("ID harus berupa angka.")

def update_lama_inap_dan_hitung_biaya_akhir():
    if not pasien:
        print("Tidak ada data pasien.")
        return
    try:
        id_pasien = int(input("Masukkan ID pasien Rawat Inap untuk Checkout: "))
        for p in pasien:
            if p["id"] == id_pasien:
                if p.get('jenis_rawat') != 'inap' or p.get('nama_kamar') == "N/A" or "Checkout" in p.get('nama_kamar', ''):
                    print("❌ Pasien ini bukan pasien rawat inap atau sudah checkout.")
                    return
                
                print("\n" + "-"*30)
                print(f"✅ Pasien Ditemukan:")
                print(f"Nama        : {p['nama']}")
                print(f"Keluhan     : {p['keluhan']}")
                print(f"Kamar       : {p.get('nama_kamar')}")
                print(f"Lama Inap Skg: {p.get('lama_inap', 1)} hari")
                print("-" * 30 + "\n")

                lama_inap_str = input(f"Masukkan lama rawat inap akhir (hari, saat ini: {p.get('lama_inap', 1)}): ")
                valid, pesan, lama_inap_baru = validasi_nilai_angka(lama_inap_str)
                
                if not valid or lama_inap_baru < 1:
                    print("Lama inap harus angka positif (minimal 1 hari).")
                    return
                
                p['lama_inap'] = lama_inap_baru
                
                biaya_harian = dapatkan_biaya_kamar(p.get("nama_kamar"))
                biaya_inap_total = biaya_harian * lama_inap_baru
                
                p['biaya_inap_final'] = biaya_inap_total 

                if p.get('memiliki_bpjs'):
                    p["total_biaya"] = 0
                else:
                    p["total_biaya"] = biaya_konsultasi + biaya_inap_total
                
                print(f"✅ Lama Inap diupdate: {lama_inap_baru} hari. Total: Rp{p['total_biaya']}")
                
                nama_kamar_lama = p.get("nama_kamar")
                set_status_kamar(nama_kamar_lama, None) 
                
                p['nama_kamar'] = f"{nama_kamar_lama} (Checkout)" 
                p['jenis_rawat'] = "Jalan/Selesai"
                
                hapus_pasien_dari_status(id_pasien) 
                print("Pasien telah checkout. Kamar dikosongkan.")
                return
        print("ID pasien tidak ditemukan.")
    except ValueError:
        print("ID harus berupa angka.")

def cetak_struk(admin_name):
    mapping_hari = {
        "Monday": "Senin", "Tuesday": "Selasa", "Wednesday": "Rabu",
        "Thursday": "Kamis", "Friday": "Jumat", "Saturday": "Sabtu", "Sunday": "Minggu"
    }

    try:
        id_pasien = int(input("Masukkan ID pasien untuk cetak struk: "))
        for p in pasien:
            if p["id"] == id_pasien:
                lama_inap = p.get('lama_inap', 0)
                biaya_inap_total = 0
                
                if 'biaya_inap_final' in p:
                    biaya_inap_total = p['biaya_inap_final']
                elif p.get("jenis_rawat") == 'inap' and p.get("nama_kamar") != "N/A":
                     biaya_harian = dapatkan_biaya_kamar(p.get("nama_kamar"))
                     biaya_inap_total = biaya_harian * lama_inap
                
                biaya_konsul = biaya_konsultasi
                total_sebelum_subsidi = biaya_konsul + biaya_inap_total
                subsidi = total_sebelum_subsidi if p.get('memiliki_bpjs', False) else 0
                total_akhir = total_sebelum_subsidi - subsidi
                
                hari_indo = mapping_hari.get(HARI_INI, HARI_INI)

                print("\n" + "="*50)
                print("         STRUK PEMBAYARAN RUMAH SAKIT")
                print("="*50)
                print(f"Admin: {admin_name}")
                print(f"Waktu Cetak: {hari_indo}")
                print("-" * 50)
                print(f"ID Pasien: {p['id']}")
                print(f"Nama: {p['nama']}")
                print(f"Rawat: {p.get('jenis_rawat', 'N/A')}")
                
                if p.get('jenis_rawat') == 'inap' or 'Checkout' in p.get('nama_kamar', ''):
                    print(f"Kamar: {p.get('nama_kamar', 'N/A')}")
                    print(f"Lama Inap: {lama_inap} hari")
                
                print(f"BPJS: {'YA' if p.get('memiliki_bpjs', False) else 'TIDAK'}")
                print(f"Dokter: {p['dokter']}")
                print(f"Status Layanan: {p.get('status_layanan', 'N/A')}")
                print(f"Tgl Konsultasi: {p.get('tanggal_konsultasi', 'N/A')}")
                print("\n--- Rincian Biaya ---")
                print(f"Biaya Konsultasi: Rp{biaya_konsul}")
                
                if biaya_inap_total > 0 or (p.get('jenis_rawat') == 'inap' or 'Checkout' in p.get('nama_kamar', '')):
                     print(f"Biaya Kamar Inap ({lama_inap} hari): Rp{biaya_inap_total}")

                print("-" * 50)
                print(f"Total Sebelum Subsidi: Rp{total_sebelum_subsidi}")
                if p.get('memiliki_bpjs'):
                    print(f"Subsidi BPJS (100%): - Rp{subsidi}")
                    print("-" * 50)
                print(f"Total Biaya Akhir: Rp{total_akhir}") 
                print("="*50)
                print("Terima kasih atas kunjungan Anda!")
                return
        print("ID pasien tidak ditemukan.")
    except ValueError:
        print("ID harus berupa angka.")

# ===================== MANAJEMEN AKUN & LOGIN =====================

def manajemen_kamar():
    while True:
        clear_screen() 
        print("\n=== Menu Manajemen Kamar Rawat Inap ===")
        print("1. Lihat Status Kamar Rawat Inap 🛌") 
        print("2. Kembali ke Menu Utama")
        pilihan = input("Pilih menu (1-2): ")

        if pilihan == "1":
            lihat_status_kamar()
        elif pilihan == "2":
            break
        else:
            print("Pilihan tidak valid.")
        input("\nTekan Enter untuk melanjutkan...")

def pilih_dokter():
    print(f"Jadwal Dokter untuk Hari: {HARI_INI}")
    dokter_tersedia = dapatkan_dokter_tersedia(HARI_INI)
    if not dokter_tersedia:
        print("Tidak ada dokter tersedia hari ini.")
        return
    
    print("Dokter yang tersedia hari ini:")
    for dokter in dokter_tersedia:
        print(f"- {dokter}")

def menu_manajemen_akun():
    while True:
        semua_akun = AKUN_ADMIN + akun_non_admin
        clear_screen()
        print("=== ⚙️  MANAJEMEN AKUN ADMIN ⚙️  ===")
        print("1. Lihat Semua Akun")
        print("2. Buat Akun Baru")
        print("3. Update/Edit Akun")
        print("4. Hapus Akun")
        print("0. Kembali ke Menu Utama")
        
        pilihan = input("Pilih menu (0-4): ")
        
        if pilihan == "1":
            lihat_semua_akun(semua_akun)
        elif pilihan == "2":
            buat_akun_baru(semua_akun)
        elif pilihan == "3":
            update_akun(semua_akun)
        elif pilihan == "4":
            hapus_akun(semua_akun)
        elif pilihan == "0":
            break
        else:
            print("Pilihan tidak valid.")
        input("Tekan Enter...")

def menu_utama(admin_name, admin_role):
    atur_hari_operasional() 
    
    while True:
        clear_screen()
        print(f"=== Sistem Rumah Sakit (Admin: {admin_name} | Role: {admin_role} | Hari: {HARI_INI}) ===")
        print("1. Tambah Pasien Baru (Poli/Rawat Jalan) ")
        print("2. Lihat Semua Pasien")
        print("3. Cari Pasien")
        print("4. Update/Edit Data Pasien")
        print("5. Hapus Pasien (Delete)")
        print("6. Manajemen Kamar Rawat Inap ") 
        print("7. Lihat Status Dokter & Jadwal ")
        print("8. PROSES MASUK RAWAT INAP (Opname)") 
        print("9. Update Lama Inap & Checkout") 
        print("10. Cetak Struk ")
        
        # --- MENU KHUSUS SUPER ADMIN ---
        if admin_role == "Super Admin":
            print("11. Manajemen Akun Admin (Khusus Super Admin)")
        
        print("0. Logout & Keluar")
        pilihan = input("Pilih menu: ")
        
        if pilihan == "1":
            tambah_pasien()
        elif pilihan == "2":
            lihat_pasien()
        elif pilihan == "3":
            cari_pasien()
        elif pilihan == "4":
            perbarui_pasien()
        elif pilihan == "5":
            hapus_pasien()
        elif pilihan == "6":
            manajemen_kamar()
        elif pilihan == "7":
            pilih_dokter() 
            lihat_status_dokter() 
        elif pilihan == "8":
            proses_masuk_rawat_inap()
        elif pilihan == "9":
            update_lama_inap_dan_hitung_biaya_akhir() 
        elif pilihan == "10":
            cetak_struk(admin_name) 
        elif pilihan == "11":
            # Proteksi Ganda: Cek role lagi sebelum masuk
            if admin_role == "Super Admin":
                menu_manajemen_akun()
            else:
                print("❌ Anda tidak memiliki akses ke menu ini.")
        elif pilihan == "0":
            print("Anda telah logout. Sampai jumpa!")
            break
        else:
            print("Pilihan tidak valid.")
        
        input("Tekan Enter untuk melanjutkan...")

# --- FUNGSI BARU MANAJEMEN AKUN (CRUD) ---

def validasi_password_baru():
    while True:
        password = input("Masukkan password baru (Min. 7 karakter): ")
        if len(password) > 6:
            return password
        print("❌ Password terlalu pendek! Minimal 7 karakter.")

def buat_akun_baru(semua_akun):
    print("\n=== Buat Akun Baru ===")
    username = input("Masukkan username baru: ")
    
    # Cek duplikat
    for a in semua_akun:
        if a["username"] == username:
            print("Username sudah terdaftar!")
            return
            
    password = validasi_password_baru()
    
    new_account = {"username": username, "password": password, "role": "Admin"}
    akun_non_admin.append(new_account)
    print(f"✅ Akun '{username}' berhasil dibuat!")

def lihat_semua_akun(semua_akun):
    print("\n=== Daftar Akun Terdaftar ===")
    print(f"| {'Username':<15} | {'Role':<12} |")
    print("-" * 32)
    for a in semua_akun:
        print(f"| {a['username']:<15} | {a.get('role', 'Admin'):<12} |")
    print("-" * 32)

def update_akun(semua_akun):
    lihat_semua_akun(semua_akun)
    target_user = input("\nMasukkan username yang ingin diedit: ")
    
    # Cek apakah target adalah Super Admin
    for admin in AKUN_ADMIN:
        if admin['username'] == target_user:
            print("❌ Akun Super Admin tidak dapat diedit dari menu ini.")
            return

    found = False
    for akun in akun_non_admin:
        if akun['username'] == target_user:
            found = True
            print(f"--- Edit Akun: {target_user} ---")
            
            new_user = input(f"Username baru ({akun['username']}): ")
            if new_user:
                is_exist = any(a['username'] == new_user for a in semua_akun if a['username'] != target_user)
                if is_exist:
                    print("Username sudah dipakai orang lain. Batal ganti username.")
                else:
                    akun['username'] = new_user
            
            ganti_pass = input("Ganti password? (y/n): ").lower()
            if ganti_pass == 'y':
                akun['password'] = validasi_password_baru()
            
            print("✅ Data akun berhasil diperbarui.")
            break
    
    if not found:
        print("Username tidak ditemukan di daftar akun tambahan.")

def hapus_akun(semua_akun):
    lihat_semua_akun(semua_akun)
    target_user = input("\nMasukkan username yang ingin DIHAPUS: ")
    
    # Cek Super Admin
    for admin in AKUN_ADMIN:
        if admin['username'] == target_user:
            print("❌ Akun Super Admin TIDAK BOLEH dihapus.")
            return

    found = False
    for i, akun in enumerate(akun_non_admin):
        if akun['username'] == target_user:
            konfirmasi = input(f"⚠️ Yakin menghapus akun {target_user}? (y/n): ").lower()
            if konfirmasi == 'y':
                del akun_non_admin[i]
                print("✅ Akun berhasil dihapus.")
            else:
                print("Penghapusan dibatalkan.")
            found = True
            break
            
    if not found:
        print("Username tidak ditemukan.")

def login(akun_list):
    print("\n=== Login Sistem Rumah Sakit ===")
    username = input("Username: ")
    password = input("Password: ")

    for a in akun_list:
        if a["username"] == username and a["password"] == password:
            role = a.get("role", "Admin") # Ambil role, default Admin biasa
            print(f"Login berhasil! Selamat datang, {username.upper()} ({role})")
            return username, role # Return nama user DAN role

    print("Login gagal! Username atau password salah.")
    return None, None

def halaman_awal():
    while True:
        semua_akun = AKUN_ADMIN + akun_non_admin
        clear_screen()
        print("=== Selamat datang di Sistem Rumah Sakit ===")
        print("1. Login Masuk Sistem")
        print("2. Keluar")
        pilih = input("Pilih menu (1-2): ")

        if pilih == "1":
            user_login, user_role = login(semua_akun)
            if user_login:
                menu_utama(user_login, user_role) # Kirim nama admin & role ke menu utama
            else:
                input("Tekan Enter untuk mencoba lagi...")
        elif pilih == "2":
            print("Keluar dari sistem.")
            exit()
        else:
            print("Pilihan tidak valid.")

# ===================== PROGRAM UTAMA =====================
if __name__ == "__main__":
    inisialisasi_status_dokter()
    print("\n[PERINGATAN: Program berjalan tanpa persistensi data. Data akan hilang setelah program ditutup.]")
    input("Tekan Enter untuk melanjutkan ke Halaman Awal...")
    halaman_awal()
