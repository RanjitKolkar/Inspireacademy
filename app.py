import streamlit as st
import pandas as pd
import os
import json

# =========================================================
# LOAD CONFIG
# =========================================================
with open("config.json", "r") as f:
    CONFIG = json.load(f)

APP_NAME = CONFIG["university_name"]
USERNAME = CONFIG["username"]
PASSWORD = CONFIG["password"]

DATA_FILE = "student_fee_data.xlsx"

# =========================================================
# PAGE CONFIG
# =========================================================
st.set_page_config(
    page_title=APP_NAME,
    page_icon="📚",
    layout="wide"
)

# =========================================================
# CUSTOM CSS
# =========================================================
# ADD THIS CSS BELOW st.set_page_config()

st.markdown("""
<style>

/* ==============================
   MAIN APP
============================== */
.main {
    background-color: #f4f7fc;
    padding: 0rem 1rem;
}

/* ==============================
   TITLE
============================== */
.title-box {
    background: linear-gradient(90deg,#1565C0,#43A047);
    padding: 18px;
    border-radius: 15px;
    text-align: center;
    color: white;
    margin-bottom: 20px;
}

.title-box h1 {
    font-size: 2rem;
}

.title-box h3 {
    font-size: 1rem;
}

/* ==============================
   BUTTONS
============================== */
.stButton>button {
    width: 100%;
    background-color: #1565C0;
    color: white;
    border-radius: 10px;
    font-weight: bold;
    border: none;
    height: 45px;
}

.stDownloadButton>button {
    width: 100%;
    border-radius: 10px;
    height: 45px;
    font-weight: bold;
}

/* ==============================
   INPUTS
============================== */
.stTextInput input,
.stNumberInput input,
.stSelectbox div[data-baseweb="select"] {
    border-radius: 10px;
}

/* ==============================
   DATAFRAME
============================== */
[data-testid="stDataFrame"] {
    overflow-x: auto;
}

/* ==============================
   METRICS
============================== */
[data-testid="metric-container"] {
    background-color: white;
    border-radius: 15px;
    padding: 15px;
    box-shadow: 0px 2px 8px rgba(0,0,0,0.08);
}

/* ==============================
   MOBILE RESPONSIVE
============================== */
@media (max-width: 768px) {

    .block-container {
        padding-top: 1rem;
        padding-left: 0.5rem;
        padding-right: 0.5rem;
    }

    .title-box {
        padding: 15px;
    }

    .title-box h1 {
        font-size: 1.5rem;
    }

    .title-box h3 {
        font-size: 0.9rem;
    }

    h1, h2, h3 {
        font-size: 1.1rem !important;
    }

    .stButton>button {
        height: 42px;
        font-size: 14px;
    }

    .stDownloadButton>button {
        height: 42px;
        font-size: 14px;
    }

    /* STACK COLUMNS */
    div[data-testid="column"] {
        width: 100% !important;
        flex: 1 1 100% !important;
        margin-bottom: 10px;
    }

    /* METRICS */
    [data-testid="metric-container"] {
        padding: 10px;
    }

    /* TABLE */
    table {
        font-size: 12px;
    }

    /* SIDEBAR */
    section[data-testid="stSidebar"] {
        width: 240px !important;
    }
}

/* ==============================
   EXTRA SMALL DEVICES
============================== */
@media (max-width: 480px) {

    .title-box h1 {
        font-size: 1.2rem;
    }

    .title-box h3 {
        font-size: 0.8rem;
    }

    .stTextInput input,
    .stNumberInput input {
        font-size: 14px;
    }

    table {
        font-size: 11px;
    }
}

</style>
""", unsafe_allow_html=True)

# =========================================================
# LOGIN
# =========================================================
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if not st.session_state.logged_in:

    st.markdown(f"""
    <div class="title-box">
        <h1>📚 {APP_NAME}</h1>
        <h3>Admin Login</h3>
    </div>
    """, unsafe_allow_html=True)

    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if st.button("Login"):

        if username == USERNAME and password == PASSWORD:

            st.session_state.logged_in = True
            st.success("Login Successful")
            st.rerun()

        else:
            st.error("Invalid Username or Password")

    st.stop()

# =========================================================
# FUNCTIONS
# =========================================================
def create_empty_data():

    df = pd.DataFrame(columns=[
        "Number",
        "Name",
        "Class",
        "Fee Paid"
    ])

    df.to_excel(DATA_FILE, index=False)

    return df


def load_data():

    if os.path.exists(DATA_FILE):
        return pd.read_excel(DATA_FILE)

    return create_empty_data()


def save_data(df):

    df.to_excel(DATA_FILE, index=False)


# =========================================================
# LOAD DATA
# =========================================================
df = load_data()

# =========================================================
# HEADER
# =========================================================
st.markdown(f"""
<div class="title-box">
    <h1>📚 {APP_NAME}</h1>
    <h3>Tuition Fee Collection & Tracking System</h3>
</div>
""", unsafe_allow_html=True)

# =========================================================
# SIDEBAR MENU
# =========================================================
st.sidebar.title("📋 Menu")

menu = st.sidebar.radio(
    "Select Option",
    [
        "Config",
        "Import",
        "Track",
        "Report"
    ]
)

if st.sidebar.button("Logout"):

    st.session_state.logged_in = False
    st.rerun()

# =========================================================
# CONFIG MENU
# =========================================================
if menu == "Config":

    st.subheader("⚙️ Application Configuration")

    config_df = pd.DataFrame({
        "Setting": [
            "University Name",
            "Username",
            "Password"
        ],
        "Value": [
            APP_NAME,
            USERNAME,
            PASSWORD
        ]
    })

    st.dataframe(
        config_df,
        use_container_width=True
    )

    st.info("Edit config.json file manually to update settings.")

    st.subheader("📥 Download Template")

    with open("student_template.xlsx", "rb") as file:

        st.download_button(
            label="Download Excel Template",
            data=file,
            file_name="student_template.xlsx"
        )

# =========================================================
# IMPORT MENU
# =========================================================
elif menu == "Import":

    st.subheader("📤 Import Student Data")

    uploaded_file = st.file_uploader(
        "Upload Excel File",
        type=["xlsx"]
    )

    if uploaded_file:

        new_df = pd.read_excel(uploaded_file)

        required_columns = [
            "Number",
            "Name",
            "Class"
        ]

        if all(col in new_df.columns for col in required_columns):

            if "Fee Paid" not in new_df.columns:
                new_df["Fee Paid"] = "No"

            combined_df = pd.concat(
                [df, new_df],
                ignore_index=True
            )

            combined_df.drop_duplicates(
                subset=["Number"],
                keep="last",
                inplace=True
            )

            save_data(combined_df)

            st.success("Data Imported Successfully")

        else:
            st.error(
                "Excel must contain Number, Name, Class columns"
            )

# =========================================================
# TRACK MENU
# =========================================================
elif menu == "Track":

    st.subheader("💰 Track & Manage Fees")

    # -----------------------------------------------------
    # ADD STUDENT
    # -----------------------------------------------------
    st.subheader("➕ Add Student")

    with st.form("add_student_form"):

        number = st.number_input(
            "Number",
            min_value=1,
            step=1
        )

        name = st.text_input("Name")

        student_class = st.text_input("Class")

        fee_status = st.selectbox(
            "Fee Paid",
            ["Yes", "No"]
        )

        submit = st.form_submit_button("Add Student")

        if submit:

            new_row = pd.DataFrame([{
                "Number": number,
                "Name": name,
                "Class": student_class,
                "Fee Paid": fee_status
            }])

            df = pd.concat(
                [df, new_row],
                ignore_index=True
            )

            save_data(df)

            st.success("Student Added Successfully")
            st.rerun()

    st.divider()

    # -----------------------------------------------------
    # SEARCH
    # -----------------------------------------------------
    search = st.text_input(
        "🔍 Search Student"
    )

    filtered_df = df.copy()

    if search:

        filtered_df = filtered_df[
            filtered_df.astype(str)
            .apply(
                lambda row: row.str.contains(
                    search,
                    case=False
                ).any(),
                axis=1
            )
        ]

    # -----------------------------------------------------
    # CRUD OPERATIONS
    # -----------------------------------------------------
    st.subheader("📝 CRUD Operations")

    if not filtered_df.empty:

        for index, row in filtered_df.iterrows():

            with st.container(border=True):

                c1, c2, c3, c4, c5, c6 = st.columns(
                    [1, 2, 2, 2, 1, 1]
                )

                updated_number = c1.number_input(
                    "No",
                    value=int(row["Number"]),
                    key=f"number_{index}"
                )

                updated_name = c2.text_input(
                    "Name",
                    value=str(row["Name"]),
                    key=f"name_{index}"
                )

                updated_class = c3.text_input(
                    "Class",
                    value=str(row["Class"]),
                    key=f"class_{index}"
                )

                updated_fee = c4.selectbox(
                    "Fee",
                    ["Yes", "No"],
                    index=0 if str(
                        row["Fee Paid"]
                    ).lower() == "yes" else 1,
                    key=f"fee_{index}"
                )

                # UPDATE
                if c5.button(
                    "Update",
                    key=f"update_{index}"
                ):

                    df.loc[index, "Number"] = updated_number
                    df.loc[index, "Name"] = updated_name
                    df.loc[index, "Class"] = updated_class
                    df.loc[index, "Fee Paid"] = updated_fee

                    save_data(df)

                    st.success(
                        f"{updated_name} Updated Successfully"
                    )

                    st.rerun()

                # DELETE
                if c6.button(
                    "Delete",
                    key=f"delete_{index}"
                ):

                    df = df.drop(index)

                    save_data(df)

                    st.warning(
                        f"{updated_name} Deleted"
                    )

                    st.rerun()

    else:
        st.warning("No Records Found")

# =========================================================
# REPORT MENU
# =========================================================
elif menu == "Report":

    st.subheader("📊 Fee Reports")

    total_students = len(df)

    paid_students = len(
        df[
            df["Fee Paid"]
            .astype(str)
            .str.lower() == "yes"
        ]
    )

    pending_students = total_students - paid_students

    c1, c2, c3 = st.columns(3)

    c1.metric(
        "Total Students",
        total_students
    )

    c2.metric(
        "Fees Paid",
        paid_students
    )

    c3.metric(
        "Fees Pending",
        pending_students
    )

    st.divider()

    st.subheader("📋 Student Records")

    st.dataframe(
        df,
        use_container_width=True,
        height=500
    )

    # -----------------------------------------------------
    # DOWNLOAD
    # -----------------------------------------------------
    st.subheader("📥 Download Database")

    with open(DATA_FILE, "rb") as file:

        st.download_button(
            label="Download Current Database",
            data=file,
            file_name="student_fee_data.xlsx"
        )

    st.divider()

    # -----------------------------------------------------
    # CLEAR DATA
    # -----------------------------------------------------
    st.subheader("⚠️ Danger Zone")

    confirm = st.checkbox(
        "I understand this will permanently delete all records."
    )

    if confirm:

        if st.button("🗑️ Clear All Data"):

            create_empty_data()

            st.success("All Data Cleared Successfully")

            st.rerun()