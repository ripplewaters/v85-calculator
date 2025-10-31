import streamlit as st

# --- Grundinställningar ---
st.set_page_config(page_title="V85 Räkneverktyg", page_icon="🐴", layout="centered")

# --- CSS ---
st.markdown("""
<style>
.stApp { background-color:#b00017 !important; color:#ffffff !important; }
.block-container { max-width:850px !important; padding-top:2rem; padding-bottom:4rem; }
h1,h2,h3,h4,h5,label,p,.stMarkdown,.stCaption { color:#ffffff !important; }

.card{
  background:#fff; color:#000; border-radius:10px; padding:20px 25px; margin-bottom:20px;
  box-shadow:0 4px 10px rgba(0,0,0,.25);
}
input,div[data-baseweb="input"]>div,div[data-baseweb="select"]{
  background:#fff !important; color:#000 !important; border-radius:6px;
}
.stButton button{
  background:#b00017 !important; color:#fff !important; border:none; border-radius:6px;
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

.toggle-container {
  display: flex;
  justify-content: center;
  flex-wrap: nowrap;
  gap: 10px;
  margin-top: 10px;
  margin-bottom: 20px;
}
.toggle-btn {
  background: #fff;
  color: #000;
  border-radius: 8px;
  padding: 0.6rem 1.2rem;
  cursor: pointer;
  font-weight: 600;
  box-shadow: 0 3px 6px rgba(0,0,0,.2);
  border: 2px solid transparent;
  transition: all 0.15s ease-in-out;
}
.toggle-btn:hover {
  background: #f3f3f3;
}
.toggle-btn.selected {
  background: #007b1a;
  color: #fff;
  border-color: #007b1a;
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

# --- Toggle-rad för rätta lopp ---
st.markdown("<div class='card'>", unsafe_allow_html=True)
st.subheader("Markera vilka avdelningar som var rätt")

if "ratt_lopp" not in st.session_state:
    st.session_state.ratt_lopp = [False for _ in range(8)]

st.markdown("<div class='toggle-container'>", unsafe_allow_html=True)
for i in range(8):
    label = f"V85-{i+1}"
    selected = st.session_state.ratt_lopp[i]
    btn_class = "toggle-btn selected" if selected else "toggle-btn"
    if st.button(label, key=f"toggle_{i}"):
        st.session_state.ratt_lopp[i] = not st.session_state.ratt_lopp[i]
st.markdown("</div>", unsafe_allow_html=True)
st.markdown("</div>", unsafe_allow_html=True)

ratt_lopp = [f"V85-{i+1}" for i, val in enumerate(st.session_state.ratt_lopp) if val]

# --- Uträkning enligt ATG-logik ---
def rakna_vinster(antal, ratt_index):
    n = len(antal)
    fel_index = [i for i in range(n) if f"V85-{i+1}" not in ratt_index]
    ratt_index_nums = [i for i in range(n) if i not in fel_index]

    if len(fel_index) == 0:
        a = [antal[i]-1 for i in range(n)]
        S = sum(a)
        Q = sum(x*x for x in a)
        C = sum(x*x*x for x in a)
        a8 = 1
        a7 = S
        a6 = (S*S - Q)//2
        a5 = (S*S*S - 3*S*Q + 2*C)//6
        rubrik = "Du hade 8 rätt"

    elif len(fel_index) == 1:
        fel_count = antal[fel_index[0]]
        a = [antal[i]-1 for i in ratt_index_nums]
        S = sum(a)
        Q = sum(x*x for x in a)
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
        a8 = 0
        a7 = 0
        a6 = 0
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
    with col1:
        st.markdown(f"<div class='metric-card'><div class='metric-label'>8 rätt</div><div class='metric-value'>{a8:,}</div></div>", unsafe_allow_html=True)
    with col2:
        st.markdown(f"<div class='metric-card'><div class='metric-label'>7 rätt</div><div class='metric-value'>{a7:,}</div></div>", unsafe_allow_html=True)
    with col3:
        st.markdown(f"<div class='metric-card'><div class='metric-label'>6 rätt</div><div class='metric-value'>{a6:,}</div></div>", unsafe_allow_html=True)
    with col4:
        st.markdown(f"<div class='metric-card'><div class='metric-label'>5 rätt</div><div class='metric-value'>{a5:,}</div></div>", unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    st.caption("Beräkningen följer ATG:s officiella rättningsmall för matematiska system (V85).")
