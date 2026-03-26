import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="智护农安 · 政府公益监管端", page_icon="🏛️", layout="wide")

st.title("🏛️ 智护农安 · 政府公益监管端")
st.markdown("**政策性农业保险补贴透明看板** —— 中央+地方财政联合补贴 · 服务乡村振兴")

# 公益核心指标
col1, col2, col3 = st.columns(3)
col1.metric("本年度补贴总额", "¥1.65亿", "广西试点")
col2.metric("已智护小农户", "28.4万户", "↑ 2025")
col3.metric("覆盖耕地面积", "312万亩", "全覆盖")

st.divider()

# 补贴发放区块链记录（体现公益透明）
st.subheader("🧾 政府补贴发放区块链记录（实时上链）")
data = pd.DataFrame({
    "发放时间": ["2026-03-24 14:30", "2026-03-22 09:15", "2026-03-20 16:45"],
    "受益主体": ["武鸣县张三（散户）", "灵山县李四合作社", "扶绥县王五家庭农场"],
    "作物类型": ["沃柑", "甘蔗", "火龙果"],
    "补贴金额": [12480, 45600, 28900],
    "补贴比例": ["80%（政府）", "80%（政府）", "80%（政府）"],
    "状态": ["✅ 已上链", "✅ 已上链", "✅ 已上链"]
})
st.dataframe(data, use_container_width=True, hide_index=True)

st.success("所有补贴资金均通过区块链公开透明，确保每一分钱都用于乡村振兴和粮食安全保障")

# 公益影响可视化
st.subheader("🌱 公益帮扶效果")
fig = px.bar(
    x=["已惠及农户", "覆盖耕地", "减贫贡献"],
    y=[284000, 3120000, 85],
    text=[284000, "312万亩", "85%"],
    title="2025年智护农安公益成果",
    color_discrete_sequence=["#166534"]
)
fig.update_traces(textposition='auto')
st.plotly_chart(fig, use_container_width=True)

st.caption("数据来源：政策性农业保险试点统计 · 智护农安平台实时汇总")
