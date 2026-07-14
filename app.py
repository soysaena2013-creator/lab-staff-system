import streamlit as st
import pandas as pd

# ลิงก์ข้อมูลจาก Google Sheets (Publish to web)
CSV_URLS = {
    "profile": "https://docs.google.com/spreadsheets/d/e/2PACX-1vRNwMjfrUFFtELYMwByAwtV5oWDe0enW7TzTJW_Dl-hjIbxPlCg9LEMahNEc4EgZHvr-XNFIcHPdfNQ/pub?gid=0&single=true&output=csv",
    "training": "https://docs.google.com/spreadsheets/d/e/2PACX-1vRNwMjfrUFFtELYMwByAwtV5oWDe0enW7TzTJW_Dl-hjIbxPlCg9LEMahNEc4EgZHvr-XNFIcHPdfNQ/pub?gid=949946920&single=true&output=csv",
    "license": "https://docs.google.com/spreadsheets/d/e/2PACX-1vRNwMjfrUFFtELYMwByAwtV5oWDe0enW7TzTJW_Dl-hjIbxPlCg9LEMahNEc4EgZHvr-XNFIcHPdfNQ/pub?gid=974412732&single=true&output=csv"
}

@st.cache_data(ttl=600)
def load_data(key):
    return pd.read_csv(CSV_URLS[key])

st.title("ระบบข้อมูลบุคลากร กลุ่มงานเทคนิคการแพทย์")

# เมนูแถบด้านข้าง
menu = st.sidebar.radio("เมนูหลัก", ["ข้อมูลทั่วไป", "ประวัติการฝึกอบรม", "ใบประกอบวิชาชีพ"])

# ส่วนแสดงผลเนื้อหาหลัก
if menu == "ข้อมูลทั่วไป":
    st.header("ข้อมูลทั่วไป")
    df = load_data("profile")
    # เพิ่มช่องค้นหาข้อมูล
    search_term = st.text_input("ค้นหาข้อมูลบุคลากร")
    if search_term:
        df = df[df.apply(lambda row: row.astype(str).str.contains(search_term, case=False).any(), axis=1)]
    # ซ่อน Index และแสดงผลเต็มความกว้าง
    st.dataframe(df, hide_index=True, use_container_width=True)

elif menu == "ประวัติการฝึกอบรม":
    st.header("ประวัติการฝึกอบรมและการศึกษาต่อเนื่อง")
    df = load_data("training")
    # ซ่อน Index และแสดงผลเต็มความกว้าง
    st.dataframe(df, hide_index=True, use_container_width=True)

elif menu == "ใบประกอบวิชาชีพ":
    st.header("ใบประกอบวิชาชีพ")
    df = load_data("license")
    # ซ่อน Index และแสดงผลเต็มความกว้าง
    st.dataframe(df, hide_index=True, use_container_width=True)