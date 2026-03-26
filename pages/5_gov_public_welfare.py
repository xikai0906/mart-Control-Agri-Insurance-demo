import streamlit as st
import pandas as pd
import plotly.express as px
import base64
from pathlib import Path

# ==================== 背景 + 统一卡片样式 ====================
def get_base64_of_bin_file(bin_file):
    with open(bin_file, 'rb') as f:
        data = f.read()
    return base64.b64encode(data).decode()

image_path = Path("assets/农民开怀大笑.png")
if image_path.exists():
    bg_base64 = get_base64_of_bin_file(str(image_path))
    background_css = f"""
    <style>
    .stApp {{
        background-image: url("data:image/png;base64,{bg_base64}");
        background-size: cover;
        background-position: center;
        background-repeat: no-repeat;
        background-attachment: fixed;
    }}
    /* 整体遮罩稍加深 */
    .stApp::before {{
        content: "";
        position: absolute;
        top: 0; left: 0; width: 100%; height: 100%;
        background: rgba(0, 0, 0, 0.75);
        z-index: -1;
    }}
    /* 顶部标题 + 指标卡片 */
    .header-card {{
        background: rgba(255, 255, 255, 0.93) !important;
        border-radius: 16px;
        padding: 24px 28px;
        margin: 10px 0 25px 0;
        box-shadow: 0 6px 20px rgba(0, 0, 0, 0.3);
        color: #1a1a1a !important;
    }}
    /* 政策文件卡片（保持不变） */
    .policy-card {{
        background: rgba(255, 255, 255, 0.92) !important;
        border-radius: 12px;
        padding: 20px 24px;
        margin: 15px 0;
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.3);
        color: #1a1a1a !important;
    }}
    .policy-card h4 {{
        color: #0066cc !important;
        margin-bottom: 12px;
    }}
    .policy-card p {{
        color: #003300 !important;
    }}
    /* 标题颜色 + 强阴影 */
    h1, h2, h3 {{
        color: #00bfff !important;
        text-shadow: 0 4px 12px rgba(0,0,0,0.95);
    }}
    /* 正文颜色 */
    p, li, .stMarkdown, .stSuccess, .stCaption {{
        color: #006633 !important;
    }}
    /* 关键数字红色 */
    .stMetricValue {{
        color: #ff4d4d !important;
    }}
    /* 下载按钮 */
    .stDownloadButton button {{
        background-color: #00bfff !important;
        color: white !important;
        border-radius: 8px;
    }}
    </style>
    """
    st.markdown(background_css, unsafe_allow_html=True)
else:
    st.error("❌ 未找到 assets/农民开怀大笑.png")

st.set_page_config(page_title="智护农安 · 政府公益监管端", page_icon="🏛️", layout="wide")

# ==================== 顶部标题 + 指标（加白色卡片） ====================
st.markdown('<div class="header-card">', unsafe_allow_html=True)
st.title("🏛️ 智护农安 · 政府公益监管端")
st.markdown("**政策性农业保险补贴透明看板** —— 中央+地方财政联合补贴 · 服务乡村振兴")

col1, col2, col3 = st.columns(3)
col1.metric("本年度补贴总额", "¥1.65亿", "广西试点")
col2.metric("已智护小农户", "28.4万户", "↑ 2025")
col3.metric("覆盖耕地面积", "312万亩", "全覆盖")
st.markdown('</div>', unsafe_allow_html=True)

st.divider()

# ==================== 区块链记录 ====================
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

st.subheader("🌱 公益帮扶效果")
fig = px.bar(x=["已惠及农户", "覆盖耕地", "减贫贡献"], y=[284000, 3120000, 85],
             text=[284000, "312万亩", "85%"], title="2025年智护农安公益成果",
             color_discrete_sequence=["#00bfff"])
fig.update_traces(textposition='auto')
st.plotly_chart(fig, use_container_width=True)

# ==================== 政策文件区 ====================
st.divider()
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
