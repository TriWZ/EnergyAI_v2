
import streamlit as st
import pandas as pd
import os
from openai import OpenAI

st.set_page_config(page_title="Triphorium AI Hub", layout="wide")
st.title("Triphorium 智能能效总控平台（AI Hub）")

# API Key 输入或从环境读取
api_key = st.text_input("请输入 OpenAI API Key", type="password")
if not api_key:
    api_key = os.getenv("OPENAI_API_KEY")

client = None
if api_key:
    client = OpenAI(api_key=api_key)

# 上传数据
uploaded_data = st.file_uploader("上传建筑或集群数据（CSV，需包含 timestamp、electricity_kwh、co2_tons 等字段）", type="csv", key="hub_upload")

if uploaded_data:
    df = pd.read_csv(uploaded_data)
    st.success(f"成功加载数据，共 {df.shape[0]} 行。")

    # 数据预览
    with st.expander("📋 数据预览"):
        st.dataframe(df.head())

    # KPI 展示
    if 'electricity_kwh' in df.columns and 'co2_tons' in df.columns:
        kwh_total = df['electricity_kwh'].sum()
        co2_total = df['co2_tons'].sum()
        st.metric("累计用电量 (kWh)", f"{kwh_total:,.0f}")
        st.metric("累计碳排放 (吨)", f"{co2_total:,.2f}")

    # 四类能耗曲线图
    st.subheader("📊 四类能源趋势图")
    df['timestamp'] = pd.to_datetime(df['timestamp'])
    df = df.sort_values('timestamp')
    df_monthly = df.set_index('timestamp').resample('M').agg({
        'electricity_kwh': 'sum',
        'water_tons': 'sum',
        'gas_m3': 'sum',
        'co2_tons': 'sum'
    }).reset_index()
    st.line_chart(df_monthly.set_index('timestamp'))

# 模块导航
st.subheader("🧭 模块导航")
cols = st.columns(5)
modules = [
    ("Forecast", "用电趋势预测"),
    ("Anomaly", "异常检测"),
    ("Classification", "等级预测+建议"),
    ("Clustering", "聚类分析"),
    ("Strategy", "策略模拟与ROI"),
    ("Optimizer", "策略组合优化"),
    ("Controller", "AI控制模拟器"),
    ("Carbon", "碳排趋势分析"),
    ("Twin", "数字孪生模拟"),
    ("Assets", "集群资产图谱")
]
for i, (file, desc) in enumerate(modules):
    with cols[i % 5]:
        st.markdown(f"### [{file}](./{file})")
        st.caption(desc)

# GPT 分析建议
if client and uploaded_data is not None:
    try:
        col_str = ", ".join(df.columns[:6])
        prompt = f"""
你是建筑能源平台的 AI 助手。上传数据包含列：{col_str}。
请判断：
1. 建议优先使用哪些模块分析；
2. 如需节能或 ESG 报告，应启动哪些功能；
3. 有哪些潜在风险或异常需警示。
"""
        response = client.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "你是 Triphorium 平台的能效分析顾问"},
                {"role": "user", "content": prompt}
            ]
        )
        msg = response.choices[0].message.content
        st.subheader("💡 GPT AI 总体建议")
        st.markdown(msg)
    except Exception as e:
        st.error(f"GPT 分析失败：{e}")
