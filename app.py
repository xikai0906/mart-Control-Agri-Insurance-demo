import streamlit as st
import pandas as pd
from datetime import datetime

# 页面配置
st.set_page_config(
    page_title="智护农安 - 政府补贴公益农险平台",
    page_icon="🌾🛡️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 自定义CSS（公益绿色+蓝色主题）
st.markdown("""
    <style>
    .main-header {font-size: 3rem; color: #1E3A8A; text-align: center; padding: 2rem 0; font-weight: bold;}
    .sub-header {font-size: 1.5rem; color: #166534; text-align: center; padding-bottom: 2rem;}
    .feature-box {background-color: #F1F8E9; padding: 1.5rem; border-radius: 10px; border-left: 5px solid #66BB6A; margin: 1rem 0; min-height: 180px; display: flex; flex-direction: column;}
    .feature-box h3 {margin-top: 0; margin-bottom: 1rem; color: #166534;}
    .feature-box p {flex-grow: 1; margin: 0; color: #555; line-height: 1.6;}
    .subsidy-highlight {background: linear-gradient(90deg, #166534, #1E3A8A); color: white; padding: 1rem; border-radius: 10px; text-align: center; margin: 1rem 0;}
    </style>
""", unsafe_allow_html=True)

# 主页标题
st.markdown('<div class="main-header">🌾 智护农安</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-header">政府补贴 · 公益农险 · AI智能守护</div>', unsafe_allow_html=True)
st.markdown("**助力乡村振兴 · 保障粮食安全 · 精准帮扶小农户**")

# 公益补贴醒目看板
st.markdown('<div class="subsidy-highlight">🏛️ 中央+地方财政联合补贴 · 农户仅需支付20% · 80%由政府公益承担</div>', unsafe_allow_html=True)

col1, col2, col3, col4 = st.columns(4)
with col1:
    st.metric("已智护农户", "1,472万户", "↑ 2025")
with col2:
    st.metric("中央财政补贴", "¥517亿元", "2025年度")
with col3:
    st.metric("政府补贴比例", "80%", "农户仅需20%")
with col4:
    st.metric("智护耕地", "3.8亿亩", "全覆盖")

st.divider()

# 顶部导航栏（已修复公益端跳转路径）
st.markdown("### 🧭 快速导航")
nav_col1, nav_col2, nav_col3, nav_col4, nav_col5 = st.columns(5)
with nav_col1:
    if st.button("👨‍🌾 农户理赔平台", use_container_width=True, type="primary"):
        st.switch_page("pages/1_农户端.py")
    st.caption("天气预警 | 价格预测 | 理赔申请")
with nav_col2:
    if st.button("🏢 保险公司管理平台", use_container_width=True, type="primary"):
        st.switch_page("pages/2_保险公司端.py")
    st.caption("风险评估 | 智能审核 | 数据分析")
with nav_col3:
    if st.button("🤖 AI演示平台", use_container_width=True, type="primary"):
        st.switch_page("pages/3_AI演示.py")
    st.caption("灾害识别 | 价格预测 | 自动理赔")
with nav_col4:
    if st.button("📊 量化模型", use_container_width=True, type="primary"):
        st.switch_page("pages/4_量化模型后台.py")
    st.caption("期权定价 | 核保理赔 | 风险分析")
with nav_col5:
    if st.button("🏛️ 政府公益端", use_container_width=True, type="secondary"):
        st.switch_page("pages/5_gov_public_welfare.py")   # ← 关键修复点：必须是这个英文文件名
    st.caption("补贴透明 | 监管看板 | 区块链记录")

st.divider()

# 项目介绍（每个卡片都渗透公益补贴）
col1, col2, col3 = st.columns(3)
with col1:
    st.markdown("""
    <div class="feature-box">
        <h3>🌡️ 天气理赔</h3>
        <p>AI实时监测极端天气，自动触发理赔预警，80%政府公益补贴保障农业生产安全</p>
    </div>
    """, unsafe_allow_html=True)
with col2:
    st.markdown("""
    <div class="feature-box">
        <h3>💰 价格理赔</h3>
        <p>智能预测农产品价格波动，价格低于保险阈值自动理赔，公益补贴助力小农户稳定收入</p>
    </div>
    """, unsafe_allow_html=True)
with col3:
    st.markdown("""
    <div class="feature-box">
        <h3>🤖 AI风控</h3>
        <p>多维数据交叉验证，提升理赔效率，防范虚假理赔风险，服务乡村振兴战略</p>
    </div>
    """, unsafe_allow_html=True)

# 核心功能介绍（每个Tab、每条内容都融入公益）
st.header("📊 核心功能")
tab1, tab2, tab3, tab4 = st.tabs(["农户端", "保险公司端", "AI技术", "量化模型"])
with tab1:
    st.subheader("👨‍🌾 农户端功能（80%政府补贴）")
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("""
        **30天气象预警Dashboard**
        - 🌦️ 未来30天极端天气预测
        - ⚠️ 极端高温/暴雨概率分析
        - 
