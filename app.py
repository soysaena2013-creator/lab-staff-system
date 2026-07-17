import streamlit as st
import pandas as pd

# เพิ่มลิงก์สำหรับ ExamResults ในนี้
CSV_URLS = {
    "profile": "https://docs.google.com/spreadsheets/d/e/2PACX-1vRNwMjfrUFFtELYMwByAwtV5oWDe0enW7TzTJW_Dl-hjIbxPlCg9LEMahNEc4EgZHvr-XNFIcHPdfNQ/pub?gid=0&single=true&output=csv",
    "training": "https://docs.google.com/spreadsheets/d/e/2PACX-1vRNwMjfrUFFtELYMwByAwtV5oWDe0enW7TzTJW_Dl-hjIbxPlCg9LEMahNEc4EgZHvr-XNFIcHPdfNQ/pub?gid=1403147110&single=true&output=csv",
    "license": "https://docs.google.com/spreadsheets/d/e/2PACX-1vRNwMjfrUFFtELYMwByAwtV5oWDe0enW7TzTJW_Dl-hjIbxPlCg9LEMahNEc4EgZHvr-XNFIcHPdfNQ/pub?gid=974412732&single=true&output=csv",
    "vaccine": "https://docs.google.com/spreadsheets/d/e/2PACX-1vRNwMjfrUFFtELYMwByAwtV5oWDe0enW7TzTJW_Dl-hjIbxPlCg9LEMahNEc4EgZHvr-XNFIcHPdfNQ/pub?gid=1712919650&single=true&output=csv",
    "health": "https://docs.google.com/spreadsheets/d/e/2PACX-1vRNwMjfrUFFtELYMwByAwtV5oWDe0enW7TzTJW_Dl-hjIbxPlCg9LEMahNEc4EgZHvr-XNFIcHPdfNQ/pub?gid=2146590874&single=true&output=csv",
    "exam": "https://docs.google.com/spreadsheets/d/e/2PACX-1vRNwMjfrUFFtELYMwByAwtV5oWDe0enW7TzTJW_Dl-hjIbxPlCg9LEMahNEc4EgZHvr-XNFIcHPdfNQ/pub?gid=190743628&single=true&output=csv"
}

@st.cache_data(ttl=0) 
def load_data(url):
    df = pd.read_csv(url, dtype=str) 
    df.columns = df.columns.str.strip()
    return df

st.markdown("### ระบบข้อมูลบุคลากร กลุ่มงานเทคนิคการแพทย์")

# โหลดข้อมูลทั้งหมด
df_profile = load_data(CSV_URLS["profile"])
df_training = load_data(CSV_URLS["training"])
df_license = load_data(CSV_URLS["license"])
df_vaccine = load_data(CSV_URLS["vaccine"])
df_health = load_data(CSV_URLS["health"])
df_exam = load_data(CSV_URLS["exam"])

user_options = df_profile.set_index("เลขบัตรประชาชน")["ชื่อ สกุล"].to_dict()
selected_id = st.sidebar.selectbox("เลือกบุคลากร:", options=list(user_options.keys()), format_func=lambda x: user_options[x])

# เพิ่มเมนู Exam Results
menu = st.sidebar.radio("เมนู", ["ข้อมูลทั่วไป", "ประวัติการฝึกอบรม", "ใบประกอบวิชาชีพ", "ประวัติการรับวัคซีน", "ประวัติการตรวจสุขภาพประจำปี", "ผลการสอบ (Exam Results)"])

st.header(f"ข้อมูลของ: {user_options[selected_id]}")

# ฟังก์ชันแสดงผลทั่วไป
def show_data(df, title):
    filtered_df = df[df["เลขบัตรประชาชน"] == selected_id]
    if not filtered_df.empty:
        for i in range(len(filtered_df)):
            st.write(filtered_df.iloc[i].T)
            st.divider()
    else:
        st.write(f"ไม่พบข้อมูล{title}")

# แสดงผลตามเมนู
if menu == "ข้อมูลทั่วไป":
    df_p = df_profile[df_profile["เลขบัตรประชาชน"] == selected_id]
    if not df_p.empty: st.write(df_p.iloc[0].T)
    else: st.write("ไม่พบข้อมูล")
elif menu == "ประวัติการฝึกอบรม": show_data(df_training, "การฝึกอบรม")
elif menu == "ใบประกอบวิชาชีพ": show_data(df_license, "ใบประกอบวิชาชีพ")
elif menu == "ประวัติการรับวัคซีน": show_data(df_vaccine, "การรับวัคซีน")
elif menu == "ประวัติการตรวจสุขภาพประจำปี": show_data(df_health, "การตรวจสุขภาพ")
elif menu == "ผลการสอบ (Exam Results)": show_data(df_exam, "ผลการสอบ")