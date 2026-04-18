import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go

st.set_page_config(
    page_title="SPK Pemilihan Laptop - TOPSIS",
    page_icon="💻",
    layout="wide"
)

# =========================================================
# CSS
# =========================================================
st.markdown("""
<style>
    .main { background-color: #f8f9fa; }
    .stMetric { background-color: white; padding: 1rem; border-radius: 8px; box-shadow: 0 1px 4px rgba(0,0,0,0.08); }
    .rank-card { background: white; border-radius: 10px; padding: 1rem 1.2rem; margin-bottom: 0.5rem;
                 box-shadow: 0 1px 4px rgba(0,0,0,0.08); border-left: 4px solid #4f8ef7; }
    .rank-1 { border-left-color: #f5a623; }
    .rank-2 { border-left-color: #9b9b9b; }
    .rank-3 { border-left-color: #c47c2f; }
    h1 { color: #1a1a2e; }
</style>
""", unsafe_allow_html=True)

# =========================================================
# TOPSIS ENGINE
# =========================================================
def topsis(df, criteria_cols, weights, benefit_flags):
    """
    df            : DataFrame
    criteria_cols : list of column names
    weights       : list of floats (harus sum = 1)
    benefit_flags : list of bool (True = benefit, False = cost)
    Returns DataFrame dengan kolom tambahan D+, D-, C_i, Rank
    """
    X = df[criteria_cols].values.astype(float)

    # Step 1: Normalisasi
    norm = np.sqrt((X ** 2).sum(axis=0))
    R = X / norm

    # Step 2: Bobot
    W = np.array(weights)
    V = R * W

    # Step 3: Solusi ideal
    A_pos = np.where(benefit_flags, V.max(axis=0), V.min(axis=0))
    A_neg = np.where(benefit_flags, V.min(axis=0), V.max(axis=0))

    # Step 4: Jarak
    D_pos = np.sqrt(((V - A_pos) ** 2).sum(axis=1))
    D_neg = np.sqrt(((V - A_neg) ** 2).sum(axis=1))

    # Step 5: Nilai preferensi
    C = D_neg / (D_pos + D_neg)

    result = df.copy()
    result["D+"] = D_pos
    result["D-"] = D_neg
    result["Nilai Preferensi (Ci)"] = C
    result["Rank"] = result["Nilai Preferensi (Ci)"].rank(ascending=False).astype(int)
    result = result.sort_values("Rank")
    return result

# =========================================================
# LOAD DATA
# =========================================================
@st.cache_data
def load_data():
    df = pd.read_csv("laptop.csv", index_col=0)
    df = df.dropna(subset=["price", "ram(GB)", "ssd(GB)", "spec_score", "no_of_cores"])
    df = df[df["price"] > 0]
    df = df.reset_index(drop=True)
    return df

df = load_data()

# =========================================================
# SIDEBAR — BOBOT & FILTER
# =========================================================
with st.sidebar:
    st.image("https://img.icons8.com/fluency/96/laptop.png", width=60)
    st.title("⚙️ Pengaturan")

    st.markdown("### 🎯 Bobot Kriteria")
    st.caption("Total bobot harus = 1.0")

    w1 = st.slider("💰 Harga (Cost)", 0.0, 1.0, 0.30, 0.05)
    w2 = st.slider("🧠 RAM (GB)", 0.0, 1.0, 0.25, 0.05)
    w3 = st.slider("💾 SSD (GB)", 0.0, 1.0, 0.20, 0.05)
    w4 = st.slider("⚡ Spec Score", 0.0, 1.0, 0.15, 0.05)
    w5 = st.slider("🔢 Jumlah Core", 0.0, 1.0, 0.10, 0.05)

    total_w = round(w1 + w2 + w3 + w4 + w5, 2)
    if abs(total_w - 1.0) > 0.01:
        st.error(f"⚠️ Total bobot = {total_w} (harus 1.0)")
        valid_weights = False
    else:
        st.success(f"✅ Total bobot = {total_w}")
        valid_weights = True

    st.markdown("---")
    st.markdown("### 🔍 Filter Dataset")
    brands = ["Semua"] + sorted(df["brand"].dropna().unique().tolist())
    selected_brand = st.selectbox("Merek", brands)

    price_min, price_max = int(df["price"].min()), int(df["price"].max())
    price_range = st.slider("Rentang Harga (₹)", price_min, price_max,
                             (price_min, price_max), step=1000)

    top_n = st.slider("Tampilkan Top-N Laptop", 5, 50, 10)

# =========================================================
# FILTER DATA
# =========================================================
df_filtered = df.copy()
if selected_brand != "Semua":
    df_filtered = df_filtered[df_filtered["brand"] == selected_brand]
df_filtered = df_filtered[
    (df_filtered["price"] >= price_range[0]) &
    (df_filtered["price"] <= price_range[1])
]

# =========================================================
# HEADER
# =========================================================
st.title("💻 Sistem Pendukung Keputusan Pemilihan Laptop")
st.markdown("**Metode:** *Technique for Order Preference by Similarity to Ideal Solution* (TOPSIS)")
st.markdown("---")

# Metrics row
col1, col2, col3, col4 = st.columns(4)
col1.metric("Total Laptop", f"{len(df_filtered):,}")
col2.metric("Merek Tersedia", df_filtered["brand"].nunique())
col3.metric("Harga Terendah", f"₹{df_filtered['price'].min():,}")
col4.metric("Harga Tertinggi", f"₹{df_filtered['price'].max():,}")

st.markdown("---")

# =========================================================
# RUN TOPSIS
# =========================================================
if not valid_weights:
    st.warning("Sesuaikan bobot di sidebar agar totalnya = 1.0 sebelum menjalankan analisis.")
    st.stop()

if len(df_filtered) < 2:
    st.warning("Data terlalu sedikit. Perluas filter.")
    st.stop()

weights = [w1, w2, w3, w4, w5]
criteria = ["price", "ram(GB)", "ssd(GB)", "spec_score", "no_of_cores"]
benefit  = [False, True, True, True, True]  # price = cost

result = topsis(df_filtered, criteria, weights, benefit)
top_result = result.head(top_n)

# =========================================================
# TAB LAYOUT
# =========================================================
tab1, tab2, tab3, tab4 = st.tabs(["🏆 Ranking", "📊 Visualisasi", "📋 Data Lengkap", "🧮 Detail Perhitungan"])

# ----------------------------------------------------------
# TAB 1: RANKING
# ----------------------------------------------------------
with tab1:
    st.subheader(f"🏆 Top {top_n} Laptop Terbaik")

    for i, row in top_result.iterrows():
        rank = int(row["Rank"])
        medal = {1: "🥇", 2: "🥈", 3: "🥉"}.get(rank, f"#{rank}")
        css_class = {1: "rank-1", 2: "rank-2", 3: "rank-3"}.get(rank, "rank-card")

        ci_bar = "█" * int(row["Nilai Preferensi (Ci)"] * 20)
        ci_pct = f"{row['Nilai Preferensi (Ci)']:.4f}"

        st.markdown(f"""
        <div class="{css_class} rank-card">
            <b>{medal} {row['model_name']}</b> &nbsp;
            <span style="color:#888; font-size:0.85em">{row['brand']}</span><br>
            <span style="font-family:monospace; color:#4f8ef7">{ci_bar}</span>
            &nbsp;<b>Ci = {ci_pct}</b><br>
            <small>
                💰 ₹{int(row['price']):,} &nbsp;|&nbsp;
                🧠 RAM {int(row['ram(GB)'])} GB &nbsp;|&nbsp;
                💾 SSD {int(row['ssd(GB)'])} GB &nbsp;|&nbsp;
                ⚡ Score {int(row['spec_score'])} &nbsp;|&nbsp;
                🔢 {int(row['no_of_cores'])} core
            </small>
        </div>
        """, unsafe_allow_html=True)

# ----------------------------------------------------------
# TAB 2: VISUALISASI
# ----------------------------------------------------------
with tab2:
    col_a, col_b = st.columns(2)

    with col_a:
        st.subheader("Nilai Preferensi Top Laptop")
        fig_bar = px.bar(
            top_result, x="Nilai Preferensi (Ci)", y="model_name",
            orientation="h", color="Nilai Preferensi (Ci)",
            color_continuous_scale="Blues",
            labels={"model_name": "Laptop", "Nilai Preferensi (Ci)": "Ci"},
            height=400
        )
        fig_bar.update_layout(yaxis={"categoryorder": "total ascending"},
                               showlegend=False, coloraxis_showscale=False)
        st.plotly_chart(fig_bar, use_container_width=True)

    with col_b:
        st.subheader("Distribusi Merek (Dataset Terfilter)")
        brand_count = df_filtered["brand"].value_counts().reset_index()
        brand_count.columns = ["Merek", "Jumlah"]
        fig_pie = px.pie(brand_count, values="Jumlah", names="Merek",
                          color_discrete_sequence=px.colors.qualitative.Pastel,
                          height=400)
        st.plotly_chart(fig_pie, use_container_width=True)

    st.subheader("Scatter: Harga vs Spec Score (warna = Nilai Ci)")
    top50 = result.head(50)
    fig_scatter = px.scatter(
        top50, x="price", y="spec_score",
        color="Nilai Preferensi (Ci)", size="ram(GB)",
        hover_name="model_name",
        color_continuous_scale="RdYlGn",
        labels={"price": "Harga (₹)", "spec_score": "Spec Score"},
        height=400
    )
    st.plotly_chart(fig_scatter, use_container_width=True)

# ----------------------------------------------------------
# TAB 3: DATA LENGKAP
# ----------------------------------------------------------
with tab3:
    st.subheader("Tabel Hasil Lengkap")
    display_cols = ["Rank", "model_name", "brand", "price", "ram(GB)",
                    "ssd(GB)", "spec_score", "no_of_cores", "Nilai Preferensi (Ci)"]
    st.dataframe(
        result[display_cols].rename(columns={
            "model_name": "Nama Laptop", "brand": "Merek",
            "price": "Harga (₹)", "ram(GB)": "RAM (GB)",
            "ssd(GB)": "SSD (GB)", "spec_score": "Spec Score",
            "no_of_cores": "Cores"
        }),
        use_container_width=True, height=500
    )

    csv_out = result[display_cols].to_csv(index=False).encode("utf-8")
    st.download_button("⬇️ Download Hasil (CSV)", csv_out, "hasil_topsis.csv", "text/csv")

# ----------------------------------------------------------
# TAB 4: DETAIL PERHITUNGAN
# ----------------------------------------------------------
with tab4:
    st.subheader("🧮 Transparansi Perhitungan TOPSIS")

    st.markdown("#### 1. Matriks Keputusan Awal (5 data pertama)")
    st.dataframe(df_filtered[criteria].head(5).rename(columns={
        "price": "Harga", "ram(GB)": "RAM", "ssd(GB)": "SSD",
        "spec_score": "Spec Score", "no_of_cores": "Cores"
    }), use_container_width=True)

    # Normalisasi manual untuk tampilan
    X = df_filtered[criteria].values.astype(float)
    norm = np.sqrt((X ** 2).sum(axis=0))
    R = X / norm
    W = np.array(weights)
    V = R * W
    A_pos = np.where(benefit, V.max(axis=0), V.min(axis=0))
    A_neg = np.where(benefit, V.min(axis=0), V.max(axis=0))

    st.markdown("#### 2. Solusi Ideal Positif (A+) dan Negatif (A-)")
    ideal_df = pd.DataFrame({
        "Kriteria": ["Harga", "RAM", "SSD", "Spec Score", "Cores"],
        "Tipe": ["Cost", "Benefit", "Benefit", "Benefit", "Benefit"],
        "Bobot": weights,
        "A+ (Ideal Positif)": A_pos.round(6),
        "A- (Ideal Negatif)": A_neg.round(6),
    })
    st.dataframe(ideal_df, use_container_width=True)

    st.markdown("#### 3. Bobot yang Digunakan")
    bobot_df = pd.DataFrame({
        "Kriteria": ["Harga", "RAM", "SSD", "Spec Score", "Cores"],
        "Bobot": weights,
        "Persentase": [f"{w*100:.0f}%" for w in weights]
    })
    fig_bobot = px.pie(bobot_df, values="Bobot", names="Kriteria",
                        title="Distribusi Bobot Kriteria",
                        color_discrete_sequence=px.colors.qualitative.Set2)
    st.plotly_chart(fig_bobot, use_container_width=True)

    st.markdown("---")
    st.caption("Sistem ini dikembangkan untuk keperluan akademik | TOPSIS by Hwang & Yoon (1981)")
