import streamlit as st
import pandas as pd
from datetime import datetime

# 页面配置
st.set_page_config(
    page_title="智控农险 - AI协同农业保险平台",
    page_icon="🌾",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 自定义CSS样式
st.markdown("""
    <style>
    .main-header {
        font-size: 3rem;
        color: #2E7D32;
        text-align: center;
        padding: 2rem 0;
        font-weight: bold;
    }
    .sub-header {
        font-size: 1.5rem;
        color: #558B2F;
        text-align: center;
        padding-bottom: 2rem;
    }
    .feature-box {
        background-color: #F1F8E9;
        padding: 1.5rem;
        border-radius: 10px;
        border-left: 5px solid #66BB6A;
        margin: 1rem 0;
    }
    </style>
""", unsafe_allow_html=True)

# 主页标题
st.markdown('<div class="main-header">🌾 智控农险</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-header">AI协同搭建农业"保险+衍生品"风险隔离防火墙</div>', unsafe_allow_html=True)

# 分隔线
st.divider()

# 顶部导航栏
st.markdown("### 🧭 快速导航")
nav_col1, nav_col2, nav_col3, nav_col4 = st.columns(4)

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

st.divider()

# 项目介绍
col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("""
    <div class="feature-box">
        <h3>🌡️ 天气理赔</h3>
        <p>AI实时监测极端天气，自动触发理赔预警，保障农业生产安全</p>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div class="feature-box">
        <h3>💰 价格理赔</h3>
        <p>智能预测农产品价格波动，价格低于保险阈值自动理赔</p>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown("""
    <div class="feature-box">
        <h3>🤖 AI风控</h3>
        <p>多维数据交叉验证，提升理赔效率，防范虚假理赔风险</p>
    </div>
    """, unsafe_allow_html=True)

# 核心功能介绍
st.header("📊 核心功能")

# Tab导航
tab1, tab2, tab3, tab4 = st.tabs(["农户端", "保险公司端", "AI技术", "量化模型"])

with tab1:
    st.subheader("👨‍🌾 农户端功能")
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        **30天气象预警Dashboard**
        - 🌦️ 未来30天极端天气预测
        - ⚠️ 极端高温/暴雨概率分析
        - 🔔 风险日历热力图
        - 📊 综合风险等级评估
        
        **价格趋势预测**
        - 📈 历史价格走势
        - 🤖 LSTM AI价格预测
        - 💡 理赔条件提示
        """)
    
    with col2:
        st.markdown("""
        **智能理赔申请**
        - 📝 在线提交理赔
        - 📷 AI识别受灾照片
        - ⏱️ 实时查看进度
        - ⚡ 2分钟快速到账
        
        **我的保单管理**
        - 📄 保单信息查询
        - 💳 保费缴纳记录
        - 📊 理赔历史统计
        """)

with tab2:
    st.subheader("🏢 保险公司端功能")
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        **风险评估看板**
        - 🗺️ 区域风险热力图
        - 📊 30天赔付趋势预测
        - 🎯 高风险预警
        
        **智能理赔审核**
        - ✅ AI交叉验证
        - 🔍 多维数据融合
        - ⚡ 批量快速审核
        """)
    
    with col2:
        st.markdown("""
        **数据分析中心**
        - 📈 保费收入统计
        - 💰 赔付率分析
        - 👥 用户行为洞察
        
        **产品管理系统**
        - 🎨 保险产品设计
        - 💵 定价模型优化
        - 🔧 参数动态调整
        """)

with tab3:
    st.subheader("🤖 AI技术应用")
    st.markdown("""
    **1️⃣ 多维数据融合验证**
    - 气象数据 + 遥感影像 + 市场数据
    - 交叉验证理赔真实性
    - 识别准确率提升至92%
    
    **2️⃣ 实时动态跟踪对冲**
    - LSTM神经网络价格预测
    - 基差风险管理
    - 场外期权优化设计
    
    **3️⃣ 数字化流程提速**
    - 自动化风险评估
    - 区块链智能合约
    - 理赔周期缩短99.5%
    
    **4️⃣ 场景化风险教育**
    - VR/AR沉浸式体验
    - 智能客服解答
    - 个性化风险建议
    """)

with tab4:
    st.subheader("📊 量化模型后台")
    st.markdown("""
    **💰 保险+期权损益分析**
    - 亚式看跌期权定价模型
    - 蒙特卡洛路径模拟
    - 多情景损益分析
    - 敏感性分析工具
    
    **📈 波动率与保费精算**
    - Black-Scholes期权定价
    - Greeks风险指标分析
    - 不同波动率情景精算
    - 动态保费调整机制
    
    **🎯 智能核保演示**
    - AI多维风险评估
    - 雷达图可视化分析
    - 自动核保决策
    - 电子保单生成
    
    **⚡ 智能理赔演示**
    - AI图像识别演示
    - 卫星数据交叉验证
    - 智能合约自动触发
    - 2分钟极速理赔
    """)

st.divider()

# 项目统计数据
st.header("📈 项目成果")
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(label="调研农户", value="1,037", delta="人")

with col2:
    st.metric(label="覆盖作物", value="15+", delta="种")

with col3:
    st.metric(label="理赔效率提升", value="70%", delta="↑")

with col4:
    st.metric(label="风险识别准确率", value="92%", delta="↑")

# 使用指南
st.header("📖 使用指南")
st.info("""
**快速开始:**
1. 👈 在左侧菜单选择您的身份(农户/保险公司)
2. 🔍 探索各项功能模块
3. 💡 体验AI智能服务

**Demo说明:** 本系统为演示版本,部分数据为模拟生成,仅供参考学习
""")

# 页脚
st.divider()
st.markdown("""
<div style="text-align: center; color: #666; padding: 2rem 0;">
    <p>🎓 广西财经学院 | 智控农险</p>
    <p>📧 联系我们: ysuy5756@gmail.com</p>
</div>
""", unsafe_allow_html=True)
