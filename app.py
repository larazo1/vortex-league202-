import streamlit as st
import pandas as pd

# --- CONFIGURATION DE LA PAGE ---
st.set_page_config(page_title="Vortex LDC 2026", layout="wide")

# --- DONNÉES INITIALES ---
TEAMS = [
    "VORTEX - BEX-VONIZONGO", "VORTEX-Nandriana", "VORTEX-NIL YLEK", "VORTEX-GOLD",
    "VORTEX-LUCLUC", "VORTEX-BELOUH-B", "VORTEX-LUCKA", "VORTEX-1Mig",
    "VORTEX-Njr", "VORTEX-LIONEL", "VORTEX-TOJO", "VORTEX-FRANCKO",
    "VORTEX-ZANDRYLEK", "VORTEX-THUNDER", "VORTEX-SANE NIRINA", "VORTEX-NAGI",
    "VORTEX-DENIS", "VORTEX-LUNO", "VORTEX-TINO"
]

# Simulation d'une base de données pour les scores (Session State)
if 'matches' not in st.session_state:
    # On crée quelques matchs par défaut pour l'exemple
    st.session_state.matches = [
        {"home": TEAMS[0], "away": TEAMS[1], "score_h": 0, "score_a": 0, "played": False},
        {"home": TEAMS[2], "away": TEAMS[3], "score_h": 0, "score_a": 0, "played": False},
    ]

# --- SYSTÈME D'AUTHENTIFICATION ---
st.sidebar.title("Connexion")
email = st.sidebar.text_input("Email")
password = st.sidebar.text_input("Mot de passe", type="password")

is_admin = (email == "lyzarzou@gmail.com" and password == "Vortex")
is_logged_in = (password == "Vortex")

# --- LOGIQUE DU CLASSEMENT (STANDING) ---
def calculate_standings():
    stats = {team: {"MJ": 0, "G": 0, "N": 0, "P": 0, "BP": 0, "BC": 0, "Pts": 0} for team in TEAMS}
    for m in st.session_state.matches:
        if m["played"]:
            stats[m["home"]]["MJ"] += 1
            stats[m["away"]]["MJ"] += 1
            stats[m["home"]]["BP"] += m["score_h"]
            stats[m["home"]]["BC"] += m["score_a"]
            stats[m["away"]]["BP"] += m["score_a"]
            stats[m["away"]]["BC"] += m["score_h"]
            
            if m["score_h"] > m["score_a"]:
                stats[m["home"]]["Pts"] += 3
                stats[m["home"]]["G"] += 1
                stats[m["away"]]["P"] += 1
            elif m["score_h"] < m["score_a"]:
                stats[m["away"]]["Pts"] += 3
                stats[m["away"]]["G"] += 1
                stats[m["home"]]["P"] += 1
            else:
                stats[m["home"]]["Pts"] += 1
                stats[m["away"]]["Pts"] += 1
                stats[m["home"]]["N"] += 1
                stats[m["away"]]["N"] += 1
    
    df = pd.DataFrame.from_dict(stats, orient='index').reset_index()
    df.columns = ['Équipe', 'MJ', 'G', 'N', 'P', 'BP', 'BC', 'Pts']
    return df.sort_values(by=["Pts", "BP"], ascending=False)

# --- INTERFACE UTILISATEUR ---
st.title("🏆 LDC VORTEX 2026 - Gestionnaire de Matchs")

if not is_logged_in:
    st.warning("Veuillez entrer le mot de passe 'Vortex' dans la barre latérale pour accéder aux données.")
else:
    tab1, tab2, tab3 = st.tabs(["📊 Classement Général", "📅 Calendrier", "⚙️ Administration"])

    with tab1:
        st.header("Classement Phase de Ligue")
        st.table(calculate_standings())

    with tab2:
        st.header("Matchs & Calendrier")
        for i, m in enumerate(st.session_state.matches):
            col1, col2, col3 = st.columns([2, 1, 2])
            col1.write(m["home"])
            col2.write(f"{m['score_h']} - {m['score_a']}" if m["played"] else "VS")
            col3.write(m["away"])

    with tab3:
        if is_admin:
            st.header("Modifier les scores (Admin)")
            match_idx = st.selectbox("Choisir le match", range(len(st.session_state.matches)), 
                                     format_func=lambda x: f"{st.session_state.matches[x]['home']} vs {st.session_state.matches[x]['away']}")
            
            c1, c2 = st.columns(2)
            s1 = c1.number_input("Score Domicile", min_value=0, step=1)
            s2 = c2.number_input("Score Extérieur", min_value=0, step=1)
            
            if st.button("Mettre à jour le score"):
                st.session_state.matches[match_idx]["score_h"] = s1
                st.session_state.matches[match_idx]["score_a"] = s2
                st.session_state.matches[match_idx]["played"] = True
                st.success("Score enregistré !")
        else:
            st.error("Accès réservé. Seul lyzarzou@gmail.com peut modifier les scores.")
