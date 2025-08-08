import streamlit as st
import pandas as pd
import plotly.express as px
import datetime
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import io
import json

# --- ΡΥΘΜΙΣΕΙΣ GOOGLE SHEETS ---
SHEET_URL = "https://docs.google.com/spreadsheets/d/14w_r_xHdVkekACZ7EK-G8HeAA2-jG4x2arPdYoxMNvQ/edit?gid=0#gid=0"
SERVICE_ACCOUNT_FILE = "service_account.json"

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
    "Θερμίδες (kcal)": [
        0,80,220,230,150,240,210,170,200,
        0,250,300,320,360,340,260,
        0,520,500,560,540,470,520,680,520,480,550,500,470,520,
        0,450,500,480,520,460,400,380,450,420,480,500,470,430
    ],
    "Πρωτεΐνη (g)": [
        0,1,6,6,9,14,12,9,3,
        0,14,16,18,14,16,12,
        0,24,36,42,34,22,38,30,22,20,28,25,20,27,
        0,28,20,26,25,27,24,22,26,23,30,28,26,24
    ],
    "Υδατάνθρακες (g)": [
        0,20,17,22,17,22,20,15,24,
        0,30,28,30,48,42,26,
        0,52,38,22,42,38,38,74,38,14,40,38,22,22,
        0,40,35,20,20,25,22,18,28,26,30,28,27,25
    ],
    "Λίπος (g)": [
        0,0,13,11,5,8,6,6,8,
        0,6,9,11,9,9,6,
        0,16,12,21,16,15,13,22,12,29,18,15,16,19,
        0,12,18,15,18,15,14,13,20,14,20,15,18,14
    ],
    "Φυτικές ίνες (g)": [
        0,3,4,5,0,2,1,1,0,
        0,3,3,4,5,6,3,
        0,9,3,2,4,9,4,7,6,5,5,6,4,4,
        0,4,6,3,3,4,5,5,6,4,6,5,5,4
    ],
    "Κορεσμένα (g)": [
        0,0,1.5,1.3,3,4,3,3,5,
        0,3,4,5,4,4,3,
        0,6,4,5,4,4,4,8,4,10,6,5,5,7,
        0,4,5,4,5,4,3.5,3,6,3.5,6,4,5,4
    ]
}

df = pd.DataFrame(data)

st.set_page_config(page_title="DietPro", layout="centered")
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
        sat_fat = 0  # FIX: αποφυγή UnboundLocalError

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

selected_df = pd.DataFrame(rows)

# --- Υπολογισμοί ---
total_cal = selected_df["Θερμίδες (kcal)"].sum()
total_prot = selected_df["Πρωτεΐνη (g)"].sum()
total_carb = selected_df["Υδατάνθρακες (g)"].sum()
total_fat = selected_df["Λίπος (g)"].sum()
total_fiber = selected_df["Φυτικές ίνες (g)"].sum()
total_sat_fat = selected_df["Κορεσμένα (g)"].sum()

# --- Ποσοστά θερμίδων ανά μακρο ---
if total_cal > 0:
    prot_pct_cal = round((total_prot * 4) / total_cal * 100, 1)
    carb_pct_cal = round((total_carb * 4) / total_cal * 100, 1)
    fat_pct_cal = round((total_fat * 9) / total_cal * 100, 1)
else:
    prot_pct_cal = carb_pct_cal = fat_pct_cal = 0.0

# --- Κάλυψη στόχων ---
prot_target, carb_target, fat_target, fiber_target, sat_fat_target = 150, 200, 70, 25, 20
prot_cov = round((total_prot / prot_target) * 100, 1)
carb_cov = round((total_carb / carb_target) * 100, 1)
fat_cov = round((total_fat / fat_target) * 100, 1)
fiber_cov = round((total_fiber / fiber_target) * 100, 1)
sat_fat_cov = round((total_sat_fat / sat_fat_target) * 100, 1)

# --- Εμφάνιση σύνολο ---
st.subheader("Σύνολο:")
st.write(f"**Θερμίδες:** {total_cal} kcal")
st.write(f"**Πρωτεΐνη:** {total_prot} g ({prot_pct_cal}% θερμίδων) | **Υδατάνθρακες:** {total_carb} g ({carb_pct_cal}% θερμίδων) | **Λίπος:** {total_fat} g ({fat_pct_cal}% θερμίδων)")
st.write(f"**Φυτικές ίνες:** {total_fiber} g | **Κορεσμένα:** {total_sat_fat} g")

# --- Progress Bars Κάλυψης Στόχων ---
st.subheader("Κάλυψη Στόχων:")
st.write(f"Πρωτεΐνη: {prot_cov}%")
st.progress(min(total_prot / prot_target, 1.0))
st.write(f"Υδατάνθρακες: {carb_cov}%")
st.progress(min(total_carb / carb_target, 1.0))
st.write(f"Λίπος: {fat_cov}%")
st.progress(min(total_fat / fat_target, 1.0))
st.write(f"Φυτικές ίνες: {fiber_cov}%")
st.progress(min(total_fiber / fiber_target, 1.0))
st.write(f"Κορεσμένα: {sat_fat_cov}%")
st.progress(min(total_sat_fat / sat_fat_target, 1.0))

# --- Pie Chart με θερμίδες μακρο ---
if total_cal > 0:
    macros_kcal = {"Πρωτεΐνη": total_prot * 4, "Υδατάνθρακες": total_carb * 4, "Λίπος": total_fat * 9}
    fig = px.pie(values=list(macros_kcal.values()), names=list(macros_kcal.keys()), title="Κατανομή Μακρο (σε θερμίδες)")
    st.plotly_chart(fig)

# --- Εμφάνιση επιλογών ---
st.write("Αναλυτικά:")
st.dataframe(selected_df)

# --- Επιλογή ημερομηνίας ---
selected_date = st.date_input("Ημερομηνία καταχώρησης", value=datetime.date.today())

# --- Αποθήκευση ---

if st.button("Αποθήκευση Ημέρας"):
    new_row = [
        str(selected_date),
        str(breakfast), str(snack1), str(main_meal),
        str(snack2), str(second_meal), str(snack3),
        int(total_cal),
        float(total_prot), float(prot_pct_cal),
        float(total_carb), float(carb_pct_cal),
        float(total_fat), float(fat_pct_cal),
        float(total_fiber), float(fiber_cov)
    ]

    try:
        all_rows = sheet.get_all_values()
        data = all_rows[1:]
        indices_to_delete = [i+2 for i, row in enumerate(data) if row and row[0] == str(selected_date)]
        for idx in sorted(indices_to_delete, reverse=True):
            sheet.delete_rows(idx)
        sheet.append_row(new_row)
        st.success(f"Η καταχώρηση για {selected_date} αποθηκεύτηκε.")
    except GSpreadException as e:
        st.error("Αποτυχία αποθήκευσης στο Google Sheet. Έλεγξε δικαιώματα/headers και ξαναπροσπάθησε.")


# --- Ιστορικό ---
from gspread.exceptions import GSpreadException  # πάνω-πάνω στα imports

# --- Ιστορικό ---
st.subheader("Ιστορικό Ημερών")

def safe_history_df(ws):
    """Ασφαλής ανάγνωση ιστορικού με fallback σε get_all_values."""
    try:
        rows = ws.get_all_records()  # προσπαθούμε πρώτα το «έξυπνο»
        return pd.DataFrame(rows)
    except GSpreadException:
        # Fallback όταν το φύλλο είναι άδειο/ασύμμετρο
        all_values = ws.get_all_values()
        if not all_values:
            return pd.DataFrame()  # τελείως άδειο sheet
        headers = all_values[0] if len(all_values) > 0 else []
        data = all_values[1:] if len(all_values) > 1 else []
        if not headers:
            return pd.DataFrame()  # δεν έχει καν headers
        # Κανονικοποίηση μήκους γραμμών ώστε να «κουμπώνουν» με headers
        norm = []
        for r in data:
            if len(r) < len(headers):
                r = r + [""] * (len(headers) - len(r))
            elif len(r) > len(headers):
                r = r[:len(headers)]
            norm.append(dict(zip(headers, r)))
        return pd.DataFrame(norm)

history_df = safe_history_df(sheet)

if not history_df.empty:
    st.dataframe(history_df)
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
    st.info("Δεν υπάρχουν καταχωρήσεις ακόμα ή λείπουν headers (1η γραμμή).")

