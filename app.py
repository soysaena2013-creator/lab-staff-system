import streamlit as st
import pandas as pd

# ลิงก์ข้อมูล
CSV_URLS = {
    "profile": "https://docs.google.com/spreadsheets/d/e/2PACX-1vRNwMjfrUFFtELYMwByAwtV5oWDe0enW7TzTJW_Dl-hjIbxPlCg9LEMahNEc4EgZHvr-XNFIcHPdfNQ/pub?gid=0&single=true&output=csv",
    "training": "https://docs.google.com/spreadsheets/d/e/2PACX-1vRNwMjfrUFFtELYMwByAwtV5oWDe0enW7TzTJW_Dl-hjIbxPlCg9LEMahNEc4EgZHvr-XNFIcHPdfNQ/pub?gid=949946920&single=true&output=csv",
    "license": "https://docs.google.com/spreadsheets/d/e/2PACX-1vRNwMjfrUFFtELYMwByAwtV5oWDe0enW7TzTJW_Dl-hjIbxPlCg9LEMahNEc4EgZHvr-XNFIcHPdfNQ/pub?gid=974412732&single=true&output=csv"
}

@st.cache_data(ttl=600)
def load_data(key):
    return pd.read_csv(CSV_URLS[key])

st.markdown("### ระบบข้อมูลบุคลากร กลุ่มงานเทคนิคการแพทย์")

# ดึงข้อมูล
df_profile = load_data("profile")
df_training = load_data("training")
df_license = load_data("license")

# เลือกบุคลากร
user_options = df_profile.set_index("เลขบัตรประชาชน")["ชื่อ สกุล"].to_dict()
selected_id = st.sidebar.selectbox("เลือกบุคลากร:", options=user_options.keys(), format_func=lambda x: user_options[x])
selected_name = user_options[selected_id]

menu = st.sidebar.radio("เมนู", ["ข้อมูลทั่วไป", "ประวัติการฝึกอบรม", "ใบประกอบวิชาชีพ"])

# กรองข้อมูล
df_p = df_profile[df_profile["เลขบัตรประชาชน"].astype(str) == str(selected_id)]
df_t = df_training[df_training["เลขบัตรประชาชน"].astype(str) == str(selected_id)]
df_l = df_license[df_license["เลขบัตรประชาชน"].astype(str) == str(selected_id)]

# แสดงผลแบบกำหนดความสูงให้พอดี
st.header(f"ข้อมูลของ: {selected_name}")

# ใช้ container เพื่อแบ่งพื้นที่ให้ดูเต็มหน้าจอ
with st.container(height=400): # กำหนดความสูง 400px เพื่อให้ไม่ล้นหน้าและใช้พื้นที่คุ้มค่า
    if menu == "ข้อมูลทั่วไป":
        st.dataframe(df_p, hide_index=True, use_container_width=True)
    elif menu == "ประวัติการฝึกอบรม":
        st.dataframe(df_t, hide_index=True, use_container_width=True)
    elif menu == "ใบประกอบวิชาชีพ":
        st.dataframe(df_l, hide_index=True, use_container_width=True)