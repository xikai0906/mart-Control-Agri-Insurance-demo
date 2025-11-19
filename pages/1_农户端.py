import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime, timedelta

st.set_page_config(page_title="农户端", page_icon="👨‍🌾", layout="wide")
# 顶部导航
col_nav1, col_nav2 = st.columns([1, 4])
with col_nav1:
    if st.button("🏠 返回首页", use_container_width=True):
        st.switch_page("app.py")

st.title("👨‍🌾 农户服务平台")
st.markdown("---")

# 侧边栏 - 用户信息
with st.sidebar:
    st.header("👤 用户信息")
    farmer_name = st.text_input("姓名", value="张三")
    farmer_location = st.selectbox("所在地区", 
        ["广西南宁-武鸣", "广西钦州-灵山", "广西崇左-扶绥", "其他地区"])
    crop_type = st.selectbox("种植作物", 
        ["沃柑", "甘蔗", "荔枝", "芒果", "火龙果"])
    planting_area = st.number_input("种植面积(亩)", min_value=0.0, value=10.0, step=0.5)
    
    st.divider()
    st.success(f"欢迎, {farmer_name}!")

# Tab导航
tab1, tab2, tab3, tab4 = st.tabs(["🌦️ 天气预警", "💰 价格预测", "📝 理赔申请", "📄 我的保单"])

# ==================== Tab1: 天气预警 ====================
with tab1:
    st.header("🌦️ 天气预警系统 - 未来30天极端天气预测")
    
    # Dashboard - 关键指标卡片
    st.subheader("📊 气象预警Dashboard")
    
    metric_col1, metric_col2, metric_col3, metric_col4 = st.columns(4)
    
    with metric_col1:
        st.metric("极端高温天数", "3天", "↑ 1天", help="未来30天预测超过35°C的天数")
    
    with metric_col2:
        st.metric("暴雨预警", "5天", "↑ 2天", help="未来30天降雨量>50mm的天数")
    
    with metric_col3:
        st.metric("综合风险等级", "中", delta="稳定", help="基于多维气象数据的综合评估")
    
    with metric_col4:
        disaster_prob = 23.5
        st.metric("极端天气概率", f"{disaster_prob:.1f}%", "↓ 5%", help="未来30天内发生极端天气的概率")
    
    st.divider()
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        # 生成模拟30天天气数据
        dates = pd.date_range(start=datetime.now(), periods=30, freq='D')
        
        # 模拟温度数据（带季节性和随机波动）
        t = np.arange(30)
        seasonal = 2 * np.sin(2 * np.pi * t / 365)
        temp_base = 28
        weather_data = pd.DataFrame({
            'date': dates,
            'temp_max': temp_base + seasonal + np.random.normal(0, 3, 30),
            'temp_min': temp_base - 7 + seasonal + np.random.normal(0, 2, 30),
            'rainfall': np.abs(np.random.exponential(15, 30) + np.random.normal(0, 5, 30)),
            'disaster_risk': np.clip(np.random.beta(2, 5, 30), 0, 1)  # 偏向低风险但有高风险天数
        })
        
        # 标注极端天气
        weather_data['is_extreme'] = (weather_data['temp_max'] > 35) | (weather_data['rainfall'] > 50)
        weather_data['extreme_type'] = weather_data.apply(
            lambda x: '高温' if x['temp_max'] > 35 else ('暴雨' if x['rainfall'] > 50 else '正常'),
            axis=1
        )
        
        # 1. 温度趋势图（标注极端高温）
        fig_temp = go.Figure()
        
        # 正常温度
        normal_mask = weather_data['temp_max'] <= 35
        fig_temp.add_trace(go.Scatter(
            x=weather_data[normal_mask]['date'], 
            y=weather_data[normal_mask]['temp_max'],
            mode='lines+markers',
            name='最高温',
            line=dict(color='orange', width=2),
            marker=dict(size=6)
        ))
        
        # 极端高温标红
        extreme_temp_mask = weather_data['temp_max'] > 35
        fig_temp.add_trace(go.Scatter(
            x=weather_data[extreme_temp_mask]['date'],
            y=weather_data[extreme_temp_mask]['temp_max'],
            mode='markers',
            name='极端高温',
            marker=dict(color='red', size=12, symbol='x')
        ))
        
        fig_temp.add_trace(go.Scatter(
            x=weather_data['date'], 
            y=weather_data['temp_min'],
            mode='lines+markers',
            name='最低温',
            line=dict(color='blue', width=2),
            marker=dict(size=4),
            fill='tonexty'
        ))
        
        # 添加极端高温阈值线
        fig_temp.add_hline(y=35, line_dash="dash", line_color="red", 
                          annotation_text="极端高温阈值: 35°C")
        
        fig_temp.update_layout(
            title="未来30天温度趋势预测",
            xaxis_title="日期",
            yaxis_title="温度(°C)",
            hovermode='x unified',
            height=400
        )
        st.plotly_chart(fig_temp, use_container_width=True)
        
        # 2. 降雨量柱状图（标注暴雨）
        # 根据降雨量分级着色
        rainfall_colors = weather_data['rainfall'].apply(
            lambda x: 'red' if x > 50 else ('orange' if x > 25 else 'lightblue')
        )
        
        fig_rain = go.Figure()
        fig_rain.add_trace(go.Bar(
            x=weather_data['date'],
            y=weather_data['rainfall'],
            marker_color=rainfall_colors,
            name='降雨量',
            text=weather_data['rainfall'].round(1),
            textposition='outside',
            hovertemplate='<b>%{x|%m-%d}</b><br>降雨量: %{y:.1f}mm<extra></extra>'
        ))
        
        # 添加暴雨阈值线
        fig_rain.add_hline(y=50, line_dash="dash", line_color="red",
                          annotation_text="暴雨阈值: 50mm")
        fig_rain.add_hline(y=25, line_dash="dot", line_color="orange",
                          annotation_text="大雨阈值: 25mm")
        
        fig_rain.update_layout(
            title="未来30天降雨量预测",
            xaxis_title="日期",
            yaxis_title="降雨量(mm)",
            height=400,
            showlegend=False
        )
        st.plotly_chart(fig_rain, use_container_width=True)
        
        # 3. 极端天气概率热力图
        st.subheader("📅 极端天气风险日历")
        
        # 将风险等级转换为0-100的概率
        weather_data['risk_percent'] = (weather_data['disaster_risk'] * 100).round(1)
        
        # 创建热力图数据（按周组织）
        weather_data['week'] = ((weather_data.index) // 7) + 1
        weather_data['day_of_week'] = weather_data.index % 7
        
        # 用pivot创建周-日矩阵
        heatmap_data = weather_data.pivot_table(
            values='risk_percent',
            index='week',
            columns='day_of_week',
            aggfunc='first'
        )
        
        fig_heatmap = go.Figure(data=go.Heatmap(
            z=heatmap_data.values,
            x=['周一', '周二', '周三', '周四', '周五', '周六', '周日'][:heatmap_data.shape[1]],
            y=[f'第{i+1}周' for i in range(len(heatmap_data))],
            colorscale='RdYlGn_r',  # 红-黄-绿反转（红色表示高风险）
            text=heatmap_data.values.round(1),
            texttemplate='%{text}%',
            textfont={"size": 10},
            colorbar=dict(title="风险等级(%)")
        ))
        
        fig_heatmap.update_layout(
            title="未来30天极端天气概率热力图",
            height=300
        )
        st.plotly_chart(fig_heatmap, use_container_width=True)
    
    with col2:
        st.subheader("⚠️ 风险预警")
        
        # 计算平均风险等级
        avg_risk = weather_data['disaster_risk'].mean()
        
        if avg_risk > 0.7:
            st.error("🚨 **高风险警报**")
            st.markdown("""
            **预警内容:**
            - 未来3天可能出现暴雨
            - 建议做好排水措施
            - 及时关注天气变化
            """)
            st.warning("💡 **理赔提示:** 如发生灾害损失,请及时拍照记录并提交理赔申请")
        elif avg_risk > 0.4:
            st.warning("⚠️ **中风险提示**")
            st.markdown("""
            **注意事项:**
            - 天气状况不稳定
            - 注意防范局部暴雨
            """)
        else:
            st.success("✅ **低风险**")
            st.markdown("天气状况良好,适合农业生产")
        
        st.divider()
        
        # 保险状态
        st.subheader("📋 保险状态")
        st.info(f"""
        **投保信息:**
        - 作物: {crop_type}
        - 面积: {planting_area}亩
        - 保险类型: 天气指数保险
        - 保障额度: ¥{planting_area * 5000:,.0f}
        """)

# ==================== Tab2: 价格预测 ====================
with tab2:
    st.header("💰 价格趋势预测")
    
    col1, col2 = st.columns([3, 1])
    
    with col1:
        # 生成模拟历史价格数据
        months = pd.date_range(start='2024-01-01', periods=12, freq='M')
        historical_prices = pd.DataFrame({
            'month': months,
            'price': [3.5, 3.2, 2.8, 2.5, 2.3, 2.0, 1.8, 2.2, 2.6, 3.0, 3.3, 3.6]
        })
        
        # 生成预测价格
        future_months = pd.date_range(start=months[-1] + timedelta(days=30), periods=3, freq='M')
        predicted_prices = pd.DataFrame({
            'month': future_months,
            'price': [3.8, 3.5, 3.3]
        })
        
        # 绘制价格趋势
        fig_price = go.Figure()
        
        # 历史价格
        fig_price.add_trace(go.Scatter(
            x=historical_prices['month'],
            y=historical_prices['price'],
            mode='lines+markers',
            name='历史价格',
            line=dict(color='green', width=3)
        ))
        
        # 预测价格
        fig_price.add_trace(go.Scatter(
            x=predicted_prices['month'],
            y=predicted_prices['price'],
            mode='lines+markers',
            name='AI预测',
            line=dict(color='orange', width=3, dash='dash')
        ))
        
        # 保险阈值线
        fig_price.add_hline(y=3.0, line_dash="dot", 
                           annotation_text="保险阈值: ¥3.0/斤", 
                           line_color="red")
        
        fig_price.update_layout(
            title=f"{crop_type}价格走势与预测",
            xaxis_title="时间",
            yaxis_title="价格(元/斤)",
            hovermode='x unified'
        )
        
        st.plotly_chart(fig_price, use_container_width=True)
        
        # 价格分析
        st.subheader("📊 价格分析")
        col_a, col_b, col_c = st.columns(3)
        
        with col_a:
            current_price = historical_prices['price'].iloc[-1]
            st.metric("当前市场价", f"¥{current_price:.1f}/斤", 
                     f"{(current_price - 3.0):.1f}")
        
        with col_b:
            future_price = predicted_prices['price'].iloc[0]
            st.metric("下月预测价", f"¥{future_price:.1f}/斤",
                     f"{(future_price - current_price):.1f}")
        
        with col_c:
            insured_price = 3.0
            st.metric("保险阈值", f"¥{insured_price:.1f}/斤")
    
    with col2:
        st.subheader("💡 价格预警")
        
        if predicted_prices['price'].iloc[0] < 3.0:
            st.error("🔔 **价格预警**")
            st.markdown("""
            **风险提示:**
            - 预测价格低于保险阈值
            - 可能触发价格理赔
            - 建议提前做好准备
            """)
            
            # 计算预计赔付
            loss = (3.0 - predicted_prices['price'].iloc[0]) * planting_area * 1000  # 假设亩产1000斤
            st.warning(f"💰 **预计赔付:** ¥{loss:,.0f}")
        else:
            st.success("✅ **价格正常**")
            st.markdown("预测价格高于保险阈值,无需担心")
        
        st.divider()
        
        st.subheader("📈 市场建议")
        st.info("""
        **销售建议:**
        - 关注市场行情变化
        - 可考虑分批次销售
        - 避免集中出售
        """)

# ==================== Tab3: 理赔申请 ====================
with tab3:
    st.header("📝 理赔申请")
    
    claim_type = st.radio("选择理赔类型", 
        ["🌦️ 天气灾害理赔", "💰 价格保险理赔"],
        horizontal=True)
    
    if "天气灾害" in claim_type:
        st.subheader("🌦️ 天气灾害理赔")
        
        col1, col2 = st.columns(2)
        
        with col1:
            disaster_date = st.date_input("灾害发生日期")
            disaster_type = st.selectbox("灾害类型", 
                ["台风", "暴雨", "洪涝", "干旱", "冰雹", "其他"])
            
            # 受灾面积 - 修改为更灵活的输入方式
            st.markdown("**受灾面积(亩)**")
            area_input_method = st.radio(
                "选择输入方式",
                ["滑块选择", "手动输入"],
                horizontal=True,
                key="面积输入方式",
                label_visibility="collapsed"
            )
            
            if area_input_method == "滑块选择":
                # 根据种植面积设置最大值
                max_area = max(100, planting_area)
                affected_area = st.slider(
                    "受灾面积(亩)",
                    min_value=0.0,
                    max_value=float(max_area),
                    value=min(10.0, planting_area),
                    step=0.5,
                    key="受灾面积_滑块",
                    help=f"最大可选{max_area}亩"
                )
            else:
                affected_area = st.number_input(
                    "受灾面积(亩)",
                    min_value=0.0,
                    max_value=10000.0,
                    value=10.0,
                    step=0.5,
                    key="受灾面积_输入",
                    help="请输入实际受灾面积"
                )
            
            # 受损程度 - 修改范围为1-100%
            damage_level = st.slider(
                "受损程度(%)",
                min_value=1,
                max_value=100,
                value=50,
                step=1,
                key="受损程度_天气",
                help="请根据实际情况选择受损程度(1-100%)"
            )
        
        with col2:
            st.markdown("**上传受灾照片**")
            uploaded_file = st.file_uploader("选择照片(支持jpg/png)", type=['jpg', 'png', 'jpeg'])
            
            if uploaded_file:
                st.image(uploaded_file, caption="受灾照片", use_container_width=True)
                
                # 模拟AI识别
                with st.spinner("AI正在分析照片..."):
                    import time
                    time.sleep(1)
                    st.success(f"✅ AI识别: {disaster_type}灾害, 受损程度约{damage_level}%")
        
        st.text_area("补充说明", placeholder="请描述灾害情况...", key="补充说明_天气")
        
        # 计算预计赔付
        compensation = affected_area * 5000 * (damage_level / 100)
        
        st.divider()
        
        col_a, col_b = st.columns([2, 1])
        with col_a:
            st.info(f"""
            💰 **预计赔付金额:** ¥{compensation:,.0f}
            
            📝 **计算方式:** {affected_area}亩 × ¥5,000/亩 × {damage_level}% = ¥{compensation:,.0f}
            """)
        with col_b:
            if st.button("🚀 提交理赔申请", type="primary", use_container_width=True, key="提交天气理赔"):
                st.success("✅ 理赔申请已提交,审核中...")
                st.balloons()
    
    else:  # 价格保险理赔
        st.subheader("💰 价格保险理赔")
        
        col1, col2 = st.columns(2)
        
        with col1:
            sale_date = st.date_input("销售日期")
            sale_amount = st.number_input("销售数量(斤)", min_value=0.0, value=1000.0, step=100.0)
            actual_price = st.number_input("实际销售价格(元/斤)", 
                min_value=0.0, value=2.5, step=0.1)
        
        with col2:
            insured_price = st.number_input("保险约定价格(元/斤)", 
                min_value=0.0, value=3.0, step=0.1)
            
            st.markdown("**上传销售凭证**")
            receipt_file = st.file_uploader("上传收购单/发票", type=['jpg', 'png', 'pdf'])
        
        st.divider()
        
        if actual_price < insured_price:
            price_diff = insured_price - actual_price
            compensation = price_diff * sale_amount
            
            st.error(f"🔔 **触发理赔条件:** 实际价格低于保险价格 ¥{price_diff:.2f}/斤")
            st.success(f"""
            💰 **预计赔付金额:** ¥{compensation:,.2f}
            
            📝 **计算方式:** (¥{insured_price:.2f} - ¥{actual_price:.2f}) × {sale_amount:,.0f}斤 = ¥{compensation:,.2f}
            """)
            
            if st.button("🚀 提交理赔申请", type="primary", use_container_width=True, key="提交价格理赔"):
                st.success("✅ 理赔申请已提交,审核中...")
                st.balloons()
        else:
            st.info("✅ 销售价格高于保险阈值,无需理赔")

# ==================== Tab4: 我的保单 ====================
with tab4:
    st.header("📄 我的保单")
    
    # 保单列表
    policies = pd.DataFrame({
        '保单号': ['ZK2024001', 'ZK2024002'],
        '险种': ['天气指数保险', '价格保险'],
        '作物': [crop_type, crop_type],
        '面积(亩)': [planting_area, planting_area],
        '保费(元)': [500, 800],
        '保额(元)': [50000, 80000],
        '状态': ['✅ 生效中', '✅ 生效中'],
        '到期日': ['2025-12-31', '2025-12-31']
    })
    
    st.dataframe(policies, use_container_width=True, hide_index=True)
    
    # 理赔历史
    st.subheader("📊 理赔历史")
    
    claims_history = pd.DataFrame({
        '申请日期': ['2024-08-15', '2024-10-20'],
        '类型': ['天气灾害', '价格理赔'],
        '申请金额': ['¥12,000', '¥5,000'],
        '状态': ['✅ 已赔付', '⏳ 审核中'],
        '赔付金额': ['¥12,000', '-']
    })
    
    st.dataframe(claims_history, use_container_width=True, hide_index=True)
    
    # 统计卡片
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("累计保费", "¥1,300", "本年")
    
    with col2:
        st.metric("累计赔付", "¥12,000", "+¥5,000")
    
    with col3:
        st.metric("保障额度", "¥130,000", "生效中")

# 页脚帮助信息
st.divider()
st.info("💡 **使用帮助:** 如有疑问请联系技术部ysuy5756@gmail.com 或访问帮助中心")
