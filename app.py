import streamlit as st
import pandas as pd

CSV_URLS = {
    "profile": "https://docs.google.com/spreadsheets/d/e/2PACX-1vRNwMjfrUFFtELYMwByAwtV5oWDe0enW7TzTJW_Dl-hjIbxPlCg9LEMahNEc4EgZHvr-XNFIcHPdfNQ/pub?gid=0&single=true&output=csv",
    "training": "https://docs.google.com/spreadsheets/d/e/2PACX-1vRNwMjfrUFFtELYMwByAwtV5oWDe0enW7TzTJW_Dl-hjIbxPlCg9LEMahNEc4EgZHvr-XNFIcHPdfNQ/pub?gid=1403147110&single=true&output=csv",
    "license": "https://docs.google.com/spreadsheets/d/e/2PACX-1vRNwMjfrUFFtELYMwByAwtV5oWDe0enW7TzTJW_Dl-hjIbxPlCg9LEMahNEc4EgZHvr-XNFIcHPdfNQ/pub?gid=974412732&single=true&output=csv"
}

@st.cache_data(ttl=0) 
def load_data(url):
    df = pd.read_csv(url, dtype=str) # บังคับอ่านข้อมูลทุกอย่างเป็น String เพื่อรักษาเลข 0 ไว้
    df.columns = df.columns.str.strip()
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
if menu == "ข้อมูลทั่วไป":
    df_p = df_profile[df_profile["เลขบัตรประชาชน"] == selected_id]
    if not df_p.empty:
        st.write(df_p.iloc[0].T)
    else:
        st.write("ไม่พบข้อมูล")

elif menu == "ประวัติการฝึกอบรม":
    df_t = df_training[df_training["เลขบัตรประชาชน"] == selected_id]
    if not df_t.empty:
        for i in range(len(df_t)):
            st.write(df_t.iloc[i].T)
            st.divider()
    else:
        st.write("ไม่พบข้อมูลการฝึกอบรม")

elif menu == "ใบประกอบวิชาชีพ":
    df_l = df_license[df_license["เลขบัตรประชาชน"] == selected_id]
    if not df_l.empty:
        for i in range(len(df_l)):
            st.write(df_l.iloc[i].T)
            st.divider()
    else:
        st.write("ไม่พบข้อมูลใบประกอบวิชาชีพ")