import streamlit as st

# --- Grundinställningar ---
st.set_page_config(page_title="V85 Räkneverktyg", page_icon="🐴", layout="centered")

# --- Anpassad CSS ---
st.markdown("""
    <style>
        /* === Grundfärger och bakgrund === */
        .stApp {
            background-color: #b00017 !important;
            color: #000000 !important;
        }

        /* === Centrering och maxbredd === */
        .block-container {
            max-width: 800px !important;
            padding-top: 2rem;
            padding-bottom: 4rem;
        }

        /* === Rubriker === */
        h1, h2, h3 {
            color: white !important;
            text-align: center;
            font-family: 'Arial Black', sans-serif;
            letter-spacing: 0.5px;
        }

        /* === Kort-stil (vit box med skugga) === */
        .card {
            background-color: white;
            color: black;
            border-radius: 10px;
            padding: 20px 25px;
            margin-bottom: 20px;
            box-shadow: 0px 4px 10px rgba(0,0,0,0.2);
        }

        /* === Inputs === */
        div[data-baseweb="input"] > div {
            background-color: #ffffff !important;
            color: #000000 !important;
            border-radius: 6px;
        }
        input {
            color: #000000 !important;
            font-weight: 600;
        }

        /* === Multiselect === */
        div[data-baseweb="select"] {
            background-color: #ffffff !important;
            color: #000000 !important;
            border-radius: 6px;
        }

        /* === Knappar === */
        .stButton button {
            background-color: #ffffff !important;
            color: #000000 !important;
            border-radius: 6px;
            border: none;
            font-weight: 700;
            width: 100%;
            padding: 0.6rem;
            box-shadow: 0px 3px 8px rgba(0,0,0,0.2);
        }
        .stButton button:hover {
            background-color: #f5f5f5 !important;
        }

        /* === Resultatrutor === */
        .metric-card {
            background-color: white;
            color: black;
            border-radius: 10px;
            padding: 20px;
            text-align: center;
            box-shadow: 0px 3px 10px rgba(0,0,0,0.25);
        }
        .metric-label {
            font-size: 16px;
            font-weight: bold;
        }
        .metric-value {
            font-size: 24px;
            font-weight: 900;
            color: #000000;
        }

        .stCaption {
            color: #ffffff !important;
            text-align: center;
        }
    </style>
""", unsafe_allow_html=True)

# --- Titel ---
st.markdown("<h1>🐴 V85 RÄKNEVERKTYG</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align:center;color:#f9f9f9;'>Beräkna hur många rader ditt matematiska system genererar för 8, 7, 6 och 5 rätt.</p>", unsafe_allow_html=True)
st.markdown("<br>", unsafe_allow_html=True)

# --- Inmatning i ett kort ---
with st.container():
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.subheader("🎯 Ange antal hästar i varje avdelning")
    antal = [st.number_input(f"Antal hästar – V85-{i+1}", min_value=1, max_value=15, value=1, step=1) for i in range(8)]

    st.subheader("✅ Markera vilka avdelningar som var rätt")
    ratt_lopp = st.multiselect("Välj rätta avdelningar", [f"V85-{i+1}" for i in range(8)], default=[f"V85-{i+1}" for i in range(8)])
    st.markdown("</div>", unsafe_allow_html=True)

# --- Funktion för att räkna vinster enligt ATG-logik ---
def rakna_vinster(antal, ratt_index):
    n = len(antal)
    markeringar = [antal[i] - 1 for i in range(n)]
    fel_index = [i for i in range(n) if f"V85-{i+1}" not in ratt_index]
    ratt_tal = [markeringar[i] for i in range(n) if i not in fel_index]

    if len(fel_index) == 0:  # 8 rätt
        s = sum(markeringar)
        q = sum(x**2 for x in markeringar)
        c = sum(x**3 for x in markeringar)
        a8, a7, a6, a5 = 1, s, (s**2 - q)//2, (s**3 - 3*s*q + 2*c)//6
        rubrik = "Du hade 8 rätt"
    elif len(fel_index) == 1:  # 7 rätt
        fel = antal[fel_index[0]]
        s = sum(ratt_tal)
        q = sum(x**2 for x in ratt_tal)
        a8 = 0
        a7 = fel
        a6 = s * fel
        a5 = ((s**2 - q)//2) * fel
        rubrik = "Du hade 7 rätt"
    elif len(fel_index) == 2:  # 6 rätt
        fel = [antal[i] for i in fel_index]
        s = sum(ratt_tal)
        a8, a7 = 0, 0
        a6 = fel[0] * fel[1]
        a5 = s * a6
        rubrik = "Du hade 6 rätt"
    elif len(fel_index) == 3:  # 5 rätt
        fel = [antal[i] for i in fel_index]
        a8, a7, a6 = 0, 0, 0
        a5 = fel[0] * fel[1] * fel[2]
        rubrik = "Du hade 5 rätt"
    else:
        rubrik = "För få rätt för att beräkna"
        a8 = a7 = a6 = a5 = 0

    return rubrik, a8, a7, a6, a5

# --- Beräkna och visa resultat ---
if st.button("BERÄKNA RESULTAT"):
    rubrik, a8, a7, a6, a5 = rakna_vinster(antal, ratt_lopp)
    st.markdown("<br>", unsafe_allow_html=True)
    st.subheader(rubrik)

    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.markdown("<div class='metric-card'><div class='metric-label'>8 rätt</div><div class='metric-value'>" + f"{a8:,}" + "</div></div>", unsafe_allow_html=True)
    with col2:
        st.markdown("<div class='metric-card'><div class='metric-label'>7 rätt</div><div class='metric-value'>" + f"{a7:,}" + "</div></div>", unsafe_allow_html=True)
    with col3:
        st.markdown("<div class='metric-card'><div class='metric-label'>6 rätt</div><div class='metric-value'>" + f"{a6:,}" + "</div></div>", unsafe_allow_html=True)
    with col4:
        st.markdown("<div class='metric-card'><div class='metric-label'>5 rätt</div><div class='metric-value'>" + f"{a5:,}" + "</div></div>", unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    st.caption("Beräkningen följer ATG:s officiella rättningsmall för matematiska system (V85).")
