# 💻 SPK Pemilihan Laptop — TOPSIS

> *Bingung milih laptop? Biar matematika yang mutusin.*

Sistem Pendukung Keputusan berbasis metode **TOPSIS** untuk membantu mahasiswa memilih laptop terbaik sesuai kebutuhan dan budget — dibangun dengan Python, Streamlit, dan sedikit keberanian akademik.

---

## ✨ Fitur

- 🎯 **Ranking otomatis** dari 1.000+ laptop menggunakan algoritma TOPSIS
- ⚖️ **Bobot kriteria bisa diubah** — prioritas harga? RAM? Tinggal geser slider
- 🔍 **Filter merek & rentang harga** secara interaktif
- 📊 **Visualisasi lengkap** — bar chart, scatter plot, pie chart distribusi merek
- 🧮 **Tab perhitungan transparan** — bisa lihat matriks normalisasi, A+, A-, sampai nilai Ci
- ⬇️ **Export hasil ke CSV** — buat laporan, buat bukti, buat pamer

---

## 🚀 Cara Pakai

### 1. Clone / download project ini

```bash
git clone https://github.com/username/spk-topsis-laptop.git
cd spk-topsis-laptop
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Jalankan aplikasi

```bash
streamlit run app.py
```

Buka browser, pergi ke `http://localhost:8501`, dan selamat memilih laptop! 🎉

---

## 📁 Struktur Project

```
spk-topsis-laptop/
├── app.py              # Aplikasi utama Streamlit
├── laptop.csv          # Dataset laptop (1.014 entri)
├── requirements.txt    # Dependencies
├── paper/
│   └── spk_topsis_laptop.tex   # Draft paper semnas (LaTeX)
└── README.md
```

---

## 🧮 Tentang Metode TOPSIS

**TOPSIS** *(Technique for Order Preference by Similarity to Ideal Solution)* adalah metode MCDM yang dikembangkan Hwang & Yoon (1981). Prinsipnya simpel tapi powerful:

> Laptop terbaik = yang **paling dekat** ke laptop ideal sempurna, sekaligus **paling jauh** dari laptop terburuk.

Langkah-langkahnya:

```
1. Normalisasi matriks keputusan
2. Kalikan dengan bobot kriteria
3. Tentukan Solusi Ideal Positif (A+) dan Negatif (A-)
4. Hitung jarak tiap laptop ke A+ dan A-
5. Hitung nilai preferensi Ci = D⁻ / (D⁺ + D⁻)
6. Ranking berdasarkan Ci — makin tinggi makin bagus ✅
```

---

## 📊 Kriteria yang Digunakan

| # | Kriteria | Tipe | Bobot Default |
|---|----------|------|:---:|
| C1 | Harga (₹) | Cost ↓ | 30% |
| C2 | RAM (GB) | Benefit ↑ | 25% |
| C3 | SSD (GB) | Benefit ↑ | 20% |
| C4 | Spec Score | Benefit ↑ | 15% |
| C5 | Jumlah Core | Benefit ↑ | 10% |

> Bobot bisa diubah langsung di sidebar aplikasi sesuai prioritas lo!

---

## 🏆 Top 5 Hasil (Bobot Default)

| Rank | Laptop | Nilai Ci |
|:----:|--------|:--------:|
| 🥇 | AGB Octev VR-1818 Gaming Laptop | 0.5366 |
| 🥈 | Asus ROG Zephyrus Duo 16 GX650RMZ | 0.5142 |
| 🥉 | MSI Creator Z16P B12UKST-209IN | 0.5125 |
| 4 | Asus ROG Strix Scar 17 SE G733CX | 0.4927 |
| 5 | Acer Predator Helios 500 Ph517-52 | 0.4901 |

---

## 📦 Requirements

```
streamlit
pandas
numpy
plotly
```

Atau langsung:

```bash
pip install streamlit pandas numpy plotly
```

---

## 👥 Tim

Dibuat dengan ☕ dan deadline mepet oleh:

| Nama | Role |
|------|------|
| [Nama Anggota 1] | — |
| Farrel [Nama Lengkap] | Frontend |
| Faridh [Nama Lengkap] | Backend |
| Jawwad Fatih Al-Mumtaz | AI/ML |

Program Studi Teknik Komputer — Universitas Darussalam Gontor, Ponorogo

---

## 📄 Publikasi

Paper ini disubmit ke **[Nama Semnas]** sebagai output UAS mata kuliah Sistem Pendukung Keputusan.

> *"Karena milih laptop itu harusnya pakai data, bukan feeling."*

---

<p align="center">Made with 💙 | TOPSIS © Hwang & Yoon, 1981</p>
