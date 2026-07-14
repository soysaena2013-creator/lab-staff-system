import streamlit as st
import pandas as pd

# ลิงก์ข้อมูลจาก Google Sheets
CSV_URLS = {
    "profile": "https://docs.google.com/spreadsheets/d/e/2PACX-1vRNwMjfrUFFtELYMwByAwtV5oWDe0enW7TzTJW_Dl-hjIbxPlCg9LEMahNEc4EgZHvr-XNFIcHPdfNQ/pub?gid=0&single=true&output=csv",
    "training": "https://docs.google.com/spreadsheets/d/e/2PACX-1vRNwMjfrUFFtELYMwByAwtV5oWDe0enW7TzTJW_Dl-hjIbxPlCg9LEMahNEc4EgZHvr-XNFIcHPdfNQ/pub?gid=1403147110&single=true&output=csv",
    "license": "https://docs.google.com/spreadsheets/d/e/2PACX-1vRNwMjfrUFFtELYMwByAwtV5oWDe0enW7TzTJW_Dl-hjIbxPlCg9LEMahNEc4EgZHvr-XNFIcHPdfNQ/pub?gid=974412732&single=true&output=csv"
}

@st.cache_data(ttl=600)
def load_data(key):
    df = pd.read_csv(CSV_URLS[key])
    # ตัดช่องว่างหน้า-หลังชื่อคอลัมน์ทิ้งทั้งหมด
    df.columns = df.columns.str.strip()
    return df

st.markdown("### ระบบข้อมูลบุคลากร กลุ่มงานเทคนิคการแพทย์")

# ดึงข้อมูล
df_profile = load_data("profile")
df_training = load_data("training")
df_license = load_data("license")

# เลือกบุคลากร
user_options = df_profile.set_index("เลขบัตรประชาชน")["ชื่อ สกุล"].to_dict()
selected_id = str(st.sidebar.selectbox("เลือกบุคลากร:", options=user_options.keys(), format_func=lambda x: user_options[x]))
selected_name = user_options[selected_id]

# เมนู
menu = st.sidebar.radio("เมนู", ["ข้อมูลทั่วไป", "ประวัติการฝึกอบรม", "ใบประกอบวิชาชีพ"])

# ฟังก์ชันช่วยกรองโดยหาคอลัมน์ชื่อ "เลขบัตรประชาชน" ในตารางนั้นๆ
def filter_by_id(df, id_val):
    # หาคอลัมน์ที่มีคำว่า "เลขบัตร"
    id_col = [col for col in df.columns if "เลขบัตร" in col]
    if id_col:
        return df[df[id_col[0]].astype(str).str.strip() == id_val.strip()]
    return pd.DataFrame()

# กรองข้อมูล
df_p = filter_by_id(df_profile, selected_id)
df_t = filter_by_id(df_training, selected_id)
df_l = filter_by_id(df_license, selected_id)

# แสดงผล
st.header(f"ข้อมูลของ: {selected_name}")

if menu == "ข้อมูลทั่วไป":
    st.write(df_p.iloc[0].T if not df_p.empty else "ไม่พบข้อมูล")

elif menu == "ประวัติการฝึกอบรม":
    if not df_t.empty:
        for i in range(len(df_t)):
            st.subheader(f"รายการที่ {i+1}")
            st.write(df_t.iloc[i].T)
            st.divider()
    else:
        st.write("ไม่พบข้อมูลการฝึกอบรม")

elif menu == "ใบประกอบวิชาชีพ":
    if not df_l.empty:
        for i in range(len(df_l)):
            st.subheader(f"รายการที่ {i+1}")
            st.write(df_l.iloc[i].T)
            st.divider()
    else:
        st.write("ไม่พบข้อมูลใบประกอบวิชาชีพ")