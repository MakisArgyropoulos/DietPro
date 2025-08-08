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


import pandas as pd

# --- Δεδομένα ---
data = {
    "Κατηγορία": [
        "Σνακ","Σνακ","Σνακ","Σνακ","Σνακ","Σνακ","Σνακ","Σνακ","Σνακ",
        "Πρωινό","Πρωινό","Πρωινό","Πρωινό","Πρωινό","Πρωινό","Πρωινό",
        "Κυρίως Γεύμα","Κυρίως Γεύμα","Κυρίως Γεύμα","Κυρίως Γεύμα","Κυρίως Γεύμα",
        "Κυρίως Γεύμα","Κυρίως Γεύμα","Κυρίως Γεύμα","Κυρίως Γεύμα","Κυρίως Γεύμα",
        "Κυρίως Γεύμα","Κυρίως Γεύμα","Κυρίως Γεύμα","Κυρίως Γεύμα",
        "Δεύτερο Γεύμα","Δεύτερο Γεύμα","Δεύτερο Γεύμα","Δεύτερο Γεύμα","Δεύτερο Γεύμα",
        "Δεύτερο Γεύμα","Δεύτερο Γεύμα","Δεύτερο Γεύμα","Δεύτερο Γεύμα","Δεύτερο Γεύμα",
        "Δεύτερο Γεύμα","Δεύτερο Γεύμα","Δεύτερο Γεύμα","Δεύτερο Γεύμα"
    ],
    "Επιλογή": [
        "Τίποτα",
        "1-2 Φρούτα",
        "1 Φρούτο με 1 χούφτα αμύγδαλα",
        "2-3 δαμάσκηνα και 12 αμύγδαλα",
        "Γιαούρτι 2% με 1 κ.γ. μέλι",
        "2 φρυγανιές/κράκερ με 2 φέτες τυρί",
        "2 φρυγανιές/κράκερ με 100 γρ. cottage cheese",
        "Smoothie με 1 κούπα γάλα και 1/2 μπανάνα",
        "1 μπάλα παγωτό",
        "Τίποτα",
        "Μικρή αραβική με 2 φέτες τυρί light",
        "Μικρή αραβική με 1 αυγό και 1 φέτα τυρί",
        "Ψωμί με 2 κ.σ. cottage cheese, 1 αυγό και 1/4 αβοκάντο",
        "Κουλούρι Θεσσαλονίκης με γιαούρτι 2%",
        "Γιαούρτι 2% με 2 κ.σ. βρώμη, 1 κ.γ. μέλι, 1 φρούτο και 2-3 καρύδια",
        "2 φρυγανιές με 100 γρ.cottage cheese, 1 κ.γ.μαρμελάδα",
        "Τίποτα",
        "Όσπρια (1,5 φλιτζ.), 50 γρ. ανθότυρο, 2 παξιμαδάκια και σαλάτα με 2 κ.γ. ελαιόλαδο",
        "Σαλάτα με 1 φλιτζ. όσπριο, 100 γρ. τόνο, 2 παξιμαδάκια και σαλάτα με 2 κ.γ. ελαιόλαδο",
        "Ψάρι (180 γρ.) με 1 πατάτα βραστή και σαλάτα με 2 κ.γ. ελαιόλαδο",
        "Μπιφτέκια (200 γρ.) ή Μπιφτέκια κοτόπουλο (250 γρ.) και σαλάτα με 2 κ.γ. ελαιόλαδο",
        "Ψαρονέφρι (180 γρ.) και σαλάτα με 2 κ.γ. ελαιόλαδο",
        "Μοσχάρι (120 γρ.) με ρύζι (1 φλιτζ.) και σαλάτα με 2 κ.γ. ελαιόλαδο",
        "Λαδερό (1,5 φλιτζ.) με τυρί (60 γρ.) και σαλάτα με 2 κ.γ. ελαιόλαδο",
        "Κοτόπουλο (150 γρ.) με πατάτες/ρύζι (1 φλιτζ.) και σαλάτα με 2 κ.γ. ελαιόλαδο",
        "Μακαρόνια (1,5 φλιτζ.) με κιμά (6 κ.σ.) και τυρί (1 κ.σ.) και σαλάτα με 2 κ.γ. ελαιόλαδο",
        "Μακαρόνια (1 φλιτζ.), γαρίδες (150 γρ.) και σαλάτα με 2 κ.γ. ελαιόλαδο",
        "Γεμιστά (2), τυρί (60 γρ.) και σαλάτα με 2 κ.γ. ελαιόλαδο",
        "Σαλάτα με 2 αυγά, 50 γρ. cottage cheese και 2 πατάτες βραστές και σαλάτα με 2 κ.γ. ελαιόλαδο",
        "Ομελέτα με 2 αυγά, 30 γρ. τυρί λαχανικά και 2 κ.γ. ελαιόλαδο και σαλάτα με 2 κ.γ. ελαιόλαδο",
        "Τίποτα",
        "1 γιαούρτι 2% με 2 κ.σ. βρώμη, 1 φρούτο και 1 χούφτα ξηρούς καρπούς",
        "Αραβική με 120 γρ. κοτόπουλο, λαχανικά και 1 κ.σ. γιαούρτι",
        "Σαλάτα Χωριάτικη/Ντάκος με 100 γρ. κατίκι, 2 παξιμάδάκια και 2 κ.γ. ελαιόλαδο",
        "Κοτομπουκιές (150γρ.) με σαλάτα και 2 κ.γ. ελαιόλαδο",
        "Μπιφτέκια (120 γρ.) ή Μπιφτέκια κοτόπουλο (150 γρ.) με σαλάτα και 2 κ.γ. ελαιόλαδο",
        "Σαλάτα με 120 γρ. κοτόπουλο, 2 κ.σ. καλαμπόκι και 2 κ.γ. ελαιόλαδο",
        "Σαλάτα με 2 αυγά, 1 πατάτα βραστή, 2 κ.γ. ελαιόλαδο",
        "Ψητά λαχανικά και μανιτάρια, 200 γρ. κατίκι, 1 φέτα ψωμί",
        "Σαλάτα με 100 γρ. τόνο, 2 κ.σ. κρουτόν και 1/4 αβοκάντο",
        "Ομελέτα με 2 αυγά, 2 ασπράδια, 30 γρ. τυρί, λαχανικά 2 κ.γ. ελαιόλαδο και 1 φέτα ψωμί",
        "Πίτσα με 1 τορτίγια με 2 φέτες τυρί, λαχανικά και σάλτσα ντομάτας",
        "3 καλαμάκια κοτόπουλο με σαλάτα με 2 κ.γ. ελαιόλαδο",
        "Σουβλάκι με αλάδωτη πίτα, καλαμάκι κοτόπουλο, χωρίς πατάτες"
    ],
    # Εκτιμήσεις θερμίδων & macros
    "Θερμίδες (kcal)": [0,80,220,230,150,240,210,170,200,0,250,300,320,360,340,250,520,500,560,540,470,520,680,520,480,500,470,520,500,520,500,470,570,520],
    "Πρωτεΐνη (g)": [0,1,6,6,9,14,12,9,3,0,14,16,18,14,16,14,24,36,42,34,22,38,30,22,20,18,30,22,28,27,30,27,28,32],
    "Υδατάνθρακες (g)": [0,20,17,22,17,22,20,15,24,0,30,28,30,48,42,28,52,38,22,42,38,38,74,38,14,40,42,38,22,22,27,20,30,32],
    "Λίπος (g)": [0,0,13,11,5,8,6,6,8,0,6,9,11,9,9,8,16,12,21,16,15,13,22,12,29,18,13,19,16,19,16,21,21,16],
    "Φυτικές ίνες (g)": [0,3,4,5,0,2,1,1,0,0,3,3,4,5,6,4,9,3,2,4,9,4,7,6,5,4,5,7,4,4,5,6,7,4],
    "Κορεσμένα (g)": [0,0,1.5,1.3,3,4,3,3,5,0,3,4,5,4,4,3,6,4,5,4,4,4,8,4,10,5,5,7,5,7,5,8,8,6]
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
        sat_fat = row["Κορεσμένα (g)"].values[0]
    else:
        cal = prot = carb = fat = fiber = 0

    rows.append({
        "Κατηγορία": category,
        "Επιλογή": item,
        "Θερμίδες (kcal)": cal,
        "Πρωτεΐνη (g)": prot,
        "Υδατάνθρακες (g)": carb,
        "Λίπος (g)": fat,
        "Φυτικές ίνες (g)": fiber,
        "Κορεσμένα (g)": sat_fat
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
total_sat_fat = selected_df["Κορεσμένα (g)"].sum()

st.subheader("Σύνολο:")
st.write(f"**Θερμίδες:** {total_cal} kcal")
st.write(f"**Πρωτεΐνη:** {total_prot} g | **Υδατάνθρακες:** {total_carb} g | **Λίπος:** {total_fat} g | **Φυτικές ίνες:** {total_fiber} g | **Κορεσμένα:** {total_sat_fat} g")

# --- Στόχοι ---
prot_target = 150
carb_target = 200
fat_target = 70
fiber_target = 25
sat_fat_target = 20

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

st.write(f"Κορεσμένα: {total_sat_fat}g / {sat_fat_target}g")
st.progress(min(total_sat_fat / sat_fat_target, 1.0))




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
    # Νέα γραμμή με σωστούς τύπους
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

    # Φέρε όλα τα δεδομένα
    all_rows = sheet.get_all_values()
    headers = all_rows[0]
    data = all_rows[1:]

    # Διέγραψε όλες τις γραμμές που έχουν ήδη αυτή την ημερομηνία
    indices_to_delete = [i+2 for i, row in enumerate(data) if row and row[0] == str(selected_date)]  # +2 λόγω header και 1-based indexing
    for idx in sorted(indices_to_delete, reverse=True):
        sheet.delete_rows(idx)

    # Πρόσθεσε τη νέα γραμμή
    sheet.append_row(new_row)
    st.success(f"Η καταχώρηση για {selected_date} αποθηκεύτηκε (αντικαταστάθηκε η παλιά, αν υπήρχε).")





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
