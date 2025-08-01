import streamlit as st
import pandas as pd
import plotly.express as px
import datetime
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import io

# --- ΡΥΘΜΙΣΕΙΣ GOOGLE SHEETS ---
SHEET_URL = "https://docs.google.com/spreadsheets/d/14w_r_xHdVkekACZ7EK-G8HeAA2-jG4x2arPdYoxMNvQ/edit?gid=0#gid=0"  # Βάλε το link του Sheet σου
SERVICE_ACCOUNT_FILE = "service_account.json"  # Το JSON που κατέβασες από Google Cloud

import json

scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]

if "gcp_service_account" in st.secrets:
    creds_dict = st.secrets["gcp_service_account"]
    creds = ServiceAccountCredentials.from_json_keyfile_dict(dict(creds_dict), scope)
else:
    creds = ServiceAccountCredentials.from_json_keyfile_name("service_account.json", scope)

client = gspread.authorize(creds)
sheet = client.open_by_url(SHEET_URL).sheet1


# --- Δεδομένα ---
data = {
    "Κατηγορία": [
        "Σνακ","Σνακ","Σνακ","Σνακ","Σνακ","Σνακ","Σνακ","Σνακ","Σνακ",
        "Πρωινό","Πρωινό","Πρωινό","Πρωινό","Πρωινό","Πρωινό",
        "Κυρίως Γεύμα","Κυρίως Γεύμα","Κυρίως Γεύμα","Κυρίως Γεύμα","Κυρίως Γεύμα",
        "Κυρίως Γεύμα","Κυρίως Γεύμα","Κυρίως Γεύμα","Κυρίως Γεύμα","Κυρίως Γεύμα",
        "Δεύτερο Γεύμα","Δεύτερο Γεύμα","Δεύτερο Γεύμα","Δεύτερο Γεύμα","Δεύτερο Γεύμα",
        "Δεύτερο Γεύμα","Δεύτερο Γεύμα","Δεύτερο Γεύμα","Δεύτερο Γεύμα"
    ],
    "Επιλογή": [
        "Τίποτα","1-2 Φρούτα","1 Φρούτο με 1 χούφτα αμύγδαλα","2-3 δαμάσκηνα και 12 αμύγδαλα","Γιαούρτι 2% με 1 κ.γ. μέλι",
        "2 φρυγανιές με 2 φέτες τυρί","2 φρυγανιές με 100 γρ. cottage cheese","1 ποτήρι κεφίρ (και 1 φρούτο)","1 μπάλα παγωτό",
        "Τίποτα","Μικρή αραβική με 2 φέτες τυρί light","Μικρή αραβική με 1 αυγό και 1 φέτα τυρί","Ψωμί με 2 κ.σ. cottage cheese, 1 αυγό και 1/4 αβοκάντο",
        "Κουλούρι Θεσσαλονίκης με γιαούρτι 2%","Γιαούρτι 2% με 2 κ.σ. βρώμη, 1 κ.γ. μέλι, 1 φρούτο και 2-3 καρύδια",
        "Τίποτα","Όσπρια (1,5 φλιτζ.), 50 γρ. ανθότυρο, 2 παξιμαδάκια","Ψάρι (180 γρ.) με 1 πατάτα βραστή","Μπιφτέκια (200 γρ.) ή Μπιφτέκια κοτόπουλο (250 γρ.)",
        "Μοσχάρι (120 γρ.) με ρύζι (1 φλιτζ.)","Αρακάς/Φασολάκια (1,5 φλιτζ.) με τυρί (60 γρ.)","Κοτόπουλο (150 γρ.) με πατάτες (1 φλιτζ.)",
        "Μακαρόνια (1,5 φλιτζ.) με κιμά (6 κ.σ.) και τυρί (1 κ.σ.)","Σαλάτα με 2 αυγά, 50 γρ. cottage cheese και 2 πατάτες βραστές","Ομελέτα με 2 αυγά, 30 γρ. τυρί λαχανικά και 2 κ.γ. ελαιόλαδο",
        "Τίποτα","Αραβική με 120 γρ. κοτόπουλο, λαχανικά και 1 κ.σ. γιαούρτι","Χωριάτικη/Ντάκος με 100 γρ. κατίκι, 2 παξιμάδάκια και 2 κ.γ. ελαιόλαδο","Κοτομπουκιές (150γρ.) με σαλάτα και 2 κ.γ. ελαιόλαδο",
        "Μπιφτέκια (120 γρ.) ή Μπιφτέκια κοτόπουλο (150 γρ.) με σαλάτα και 2 κ.γ. ελαιόλαδο","Σαλάτα με 120 γρ. κοτόπουλο, 2 κ.σ. καλαμπόκι και 2 κ.γ. ελαιόλαδο",
        "Σαλάτα με 100 γρ. τόνο, 2 κ.σ. κρουτόν και 1/4 αβοκάντο","Ομελέτα με 2 αυγά, 2 ασπράδια, 30 γρ. τυρί, λαχανικά 2 κ.γ. ελαιόλαδο και 1 φέτα ψωμί","2 καλαμάκια κοτόπουλο με 1 πιτάκι"
    ],
    "Θερμίδες (kcal)": [0,80,200,220,140,220,190,150,180,0,220,280,300,350,320,0,500,480,550,520,450,500,650,500,450,0,450,500,480,500,480,450,550,500],
    "Πρωτεΐνη (g)": [0,1,6,5,8,12,10,8,3,0,12,15,16,12,14,0,22,35,40,32,20,35,28,20,18,0,28,20,26,25,28,25,26,30],
    "Υδατάνθρακες (g)": [0,20,15,20,15,20,18,12,22,0,28,26,28,45,40,0,50,35,20,40,35,35,70,35,12,0,40,35,20,20,25,18,28,30],
    "Λίπος (g)": [0,0,12,10,4,7,5,5,7,0,5,8,10,8,8,0,15,10,20,15,14,12,20,10,28,0,12,18,15,18,15,20,20,15],
    "Φυτικές ίνες (g)": [0,3,4,5,0,2,1,0,0,0,2,2,3,4,5,0,9,2,1,3,8,3,6,5,4,0,4,6,3,3,4,5,6,3]
}

df = pd.DataFrame(data)


st.set_page_config(page_title="DietPro", page_icon="🥗", layout="centered")
st.title("DietPro – Ημερήσιος Υπολογισμός Θερμίδων & Μακροθρεπτικών")
st.write("Επίλεξε 3 σνακ και 3 γεύματα. Μπορείς να αποθηκεύσεις την ημέρα σου και να κατεβάσεις το ιστορικό.")

# --- Επιλογές ανά κατηγορία ---
breakfast_options = df[df["Κατηγορία"] == "Πρωινό"]["Επιλογή"].tolist()
snack_options = df[df["Κατηγορία"] == "Σνακ"]["Επιλογή"].tolist()
main_meal_options = df[df["Κατηγορία"] == "Κυρίως Γεύμα"]["Επιλογή"].tolist()
second_meal_options = df[df["Κατηγορία"] == "Δεύτερο Γεύμα"]["Επιλογή"].tolist()

# --- Επιλογές με σειρά ---
breakfast = st.selectbox("Πρωινό", breakfast_options, key="breakfast")
snack1 = st.selectbox("Σνακ 1", snack_options, key="snack1")
main_meal = st.selectbox("Κυρίως Γεύμα", main_meal_options, key="main_meal")
snack2 = st.selectbox("Σνακ 2", snack_options, key="snack2")
second_meal = st.selectbox("Δεύτερο Γεύμα", second_meal_options, key="second_meal")
snack3 = st.selectbox("Σνακ 3", snack_options, key="snack3")

# --- Σταθερή σειρά επιλογών ---
choices = {
    "Πρωινό": breakfast,
    "Σνακ 1": snack1,
    "Κυρίως Γεύμα": main_meal,
    "Σνακ 2": snack2,
    "Δεύτερο Γεύμα": second_meal,
    "Σνακ 3": snack3
}

rows = []
total_cal = total_prot = total_carb = total_fat = total_fiber = 0

for category, item in choices.items():
    row = df[df["Επιλογή"] == item]
    if not row.empty:
        cal = row["Θερμίδες (kcal)"].values[0]
        prot = row["Πρωτεΐνη (g)"].values[0]
        carb = row["Υδατάνθρακες (g)"].values[0]
        fat = row["Λίπος (g)"].values[0]
        fiber = row["Φυτικές ίνες (g)"].values[0]
    else:
        cal = prot = carb = fat = fiber = 0

    rows.append({
        "Κατηγορία": category,
        "Επιλογή": item,
        "Θερμίδες (kcal)": cal,
        "Πρωτεΐνη (g)": prot,
        "Υδατάνθρακες (g)": carb,
        "Λίπος (g)": fat,
        "Φυτικές ίνες (g)": fiber
    })

    total_cal += cal
    total_prot += prot
    total_carb += carb
    total_fat += fat
    total_fiber += fiber

# DataFrame για εμφάνιση
selected_df = pd.DataFrame(rows)





# --- Υπολογισμοί ---
total_cal = selected_df["Θερμίδες (kcal)"].sum()
total_prot = selected_df["Πρωτεΐνη (g)"].sum()
total_carb = selected_df["Υδατάνθρακες (g)"].sum()
total_fat = selected_df["Λίπος (g)"].sum()
total_fiber = selected_df["Φυτικές ίνες (g)"].sum()

st.subheader("Σύνολο:")
st.write(f"**Θερμίδες:** {total_cal} kcal")
st.write(f"**Πρωτεΐνη:** {total_prot} g | **Υδατάνθρακες:** {total_carb} g | **Λίπος:** {total_fat} g | **Φυτικές ίνες:** {total_fiber} g")

# --- Στόχοι ---
prot_target = 150
carb_target = 200
fat_target = 70
fiber_target = 25

# --- Progress για κάθε μακροθρεπτικό ---
st.subheader("Κάλυψη Στόχων Μακροθρεπτικών:")
st.write(f"Πρωτεΐνη: {total_prot}g / {prot_target}g")
st.progress(min(total_prot / prot_target, 1.0))

st.write(f"Υδατάνθρακες: {total_carb}g / {carb_target}g")
st.progress(min(total_carb / carb_target, 1.0))

st.write(f"Λίπος: {total_fat}g / {fat_target}g")
st.progress(min(total_fat / fat_target, 1.0))

st.write(f"Φυτικές ίνες: {total_fiber}g / {fiber_target}g")
st.progress(min(total_fiber / fiber_target, 1.0))




# --- Διάγραμμα Πίτας ---
if total_cal > 0:
    macros = {"Πρωτεΐνη": total_prot, "Υδατάνθρακες": total_carb, "Λίπος": total_fat}
    fig = px.pie(values=macros.values(), names=macros.keys(), title="Κατανομή Μακροθρεπτικών")
    st.plotly_chart(fig)

st.write("Αναλυτικά:")
st.dataframe(selected_df)
# --- Υπολογισμός ποσοστών κάλυψης ---
prot_target = 150
carb_target = 200
fat_target = 70
fiber_target = 25

prot_pct = round((total_prot / prot_target) * 100, 1)
carb_pct = round((total_carb / carb_target) * 100, 1)
fat_pct = round((total_fat / fat_target) * 100, 1)
fiber_pct = round((total_fiber / fiber_target) * 100, 1)

# --- Επιλογή ημερομηνίας ---
selected_date = st.date_input("Ημερομηνία καταχώρησης", value=datetime.date.today())

# --- Αποθήκευση Ημέρας στο Google Sheet ---
if st.button("Αποθήκευση Ημέρας"):
    new_row = [
    str(selected_date),
    str(breakfast),
    str(snack1),
    str(main_meal),
    str(snack2),
    str(second_meal),
    str(snack3),
    int(total_cal),
    float(total_prot),
    float(prot_pct),
    float(total_carb),
    float(carb_pct),
    float(total_fat),
    float(fat_pct),
    float(total_fiber),
    float(fiber_pct)
]

    sheet.append_row(new_row)
    st.success(f"Η καταχώρηση για {selected_date} αποθηκεύτηκε στο Google Sheet!")




st.subheader("Ιστορικό Ημερών")
rows = sheet.get_all_records()
if rows:
    history_df = pd.DataFrame(rows)
    st.dataframe(history_df)

    # Κατέβασμα Excel
    output = io.BytesIO()
    with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
        history_df.to_excel(writer, index=False, sheet_name='Ιστορικό')
    st.download_button(
        label="Λήψη Ιστορικού σε Excel",
        data=output.getvalue(),
        file_name="history.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )
else:
    st.info("Δεν υπάρχουν καταχωρήσεις ακόμα.")
