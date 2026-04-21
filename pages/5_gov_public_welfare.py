import streamlit as st
import pandas as pd
import plotly.express as px
import base64
from pathlib import Path
import time

# ==================== 背景图片加载函数 ====================
def get_base64_of_bin_file(bin_file):
    with open(bin_file, 'rb') as f:
        data = f.read()
    return base64.b64encode(data).decode()

# ==================== 使用 GitHub 仓库中的图片作为背景 ====================
image_path = Path("assets/农民开怀大笑.png")

if image_path.exists():
    bg_base64 = get_base64_of_bin_file(str(image_path))
    background_css = """
    <style>
    .stApp {
        background-image: url("data:image/png;base64,PLACEHOLDER");
        background-size: cover;
        background-position: center;
        background-repeat: no-repeat;
        background-attachment: fixed;
    }
    .stApp::before {
        content: "";
        position: absolute;
        top: 0; left: 0; width: 100%; height: 100%;
        background: rgba(0, 0, 0, 0.78);
        z-index: -1;
    }
    .policy-card {
        background: rgba(255, 255, 255, 0.92) !important;
        border-radius: 12px;
        padding: 20px 24px;
        margin: 15px 0;
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.3);
        color: #1a1a1a !important;
    }
    .policy-card h4 {
        color: #0066cc !important;
        margin-bottom: 12px;
    }
    .policy-card p {
        color: #003300 !important;
    }
    h1, h2, h3 {
        color: #00bfff !important;
        text-shadow: 0 4px 12px rgba(0,0,0,0.95) !important;
    }
    .stMetricLabel, .stMetricValue, .stMetricDelta,
    p strong, .stMarkdown, .stMarkdown p {
        color: #ffffff !important;
        font-weight: bold;
        text-shadow: 0 2px 4px rgba(0,0,0,0.8);
    }
    .stSuccess, .stMarkdown strong {
        color: #ffffff !important;
        font-weight: bold;
    }
    .stDownloadButton button {
        background-color: #00bfff !important;
        color: white !important;
        border-radius: 8px;
    }
    </style>
    """.replace("PLACEHOLDER", bg_base64)
    st.markdown(background_css, unsafe_allow_html=True)
else:
    st.error("❌ 未找到 assets/农民开怀大笑.png，请确认文件已上传到 GitHub 仓库的 assets 文件夹")

st.set_page_config(page_title="智护农安 · 政府公益监管端", page_icon="🏛️", layout="wide")

# ==================== 顶部标题 + 指标 ====================
st.title("🏛️ 智护农安 · 政府公益监管端")
st.markdown("**政策性农业保险补贴透明看板** —— 中央+地方财政联合补贴 · 服务乡村振兴")

col1, col2, col3 = st.columns(3)
col1.metric("本年度补贴总额", "¥1.65亿", "广西试点")
col2.metric("已智护小农户", "28.4万户", "↑ 2025")
col3.metric("覆盖耕地面积", "312万亩", "全覆盖")
st.divider()

# ==================== 政府补贴发放区块链记录 ====================
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

st.markdown("**所有补贴资金均通过区块链公开透明，确保每一分钱都用于乡村振兴和粮食安全保障**")

# ==================== 公益帮扶效果 ====================
st.subheader("🌱 公益帮扶效果")
fig = px.bar(
    x=["已惠及农户", "覆盖耕地", "减贫贡献"],
    y=[284000, 3120000, 85],
    text=[284000, "312万亩", "85%"],
    title="2025年智护农安公益成果",
    color_discrete_sequence=["#00bfff"]
)
fig.update_traces(textposition='auto')
st.plotly_chart(fig, use_container_width=True)
st.divider()

# ====================== 政府公益风险综合解决方案 ======================
st.subheader("🌟 政府公益风险综合解决方案")
st.markdown("**服务整合** · 地域灾害风险监测和预警 + 灾中智能响应 + 灾后高效理赔 + 灾害数据·保险数据融合 → 一键打包生成风险方案")
st.info("本平台已实现全链路服务整合，为政府提供“一站式”区域风险管理打包方案，助力精准补贴、快速响应与乡村振兴")

col_service1, col_service2, col_service3, col_service4 = st.columns(4)

with col_service1:
    st.markdown("""
    <div class="policy-card">
        <h4>🌍 地域灾害风险监测与预警</h4>
        <p>实时整合气象卫星、遥感影像与历史灾害数据，实现县域级高精度风险热力图与30天滚动预警</p>
    </div>
    """, unsafe_allow_html=True)

with col_service2:
    st.markdown("""
    <div class="policy-card">
        <h4>🚨 灾中智能响应</h4>
        <p>AI驱动的灾害发生后即时响应系统，自动推送应急指令、资源调度建议与农户预警短信</p>
    </div>
    """, unsafe_allow_html=True)

with col_service3:
    st.markdown("""
    <div class="policy-card">
        <h4>⚡ 灾后高效理赔</h4>
        <p>AI图像识别+区块链智能合约，实现“秒级”理赔审核与补贴同步发放，理赔周期缩短99%</p>
    </div>
    """, unsafe_allow_html=True)

with col_service4:
    st.markdown("""
    <div class="policy-card">
        <h4>📊 灾害·保险数据融合</h4>
        <p>多源数据（灾害、气象、保险理赔、价格）实时融合，为政府提供决策级风险评估报告</p>
    </div>
    """, unsafe_allow_html=True)

st.divider()

st.subheader("📦 一键生成区域风险方案")
st.markdown("**点击下方按钮，即可为指定区域生成完整《政府公益风险管理打包方案》**")

if st.button("🚀 生成当前广西试点区域风险方案", type="primary", use_container_width=True):
    with st.spinner("正在整合灾害监测、保险数据与补贴政策..."):
        time.sleep(1.8)
    
    scheme_data = pd.DataFrame({
        "风险模块": ["地域灾害监测预警", "灾中智能响应", "灾后高效理赔", "数据融合分析"],
        "覆盖范围": ["全广西14市", "实时响应", "2小时内完成", "灾害+保险全链路"],
        "关键指标": ["30天预警准确率92%", "响应时间<5分钟", "理赔效率提升70%", "补贴透明度100%"],
        "政府补贴支持": ["80%中央+地方", "应急资金联动", "区块链自动发放", "精准帮扶测算"]
    })
    
    st.success("✅ 风险方案生成完成！（已打包为政府决策参考文件）")
    st.dataframe(scheme_data, use_container_width=True, hide_index=True)
    
    st.download_button(
        label="📥 下载《广西试点区域公益风险管理打包方案.pdf》",
        data="模拟打包方案文件内容（实际部署时替换为真实PDF）".encode("utf-8"),
        file_name="广西试点区域公益风险管理打包方案.pdf",
        mime="application/pdf"
    )

st.divider()

# ==================== 重要政策文件下载 ====================
st.subheader("📄 重要政策文件下载（政府监管依据）")
st.markdown("**以下为当前重点政策文件，均涉及农业保险补贴、防止返贫和乡村振兴金融支持：**")

# 文件1
st.markdown("""
<div class="policy-card">
    <h4>1. 国家层面金融支持意见（中国人民银行等四部门）</h4>
    <p><strong>补贴核心：</strong>调整脱贫人口小额信贷、农户信用贷款；新增资金优先投向乡村振兴重点帮扶县；支持粮油生产、农业全产业链和农村基础设施中长期贷款。</p>
""", unsafe_allow_html=True)
if Path("assets/国家金融支持意见.pdf").exists():
    with open("assets/国家金融支持意见.pdf", "rb") as f:
        st.download_button("📥 下载国家金融支持意见.pdf", data=f, file_name="国家金融支持意见.pdf", mime="application/pdf")
st.markdown("</div>", unsafe_allow_html=True)

# 文件2
st.markdown("""
<div class="policy-card">
    <h4>2. 广西金融惠企三年行动方案（2025—2027年）</h4>
    <p><strong>补贴核心：</strong>统筹75亿元财政资金，带动贴息贷款6000亿元以上；担保费率补贴0.2%-0.4%；每年支农支小再贷款不少于1000亿元。</p>
""", unsafe_allow_html=True)
if Path("assets/广西金融惠企方案.pdf").exists():
    with open("assets/广西金融惠企方案.pdf", "rb") as f:
        st.download_button("📥 下载广西金融惠企方案.pdf", data=f, file_name="广西金融惠企方案.pdf", mime="application/pdf")
st.markdown("</div>", unsafe_allow_html=True)

# 文件3
st.markdown("""
<div class="policy-card">
    <h4>3. 中共中央 国务院 乡村全面振兴意见（2026年国务院公报）</h4>
    <p><strong>补贴核心：</strong>粮食产量稳定1.4万亿斤；高标准农田建设；新一轮千亿斤粮食产能提升行动；加强农业保险、信贷支持。</p>
""", unsafe_allow_html=True)
if Path("assets/国务院乡村振兴意见.pdf").exists():
    with open("assets/国务院乡村振兴意见.pdf", "rb") as f:
        st.download_button("📥 下载中央乡村全面振兴意见.pdf", data=f, file_name="国务院乡村振兴意见.pdf", mime="application/pdf")
st.markdown("</div>", unsafe_allow_html=True)
