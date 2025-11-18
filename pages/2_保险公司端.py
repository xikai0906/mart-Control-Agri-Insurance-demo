import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime, timedelta

st.set_page_config(page_title="保险公司端", page_icon="🏢", layout="wide")

st.title("🏢 保险公司管理平台")
st.markdown("---")

# Tab导航
tab1, tab2, tab3 = st.tabs(["📊 风险评估看板", "✅ 理赔审核", "📈 数据分析"])

# ==================== Tab1: 风险评估看板 ====================
with tab1:
    st.header("📊 风险评估看板")
    
    # 核心指标卡片
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric(label="总投保农户", value="2,847", delta="↑ 12%")
    
    with col2:
        st.metric(label="保费收入(万元)", value="358.6", delta="↑ 8%")
    
    with col3:
        st.metric(label="待审核理赔", value="47", delta="↑ 5")
    
    with col4:
        st.metric(label="本月赔付率", value="68%", delta="↓ 5%")
    
    st.divider()
    
    # 区域风险地图 + 风险列表
    col_map, col_list = st.columns([2, 1])
    
    with col_map:
        st.subheader("🗺️ 区域风险热力图")
        
        # 模拟区域风险数据
        regions_data = pd.DataFrame({
            'region': ['南宁-武鸣', '钦州-灵山', '崇左-扶绥', '百色-田阳', '河池-宜州'],
            'lat': [23.1566, 22.2893, 22.6362, 23.7368, 24.4925],
            'lon': [108.2733, 109.3122, 107.9043, 106.9152, 108.6364],
            'insured_amount': [5000, 3200, 2800, 2100, 1900],
            'risk_level': [0.75, 0.45, 0.62, 0.38, 0.52]
        })
        
        # 风险等级映射颜色
        regions_data['risk_color'] = regions_data['risk_level'].apply(
            lambda x: 'high' if x > 0.7 else ('medium' if x > 0.4 else 'low')
        )
        
        # 创建地图
        fig_map = px.scatter_mapbox(
            regions_data,
            lat='lat',
            lon='lon',
            size='insured_amount',
            color='risk_level',
            hover_name='region',
            hover_data={'insured_amount': ':,.0f', 'risk_level': ':.2%'},
            color_continuous_scale=['green', 'yellow', 'red'],
            size_max=30,
            zoom=6.5,
            mapbox_style="open-street-map"
        )
        
        fig_map.update_layout(
            height=500,
            margin={"r":0,"t":0,"l":0,"b":0}
        )
        
        st.plotly_chart(fig_map, use_container_width=True)
    
    with col_list:
        st.subheader("⚠️ 高风险区域")
        
        high_risk_regions = regions_data[regions_data['risk_level'] > 0.6].sort_values('risk_level', ascending=False)
        
        for _, row in high_risk_regions.iterrows():
            risk_pct = row['risk_level'] * 100
            st.error(f"""
            **{row['region']}**  
            风险等级: {risk_pct:.1f}%  
            投保金额: ¥{row['insured_amount']:,.0f}万
            """)
        
        st.divider()
        
        st.subheader("📅 近期事件")
        st.warning("🌀 **台风预警:** 钦州地区预计3天内受影响")
        st.info("📉 **价格波动:** 沃柑价格持续走低")
    
    # 赔付趋势预测
    st.subheader("📈 赔付趋势预测")
    
    # 生成模拟数据
    months = pd.date_range(start='2024-01-01', periods=12, freq='M')
    payout_data = pd.DataFrame({
        'month': months,
        'actual': [120, 135, 150, 180, 160, 200, 190, 210, 185, 195, 220, 240],
        'predicted': [None]*10 + [230, 245, 255]
    })
    
    fig_payout = go.Figure()
    
    # 实际赔付
    fig_payout.add_trace(go.Scatter(
        x=payout_data['month'][:10],
        y=payout_data['actual'][:10],
        mode='lines+markers',
        name='实际赔付',
        line=dict(color='blue', width=3)
    ))
    
    # 预测赔付
    future_months = payout_data['month'][9:]
    future_predicted = payout_data['predicted'][9:]
    
    fig_payout.add_trace(go.Scatter(
        x=future_months,
        y=future_predicted,
        mode='lines+markers',
        name='AI预测',
        line=dict(color='red', width=3, dash='dash')
    ))
    
    fig_payout.update_layout(
        title="月度赔付金额趋势(万元)",
        xaxis_title="月份",
        yaxis_title="赔付金额(万元)",
        hovermode='x unified'
    )
    
    st.plotly_chart(fig_payout, use_container_width=True)

# ==================== Tab2: 理赔审核 ====================
with tab2:
    st.header("✅ 智能理赔审核系统")
    
    # 待审核列表
    st.subheader("📋 待审核理赔申请")
    
    pending_claims = pd.DataFrame({
        '申请编号': ['CL202400145', 'CL202400146', 'CL202400147', 'CL202400148'],
        '农户姓名': ['张三', '李四', '王五', '赵六'],
        '地区': ['南宁-武鸣', '钦州-灵山', '崇左-扶绥', '南宁-武鸣'],
        '类型': ['天气灾害', '价格理赔', '天气灾害', '价格理赔'],
        '申请金额': [12000, 5000, 8000, 3500],
        '申请时间': ['2024-11-15 10:30', '2024-11-15 14:20', '2024-11-16 09:15', '2024-11-16 11:45'],
        '状态': ['待审核', '待审核', '待审核', '待审核']
    })
    
    # 选择要审核的理赔
    selected_claim = st.selectbox(
        "选择理赔申请",
        pending_claims['申请编号'].tolist(),
        format_func=lambda x: f"{x} - {pending_claims[pending_claims['申请编号']==x]['农户姓名'].values[0]} - ¥{pending_claims[pending_claims['申请编号']==x]['申请金额'].values[0]:,.0f}"
    )
    
    # 显示理赔详情
    claim_detail = pending_claims[pending_claims['申请编号'] == selected_claim].iloc[0]
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.subheader("📄 理赔详情")
        
        st.markdown(f"""
        **申请编号:** {claim_detail['申请编号']}  
        **农户姓名:** {claim_detail['农户姓名']}  
        **所在地区:** {claim_detail['地区']}  
        **理赔类型:** {claim_detail['类型']}  
        **申请金额:** ¥{claim_detail['申请金额']:,.0f}  
        **申请时间:** {claim_detail['申请时间']}  
        """)
        
        st.divider()
        
        # 显示申请材料
        st.markdown("**📎 申请材料**")
        
        if '天气灾害' in claim_detail['类型']:
            st.image("https://via.placeholder.com/400x300?text=受灾照片", caption="受灾现场照片")
            
            st.markdown("""
            **灾害信息:**
            - 灾害类型: 暴雨洪涝
            - 发生日期: 2024-11-10
            - 受灾面积: 8亩
            - 受损程度: 60%
            """)
        else:
            st.markdown("""
            **销售信息:**
            - 销售日期: 2024-11-12
            - 销售数量: 5000斤
            - 实际价格: ¥2.3/斤
            - 保险价格: ¥3.0/斤
            - 价格差额: ¥0.7/斤
            """)
    
    with col2:
        st.subheader("🤖 AI交叉验证")
        
        with st.spinner("AI验证中..."):
            import time
            time.sleep(1)
        
        # 模拟AI验证结果
        st.success("✅ **验证完成**")
        
        verification_results = {
            '气象数据验证': np.random.choice([True, False], p=[0.9, 0.1]),
            '遥感影像验证': np.random.choice([True, False], p=[0.85, 0.15]),
            '市场价格验证': np.random.choice([True, False], p=[0.88, 0.12])
        }
        
        for check, result in verification_results.items():
            if result:
                st.success(f"✅ {check}")
            else:
                st.error(f"❌ {check}")
        
        # 综合评分
        confidence = sum(verification_results.values()) / len(verification_results)
        
        st.divider()
        
        st.metric("置信度评分", f"{confidence*100:.0f}%")
        
        if confidence >= 0.8:
            st.success("🎯 **建议:** 通过审核")
        elif confidence >= 0.6:
            st.warning("⚠️ **建议:** 进一步核实")
        else:
            st.error("❌ **建议:** 拒绝理赔")
        
        st.divider()
        
        # 审核操作
        st.subheader("📝 审核操作")
        
        approved_amount = st.number_input(
            "批准金额(元)", 
            min_value=0, 
            max_value=int(claim_detail['申请金额']),
            value=int(claim_detail['申请金额'] * confidence)
        )
        
        审核意见 = st.text_area("审核意见", placeholder="请填写审核意见...")
        
        col_a, col_b = st.columns(2)
        
        with col_a:
            if st.button("✅ 批准", type="primary", use_container_width=True):
                st.success(f"✅ 理赔已批准,赔付金额: ¥{approved_amount:,.0f}")
                st.balloons()
        
        with col_b:
            if st.button("❌ 拒绝", type="secondary", use_container_width=True):
                st.error("❌ 理赔已拒绝")
    
    st.divider()
    
    # 批量审核
    st.subheader("⚡ 批量审核")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.info("**高置信度案件**\n自动批准: 23件")
    
    with col2:
        st.warning("**中置信度案件**\n待人工复核: 12件")
    
    with col3:
        st.error("**低置信度案件**\n建议拒绝: 8件")
    
    if st.button("🚀 执行批量审核", type="primary"):
        with st.spinner("批量处理中..."):
            import time
            time.sleep(2)
        st.success("✅ 批量审核完成!")

# ==================== Tab3: 数据分析 ====================
with tab3:
    st.header("📈 数据分析中心")
    
    # 时间选择器
    date_range = st.date_input(
        "选择时间范围",
        value=(datetime.now() - timedelta(days=90), datetime.now()),
        max_value=datetime.now()
    )
    
    # 业务概览
    st.subheader("💼 业务概览")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("保费收入", "¥358.6万", "↑ 8.5%")
    
    with col2:
        st.metric("赔付支出", "¥240.3万", "↓ 3.2%")
    
    with col3:
        st.metric("综合赔付率", "67%", "↓ 5%")
    
    with col4:
        st.metric("利润率", "12.5%", "↑ 2.1%")
    
    st.divider()
    
    # 险种分布
    col_pie, col_bar = st.columns(2)
    
    with col_pie:
        st.subheader("📊 险种保费分布")
        
        insurance_types = pd.DataFrame({
            'type': ['天气指数保险', '价格保险', '产量保险', '收入保险'],
            'amount': [150, 120, 60, 28.6]
        })
        
        fig_pie = px.pie(insurance_types, values='amount', names='type',
                        title='保费收入占比')
        st.plotly_chart(fig_pie, use_container_width=True)
    
    with col_bar:
        st.subheader("📊 作物保费排名")
        
        crops = pd.DataFrame({
            'crop': ['沃柑', '甘蔗', '荔枝', '芒果', '火龙果'],
            'premium': [120, 95, 68, 45, 30.6]
        })
        
        fig_bar = px.bar(crops, x='crop', y='premium',
                        title='各作物保费收入(万元)')
        st.plotly_chart(fig_bar, use_container_width=True)
    
    # 理赔分析
    st.subheader("💰 理赔分析")
    
    col1, col2 = st.columns(2)
    
    with col1:
        # 理赔类型分布
        claim_types = pd.DataFrame({
            'type': ['天气灾害', '价格波动', '产量不足', '其他'],
            'count': [145, 98, 42, 15],
            'amount': [88, 76, 45, 31.3]
        })
        
        fig_claims = go.Figure()
        fig_claims.add_trace(go.Bar(
            x=claim_types['type'],
            y=claim_types['count'],
            name='理赔件数',
            yaxis='y',
            marker_color='lightblue'
        ))
        fig_claims.add_trace(go.Scatter(
            x=claim_types['type'],
            y=claim_types['amount'],
            name='理赔金额(万元)',
            yaxis='y2',
            mode='lines+markers',
            marker_color='red'
        ))
        
        fig_claims.update_layout(
            title='理赔类型分析',
            yaxis=dict(title='件数'),
            yaxis2=dict(title='金额(万元)', overlaying='y', side='right'),
            hovermode='x unified'
        )
        
        st.plotly_chart(fig_claims, use_container_width=True)
    
    with col2:
        # 区域赔付率
        region_payout = pd.DataFrame({
            'region': ['南宁-武鸣', '钦州-灵山', '崇左-扶绥', '百色-田阳', '河池-宜州'],
            'payout_rate': [75, 62, 58, 48, 52]
        })
        
        fig_region = px.bar(region_payout, x='region', y='payout_rate',
                           title='各地区赔付率(%)',
                           color='payout_rate',
                           color_continuous_scale=['green', 'yellow', 'red'])
        st.plotly_chart(fig_region, use_container_width=True)
    
    # 用户分析
    st.subheader("👥 用户分析")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("活跃农户", "2,847户", "↑ 12%")
    
    with col2:
        st.metric("新增用户", "347户", "↑ 25%")
    
    with col3:
        st.metric("复购率", "78%", "↑ 5%")

# 页脚
st.divider()
st.info("💡 **数据更新:** 数据每小时自动更新 | 最后更新时间: " + datetime.now().strftime("%Y-%m-%d %H:%M"))
