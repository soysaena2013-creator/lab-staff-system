import streamlit as st
import pandas as pd

# ลิงก์ข้อมูล
CSV_URLS = {
    "profile": "https://docs.google.com/spreadsheets/d/e/2PACX-1vRNwMjfrUFFtELYMwByAwtV5oWDe0enW7TzTJW_Dl-hjIbxPlCg9LEMahNEc4EgZHvr-XNFIcHPdfNQ/pub?gid=0&single=true&output=csv",
    "training": "https://docs.google.com/spreadsheets/d/e/2PACX-1vRNwMjfrUFFtELYMwByAwtV5oWDe0enW7TzTJW_Dl-hjIbxPlCg9LEMahNEc4EgZHvr-XNFIcHPdfNQ/pub?gid=1403147110&single=true&output=csv",
    "license": "https://docs.google.com/spreadsheets/d/e/2PACX-1vRNwMjfrUFFtELYMwByAwtV5oWDe0enW7TzTJW_Dl-hjIbxPlCg9LEMahNEc4EgZHvr-XNFIcHPdfNQ/pub?gid=974412732&single=true&output=csv"
}

# ปรับ TTL เป็น 0 เพื่อไม่ให้ Streamlit เก็บข้อมูลเก่าไว้ (บังคับดึงใหม่เสมอ)
@st.cache_data(ttl=0) 
def load_data(url):
    df = pd.read_csv(url)
    df.columns = df.columns.str.strip()
    # บังคับแปลงเลขบัตรเป็น string ทันทีที่โหลด
    if "เลขบัตรประชาชน" in df.columns:
        df["เลขบัตรประชาชน"] = df["เลขบัตรประชาชน"].astype(str).str.strip()
    return df

st.markdown("### ระบบข้อมูลบุคลากร กลุ่มงานเทคนิคการแพทย์")

df_profile = load_data(CSV_URLS["profile"])
df_training = load_data(CSV_URLS["training"])
df_license = load_data(CSV_URLS["license"])

user_options = df_profile.set_index("เลขบัตรประชาชน")["ชื่อ สกุล"].to_dict()
selected_id = st.sidebar.selectbox("เลือกบุคลากร:", options=list(user_options.keys()), format_func=lambda x: user_options[x])

menu = st.sidebar.radio("เมนู", ["ข้อมูลทั่วไป", "ประวัติการฝึกอบรม", "ใบประกอบวิชาชีพ"])

st.header(f"ข้อมูลของ: {user_options[selected_id]}")

# กรองข้อมูล
elif menu == "ข้อมูลทั่วไป":
    if not df_p.empty:
        # ดึงข้อมูลมาเป็น Series
        data_to_show = df_p.iloc[0].T
        
        # ตรวจสอบว่ามีคอลัมน์ "เบอร์โทรศัพท์" หรือไม่
        if "เบอร์โทรศัพท์" in data_to_show.index:
            phone_val = str(data_to_show["เบอร์โทรศัพท์"])
            # ถ้าเลขเบอร์โทรสั้นกว่า 10 หลัก ให้เติม 0 ข้างหน้า
            if len(phone_val) < 10:
                data_to_show["เบอร์โทรศัพท์"] = phone_val.zfill(10)
        
        st.write(data_to_show)

elif menu == "ประวัติการฝึกอบรม":
    df_t = df_training[df_training["เลขบัตรประชาชน"] == selected_id]
    for i in range(len(df_t)):
        st.write(df_t.iloc[i].T)
        st.divider()

elif menu == "ใบประกอบวิชาชีพ":
    df_l = df_license[df_license["เลขบัตรประชาชน"] == selected_id]
    if not df_l.empty:
        for i in range(len(df_l)):
            st.write(df_l.iloc[i].T)
            st.divider()
    else:
        st.write("ไม่พบข้อมูลใบประกอบวิชาชีพ")