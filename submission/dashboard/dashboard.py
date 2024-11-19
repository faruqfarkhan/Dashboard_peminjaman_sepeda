import streamlit as st
from calendar import month_abbr
from datetime import datetime
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st




########################################## Mengelola Data ###################################


# file = "subbmission/data/day_data.csv"
day_data = pd.read_csv(r"submission/dashboard/day_data.csv")
day_data["dteday"] = pd.to_datetime(day_data["dteday"])


# file = "dashboard/day_data.csv"
hour_data = pd.read_csv("hour_data.csv")
hour_data["dteday"] = pd.to_datetime(hour_data["dteday"])

####Data Peminjam Per 1 Bulan ####
def data_peminjam_per_satu_bulan(tahun_bulan):
    data_per_bulan = day_data.resample(rule='1D', on='dteday').agg({
        "registered": "sum",
        "casual": "sum",
        "cnt": "sum"
    })
    data_per_bulan.index = data_per_bulan.index.strftime('%Y-%m-%d')
    data_per_bulan = data_per_bulan.reset_index()
    data_per_bulan['day'] = data_per_bulan['dteday'].str[-2:]
    data_per_bulan["hari libur"]= day_data["workingday"]
    data_tahun_bulan = data_per_bulan[data_per_bulan['dteday'].str.startswith(tahun_bulan)]
    return data_tahun_bulan

####Data meminjam berdasarkan cuaca per 1 bulan###
def data_cuaca_per_satu_bulan(tahun_bulan):
    data_cuaca = hour_data.groupby([pd.Grouper(key='dteday', freq='1ME'), "weathersit"]).agg({
    "cnt": ["sum", "std"]
    })
    data_cuaca['cnt', 'std'] = data_cuaca['cnt', 'std'].fillna(0)
    # Reset index untuk memindahkan 'dteday' dan 'weathersit' ke kolom biasa
    data_cuaca = data_cuaca.reset_index()
    data_cuaca['dteday'] = data_cuaca['dteday'].astype(str)
    data_cuaca['cuaca'] = data_cuaca['weathersit'].astype(int).apply(
    lambda x: 'clear' if x == 1 else
              'mist' if x == 2 else
              'rain' if x == 4 else
              'snow'
    )
    data_cuaca_perbulan = data_cuaca[data_cuaca['dteday'].str.startswith(tahun_bulan)]
    return data_cuaca_perbulan

#data meminjam berdasarkan hari libur dan hari kerja berdasarkan bulan

def data_hari_kerja(tanggal):
    data_berdasarkan_working_day = hour_data.groupby(by=[pd.Grouper(key='dteday', freq='1ME'), "workingday"]).agg({
    "casual":"sum",
    "registered":"sum"
    })

    data_berdasarkan_working_day = data_berdasarkan_working_day.reset_index()
    data_berdasarkan_working_day["dteday"]=data_berdasarkan_working_day["dteday"].astype(str) 

    data_berdasarkan_working_day_perbulan = data_berdasarkan_working_day[
    data_berdasarkan_working_day['dteday'].str.startswith(tanggal)
    ]
    data_hari_kerja = data_berdasarkan_working_day_perbulan[
    data_berdasarkan_working_day_perbulan['workingday'] == 1
    ]   
    hari_kerja_sizes = [
    data_hari_kerja["casual"].values[0] if not data_hari_kerja.empty else 0,
    data_hari_kerja["registered"].values[0] if not data_hari_kerja.empty else 0
    ]   
    return hari_kerja_sizes


def data_hari_libur(tanggal):
    data_berdasarkan_working_day = hour_data.groupby(by=[pd.Grouper(key='dteday', freq='1ME'), "workingday"]).agg({
    "casual":"sum",
    "registered":"sum"
    })

    data_berdasarkan_working_day = data_berdasarkan_working_day.reset_index()
    data_berdasarkan_working_day["dteday"]=data_berdasarkan_working_day["dteday"].astype(str) 

    data_berdasarkan_working_day_perbulan = data_berdasarkan_working_day[
    data_berdasarkan_working_day['dteday'].str.startswith(tanggal)
    ]
    data_akhir_pekan = data_berdasarkan_working_day_perbulan[
    data_berdasarkan_working_day_perbulan['workingday'] == 0
    ]
    akhir_pekan_sizes = [
    data_akhir_pekan["casual"].values[0] if not data_akhir_pekan.empty else 0,
    data_akhir_pekan["registered"].values[0] if not data_akhir_pekan.empty else 0
    ]
    return akhir_pekan_sizes

def jumlah_data(data_kerja_size):
    total_hari_kerja = sum(data_kerja_size)
    return total_hari_kerja

def data_jumlah_peminjaman_permusin(tahun):
    data_per_musim =day_data.groupby(by=["year","season"]).agg({
    "cnt": "sum"
    })
    data_per_musim = data_per_musim.reset_index ()
    data_per_musim["year"] =  data_per_musim["year"].astype(str)
    data_permusim_pertahun = data_per_musim[data_per_musim['year'].str.startswith(tahun)]
    return data_permusim_pertahun

#data meminjam berdasarkan hari libur dan hari kerja berdasarkan tahun

def data_hari_kerja_pertahun(tahun):
    data_berdasarkan_working_day = hour_data.groupby(by=[pd.Grouper(key='dteday', freq='1ME'), "workingday"]).agg({
    "casual":"sum",
    "registered":"sum"
    })

    data_berdasarkan_working_day = data_berdasarkan_working_day.reset_index()
    data_berdasarkan_working_day["dteday"]=data_berdasarkan_working_day["dteday"].astype(str) 
    data_berdasarkan_working_day_pertahun = data_berdasarkan_working_day[
        data_berdasarkan_working_day['dteday'].str.startswith(tahun)
    ]
    data_hari_kerja = data_berdasarkan_working_day_pertahun[data_berdasarkan_working_day_pertahun['workingday'] == 1]
    hari_kerja_casual = data_hari_kerja['casual'].sum()
    hari_kerja_registered = data_hari_kerja['registered'].sum()
    hari_kerja_sizes = [hari_kerja_casual, hari_kerja_registered]
    return hari_kerja_sizes

def data_hari_libur_pertahun(tahun):
    data_berdasarkan_working_day = hour_data.groupby(by=[pd.Grouper(key='dteday', freq='1ME'), "workingday"]).agg({
        "casual":"sum",
        "registered":"sum"
    })

    data_berdasarkan_working_day = data_berdasarkan_working_day.reset_index()
    data_berdasarkan_working_day["dteday"]=data_berdasarkan_working_day["dteday"].astype(str)   
    data_berdasarkan_working_day_pertahun = data_berdasarkan_working_day[
        data_berdasarkan_working_day['dteday'].str.startswith(tahun)
    ]
    data_akhir_pekan = data_berdasarkan_working_day_pertahun[data_berdasarkan_working_day_pertahun['workingday'] == 0]
    akhir_pekan_casual = data_akhir_pekan['casual'].sum()
    akhir_pekan_registered = data_akhir_pekan['registered'].sum()
    akhir_pekan_sizes = [akhir_pekan_casual, akhir_pekan_registered]
    return akhir_pekan_sizes

def peminjaman_perquarter(tahun):
    data_quartal = hour_data.resample(rule='3ME', on='dteday').agg({
        "registered": "sum",
        "casual": "sum",
        "cnt": "sum"
    })

    data_quartal.index = data_quartal.index.strftime('%Y -  %m')
    data_quartal = data_quartal.reset_index()
    data_quartal['month'] = data_quartal['dteday'].str[-2:]
    # data_quartal
    data_quartal['quarter'] = data_quartal['month'].astype(int).apply(
        lambda x: 'Q1' if x in [1, 2, 3] else
                'Q2' if x in [4, 5, 6] else
                'Q3' if x in [7, 8, 9] else
                'Q4'
    )
    data_tahun = data_quartal[data_quartal['dteday'].str.startswith(tahun)]
    return data_tahun

def peminjam():
    jumlah_peminjam = hour_data.resample(rule='YE', on='dteday').agg({
        "registered": "sum",
        "casual": "sum",
        "cnt": "sum"
    })

    jumlah_peminjam.index = jumlah_peminjam.index.strftime('%Y')
    jumlah_peminjam = jumlah_peminjam.reset_index()
    return jumlah_peminjam

def perbandingan_2011_2012():
    jumlah_peminjam = hour_data.resample(rule='1ME', on='dteday').agg({
        "registered": "sum",
        "casual": "sum",
        "cnt": "sum"
    })

    jumlah_peminjam.index = jumlah_peminjam.index.strftime('%Y - %m')
    jumlah_peminjam = jumlah_peminjam.reset_index()
    return jumlah_peminjam

############################################## Menampilkan pages ######################################


def intro():
    import streamlit as st

    st.write("# Halo Selamat Datang Di Dashboard Faruq! 👋")

    st.markdown(
        """
        Ini merupakan sebuah proyek yang saya kerjakan untuk memenuhi syarat kelulusan dari pelatihan data analyst menggunakan python di decoding.

        Di web ini kalian bisa melihat dasbhboard yang saya bagi berdasarkan tahunan dan bulanan,

        **👈 Kalian bisa coba check di side bar**

        Untuk di halaman ini saya juga menampilkan 2 buat chart yaitu
        - Perbandingan Peminjaman Sepeda antara tahun 2011 dan 2012
        - Perbandingan Jumlah peminjaman Sepeda dengan Frequensi 1 bulan antara tahun 2011 dan 2012

    """
    )

    jumlah_peminjam = peminjam()
    jumlah_peminjam_2011vs2012 = perbandingan_2011_2012()
    fig, ax = plt.subplots(figsize=(5, 5))

    # Define explode untuk memberi efek pada satu bagian pie chart
    explode = (0, 0.1)  # Sedikit meledakkan bagian kedua (casual)

    # Pie chart dengan tambahan informasi persentase
    plt.pie(jumlah_peminjam["cnt"], 
            autopct='%1.1f%%',  # Format persentase
            colors=["#DA8359", "#A5B68D"], 
            shadow=True, 
            explode=explode, 
            startangle=90,  # Memulai pie chart dari sudut 90 derajat
            wedgeprops={'edgecolor': 'black', 'linewidth': 1.5})  # Menambahkan garis tepi

    # Judul grafik
    ax.set_title("Perbandingan Peminjaman Sepeda", size=18, fontweight='bold')

    # Menambahkan legend di luar pie chart dan menyesuaikan posisi
    plt.legend(labels=jumlah_peminjam['dteday'], 
            loc='upper left', 
            bbox_to_anchor=(1, 1),  # Menempatkan legend di luar chart
            title="Tanggal Peminjaman", fontsize=10, title_fontsize=12)

    # Menambahkan grid ringan agar chart terlihat lebih rapi
    plt.grid(axis='y', alpha=0.3)

    st.pyplot(plt)

    jumlah_peminjam_filtered = jumlah_peminjam_2011vs2012[jumlah_peminjam_2011vs2012['dteday'].str.startswith(('2011', '2012'))]

    # Tambahkan kolom 'periode' untuk menyamakan bulan & triwulan antar tahun
    jumlah_peminjam_filtered['periode'] = jumlah_peminjam_filtered['dteday'].str[-2:]  # Ambil bulan

    # Pisahkan data berdasarkan tahun
    data_2011 = jumlah_peminjam_filtered[jumlah_peminjam_filtered['dteday'].str.startswith('2011')]
    data_2012 = jumlah_peminjam_filtered[jumlah_peminjam_filtered['dteday'].str.startswith('2012')]
    colors=["#024CAA","#EC8305"]
    # Plot
    plt.figure(figsize=(12, 6))

    # Line untuk 2011
    plt.plot(data_2011['periode'], data_2011['cnt'], 
            label='Jumlah Peminjaman (2011)', color=colors[1], marker='o', linestyle='-', linewidth=1.5)

    # Line untuk 2012
    plt.plot(data_2012['periode'], data_2012['cnt'], 
            label='Jumlah Peminjaman (2012)', color=colors[0], marker='o', linestyle='-', linewidth=1.5)

    # Judul dan Label
    plt.title('Perbandingan Jumlah Peminjaman Sepeda: 2011 vs 2012', size=16)
    plt.xlabel('Dalam 1 Tahun', size=12)
    plt.ylabel('Jumlah Peminjaman', size=12)
    plt.xticks(data_2011['periode'], fontsize=10)  # Menggunakan label bulan
    plt.legend()
    plt.grid(True, linestyle='--', alpha=0.7)

    st.pyplot(plt)
def data_pertahun():
    import streamlit as st
    import time
    import numpy as np
    import matplotlib.pyplot as plt
    import matplotlib.ticker as ticker
    from calendar import month_abbr
    from datetime import datetime
    import streamlit as st
    import pandas as pd
    
    st.write("# Page data pertahun")

    st.markdown(
        """
        Kalau di menu ini merupakan kumpulan pengelompokan dengan frequensi pertahun.
        Pada bagian bawah kalian juga bisa menentukan data pada tahun yang mau kalian lihat

        Untuk di halaman ini saya juga menampilkan 3 buat chart yaitu
        - Peminjaman sepeda permusim dalam 1 tahun
        - Total peminjaman pertahun berdasarkan hari kerja & hari libur
        - Data peminjaman perquartal

    """
    )

    explode = (0, 0.1) 
    with st.expander('Report Year'):
        report_year = st.selectbox("", range(2011, 2013))
        tahun_bulan = f"{report_year}"
        date_object = datetime.strptime(tahun_bulan, "%Y")
        st.write(date_object.strftime("%Y"))


    # Konversi elemen list ke tipe integer (jika diperlukan)
    
    
    data_permusim_pertahun = data_jumlah_peminjaman_permusin(date_object.strftime("%Y"))
    hari_kerja_sizes =data_hari_kerja_pertahun(date_object.strftime("%Y"))
    akhir_pekan_sizes = data_hari_libur_pertahun(date_object.strftime("%Y"))
    total_hari_kerja = sum(hari_kerja_sizes)
    total_akhir_pekan = sum(akhir_pekan_sizes)  
    data_tahun = peminjaman_perquarter(date_object.strftime("%Y"))

    

    



    st.subheader("Peminjaman sepeda permusim dalam 1 tahun")
    colors = ['#2a9d8f', '#e76f51', '#f4a261', '#264653']


    # Plot horizontal bar chart
    plt.figure(figsize=(12, 6))

    bars = plt.barh(
        data_permusim_pertahun['season'].apply(lambda x: 
            'Spring' if x == 1 else
            'Summer' if x == 2 else
            'Fall' if x == 3 else
            'Winter'),
        data_permusim_pertahun['cnt'], 
        color=colors, 
        edgecolor='black'
    )

    # Menambahkan nilai pada ujung batang
    for bar in bars:
        plt.text(
            bar.get_width() + 500,  
            bar.get_y() + bar.get_height() / 2, 
            f"{int(bar.get_width()):,}", 
            va='center', 
            fontsize=12, 
            color='#333333'
        )

    # Menambahkan garis grid horizontal
    plt.grid(axis='x', linestyle='--', alpha=0.5)

    # Menambahkan label dan judul
    plt.title(
        f'Jumlah Peminjaman Sepeda Per Musim (Tahun {date_object.strftime("%Y")})', 
        fontsize=14, 
        fontweight='bold', 
        color='#333333'
    )
    plt.xlabel('Jumlah Peminjaman (cnt)', fontsize=12, color='#333333')
    plt.ylabel('Musim', fontsize=12, color='#333333')

    # Menyesuaikan tampilan ticks
    plt.gca().xaxis.set_major_formatter(ticker.FuncFormatter(lambda x, _: f'{int(x):,}'))

    # Menyesuaikan margin agar tidak ada elemen yang terpotong
    plt.tight_layout()

    # Menampilkan plot di Streamlit
    st.pyplot(plt)


    st.subheader("Total peminjaman pertahun berdasarkan hari kerja & hari libur")
    
    fig, axes = plt.subplots(1, 2, figsize=(13, 20))

    # Pie chart untuk hari kerja
    axes[0].pie(hari_kerja_sizes, autopct='%1.1f%%',  # Format persentase
            colors=["#DA8359", "#A5B68D"], 
            shadow=True, 
            explode=explode, 
            startangle=90,  # Memulai pie chart dari sudut 90 derajat
            wedgeprops={'edgecolor': 'black', 'linewidth': 1.5})

    axes[0].set_title('Peminjaman Sepeda pada Hari Kerja', fontsize=14, fontweight='bold')
    axes[0].set_title(f'Peminjaman Sepeda pada Hari Kerja\n(Total: {total_hari_kerja:,})', fontsize=14, fontweight='bold')


    # # Pie chart untuk akhir pekan
    axes[1].pie(akhir_pekan_sizes, autopct='%1.1f%%',  # Format persentase
            colors=["#DA8359", "#A5B68D"], 
            shadow=True, 
            explode=explode, 
            startangle=90,  # Memulai pie chart dari sudut 90 derajat
            wedgeprops={'edgecolor': 'black', 'linewidth': 1.5})

    axes[1].set_title('Peminjaman Sepeda pada Akhir Pekan', fontsize=14, fontweight='bold')
    axes[1].set_title(f'Peminjaman Sepeda pada Hari Libur\n(Total: {total_akhir_pekan:,})', fontsize=14, fontweight='bold')

    plt.legend(labels=['Casual', 'Registered'], 
            loc='upper left', 
            bbox_to_anchor=(1, 1),  # Menempatkan legend di luar chart
            title="Tanggal Peminjaman", fontsize=10, title_fontsize=12)
    
    st.pyplot(fig)

    st.subheader("data peminjaman perquartal")
    width = 0.4
    x = np.arange(len(data_tahun))  # Posisi untuk bar

    plt.figure(figsize=(10, 6))  # Ukuran grafik
    plt.bar(x - width / 2, data_tahun["casual"], width, label="Casual", color="#FFA07A", edgecolor="black") 
    plt.bar(x + width / 2, data_tahun["registered"], width, label="Registered", color="#4682B4", edgecolor="black") 

    # Tambahkan label, grid, dan judul
    plt.xticks(x, data_tahun["quarter"], fontsize=12)  # Menampilkan quarter
    plt.xlabel("Quarter", fontsize=14)
    plt.ylabel("Jumlah Peminjaman", fontsize=14)
    plt.title(f"Perbandingan Peminjaman Sepeda Tahun {date_object.strftime("%Y")}", fontsize=16, fontweight="bold")
    plt.legend(fontsize=12)
    plt.grid(axis="y", linestyle="--", alpha=0.7)  # Tambahkan grid horizontal

    # Tambahkan angka di atas bar
    for i, casual in enumerate(data_tahun["casual"]):
        plt.text(i - width / 2, casual + 5000, f"{casual}", ha="center", fontsize=10, color="black")
    for i, registered in enumerate(data_tahun["registered"]):
        plt.text(i + width / 2, registered + 5000, f"{registered}", ha="center", fontsize=10, color="black")

    st.pyplot(plt)

def data_perbulan():
    from calendar import month_abbr
    from datetime import datetime
    import streamlit as st

    st.write("# Page Data Perbulan")

    st.markdown(
        """
        Kalau di menu ini merupakan kumpulan pengelompokan dengan frequensi perbulan.
        Pada bagian bawah kalian juga bisa menentukan data pada tahun yang mau kalian lihat

        Untuk di halaman ini saya juga menampilkan 3 buat chart yaitu
        - Chart perbandingan Peminjam Casual & Registered Sepeda Perbulan
        - Chart Peminjaman Sepeda Perbulan Berdasarkan Cuaca
        - Chart perbandingan Peminjam Casual & Register pada hari kerja & hari libur

    """
    )


    explode = (0, 0.1) 
    colors=["#024CAA","#EC8305"]

    with st.expander('Report month'):
        this_month = datetime.now().month
        report_year = st.selectbox("", range(2011, 2013))
        month_abbr = month_abbr[1:]
        report_month_str = st.radio("", month_abbr, index=this_month - 1, horizontal=True)
        report_month = month_abbr.index(report_month_str) + 1
        tahun_bulan = f"{report_year}-{report_month}"
        date_object = datetime.strptime(tahun_bulan, "%Y-%m")
        st.write(date_object.strftime("%Y-%m"))

    data_tahun_bulan = data_peminjam_per_satu_bulan(date_object.strftime("%Y-%m"))
    data_cuaca_perbulan = data_cuaca_per_satu_bulan(date_object.strftime("%Y-%m"))
    data_hari_kerja_perbulan = data_hari_kerja(date_object.strftime("%Y-%m"))
    data_hari_libur_perbulan = data_hari_libur(date_object.strftime("%Y-%m"))
    jumlah_data_kerja = jumlah_data(data_hari_kerja_perbulan)
    jumlah_data_libur = jumlah_data(data_hari_libur_perbulan)


    st.subheader('Chart perbandingan Peminjam Casual & Registered Sepeda Perbulan')

    plt.figure(figsize=(12, 6))

    # Plot data Casual
    plt.plot(data_tahun_bulan["day"], data_tahun_bulan["casual"], 
            label='Casual', color=colors[1], marker='o', linestyle='-', linewidth=1.5)

    # Plot data Registered
    plt.plot(data_tahun_bulan["day"], data_tahun_bulan["registered"], 
            label='Registered', color=colors[0], marker='o', linestyle='-', linewidth=1.5)

    # Highlight hari libur dengan marker merah dengan outline
    for idx, row in data_tahun_bulan.iterrows():
        if row["hari libur"] == 0:  # Jika hari libur
            # Casual
            plt.scatter(row["day"], row["casual"], 
                        color='red', edgecolor='black', linewidth=1.5, s=100, zorder=5)
            # Registered
            plt.scatter(row["day"], row["registered"], 
                        color='red', edgecolor='black', linewidth=1.5, s=100, zorder=5)

    # Menambahkan judul, label, dan elemen lainnya
    plt.scatter([], [], color='red', edgecolor='black', linewidth=1.5, s=100, label="Hari Libur")
    plt.title(f"Data Peminjaman Sepeda untuk {tahun_bulan}", fontsize=16)
    plt.xlabel("Hari dalam Bulan", fontsize=12)
    plt.ylabel("Jumlah Peminjam", fontsize=12)
    plt.xticks(fontsize=10)
    plt.yticks(fontsize=10)
    plt.legend(fontsize=12)
    plt.grid(alpha=0.3)

    st.pyplot(plt)

    st.subheader('Chart Peminjaman Sepeda Perbulan Berdasarkan Cuaca')
    # Pilih kolom yang sesuai untuk perhitungan 'cnt' berdasarkan 'sum'
    plt.figure(figsize=(10, 6))

    # Set warna untuk setiap kategori cuaca
    colors = ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728']

    # Bar chart menggunakan kolom 'cnt' yang sudah di-group
    bars = plt.bar(data_cuaca_perbulan["cuaca"], data_cuaca_perbulan[('cnt', 'sum')], color=colors)



    # Menambahkan angka di atas bar
    for bar in bars:
        yval = bar.get_height()
        plt.text(bar.get_x() + bar.get_width() / 2, yval + 50, f'{yval:.0f}', ha='center', va='bottom', fontsize=12, fontweight='bold')

    # Menambahkan label dan judul
    plt.title(f'Jumlah Peminjaman Sepeda pada {tahun_bulan} Berdasarkan Cuaca', fontsize=16, fontweight='bold')
    plt.xlabel('Kondisi Cuaca (Weather Situation)', fontsize=14)
    plt.ylabel('Jumlah Peminjaman (cnt)', fontsize=14)

    # Menambahkan grid untuk sumbu Y
    plt.grid(axis='y', linestyle='--', alpha=0.7)
    st.pyplot(plt)


    st.subheader('Chart perbandingan Peminjam Casual & Register pada hari kerja & hari libur')
    fig, axes = plt.subplots(1, 2, figsize=(14, 7))


    # Pie chart untuk Hari Kerja
    axes[0].pie(data_hari_kerja_perbulan,
                autopct='%1.1f%%',
                colors=["#DA8359", "#A5B68D"],
                explode=explode,
                shadow=True,
                startangle=90,
                wedgeprops={'edgecolor': 'black', 'linewidth': 1.5})
    axes[0].set_title(f'Hari Kerja - {tahun_bulan}', fontsize=14, fontweight='bold')
    axes[0].set_title(f'Peminjaman Sepeda pada Hari Kerja\n(Total: {jumlah_data_kerja:,})', fontsize=14, fontweight='bold')


    # Pie chart untuk Akhir Pekan
    axes[1].pie(data_hari_libur_perbulan,
                autopct='%1.1f%%',
                colors=["#DA8359", "#A5B68D"],
                explode=explode,
                shadow=True,
                startangle=90,
                wedgeprops={'edgecolor': 'black', 'linewidth': 1.5})
    axes[1].set_title(f'Akhir Pekan - {tahun_bulan}', fontsize=14, fontweight='bold')
    axes[1].set_title(f'Peminjaman Sepeda pada Akhir Pekan\n(Total: {jumlah_data_libur:,})', fontsize=14, fontweight='bold')

    plt.legend(labels=['Casual', 'Registered'], 
            loc='upper left', 
            bbox_to_anchor=(1, 1),  # Menempatkan legend di luar chart
            title="Tanggal Peminjaman", fontsize=10, title_fontsize=12)
    st.pyplot(fig)




######################################## Mengature MultiPage ####################################################3    
#saya coba mengikuti https://docs.streamlit.io/get-started/tutorials/create-a-multipage-app
page_names_to_funcs = {
    "Intro": intro,
    "Data Pertahun": data_pertahun,
    "Data Perbulan": data_perbulan
   
}

demo_name = st.sidebar.selectbox("Menu", page_names_to_funcs.keys())
page_names_to_funcs[demo_name]()

#menampilkan caption
st.caption("Punya Faruq")
