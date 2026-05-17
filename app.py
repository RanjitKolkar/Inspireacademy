import streamlit as st
import pandas as pd
import os

st.set_page_config(
    page_title="Inspire Academy Haliyal - Tuition Fee Tracker",
    page_icon="📚",
    layout="wide"
)

DATA_FILE = "student_fee_data.xlsx"

st.markdown("""
<style>
.main {
    background-color: #f5f7fa;
}
.stButton>button {
    background-color: #1f77b4;
    color: white;
    border-radius: 10px;
    height: 45px;
    font-size: 16px;
    font-weight: bold;
}
.stDownloadButton>button {
    background-color: #28a745;
    color: white;
    border-radius: 10px;
}
.title-box {
    background: linear-gradient(90deg,#1f77b4,#4CAF50);
    padding: 20px;
    border-radius: 15px;
    text-align: center;
    color: white;
    margin-bottom: 20px;
}
.metric-box {
    background-color: white;
    padding: 15px;
    border-radius: 12px;
    box-shadow: 0px 0px 10px rgba(0,0,0,0.1);
}
</style>
""", unsafe_allow_html=True)

st.markdown("""
<div class="title-box">
    <h1>📚 Inspire Academy Haliyal</h1>
    <h3>Tuition Fee Collection & Tracking System</h3>
</div>
""", unsafe_allow_html=True)

def create_empty_data():
    df = pd.DataFrame(columns=["Number", "Name", "Class", "Fee Paid"])
    df.to_excel(DATA_FILE, index=False)
    return df

def load_data():
    if os.path.exists(DATA_FILE):
        return pd.read_excel(DATA_FILE)
    return create_empty_data()

def save_data(df):
    df.to_excel(DATA_FILE, index=False)

st.subheader("📥 Download Template")

template_path = "student_template.xlsx"

with open(template_path, "rb") as file:
    st.download_button(
        label="Download Excel Template",
        data=file,
        file_name="student_template.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )

st.divider()

df = load_data()

st.subheader("📤 Upload Student Excel Sheet")

uploaded_file = st.file_uploader("Upload Excel File", type=["xlsx"])

if uploaded_file:
    new_df = pd.read_excel(uploaded_file)

    required_columns = ["Number", "Name", "Class"]

    if all(col in new_df.columns for col in required_columns):

        if "Fee Paid" not in new_df.columns:
            new_df["Fee Paid"] = "No"

        if not df.empty:
            combined_df = pd.concat([df, new_df], ignore_index=True)
            combined_df.drop_duplicates(subset=["Number"], keep="last", inplace=True)
        else:
            combined_df = new_df

        combined_df["Fee Paid"] = combined_df["Fee Paid"].fillna("No")

        save_data(combined_df)
        df = combined_df

        st.success("✅ Data uploaded and updated successfully!")
    else:
        st.error("❌ Excel must contain: Number, Name, Class")

st.divider()

st.subheader("📊 Fee Dashboard")

total_students = len(df)
paid_students = len(df[df["Fee Paid"].astype(str).str.lower() == "yes"])
unpaid_students = total_students - paid_students

c1, c2, c3 = st.columns(3)

c1.metric("Total Students", total_students)
c2.metric("Fees Paid", paid_students)
c3.metric("Fees Pending", unpaid_students)

st.divider()

st.subheader("🔍 Search Student")

search = st.text_input("Search by Name / Number / Class")

filtered_df = df.copy()

if search:
    filtered_df = filtered_df[
        filtered_df.astype(str).apply(
            lambda row: row.str.contains(search, case=False).any(), axis=1
        )
    ]

st.subheader("💰 Update Fee Status")

if not filtered_df.empty:

    for index, row in filtered_df.iterrows():

        a, b, c, d, e = st.columns([1,3,2,2,2])

        a.write(row["Number"])
        b.write(row["Name"])
        c.write(row["Class"])

        current_status = str(row["Fee Paid"])

        status = d.selectbox(
            f"Status {index}",
            ["Yes", "No"],
            index=0 if current_status.lower() == "yes" else 1,
            key=f"status_{index}"
        )

        if e.button("Update", key=f"update_{index}"):
            df.loc[df["Number"] == row["Number"], "Fee Paid"] = status
            save_data(df)
            st.success(f"Updated {row['Name']}")
            st.rerun()

else:
    st.warning("No student records found.")

st.divider()

st.subheader("📋 Student Records")

st.dataframe(df, use_container_width=True, height=400)

st.subheader("📥 Download Updated Data")

with open(DATA_FILE, "rb") as file:
    st.download_button(
        label="Download Current Database",
        data=file,
        file_name="student_fee_data.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )

st.divider()

st.subheader("⚠️ Danger Zone")

confirm = st.checkbox("I understand this will permanently delete all student data.")

if confirm:
    if st.button("🗑️ Clear All Data"):
        create_empty_data()
        st.success("All data cleared successfully!")
        st.rerun()

st.markdown("<hr><center><h4>Developed for Inspire Academy Haliyal</h4></center>", unsafe_allow_html=True)
