import streamlit as st
import sqlite3
from datetime import datetime

# ==========================================
# 1. DATENBANK AUFBAUEN
# ==========================================
connection = sqlite3.connect("fitfocus.db")
db_worker = connection.cursor()

db_worker.execute("CREATE TABLE IF NOT EXISTS tiles (id INTEGER PRIMARY KEY, name TEXT UNIQUE, is_done INTEGER)")
db_worker.execute("CREATE TABLE IF NOT EXISTS supplies (id INTEGER PRIMARY KEY, name TEXT UNIQUE, amount INTEGER)")
db_worker.execute("CREATE TABLE IF NOT EXISTS streak (id INTEGER PRIMARY KEY, count INTEGER)")

# Standardwerte füllen, falls leer
db_worker.execute("SELECT COUNT(*) FROM tiles")
if db_worker.fetchone()[0] == 0:
    for name in ["Kreatin", "3L Wasser", "Workout", "Omega 3"]:
        db_worker.execute("INSERT INTO tiles (name, is_done) VALUES (?, 0)", (name,))

db_worker.execute("SELECT COUNT(*) FROM supplies")
if db_worker.fetchone()[0] == 0:
    db_worker.execute("INSERT INTO supplies (name, amount) VALUES (?, ?)", ("Kreatin", 120))
    db_worker.execute("INSERT INTO supplies (name, amount) VALUES (?, ?)", ("Omega 3", 90))

db_worker.execute("SELECT COUNT(*) FROM streak")
if db_worker.fetchone()[0] == 0:
    db_worker.execute("INSERT INTO streak (count) VALUES (0)")

connection.commit()
connection.close()

# ==========================================
# 2. DESIGN SETZEN
# ==========================================
st.set_page_config(page_title="FitFocus", page_icon="⚡", layout="centered")

st.markdown("""
    <style>
    .block-container { padding-top: 4rem; padding-bottom: 0rem; }
    .stApp { background-color: #006064 !important; }
    h1, h2, p { color: #E0F2F1 !important; text-align: center; }
    div[data-testid="stVerticalBlockBorderWrapper"], [data-testid="stMetricBorderWrapper"] {
        background-color: #E0F2F1 !important;
        border: 2px solid #B2DFDB !important;
        border-radius: 16px !important;
        padding: 20px !important;
    }
    [data-testid="stVerticalBlockBorderWrapper"] h3,
    .stCheckbox label p, .stMarkdown p, .stMarkdown span, .stMarkdown b {
        color: #0A1416 !important;
        font-weight: 700 !important;
        font-size: 1.1rem !important;
    }
    .stButton button {
        background-color: #00796B !important;
        color: white !important;
        font-weight: 700 !important;
        border-radius: 8px !important;
    }
    </style>
""", unsafe_allow_html=True)

# STREAK BERECHNEN
connection = sqlite3.connect("fitfocus.db")
db_worker = connection.cursor()

db_worker.execute("SELECT COUNT(*) FROM tiles")
gesamt_anzahl = db_worker.fetchone()[0]

db_worker.execute("SELECT COUNT(*) FROM tiles WHERE is_done = 1")
erledigte_anzahl = db_worker.fetchone()[0]

if gesamt_anzahl > 0 and gesamt_anzahl == erledigte_anzahl:
    neuer_streak = 1
else:
    neuer_streak = 0

db_worker.execute("UPDATE streak SET count = ? WHERE id = 1", (neuer_streak,))
connection.commit()

db_worker.execute("SELECT count FROM streak WHERE id = 1")
aktueller_streak = db_worker.fetchone()[0]
connection.close()

st.title("⚡ FitFocus Dashboard")
st.markdown(f"<p style='color: #FF9100 !important; font-weight: bold; font-size: 1.3rem;'>🔥 Serie: {aktueller_streak} Tage</p>", unsafe_allow_html=True)
st.divider()

# ==========================================
# 3. DAS RASTER (2 Spalten)
# ==========================================
col1, col2 = st.columns(2)

with col1:
    with st.container(border=True):
        st.markdown("### ✅ Tagesziele")
        connection = sqlite3.connect("fitfocus.db")
        db_worker = connection.cursor()
        db_worker.execute("SELECT name, is_done FROM tiles")
        tasks = db_worker.fetchall()
        connection.close()
        
        for name, is_done in tasks:
            status = True if is_done == 1 else False
            if st.checkbox(name, value=status, key=f"check_{name}"):
                new_status = 1
            else:
                new_status = 0
                
            if new_status != is_done:
                connection = sqlite3.connect("fitfocus.db")
                db_worker = connection.cursor()
                db_worker.execute("UPDATE tiles SET is_done = ? WHERE name = ?", (new_status, name))
                connection.commit()
                connection.close()
                st.rerun()

with col2:
    with st.container(border=True):
        st.markdown("### 📦 Vorrat")
        connection = sqlite3.connect("fitfocus.db")
        db_worker = connection.cursor()
        db_worker.execute("SELECT name, amount FROM supplies")
        supplies_data = db_worker.fetchall()
        connection.close()
        
        for name, amount in supplies_data:
            st.write(f"**{name}:** {amount} Stück")
            if st.button(f"1 verbraucht ({name})", key=f"sub_{name}", use_container_width=True):
                if amount > 0:
                    new_amount = amount - 1
                    connection = sqlite3.connect("fitfocus.db")
                    db_worker = connection.cursor()
                    db_worker.execute("UPDATE supplies SET amount = ? WHERE name = ?", (new_amount, name))
                    connection.commit()
                    connection.close()
                    st.rerun()

st.divider()

# ==========================================
# 4. NEUE DATEN HINZUFÜGEN
# ==========================================
st.markdown("## ➕ Neues Element hinzufügen")
col_add1, col_add2 = st.columns(2)

with col_add1:
    with st.container(border=True):
        st.markdown("### 🎯 Neues Tagesziel")
        neues_ziel = st.text_input("Name des Ziels", key="input_ziel")
        if st.button("Ziel hinzufügen", use_container_width=True):
            if neues_ziel:
                try:
                    connection = sqlite3.connect("fitfocus.db")
                    db_worker = connection.cursor()
                    db_worker.execute("INSERT INTO tiles (name, is_done) VALUES (?, 0)", (neues_ziel,))
                    connection.commit()
                    connection.close()
                    st.rerun()
                except sqlite3.IntegrityError:
                    st.error("Dieses Ziel existiert bereits!")

with col_add2:
    with st.container(border=True):
        st.markdown("### 💊 Neuen Vorrat")
        neuer_vorrat_name = st.text_input("Name des Supplements", key="input_vorrat")
        neuer_vorrat_menge = st.number_input("Menge (Stück)", min_value=1, value=90, step=1, key="input_menge")
        if st.button("Vorrat hinzufügen", use_container_width=True):
            if neuer_vorrat_name:
                try:
                    connection = sqlite3.connect("fitfocus.db")
                    db_worker = connection.cursor()
                    db_worker.execute("INSERT INTO supplies (name, amount) VALUES (?, ?)", (neuer_vorrat_name, int(neuer_vorrat_menge)))
                    connection.commit()
                    connection.close()
                    st.rerun()
                except sqlite3.IntegrityError:
                    st.error("Dieser Vorrat existiert bereits!")

st.divider()

# ==========================================
# 5. DER EINFACHE E-MAIL WECKER (Portfolio-Mockup)
# ==========================================
st.markdown("<h2>⏰ Täglicher E-Mail-Wecker</h2>", unsafe_allow_html=True)

with st.container(border=True):
    st.markdown("### 📧 Benachrichtigung einrichten")
    
    # Fehlervermeidung: Wir stellen SICHER, dass die Tabelle existiert, bevor wir lesen!
    connection = sqlite3.connect("fitfocus.db")
    db_worker = connection.cursor()
    db_worker.execute("CREATE TABLE IF NOT EXISTS settings (id INTEGER PRIMARY KEY, email TEXT)")
    
    # Prüfen, ob ein Eintrag da ist. Wenn nicht, legen wir einen leeren an.
    db_worker.execute("SELECT COUNT(*) FROM settings")
    if db_worker.fetchone()[0] == 0:
        db_worker.execute("INSERT INTO settings (email) VALUES ('')")
        connection.commit()
    
    # Jetzt können wir absolut sicher auslesen (READ)
    gespeicherte_mail_row = db_worker.execute("SELECT email FROM settings WHERE id = 1").fetchone()
    connection.close()
    
    gespeicherte_mail = gespeicherte_mail_row[0] if gespeicherte_mail_row else ""
    
    # Nutzer gibt NUR seine E-Mail ein!
    user_email = st.text_input("Deine E-Mail-Adresse fürs Handy", value=gespeicherte_mail, key="input_email_alarm")
    
    if user_email != gespeicherte_mail:
        connection = sqlite3.connect("fitfocus.db")
        db_worker = connection.cursor()
        db_worker.execute("UPDATE settings SET email = ? WHERE id = 1", (user_email,))
        connection.commit()
        connection.close()
        st.rerun()
    
    if st.button("🔔 Test-Erinnerung jetzt an mein Handy senden", use_container_width=True):
        if user_email:
            with st.spinner("Verbindung zum SMTP-Gateway wird aufgebaut..."):
                st.success(f"📬 Simulations-Modus aktiv: Nachricht erfolgreich an {user_email} vermittelt!")
                st.balloons()
        else:
            st.warning("Bitte trage zuerst deine E-Mail-Adresse ein.")
