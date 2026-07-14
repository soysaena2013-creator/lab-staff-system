import streamlit as st
import pandas as pd

CSV_URLS = {
    "profile": "https://docs.google.com/spreadsheets/d/e/2PACX-1vRNwMjfrUFFtELYMwByAwtV5oWDe0enW7TzTJW_Dl-hjIbxPlCg9LEMahNEc4EgZHvr-XNFIcHPdfNQ/pub?gid=0&single=true&output=csv",
    "training": "https://docs.google.com/spreadsheets/d/e/2PACX-1vRNwMjfrUFFtELYMwByAwtV5oWDe0enW7TzTJW_Dl-hjIbxPlCg9LEMahNEc4EgZHvr-XNFIcHPdfNQ/pub?gid=1403147110&single=true&output=csv",
    "license": "https://docs.google.com/spreadsheets/d/e/2PACX-1vRNwMjfrUFFtELYMwByAwtV5oWDe0enW7TzTJW_Dl-hjIbxPlCg9LEMahNEc4EgZHvr-XNFIcHPdfNQ/pub?gid=974412732&single=true&output=csv"
}

@st.cache_data(ttl=600)
def load_data(key):
    df = pd.read_csv(CSV_URLS[key])
    # ตัดช่องว่างออกจากชื่อคอลัมน์และข้อมูล
    df.columns = df.columns.str.strip()
    if "เลขบัตรประชาชน" in df.columns:
        df["เลขบัตรประชาชน"] = df["เลขบัตรประชาชน"].astype(str).str.strip()
    return df

st.markdown("### ระบบข้อมูลบุคลากร กลุ่มงานเทคนิคการแพทย์")

df_profile = load_data("profile")
df_training = load_data("training")
df_license = load_data("license")

user_options = df_profile.set_index("เลขบัตรประชาชน")["ชื่อ สกุล"].to_dict()
selected_id = st.sidebar.selectbox("เลือกบุคลากร:", options=user_options.keys(), format_func=lambda x: user_options[x])

menu = st.sidebar.radio("เมนู", ["ข้อมูลทั่วไป", "ประวัติการฝึกอบรม", "ใบประกอบวิชาชีพ"])

# --- ตรวจสอบส่วนนี้ ---
if menu == "ใบประกอบวิชาชีพ":
    st.write("ชื่อคอลัมน์ที่มีในตารางใบประกอบฯ:", df_license.columns.tolist())
    
    # กรองข้อมูล
    df_l = df_license[df_license["เลขบัตรประชาชน"] == selected_id.strip()]
    
    if not df_l.empty:
        st.write(df_l.iloc[0].T)
    else:
        st.error(f"ไม่พบข้อมูลใบประกอบฯ สำหรับเลขบัตร {selected_id}")
        st.write("ข้อมูลเลขบัตรที่มีในตารางนี้:", df_license["เลขบัตรประชาชน"].unique())