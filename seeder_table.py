import streamlit as st
import pandas as pd
from io import BytesIO

# ========== 页面基础设置 ==========
st.set_page_config(
    page_title="播种机机型选择",
    page_icon="🌾",
    layout="wide"
)

# ========== 机型数据【在这里修改你的真实机型】 ==========
data = [
    {"机型":"德沃2BMF-6", "行数":6, "播种行距(cm)":40, "配套马力":60, "适用作物":"玉米"},
    {"机型":"德沃2BMF-8", "行数":8, "播种行距(cm)":40, "配套马力":80, "适用作物":"玉米"},
    {"机型":"德沃2BS-4",  "行数":4, "播种行距(cm)":30, "配套马力":40, "适用作物":"大豆"},
    {"机型":"德沃2BS-6",  "行数":6, "播种行距(cm)":30, "配套马力":55, "适用作物":"大豆"},
]
df = pd.DataFrame(data)

# ========== 页面标题和查询区 ==========
st.title("播种机机型选择")
search_text = st.text_input("输入机型/作物查询：")

# 三个按钮并排
col1, col2, col3 = st.columns(3)
with col1:
    btn_query = st.button("查询")
with col2:
    btn_sort = st.button("整理表")
with col3:
    btn_export = st.button("导出Excel")

# ========== 业务逻辑 ==========
show_df = df.copy()
if btn_query:
    if search_text:
        mask = show_df.apply(lambda x: search_text.lower() in str(x).lower(), axis=1)
        show_df = show_df[mask]
    st.success("查询完成")

if btn_sort:
    # 整理表：按配套马力从小到大排序
    show_df = show_df.sort_values("配套马力", ascending=True)
    st.success("表格已整理排序")

if btn_export:
    output = BytesIO()
    with pd.ExcelWriter(output, engine='openpyxl') as writer:
        show_df.to_excel(writer, index=False, sheet_name="播种机机型")
    excel_data = output.getvalue()
    st.download_button(
        label="点击下载Excel文件",
        data=excel_data,
        file_name="播种机机型表.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )
    st.success("Excel文件已生成，请点按钮下载")

# ========== 展示表格 ==========
st.subheader("机型列表")
st.dataframe(show_df, use_container_width=True)