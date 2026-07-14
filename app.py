import streamlit as st
import pandas as pd

# ลิงก์ข้อมูล (อัปเดตลิงก์ล่าสุดตามรูปภาพของคุณ)
CSV_URLS = {
    "profile": "https://docs.google.com/spreadsheets/d/e/2PACX-1vRNwMjfrUFFtELYMwByAwtV5oWDe0enW7TzTJW_Dl-hjIbxPlCg9LEMahNEc4EgZHvr-XNFIcHPdfNQ/pub?gid=0&single=true&output=csv",
    "training": "https://docs.google.com/spreadsheets/d/e/2PACX-1vRNwMjfrUFFtELYMwByAwtV5oWDe0enW7TzTJW_Dl-hjIbxPlCg9LEMahNEc4EgZHvr-XNFIcHPdfNQ/pub?gid=1403147110&single=true&output=csv",
    "license": "https://docs.google.com/spreadsheets/d/e/2PACX-1vRNwMjfrUFFtELYMwByAwtV5oWDe0enW7TzTJW_Dl-hjIbxPlCg9LEMahNEc4EgZHvr-XNFIcHPdfNQ/pub?gid=974412732&single=true&output=csv"
}

@st.cache_data(ttl=600)
def load_data(url):
    df = pd.read_csv(url)
    df.columns = df.columns.str.strip() # ทำความสะอาดชื่อคอลัมน์
    return df

st.markdown("### ระบบข้อมูลบุคลากร กลุ่มงานเทคนิคการแพทย์")

# ดึงข้อมูล
df_profile = load_data(CSV_URLS["profile"])
df_training = load_data(CSV_URLS["training"])
df_license = load_data(CSV_URLS["license"])

# เลือกบุคลากร
user_options = df_profile.set_index("เลขบัตรประชาชน")["ชื่อ สกุล"].to_dict()
selected_id = str(st.sidebar.selectbox("เลือกบุคลากร:", options=user_options.keys(), format_func=lambda x: user_options[x]))

menu = st.sidebar.radio("เมนู", ["ข้อมูลทั่วไป", "ประวัติการฝึกอบรม", "ใบประกอบวิชาชีพ"])

# กรองข้อมูล
def get_filtered_data(df, target_id):
    # เปลี่ยนคอลัมน์เลขบัตรให้เป็น string เพื่อเทียบค่า
    df["เลขบัตรประชาชน"] = df["เลขบัตรประชาชน"].astype(str).str.strip()
    return df[df["เลขบัตรประชาชน"] == target_id.strip()]

st.header(f"ข้อมูลของ: {user_options[selected_id]}")

if menu == "ข้อมูลทั่วไป":
    df_p = get_filtered_data(df_profile, selected_id)
    st.write(df_p.iloc[0].T if not df_p.empty else "ไม่พบข้อมูล")

elif menu == "ประวัติการฝึกอบรม":
    df_t = get_filtered_data(df_training, selected_id)
    if not df_t.empty:
        for i in range(len(df_t)):
            st.subheader(f"รายการที่ {i+1}")
            st.write(df_t.iloc[i].T)
            st.divider()
    else:
        st.write("ไม่พบข้อมูลการฝึกอบรม")

elif menu == "ใบประกอบวิชาชีพ":
    df_l = get_filtered_data(df_license, selected_id)
    if not df_l.empty:
        for i in range(len(df_l)):
            st.subheader(f"รายการที่ {i+1}")
            st.write(df_l.iloc[i].T)
            st.divider()
    else:
        st.write("ไม่พบข้อมูลใบประกอบวิชาชีพ")