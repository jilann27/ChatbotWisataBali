from dotenv import load_dotenv
load_dotenv()

import streamlit as st
from helpers.llm_helper import chat

# =========================
# KONFIGURASI HALAMAN
# =========================
st.set_page_config(
    page_title="Wisata Bali",
    initial_sidebar_state="collapsed",
    layout="wide"
)

# =========================
# SESSION STATE
# =========================
if "page" not in st.session_state:
    st.session_state.page = "home"

if "messages" not in st.session_state:
    st.session_state.messages = []

if "quick_prompt" not in st.session_state:
    st.session_state.quick_prompt = None

# =========================
# KONFIGURASI MODEL
# =========================
MODEL_DEFAULT = "openai/gpt-4o-mini"
TEMPERATURE_DEFAULT = 0.7
MAX_TOKEN_DEFAULT = 800

# =========================
# HOME / COVER
# =========================
if st.session_state.page == "home":

    st.markdown("""
    <style>
    .block-container {
        padding-top: 8rem !important;
        padding-bottom: 3rem;
        max-width: 100% !important;
    }
    .hero-title {
        font-size: 72px;
        font-weight: 800;
        line-height: 1.2;
        margin-bottom: 30px;
        background: linear-gradient(135deg, #e85d04 0%, #dc2f02 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }
    .hero-subtitle {
        font-size: 24px;
        color: #6b7280;
        line-height: 1.6;
        margin-bottom: 30px;
    }
    .info-box {
        background: #f9fafb;
        border-radius: 8px;
        padding: 15px;
        margin-bottom: 12px;
        font-size: 15px;
        color: #4b5563;
    }
    </style>
    """, unsafe_allow_html=True)

    col_left, col_right = st.columns([1.2, 1], gap="large")

    with col_left:
        st.markdown("""
        <div class="hero-title">
            Jelajahi Keindahan Bali dengan Panduan AI Pribadi Anda
        </div>
        """, unsafe_allow_html=True)

        st.markdown("""
        <div class="hero-subtitle">
            Dapatkan rekomendasi wisata Bali yang dipersonalisasi sesuai minat, waktu, dan budget Anda dalam sekejap
        </div>
        """, unsafe_allow_html=True)

    with col_right:
        st.markdown("### Halo! 👋")
        st.markdown("*Apa yang bisa saya bantu hari ini?*")

        c1, c2 = st.columns(2)
        with c1:
            st.markdown('<div class="info-box">✈️ Rekomendasi Wisata</div>', unsafe_allow_html=True)
            st.markdown('<div class="info-box">❓ Tips Perjalanan</div>', unsafe_allow_html=True)
        with c2:
            st.markdown('<div class="info-box">🗺️ Itinerary Lengkap</div>', unsafe_allow_html=True)
            st.markdown('<div class="info-box">💰 Budget Planning</div>', unsafe_allow_html=True)

        if st.button("🚀 Mulai Jelajah Bali", use_container_width=True, type="primary"):
            st.session_state.page = "chat"
            st.rerun()

    st.stop()  # ⬅️ STOP CUMA DI HOME

# =========================
# CHAT PAGE
# =========================
st.title("Wisata Bali 🏝️")
st.caption("Yuk temukan rekomendasi wisata Bali sesuai minat, waktu, dan budget kamu!")

# =========================
# SIDEBAR
# =========================
with st.sidebar:
    if st.button("⬅️ Kembali ke Beranda"):
        st.session_state.page = "home"
        st.rerun()

    st.markdown("## Preferensi Wisata 🌴")

    minat = st.multiselect("Minat Wisata", ["Pantai", "Budaya", "Alam"])
    durasi = st.selectbox("Durasi Liburan", ["1 Hari", "2 Hari", "3 Hari"])
    budget = st.selectbox("Budget", ["Murah", "Sedang", "Bebas"])

    if st.button("🔍 Cari Rekomendasi"):
        st.session_state.quick_prompt = f"""
Buatkan rekomendasi wisata Bali:
- Minat: {', '.join(minat) if minat else 'Bebas'}
- Durasi: {durasi}
- Budget: {budget}
"""

    st.markdown("---")
    st.markdown("### Rekomendasi Cepat ⚡")

    if st.button("🏖️ Pantai Populer"):
        st.session_state.quick_prompt = "Rekomendasikan pantai populer di Bali."

    if st.button("🏛️ Wisata Budaya 1 Hari"):
        st.session_state.quick_prompt = "Buatkan wisata budaya Bali 1 hari."

    if st.button("🌿 Wisata Alam Murah"):
        st.session_state.quick_prompt = "Wisata alam Bali budget murah."

# =========================
# RIWAYAT CHAT
# =========================
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# =========================
# INPUT CHAT
# =========================
user_prompt = st.chat_input("Tanyakan seputar wisata Bali...")

if st.session_state.quick_prompt:
    user_prompt = st.session_state.quick_prompt
    st.session_state.quick_prompt = None

# =========================
# PROSES CHAT
# =========================
if user_prompt:
    st.session_state.messages.append({"role": "user", "content": user_prompt})

    with st.chat_message("user"):
        st.markdown(user_prompt)

    response = chat(
        user_prompt,
        model=MODEL_DEFAULT,
        max_tokens=MAX_TOKEN_DEFAULT,
        temp=TEMPERATURE_DEFAULT
    )

    with st.chat_message("assistant"):
        st.markdown(response)

    st.session_state.messages.append({"role": "assistant", "content": response})
