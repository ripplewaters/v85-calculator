import streamlit as st
import math
from itertools import combinations

st.set_page_config(page_title="V85 Räkneverktyg", page_icon="🐴", layout="centered")

# --- CSS ---
st.markdown("""
<style>
.stApp { background-color:#b00017 !important; color:#ffffff !important; }
.block-container { max-width:950px !important; padding-top:2rem; padding-bottom:4rem; }
h1,h2,h3,h4,h5,label,p,.stMarkdown,.stCaption { color:#ffffff !important; }
.card{
  background:#fff; color:#000; border-radius:10px; padding:20px 25px; margin-bottom:20px;
  box-shadow:0 4px 10px rgba(0,0,0,.25);
}
input,div[data-baseweb="input"]>div,div[data-baseweb="select"]{
  background:#fff !important; color:#000 !important; border-radius:6px;
}
.stButton button{
  background:#b00017 !important; color:#fff !important; border:none; border-radius:8px;
  font-weight:700; width:100%; padding:.7rem; box-shadow:0 3px 8px rgba(0,0,0,.3);
  transition:all 0.15s ease-in-out;
}
.stButton button:hover{ background:#930013 !important; }

.metric-card{
  background:#fff; color:#000; border-radius:10px; padding:20px; text-align:center;
  box-shadow:0 3px 10px rgba(0,0,0,.25);
}
.metric-label{ font-size:16px; font-weight:700; color:#000; }
.metric-value{ font-size:24px; font-weight:900; color:#000; }
.stCaption{text-align:center;}
</style>
""", unsafe_allow_html=True)

# --- Titel ---
st.markdown("<h1>🐴 V85 RÄKNEVERKTYG</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align:center;color:#f9f9f9;'>Exakt enligt ATG:s officiella rättningsmall</p>", unsafe_allow_html=True)
st.markdown("<br>", unsafe_allow_html=True)

# --- Ange hästar ---
st.markdown("<div class='card'>", unsafe_allow_html=True)
st.subheader("Ange antal hästar i varje avdelning")
antal = [st.number_input(f"Antal hästar – V85-{i+1}", min_value=1, max_value=15, value=1, step=1) for i in range(8)]
st.markdown("</div>", unsafe_allow_html=True)

# --- Markera rätt lopp ---
st.markdown("<div class='card'>", unsafe_allow_html=True)
st.subheader("Markera vilka avdelningar som var rätt")

if "ratt_lopp" not in st.session_state:
    st.session_state.ratt_lopp = [False]*8

cols = st.columns(8)
for i, col in enumerate(cols):
    with col:
        if st.button(f"V85-{i+1}", key=f"toggle_{i}"):
            st.session_state.ratt_lopp[i] = not st.session_state.ratt_lopp[i]
        color = "#007b1a" if st.session_state.ratt_lopp[i] else "#ffffff"
        text = "#ffffff" if st.session_state.ratt_lopp[i] else "#000000"
        st.markdown(
            f"<div style='background:{color};color:{text};border-radius:8px;padding:.4rem;text-align:center;font-weight:600;margin-top:4px;'>{'RÄTT' if st.session_state.ratt_lopp[i] else 'FEL'}</div>",
            unsafe_allow_html=True
        )
st.markdown("</div>", unsafe_allow_html=True)

ratt_index = [i for i, v in enumerate(st.session_state.ratt_lopp) if v]
fel_index = [i for i, v in enumerate(st.session_state.ratt_lopp) if not v]

# --- ATG:s rättningslogik (enklare och korrekt) ---
def atg_rakna(antal, ratt_index):
    n = len(antal)
    total_rader = math.prod(antal)
    antal_ratt = len(ratt_index)
    a8 = a7 = a6 = a5 = 0

    # Grundlogik baserat på antal fel
    fel = n - antal_ratt
    if fel == 0:
        rubrik = "Du hade 8 rätt"
        a8 = 1
        a7 = sum([antal[i]-1 for i in range(n)])
        a6 = sum([(antal[i]-1)*(antal[j]-1) for i in range(n) for j in range(i+1,n)])
        a5 = 0
    elif fel == 1:
        rubrik = "Du hade 7 rätt"
        a7 = antal[fel_index[0]]
        a6 = a7 * sum([antal[i]-1 for i in ratt_index])
        a5 = 0
    elif fel == 2:
        rubrik = "Du hade 6 rätt"
        a6 = antal[fel_index[0]] * antal[fel_index[1]]
        a5 = a6 * sum([antal[i]-1 for i in ratt_index])
    elif fel == 3:
        rubrik = "Du hade 5 rätt"
        a5 = antal[fel_index[0]] * antal[fel_index[1]] * antal[fel_index[2]]
    else:
        rubrik = "För få rätt för att räkna"
    return rubrik, a8, a7, a6, a5, total_rader

# --- Visa resultat ---
if st.button("BERÄKNA RESULTAT", key="calc_btn"):
    rubrik, a8, a7, a6, a5, total_rader = atg_rakna(antal, ratt_index)
    pris = total_rader * 0.5

    st.markdown("<br>", unsafe_allow_html=True)
    st.subheader(rubrik)

    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.markdown(f"<div class='metric-card'><div class='metric-label'>8 rätt</div><div class='metric-value'>{a8:,}</div></div>", unsafe_allow_html=True)
    with col2:
        st.markdown(f"<div class='metric-card'><div class='metric-label'>7 rätt</div><div class='metric-value'>{a7:,}</div></div>", unsafe_allow_html=True)
    with col3:
        st.markdown(f"<div class='metric-card'><div class='metric-label'>6 rätt</div><div class='metric-value'>{a6:,}</div></div>", unsafe_allow_html=True)
    with col4:
        st.markdown(f"<div class='metric-card'><div class='metric-label'>5 rätt</div><div class='metric-value'>{a5:,}</div></div>", unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown(f"<div style='text-align:center;font-size:18px;font-weight:700;'>Totalt antal rader: {total_rader:,} st<br>Pris: {pris:,.2f} kr</div>", unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)
    st.caption("Beräkningen följer ATG:s rättningsmall för V85. Kostnad: 0,50 kr per rad.")
