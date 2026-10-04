
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import requests
import sqlite3
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from datetime import datetime


API_KEY = "Buraya_API_Key_gelecek"
DB_ADI = "hava_durumu.db"


sehirler = {
    "Adana": (37.0000, 35.3213),
    "Adiyaman": (37.7648, 38.2786),
    "Afyonkarahisar": (38.7507, 30.5567),
    "Agri": (39.7191, 43.0503),
    "Aksaray": (38.3687, 34.0370),
    "Amasya": (40.6499, 35.8353),
    "Ankara": (39.9334, 32.8597),
    "Antalya": (36.8969, 30.7133),
    "Ardahan": (41.1105, 42.7022),
    "Artvin": (41.1828, 41.8183),
    "Aydin": (37.8560, 27.8416),
    "Balikesir": (39.6484, 27.8826),
    "Bartin": (41.6344, 32.3375),
    "Batman": (37.8812, 41.1351),
    "Bayburt": (40.2552, 40.2249),
    "Bilecik": (40.1451, 29.9793),
    "Bingol": (38.8847, 40.4983),
    "Bitlis": (38.4006, 42.1095),
    "Bolu": (40.7392, 31.6116),
    "Burdur": (37.7203, 30.2908),
    "Bursa": (40.1828, 29.0665),
    "Canakkale": (40.1553, 26.4142),
    "Cankiri": (40.6013, 33.6134),
    "Corum": (40.5499, 34.9533),
    "Denizli": (37.7765, 29.0864),
    "Diyarbakir": (37.9144, 40.2306),
    "Duzce": (40.8438, 31.1565),
    "Edirne": (41.6764, 26.5559),
    "Elazig": (38.6810, 39.2264),
    "Erzincan": (39.7500, 39.5000),
    "Erzurum": (39.9000, 41.2700),
    "Eskisehir": (39.7767, 30.5206),
    "Gaziantep": (37.0662, 37.3833),
    "Giresun": (40.9128, 38.3895),
    "Gumushane": (40.4386, 39.5086),
    "Hakkari": (37.5833, 43.7333),
    "Hatay": (36.4018, 36.3498),
    "Igdir": (39.9237, 44.0450),
    "Isparta": (37.7648, 30.5566),
    "Istanbul": (41.0082, 28.9784),
    "Izmir": (38.4192, 27.1287),
    "Kahramanmaras": (37.5858, 36.9371),
    "Karabuk": (41.2061, 32.6204),
    "Karaman": (37.1759, 33.2287),
    "Kars": (40.6013, 43.0975),
    "Kastamonu": (41.3887, 33.7827),
    "Kayseri": (38.7205, 35.4826),
    "Kilis": (36.7184, 37.1212),
    "Kirikkale": (39.8468, 33.5153),
    "Kirklareli": (41.7333, 27.2167),
    "Kirsehir": (39.1425, 34.1709),
    "Kocaeli": (40.8533, 29.8815),
    "Konya": (37.8746, 32.4932),
    "Kutahya": (39.4242, 29.9833),
    "Malatya": (38.3552, 38.3095),
    "Manisa": (38.6191, 27.4289),
    "Mardin": (37.3212, 40.7245),
    "Mersin": (36.8121, 34.6415),
    "Mugla": (37.2153, 28.3636),
    "Mus": (38.7432, 41.5065),
    "Nevsehir": (38.6939, 34.6857),
    "Nigde": (37.9667, 34.6833),
    "Ordu": (40.9839, 37.8764),
    "Osmaniye": (37.0742, 36.2461),
    "Rize": (41.0201, 40.5234),
    "Sakarya": (40.6940, 30.4358),
    "Samsun": (41.2867, 36.3300),
    "Sanliurfa": (37.1591, 38.7969),
    "Siirt": (37.9333, 41.9500),
    "Sinop": (42.0231, 35.1531),
    "Sirnak": (37.4187, 42.4918),
    "Sivas": (39.7477, 37.0179),
    "Tekirdag": (40.9833, 27.5167),
    "Tokat": (40.3167, 36.5500),
    "Trabzon": (41.0015, 39.7178),
    "Tunceli": (39.3074, 39.4388),
    "Usak": (38.6823, 29.4082),
    "Van": (38.4942, 43.3800),
    "Yalova": (40.6500, 29.2667),
    "Yozgat": (39.8181, 34.8147),
    "Zonguldak": (41.4564, 31.7987),
}


def hava_ikonu(kod):
    if kod == None:
        return "🌡️"
    if kod == 0:
        return "☀️"
    if kod == 1 or kod == 2:
        return "🌤️"
    if kod == 3:
        return "☁️"
    if kod == 45 or kod == 48:
        return "🌫️"
    if kod >= 51 and kod <= 57:
        return "🌦️"
    if kod >= 61 and kod <= 67:
        return "🌧️"
    if kod >= 71 and kod <= 77:
        return "❄️"
    if kod >= 80 and kod <= 82:
        return "🌧️"
    if kod >= 95 and kod <= 99:
        return "⛈️"
    return "🌡️"


def hava_aciklama(kod):
    if kod == None:
        return ""
    if kod == 0:
        return "Acik"
    if kod == 1 or kod == 2:
        return "Az Bulutlu"
    if kod == 3:
        return "Bulutlu"
    if kod == 45 or kod == 48:
        return "Sisli"
    if kod >= 51 and kod <= 57:
        return "Cisenti"
    if kod >= 61 and kod <= 67:
        return "Yagmurlu"
    if kod >= 71 and kod <= 77:
        return "Karli"
    if kod >= 80 and kod <= 82:
        return "Saganak"
    if kod >= 95 and kod <= 99:
        return "Firtina"
    return ""


def db_olustur():
    conn = sqlite3.connect(DB_ADI)
    cur = conn.cursor()

    cur.execute("""
        CREATE TABLE IF NOT EXISTS gunluk_veri (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            sehir TEXT,
            tarih TEXT,
            sicaklik REAL,
            nem REAL,
            cekme_zamani TEXT
        )
    """)

    cur.execute("""
        CREATE TABLE IF NOT EXISTS saatlik_veri (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            sehir TEXT,
            saat TEXT,
            sicaklik REAL,
            nem REAL,
            kod INTEGER,
            cekme_zamani TEXT
        )
    """)

    conn.commit()
    conn.close()


def gunluk_kaydet(sehir, tarih, sic, nem):
    conn = sqlite3.connect(DB_ADI)
    cur = conn.cursor()
    simdi = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    cur.execute(
        "INSERT INTO gunluk_veri (sehir, tarih, sicaklik, nem, cekme_zamani) VALUES (?, ?, ?, ?, ?)",
        (sehir, tarih, sic, nem, simdi)
    )
    conn.commit()
    conn.close()


def saatlik_kaydet(sehir, saat, sic, nem, kod):
    conn = sqlite3.connect(DB_ADI)
    cur = conn.cursor()
    simdi = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    cur.execute(
        "INSERT INTO saatlik_veri (sehir, saat, sicaklik, nem, kod, cekme_zamani) VALUES (?, ?, ?, ?, ?, ?)",
        (sehir, saat, sic, nem, kod, simdi)
    )
    conn.commit()
    conn.close()


def gunluk_getir(sehir):
    conn = sqlite3.connect(DB_ADI)
    cur = conn.cursor()

    cur.execute("SELECT MAX(cekme_zamani) FROM gunluk_veri WHERE sehir = ?", (sehir,))
    row = cur.fetchone()
    son_zaman = row[0]

    if son_zaman == None:
        conn.close()
        return [], None

    cur.execute(
        "SELECT tarih, sicaklik, nem FROM gunluk_veri WHERE sehir = ? AND cekme_zamani = ? ORDER BY id",
        (sehir, son_zaman)
    )
    data = cur.fetchall()
    conn.close()
    return data, son_zaman


def saatlik_getir(sehir):
    conn = sqlite3.connect(DB_ADI)
    cur = conn.cursor()

    cur.execute("SELECT MAX(cekme_zamani) FROM saatlik_veri WHERE sehir = ?", (sehir,))
    row = cur.fetchone()
    son_zaman = row[0]

    if son_zaman == None:
        conn.close()
        return [], None

    cur.execute(
        "SELECT saat, sicaklik, nem, kod FROM saatlik_veri WHERE sehir = ? AND cekme_zamani = ? ORDER BY saat",
        (sehir, son_zaman)
    )
    data = cur.fetchall()
    conn.close()
    return data, son_zaman


def collectapi_cek(sehir):
    url = "https://api.collectapi.com/weather/getWeather"
    headers = {
        "content-type": "application/json",
        "authorization": "apikey " + API_KEY
    }
    params = {"lang": "tr", "city": sehir}

    try:
        res = requests.get(url, headers=headers, params=params, timeout=15)
        data = res.json()

        if type(data) == list:
            gunler = data
        elif type(data) == dict:
            if "result" in data:
                gunler = data["result"]
            else:
                gunler = []
        else:
            return False, "API formati anlasilmadi"

        if len(gunler) == 0:
            return False, "API'den veri gelmedi"

        i = 0
        while i < len(gunler):
            gun = gunler[i]
            tarih = gun.get("date", "")
            derece = gun.get("degree", "0")
            nem_str = gun.get("humidity", "0")

            try:
                sic = float(str(derece).replace(",", ".").replace("°", ""))
            except:
                sic = 0.0

            try:
                nem = float(str(nem_str).replace(",", ".").replace("%", ""))
            except:
                nem = 0.0

            gunluk_kaydet(sehir, tarih, sic, nem)
            i = i + 1

        return True, str(len(gunler)) + " gunluk veri alindi"

    except Exception as e:
        return False, "Hata: " + str(e)


def openmeteo_cek(sehir):
    if sehir not in sehirler:
        return False, sehir + " icin koordinat yok"

    enlem = sehirler[sehir][0]
    boylam = sehirler[sehir][1]

    url = "https://api.open-meteo.com/v1/forecast"
    params = {
        "latitude": enlem,
        "longitude": boylam,
        "hourly": "temperature_2m,relative_humidity_2m,weather_code",
        "timezone": "Europe/Istanbul",
        "forecast_days": 1
    }

    try:
        res = requests.get(url, params=params, timeout=15)
        data = res.json()

        saatler = data["hourly"]["time"]
        sicakliklar = data["hourly"]["temperature_2m"]
        nemler = data["hourly"]["relative_humidity_2m"]
        kodlar = data["hourly"]["weather_code"]

        if len(saatler) == 0:
            return False, "Veri gelmedi"

        i = 0
        while i < len(saatler):
            saatlik_kaydet(sehir, saatler[i], float(sicakliklar[i]), float(nemler[i]), int(kodlar[i]))
            i = i + 1

        return True, str(len(saatler)) + " saatlik veri alindi"

    except Exception as e:
        return False, "Hata: " + str(e)


def tarih_cevir(tarih_str):
    if tarih_str == None or tarih_str == "":
        return None

    formatlar = ["%m/%d/%Y", "%d.%m.%Y", "%Y-%m-%d", "%d/%m/%Y"]
    i = 0
    while i < len(formatlar):
        try:
            return datetime.strptime(tarih_str.strip(), formatlar[i])
        except:
            pass
        i = i + 1
    return None


def grafik_ciz(canvas_alani, ozet_alani, sehir, mod, grafik_turu, son_label):
    x_list = []
    sic_list = []
    nem_list = []
    anki_kod = None
    cekme_zaman = None

    if mod == "Saatlik":
        data, cekme_zaman = saatlik_getir(sehir)
        if len(data) == 0:
            messagebox.showwarning("Uyari", "Veri yok! Once API'den veri cekin.")
            return

        simdi = datetime.now().hour
        en_yakin = 99

        i = 0
        while i < len(data):
            satir = data[i]
            saat_str = satir[0]
            sic = satir[1]
            nem = satir[2]
            kod = satir[3]

            try:
                dt = datetime.fromisoformat(saat_str)
                etiket = dt.strftime("%H:00")
                fark = abs(dt.hour - simdi)
                if fark < en_yakin:
                    en_yakin = fark
                    anki_kod = kod
            except:
                etiket = saat_str

            x_list.append(etiket)
            sic_list.append(sic)
            nem_list.append(nem)
            i = i + 1

    else:
        data, cekme_zaman = gunluk_getir(sehir)
        if len(data) == 0:
            messagebox.showwarning("Uyari", "Veri yok! Once API'den veri cekin.")
            return

        i = 0
        while i < len(data):
            satir = data[i]
            tarih_str = satir[0]
            sic = satir[1]
            nem = satir[2]

            dt = tarih_cevir(tarih_str)
            if dt != None:
                etiket = dt.strftime("%d.%m")
            else:
                etiket = tarih_str

            x_list.append(etiket)
            sic_list.append(sic)
            nem_list.append(nem)
            i = i + 1

    if len(x_list) == 0:
        messagebox.showwarning("Uyari", "Grafik icin veri yok")
        return

    ozet_goster(ozet_alani, sehir, sic_list, nem_list, anki_kod)

    if cekme_zaman != None:
        try:
            dt = datetime.strptime(cekme_zaman, "%Y-%m-%d %H:%M:%S")
            son_label.config(text="Son guncelleme: " + dt.strftime("%d.%m.%Y %H:%M"))
        except:
            son_label.config(text="Son guncelleme: " + cekme_zaman)

    for w in canvas_alani.winfo_children():
        w.destroy()

    fig, ax = plt.subplots(figsize=(8, 3.8))
    fig.patch.set_facecolor("#FFFFFF")
    ax.set_facecolor("#FFFFFF")

    if len(x_list) == 1:
        nokta_boyutu = 12
    else:
        nokta_boyutu = 6

    if grafik_turu == "Sicaklik":
        ax.plot(x_list, sic_list, marker='o', color='#E07A5F',
                linewidth=2.5, markersize=nokta_boyutu, label="Sicaklik (°C)")
        ax.set_ylabel("Sicaklik (°C)", color='#E07A5F')
        ax.tick_params(axis='y', labelcolor='#E07A5F')
        ax.legend(loc="upper left")

    elif grafik_turu == "Nem":
        ax.plot(x_list, nem_list, marker='s', color='#81B29A',
                linewidth=2.5, markersize=nokta_boyutu, label="Nem (%)")
        ax.set_ylabel("Nem (%)", color='#81B29A')
        ax.tick_params(axis='y', labelcolor='#81B29A')
        ax.legend(loc="upper left")

    else:
        ax.plot(x_list, sic_list, marker='o', color='#E07A5F',
                linewidth=2.5, markersize=nokta_boyutu, label="Sicaklik (°C)")
        ax.set_ylabel("Sicaklik (°C)", color='#E07A5F')
        ax.tick_params(axis='y', labelcolor='#E07A5F')

        ax2 = ax.twinx()
        ax2.plot(x_list, nem_list, marker='s', color='#81B29A',
                 linewidth=2.5, markersize=nokta_boyutu, label="Nem (%)")
        ax2.set_ylabel("Nem (%)", color='#81B29A')
        ax2.tick_params(axis='y', labelcolor='#81B29A')

        l1, e1 = ax.get_legend_handles_labels()
        l2, e2 = ax2.get_legend_handles_labels()
        ax.legend(l1 + l2, e1 + e2, loc="upper left")

    ax.set_title(sehir + " - " + mod + " Gorunum", fontsize=12, fontweight='bold',
                 color="#3D5A80", pad=10)
    ax.set_xlabel("Zaman", color="#3D5A80")
    ax.grid(True, alpha=0.25, linestyle='--')

    if mod == "Saatlik" and len(x_list) > 12:
        j = 0
        for etiket in ax.get_xticklabels():
            if j % 2 != 0:
                etiket.set_visible(False)
            j = j + 1
        plt.xticks(rotation=0, ha='center')
    else:
        plt.xticks(rotation=45, ha='right')

    plt.tight_layout()

    canvas = FigureCanvasTkAgg(fig, master=canvas_alani)
    canvas.draw()
    canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)


def ozet_goster(ozet_alani, sehir, sic_list, nem_list, kod):
    for w in ozet_alani.winfo_children():
        w.destroy()

    anki_sic = sic_list[0]
    anki_nem = nem_list[0]

    toplam = 0
    i = 0
    while i < len(sic_list):
        toplam = toplam + sic_list[i]
        i = i + 1
    ort = toplam / len(sic_list)

    sol = tk.Frame(ozet_alani, bg="#FFFFFF")
    sol.pack(side="left", padx=20, pady=10)

    if kod != None:
        ikon = hava_ikonu(kod)
    else:
        ikon = "🌡️"

    tk.Label(sol, text=ikon, font=("Arial", 56), bg="#FFFFFF").pack()
    tk.Label(sol, text=sehir, font=("Arial", 14, "bold"),
             bg="#FFFFFF", fg="#3D5A80").pack()

    if kod != None:
        aciklama = hava_aciklama(kod)
        if aciklama != "":
            tk.Label(sol, text=aciklama, font=("Arial", 10),
                     bg="#FFFFFF", fg="#8D99AE").pack()

    orta = tk.Frame(ozet_alani, bg="#FFFFFF")
    orta.pack(side="left", padx=30, pady=10)
    tk.Label(orta, text=str(round(anki_sic, 1)) + "°C",
             font=("Arial", 42, "bold"), bg="#FFFFFF", fg="#E07A5F").pack()
    tk.Label(orta, text="Sicaklik", font=("Arial", 10),
             bg="#FFFFFF", fg="#8D99AE").pack()

    sag = tk.Frame(ozet_alani, bg="#FFFFFF")
    sag.pack(side="left", padx=30, pady=10)
    tk.Label(sag, text="%" + str(round(anki_nem)),
             font=("Arial", 42, "bold"), bg="#FFFFFF", fg="#81B29A").pack()
    tk.Label(sag, text="Nem", font=("Arial", 10),
             bg="#FFFFFF", fg="#8D99AE").pack()

    mini = tk.Frame(ozet_alani, bg="#FFFFFF")
    mini.pack(side="right", padx=20, pady=10)
    tk.Label(mini, text="Ortalama Sicaklik", font=("Arial", 9),
             bg="#FFFFFF", fg="#8D99AE").pack(anchor="e")
    tk.Label(mini, text=str(round(ort, 1)) + "°C",
             font=("Arial", 18, "bold"), bg="#FFFFFF", fg="#3D5A80").pack(anchor="e")
    tk.Label(mini, text="(" + str(len(sic_list)) + " kayit)",
             font=("Arial", 8, "italic"), bg="#FFFFFF", fg="#8D99AE").pack(anchor="e")


def main():
    db_olustur()

    pencere = tk.Tk()
    pencere.title("Hava Durumu Takip")
    pencere.geometry("980x820")
    pencere.configure(bg="#FFF5F0")
    pencere.minsize(900, 750)

    tk.Label(pencere, text="🌤️  Hava Durumu Takip Uygulamasi",
             font=("Arial", 18, "bold"), bg="#FFF5F0", fg="#3D5A80").pack(pady=(15, 4))

    kontrol = tk.Frame(pencere, bg="#FFF5F0")
    kontrol.pack(pady=8)

    tk.Label(kontrol, text="Sehir:", bg="#FFF5F0", fg="#3D5A80",
             font=("Arial", 11, "bold")).grid(row=0, column=0, padx=5)
    sehir_var = tk.StringVar(value="Istanbul")

    sehir_listesi = sorted(sehirler.keys())

    sehir_combo = ttk.Combobox(kontrol, textvariable=sehir_var,
                               values=sehir_listesi, width=15,
                               font=("Arial", 11), height=20)
    sehir_combo.grid(row=0, column=1, padx=5)

    tk.Label(kontrol, text="Gorunum:", bg="#FFF5F0", fg="#3D5A80",
             font=("Arial", 11, "bold")).grid(row=0, column=2, padx=5)
    mod_var = tk.StringVar(value="Saatlik")
    mod_combo = ttk.Combobox(kontrol, textvariable=mod_var,
                             values=["Saatlik", "Gunluk"], width=10,
                             font=("Arial", 11), state="readonly")
    mod_combo.grid(row=0, column=3, padx=5)

    tk.Label(kontrol, text="Grafik:", bg="#FFF5F0", fg="#3D5A80",
             font=("Arial", 11, "bold")).grid(row=0, column=4, padx=5)
    grafik_var = tk.StringVar(value="Her Ikisi")
    grafik_combo = ttk.Combobox(kontrol, textvariable=grafik_var,
                                values=["Sicaklik", "Nem", "Her Ikisi"],
                                width=10, font=("Arial", 11), state="readonly")
    grafik_combo.grid(row=0, column=5, padx=5)

    durum_label = tk.Label(pencere, text="", bg="#FFF5F0",
                           fg="#84A59D", font=("Arial", 10))
    durum_label.pack(pady=2)

    ozet_dis = tk.Frame(pencere, bg="#FFF5F0")
    ozet_dis.pack(fill="x", padx=20, pady=(5, 8))

    ozet_alani = tk.Frame(ozet_dis, bg="#FFFFFF", relief="solid", bd=1,
                          highlightbackground="#A8DADC", highlightthickness=1)
    ozet_alani.pack(fill="x")

    tk.Label(ozet_alani, text="📊 Bir sehir secip 'API'den Veri Cek'e basin.",
             font=("Arial", 12, "italic"), bg="#FFFFFF", fg="#8D99AE",
             pady=40).pack()

    son_label = tk.Label(pencere, text="Henuz veri cekilmedi",
                         bg="#FFF5F0", fg="#8D99AE",
                         font=("Arial", 9, "italic"))
    son_label.pack(anchor="e", padx=25)

    canvas_dis = tk.Frame(pencere, bg="#FFF5F0")
    canvas_dis.pack(fill="both", expand=True, padx=20, pady=(2, 10))

    canvas_alani = tk.Frame(canvas_dis, bg="#FFFFFF", relief="solid", bd=1,
                            highlightbackground="#A8DADC", highlightthickness=1)
    canvas_alani.pack(fill="both", expand=True)

    def veri_cek():
        sehir = sehir_var.get().strip()
        if sehir == "":
            messagebox.showerror("Hata", "Sehir secin!")
            return

        mod = mod_var.get()
        durum_label.config(text="Veri cekiliyor...", fg="#FFB5A7")
        pencere.update()

        if mod == "Saatlik":
            ok, msg = openmeteo_cek(sehir)
        else:
            ok, msg = collectapi_cek(sehir)

        if ok:
            durum_label.config(text="✅ " + msg, fg="#84A59D")
            grafik_ciz(canvas_alani, ozet_alani, sehir, mod, grafik_var.get(), son_label)
        else:
            durum_label.config(text="❌ " + msg, fg="#F28482")

    def secim_degisti(event=None):
        sehir = sehir_var.get().strip()
        if sehir == "":
            return

        mod = mod_var.get()

        if mod == "Saatlik":
            data, _ = saatlik_getir(sehir)
        else:
            data, _ = gunluk_getir(sehir)

        if len(data) > 0:
            grafik_ciz(canvas_alani, ozet_alani, sehir, mod, grafik_var.get(), son_label)

    sehir_combo.bind("<<ComboboxSelected>>", secim_degisti)
    mod_combo.bind("<<ComboboxSelected>>", secim_degisti)
    grafik_combo.bind("<<ComboboxSelected>>", secim_degisti)

    buton_kutu = tk.Frame(pencere, bg="#FFF5F0")
    buton_kutu.pack(pady=10)

    tk.Button(buton_kutu, text="🌐  API'den Veri Cek",
              command=veri_cek, bg="#84A59D", fg="white",
              font=("Arial", 12, "bold"), padx=20, pady=8,
              relief="flat", cursor="hand2",
              activebackground="#3D5A80",
              activeforeground="white").pack()

    pencere.mainloop()


if __name__ == "__main__":
    main()
