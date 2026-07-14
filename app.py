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
    df = pd.read_csv(CSV_URLS[key])
    # ทำความสะอาดข้อมูล: เปลี่ยนเลขบัตรให้เป็น string และตัดช่องว่างออกทั้งหมด
    df["เลขบัตรประชาชน"] = df["เลขบัตรประชาชน"].astype(str).str.strip()
    return df

st.markdown("### ระบบข้อมูลบุคลากร กลุ่มงานเทคนิคการแพทย์")

df_profile = load_data("profile")
df_training = load_data("training")
df_license = load_data("license")

# เลือกบุคลากร
user_options = df_profile.set_index("เลขบัตรประชาชน")["ชื่อ สกุล"].to_dict()
selected_id = st.sidebar.selectbox("เลือกบุคลากร:", options=user_options.keys(), format_func=lambda x: user_options[x])
selected_name = user_options[selected_id]

menu = st.sidebar.radio("เมนู", ["ข้อมูลทั่วไป", "ประวัติการฝึกอบรม", "ใบประกอบวิชาชีพ"])

# กรองข้อมูลโดยเทียบเลขบัตรที่ทำความสะอาดแล้ว
df_p = df_profile[df_profile["เลขบัตรประชาชน"] == selected_id.strip()]
df_t = df_training[df_training["เลขบัตรประชาชน"] == selected_id.strip()]
df_l = df_license[df_license["เลขบัตรประชาชน"] == selected_id.strip()]

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
        st.write("ไม่พบข้อมูลการฝึกอบรม (โปรดตรวจสอบเลขบัตรประชาชนในตาราง training)")

elif menu == "ใบประกอบวิชาชีพ":
    if not df_l.empty:
        for i in range(len(df_l)):
            st.subheader(f"รายการที่ {i+1}")
            st.write(df_l.iloc[i].T)
            st.divider()
    else:
        st.write("ไม่พบข้อมูลใบประกอบวิชาชีพ")