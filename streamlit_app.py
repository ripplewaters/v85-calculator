import streamlit as st

# --- Grundinställningar ---
st.set_page_config(page_title="V85 Räkneverktyg", page_icon="🐴", layout="centered")

# --- Anpassad Dark Mode-stil ---
st.markdown(
    """
    <style>
        :root {
            color-scheme: dark;
        }
        body {
            background-color: #0e1117;
            color: #fafafa;
        }
        .stApp {
            background-color: #0e1117;
            color: #fafafa;
        }
        h1, h2, h3, h4, h5 {
            color: #ffffff;
        }
        .stNumberInput label {
            font-weight: 600;
            color: #cfcfcf;
        }
        .stMultiSelect label {
            font-weight: 600;
            color: #cfcfcf;
        }
        div[data-testid="stMetricValue"] {
            color: #f5f5f5;
        }
    </style>
    """,
    unsafe_allow_html=True
)

# --- Titel ---
st.title("🐴 V85 Räkneverktyg")

st.markdown("""
Det här verktyget hjälper dig att räkna ut hur många rader du får med 8, 7, 6 och 5 rätt
utifrån ditt matematiska system på **V85**.

👉 Fyll i hur många hästar du spelat i varje avdelning  
👉 Markera vilka avdelningar som var **rätt**  
👉 Klicka **Beräkna** för att se resultatet
""")

st.divider()

# --- Input: antal hästar per avdelning ---
antal = [st.number_input(f"**Antal hästar – V85-{i+1}**", min_value=1, max_value=15, value=1, step=1) for i in range(8)]

# --- Välj vilka avdelningar som var rätt ---
ratt_lopp = st.multiselect("Vilka avdelningar var rätt?", [f"V85-{i+1}" for i in range(8)], default=[f"V85-{i+1}" for i in range(8)])

st.divider()

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
        rubrik = "🎯 Du hade 8 rätt"
    elif len(fel_index) == 1:  # 7 rätt
        fel = antal[fel_index[0]]
        s = sum(ratt_tal)
        q = sum(x**2 for x in ratt_tal)
        a8 = 0
        a7 = fel
        a6 = s * fel
        a5 = ((s**2 - q)//2) * fel
        rubrik = "✅ Du hade 7 rätt"
    elif len(fel_index) == 2:  # 6 rätt
        fel = [antal[i] for i in fel_index]
        s = sum(ratt_tal)
        a8, a7 = 0, 0
        a6 = fel[0] * fel[1]
        a5 = s * a6
        rubrik = "🟡 Du hade 6 rätt"
    elif len(fel_index) == 3:  # 5 rätt
        fel = [antal[i] for i in fel_index]
        a8, a7, a6 = 0, 0, 0
        a5 = fel[0] * fel[1] * fel[2]
        rubrik = "🟠 Du hade 5 rätt"
    else:
        rubrik = "⚪ För få rätt för att beräkna"
        a8 = a7 = a6 = a5 = 0

    return rubrik, a8, a7, a6, a5

# --- Beräkna och visa resultat ---
if st.button("🔢 Beräkna"):
    rubrik, a8, a7, a6, a5 = rakna_vinster(antal, ratt_lopp)
    st.subheader(rubrik)
    st.markdown("---")
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("8 rätt", f"{a8:,}")
    col2.metric("7 rätt", f"{a7:,}")
    col3.metric("6 rätt", f"{a6:,}")
    col4.metric("5 rätt", f"{a5:,}")

    st.markdown("---")
    st.caption("Beräkningen följer ATG:s officiella rättningsmall för matematiska system (V85).")
