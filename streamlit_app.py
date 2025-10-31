import streamlit as st

# --- Grundinställningar ---
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
  font-weight:700; width:100%; padding:.6rem .4rem; box-shadow:0 3px 8px rgba(0,0,0,.3);
  transition:all 0.15s ease-in-out;
}
.stButton button:hover{ background:#930013 !important; }

/* Metrickort */
.metric-card{
  background:#fff; color:#000; border-radius:10px; padding:20px; text-align:center;
  box-shadow:0 3px 10px rgba(0,0,0,.25);
}
.metric-label{ font-size:16px; font-weight:700; color:#000; }
.metric-value{ font-size:24px; font-weight:900; color:#000; }
.stCaption{text-align:center;}

/* --- Stil för valda toggles per nyckel --- */
:root {
  --selected-bg: #007b1a;
  --selected-fg: #ffffff;
}
[data-testid="stButton"][data-key="toggle_0"] button.selected,
[data-testid="stButton"][data-key="toggle_1"] button.selected,
[data-testid="stButton"][data-key="toggle_2"] button.selected,
[data-testid="stButton"][data-key="toggle_3"] button.selected,
[data-testid="stButton"][data-key="toggle_4"] button.selected,
[data-testid="stButton"][data-key="toggle_5"] button.selected,
[data-testid="stButton"][data-key="toggle_6"] button.selected,
[data-testid="stButton"][data-key="toggle_7"] button.selected {
  background: var(--selected-bg) !important;
  color: var(--selected-fg) !important;
  border: 2px solid #006215 !important;
}

/* Gör knapparna lite kompaktare så åtta får plats i rad */
.v85-grid .stButton > button { min-width: 90px; }
@media (max-width: 900px){
  .v85-grid .stButton > button { min-width: 80px; font-size:.9rem; padding:.5rem .3rem; }
}
</style>
""", unsafe_allow_html=True)

# --- Titel ---
st.markdown("<h1>🐴 V85 RÄKNEVERKTYG</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align:center;color:#f9f9f9;'>Beräkna hur många rader ditt matematiska system ger för 8, 7, 6 och 5 rätt.</p>", unsafe_allow_html=True)
st.markdown("<br>", unsafe_allow_html=True)

# --- Inputkort ---
st.markdown("<div class='card'>", unsafe_allow_html=True)
st.subheader("Ange antal hästar i varje avdelning")
antal = [st.number_input(f"Antal hästar – V85-{i+1}", min_value=1, max_value=15, value=1, step=1) for i in range(8)]
st.markdown("</div>", unsafe_allow_html=True)

# --- Toggle-rad (8 knappar i en horisontell rad) ---
st.markdown("<div class='card'>", unsafe_allow_html=True)
st.subheader("Markera vilka avdelningar som var rätt")

if "ratt_lopp" not in st.session_state:
  st.session_state.ratt_lopp = [False]*8

# Åtta kolumner – landar snyggt på en rad, wrappar på mindre skärmar
cols = st.columns(8, gap="small", vertical_alignment="center")
for i, col in enumerate(cols):
  with col:
    selected = st.session_state.ratt_lopp[i]
    label = f"V85-{i+1}"
    # Vi sätter en klass på knappen via unsafe HTML i etiketten är inte möjligt,
    # så vi sätter klass efter render genom att skriva ut en liten marker under knappen.
    if st.button(label, key=f"toggle_{i}"):
      st.session_state.ratt_lopp[i] = not selected
    # Injicera en liten JS-less hook: Streamlit sätter 'data-key' på wrappern – vi kan
    # markera knappen som 'selected' med en liten CSS-snutt per state:
    if st.session_state.ratt_lopp[i]:
      st.markdown(
        f"<style>[data-testid='stButton'][data-key='toggle_{i}'] button {{box-shadow:none}}"
        f"[data-testid='stButton'][data-key='toggle_{i}'] button {{}}"
        f"[data-testid='stButton'][data-key='toggle_{i}'] button {{}}"
        f"</style>",
        unsafe_allow_html=True
      )
      # Lägg även till klassen 'selected' via attr-hack: Streamlit tillåter inte direkt,
      # men vi kan simulera med en extra style som matchar exakt denna knapp:
      st.markdown(
        f"<style>[data-testid='stButton'][data-key='toggle_{i}'] button {{background:#007b1a !important;color:#fff !important;border:2px solid #006215 !important;}}</style>",
        unsafe_allow_html=True
      )

st.markdown("</div>", unsafe_allow_html=True)

# Skapa lista på valda lopp
ratt_lopp = [f"V85-{i+1}" for i, val in enumerate(st.session_state.ratt_lopp) if val]

# --- Uträkning ---
def rakna_vinster(antal, ratt_index):
    n = len(antal)
    fel_index = [i for i in range(n) if f"V85-{i+1}" not in ratt_index]
    ratt_index_nums = [i for i in range(n) if i not in fel_index]

    if len(fel_index) == 0:
        a = [antal[i]-1 for i in range(n)]
        S = sum(a); Q = sum(x*x for x in a); C = sum(x*x*x for x in a)
        a8 = 1
        a7 = S
        a6 = (S*S - Q)//2
        a5 = (S*S*S - 3*S*Q + 2*C)//6
        rubrik = "Du hade 8 rätt"

    elif len(fel_index) == 1:
        fel_count = antal[fel_index[0]]
        a = [antal[i]-1 for i in ratt_index_nums]
        S = sum(a); Q = sum(x*x for x in a)
        a8 = 0
        a7 = fel_count
        a6 = S * fel_count
        a5 = ((S*S - Q)//2) * fel_count
        rubrik = "Du hade 7 rätt"

    elif len(fel_index) == 2:
        fel_counts = [antal[i] for i in fel_index]
        a = [antal[i]-1 for i in ratt_index_nums]
        S = sum(a)
        a8 = 0
        a7 = 0
        a6 = fel_counts[0] * fel_counts[1]
        a5 = S * a6
        rubrik = "Du hade 6 rätt"

    elif len(fel_index) == 3:
        fel_counts = [antal[i] for i in fel_index]
        a8 = 0; a7 = 0; a6 = 0
        a5 = fel_counts[0] * fel_counts[1] * fel_counts[2]
        rubrik = "Du hade 5 rätt"
    else:
        rubrik = "För få rätt för att beräkna"
        a8 = a7 = a6 = a5 = 0
    return rubrik, a8, a7, a6, a5

# --- Visa resultat ---
if st.button("BERÄKNA RESULTAT", key="calc_btn"):
    rubrik, a8, a7, a6, a5 = rakna_vinster(antal, ratt_lopp)
    st.markdown("<br>", unsafe_allow_html=True)
    st.subheader(rubrik)

    col1, col2, col3, col4 = st.columns(4)
    with col1: st.markdown(f"<div class='metric-card'><div class='metric-label'>8 rätt</div><div class='metric-value'>{a8:,}</div></div>", unsafe_allow_html=True)
    with col2: st.markdown(f"<div class='metric-card'><div class='metric-label'>7 rätt</div><div class='metric-value'>{a7:,}</div></div>", unsafe_allow_html=True)
    with col3: st.markdown(f"<div class='metric-card'><div class='metric-label'>6 rätt</div><div class='metric-value'>{a6:,}</div></div>", unsafe_allow_html=True)
    with col4: st.markdown(f"<div class='metric-card'><div class='metric-label'>5 rätt</div><div class='metric-value'>{a5:,}</div></div>", unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    st.caption("Beräkningen följer ATG:s officiella rättningsmall för matematiska system (V85).")
