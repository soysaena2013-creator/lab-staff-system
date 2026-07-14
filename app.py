import streamlit as st
import pandas as pd

CSV_URLS = {
    "profile": "https://docs.google.com/spreadsheets/d/e/2PACX-1vRNwMjfrUFFtELYMwByAwtV5oWDe0enW7TzTJW_Dl-hjIbxPlCg9LEMahNEc4EgZHvr-XNFIcHPdfNQ/pub?gid=0&single=true&output=csv",
    "training": "https://docs.google.com/spreadsheets/d/e/2PACX-1vRNwMjfrUFFtELYMwByAwtV5oWDe0enW7TzTJW_Dl-hjIbxPlCg9LEMahNEc4EgZHvr-XNFIcHPdfNQ/pub?gid=1403147110&single=true&output=csv",
    "license": "https://docs.google.com/spreadsheets/d/e/2PACX-1vRNwMjfrUFFtELYMwByAwtV5oWDe0enW7TzTJW_Dl-hjIbxPlCg9LEMahNEc4EgZHvr-XNFIcHPdfNQ/pub?gid=974412732&single=true&output=csv"
}

@st.cache_data(ttl=600)
def load_data(key):
    return pd.read_csv(CSV_URLS[key])

st.markdown("### ระบบข้อมูลบุคลากร กลุ่มงานเทคนิคการแพทย์")

df_profile = load_data("profile")
df_training = load_data("training")
df_license = load_data("license")

# ใช้โครงสร้างเดิมที่คุณมั่นใจว่าทำงานได้
user_options = df_profile.set_index("เลขบัตรประชาชน")["ชื่อ สกุล"].to_dict()
selected_id = st.sidebar.selectbox("เลือกบุคลากร:", options=user_options.keys(), format_func=lambda x: user_options[x])
selected_name = user_options[selected_id]

menu = st.sidebar.radio("เมนู", ["ข้อมูลทั่วไป", "ประวัติการฝึกอบรม", "ใบประกอบวิชาชีพ"])

# กรองข้อมูล (โครงสร้างเดิม)
df_p = df_profile[df_profile["เลขบัตรประชาชน"].astype(str) == str(selected_id)]
df_t = df_training[df_training["เลขบัตรประชาชน"].astype(str) == str(selected_id)]

# ส่วนใบประกอบฯ: เพิ่มการแปลง type ให้ตรงกันเป๊ะเพื่อแก้ปัญหาหาข้อมูลไม่เจอ
df_license["เลขบัตรประชาชน"] = df_license["เลขบัตรประชาชน"].astype(str)
df_l = df_license[df_license["เลขบัตรประชาชน"] == str(selected_id)]

if menu == "ข้อมูลทั่วไป":
    st.header(f"ข้อมูลของ: {selected_name}")
    st.dataframe(df_p, hide_index=True, use_container_width=True)

elif menu == "ประวัติการฝึกอบรม":
    st.header(f"ประวัติการฝึกอบรมของ: {selected_name}")
    st.dataframe(df_t, hide_index=True, use_container_width=True)

elif menu == "ใบประกอบวิชาชีพ":
    st.header(f"ใบประกอบวิชาชีพของ: {selected_name}")
    if not df_l.empty:
        st.dataframe(df_l, hide_index=True, use_container_width=True)
    else:
        st.write("ไม่พบข้อมูลใบประกอบวิชาชีพ (โปรดตรวจสอบว่าเลขบัตรในตารางนี้ตรงกับตารางหลักหรือไม่)")