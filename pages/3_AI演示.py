import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from datetime import datetime
import time

st.set_page_config(page_title="AI技术演示", page_icon="🤖", layout="wide")

# 顶部导航
col_nav1, col_nav2 = st.columns([1, 4])
with col_nav1:
    if st.button("🏠 返回首页", use_container_width=True):
        st.switch_page("app.py")

st.title("🤖 AI技术演示中心")
st.markdown("---")

# Tab导航
tab1, tab2, tab3, tab4 = st.tabs([
    "🌦️ AI灾害识别", 
    "💰 AI价格预测", 
    "⚡ 自动化理赔流程",
    "📊 技术架构"
])

# ==================== Tab1: AI灾害识别 ====================
with tab1:
    st.header("🌦️ AI灾害识别系统")
    
    st.markdown("""
    本系统基于深度学习的计算机视觉技术,能够自动识别农业灾害类型和受损程度。
    
    **核心技术:**
    - 卷积神经网络(CNN)
    - 迁移学习(ResNet-50)
    - 多模态数据融合
    """)
    
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.subheader("📤 上传受灾照片")
        
        uploaded_file = st.file_uploader(
            "选择图片文件",
            type=['jpg', 'png', 'jpeg'],
            help="支持jpg/png格式,建议分辨率不低于800x600"
        )
        
        if uploaded_file:
            st.image(uploaded_file, caption="待识别图片", use_container_width=True)
            
            if st.button("🚀 开始AI识别", type="primary", use_container_width=True, key="识别按钮"):
                
                # 模拟AI识别过程
                progress_bar = st.progress(0)
                status_text = st.empty()
                
                steps = [
                    ("图像预处理...", 0.2),
                    ("特征提取...", 0.4),
                    ("模型推理...", 0.7),
                    ("结果分析...", 0.9),
                    ("完成!", 1.0)
                ]
                
                for step, progress in steps:
                    status_text.text(step)
                    progress_bar.progress(progress)
                    time.sleep(0.5)
                
                status_text.success("✅ 识别完成!")
                st.session_state.识别完成 = True
    
    with col2:
        if uploaded_file and st.session_state.get("识别完成", False):
            st.subheader("📊 AI识别结果")
            
            # 模拟识别结果
            disaster_types = ['洪涝', '干旱', '病虫害', '台风', '冰雹']
            
            # 使用固定的随机种子保证结果一致性
            if 'disaster_result' not in st.session_state:
                np.random.seed(42)
                st.session_state.disaster_result = {
                    'probabilities': np.random.dirichlet(np.ones(5)) * 100,
                    'damage_level': np.random.randint(30, 90)
                }
            
            probabilities = st.session_state.disaster_result['probabilities']
            damage_level = st.session_state.disaster_result['damage_level']
            
            # 主要灾害类型
            main_disaster = disaster_types[np.argmax(probabilities)]
            main_prob = np.max(probabilities)
            
            st.success(f"### 🎯 识别结果: **{main_disaster}**")
            st.metric("置信度", f"{main_prob:.1f}%")
            
            # 受损程度评估
            st.metric("受损程度", f"{damage_level}%")
            
            st.divider()
            
            # 各类灾害概率分布
            st.markdown("**📈 各类灾害概率分布**")
            
            prob_df = pd.DataFrame({
                '灾害类型': disaster_types,
                '概率': probabilities
            }).sort_values('概率', ascending=False)
            
            fig_prob = go.Figure(go.Bar(
                x=prob_df['概率'],
                y=prob_df['灾害类型'],
                orientation='h',
                marker_color='lightblue'
            ))
            
            fig_prob.update_layout(
                xaxis_title="概率(%)",
                yaxis_title="",
                height=300,
                margin=dict(l=0, r=0, t=10, b=0)
            )
            
            st.plotly_chart(fig_prob, use_container_width=True)
            
            # 建议理赔金额
            st.divider()
            st.markdown("**💰 建议理赔金额计算**")
            
            # 农户规模选择
            farm_scale = st.selectbox(
                "选择农户规模",
                ["小农户(1-100亩)", "中等农户(100-300亩)", "大型农场(300-2000亩)"],
                key="农户规模"
            )
            
            # 根据规模设置滑块范围
            if "小农户" in farm_scale:
                max_area = 100
                default_area = 15
                step = 1
            elif "中等农户" in farm_scale:
                max_area = 300
                default_area = 50
                step = 5
            else:  # 大型农场
                max_area = 2000
                default_area = 100
                step = 10
            
            area = st.slider(
                "受灾面积(亩)", 
                min_value=1, 
                max_value=max_area,
                value=default_area,
                step=step,
                key="受灾面积",
                help=f"请选择受灾面积（1-{max_area}亩）"
            )
            
            unit_amount = 5000  # 每亩保额
            
            suggested_amount = area * unit_amount * (damage_level / 100)
            
            st.success(f"### 建议理赔: ¥{suggested_amount:,.0f}")
            st.caption(f"💡 计算方式: {area}亩 × ¥{unit_amount}/亩 × {damage_level}% = ¥{suggested_amount:,.0f}")
    
    st.divider()
    
    # 技术说明
    with st.expander("🔧 技术细节"):
        st.markdown("""
        ### 模型架构
        
        **1. 数据预处理**
        - 图像尺寸标准化: 224x224
        - 数据增强: 旋转、翻转、色彩抖动
        - 归一化处理
        
        **2. 特征提取**
        - 基础模型: ResNet-50 (ImageNet预训练)
        - 迁移学习fine-tune
        - 特征维度: 2048
        
        **3. 分类器**
        - 全连接层 + Dropout(0.5)
        - Softmax输出5类灾害概率
        
        **4. 性能指标**
        - 准确率: 92.3%
        - 召回率: 89.7%
        - F1-Score: 90.8%
        """)

# ==================== Tab2: AI价格预测 ====================
with tab2:
    st.header("💰 AI价格预测系统")
    
    st.markdown("""
    基于LSTM(长短期记忆网络)的时间序列预测模型,综合考虑历史价格、天气、供需等多维因素。
    
    **核心技术:**
    - LSTM神经网络
    - 多变量时间序列建模
    - 注意力机制
    """)
    
    col1, col2 = st.columns([1, 2])
    
    with col1:
        st.subheader("⚙️ 预测参数设置")
        
        crop = st.selectbox("选择作物", ['沃柑', '甘蔗', '荔枝', '芒果'], key="作物选择")
        forecast_days = st.slider("预测天数", 7, 90, 30, key="预测天数")
        
        st.divider()
        
        st.markdown("**影响因素设置**")
        st.caption("💡 提示: 调整系数越高，对价格的影响越大")
        
        weather_factor = st.slider(
            "天气影响系数", 
            0.0, 1.0, 0.5, 0.1, 
            key="天气系数",
            help="0=天气良好(利于生产,供应增加,价格可能下降)\n1=天气恶劣(影响生产,供应减少,价格可能上涨)"
        )
        
        supply_factor = st.slider(
            "供需影响系数", 
            0.0, 1.0, 0.5, 0.1, 
            key="供需系数",
            help="0=供过于求(价格下跌)\n1=供不应求(价格上涨)"
        )
        
        policy_factor = st.slider(
            "政策影响系数", 
            0.0, 1.0, 0.5, 0.1, 
            key="政策系数",
            help="0=政策不利(如减少补贴,价格下跌)\n1=政策利好(如增加补贴,价格上涨)"
        )
        
        if st.button("🚀 开始预测", type="primary", use_container_width=True, key="预测按钮"):
            st.session_state.predict_done = True
            st.session_state.weather_factor = weather_factor
            st.session_state.supply_factor = supply_factor
            st.session_state.policy_factor = policy_factor
            st.session_state.forecast_days = forecast_days
            st.session_state.crop = crop
    
    with col2:
        st.subheader("📈 价格预测结果")
        
        # 生成历史价格
        historical_days = 180
        dates = pd.date_range(end=datetime.now(), periods=historical_days, freq='D')
        
        # 模拟历史价格(带季节性) - 提高基准价格到3.5
        np.random.seed(123)
        t = np.arange(historical_days)
        seasonal = 0.3 * np.sin(2 * np.pi * t / 365)
        trend = -0.001 * t
        noise = np.random.normal(0, 0.08, historical_days)
        historical_prices = 3.5 + seasonal + trend + noise
        
        # 生成预测价格
        if st.session_state.get('predict_done', False):
            
            with st.spinner("AI模型预测中..."):
                time.sleep(1.5)
            
            # 使用保存的参数
            forecast_days_used = st.session_state.forecast_days
            weather_factor_used = st.session_state.weather_factor
            supply_factor_used = st.session_state.supply_factor
            policy_factor_used = st.session_state.policy_factor
            crop_used = st.session_state.crop
            
            future_dates = pd.date_range(
                start=dates[-1] + pd.Timedelta(days=1),
                periods=forecast_days_used,
                freq='D'
            )
            
            # 考虑影响因素的预测
            t_future = np.arange(forecast_days_used)
            seasonal_future = 0.3 * np.sin(2 * np.pi * (historical_days + t_future) / 365)
            trend_future = -0.001 * (historical_days + t_future)
            
            # 修正影响因子计算
            weather_impact = (weather_factor_used - 0.5) * 1.2
            supply_impact = (supply_factor_used - 0.5) * 1.5
            policy_impact = (policy_factor_used - 0.5) * 0.8
            
            # 综合影响
            total_impact = weather_impact + supply_impact + policy_impact
            
            # 生成预测价格
            np.random.seed(456)
            noise_future = np.random.normal(0, 0.12, forecast_days_used)
            predicted_prices = 3.5 + seasonal_future + trend_future + total_impact + noise_future
            
            # 置信区间
            confidence_upper = predicted_prices + 0.35
            confidence_lower = predicted_prices - 0.35
            
            # 绘制价格走势
            fig_forecast = go.Figure()
            
            # 历史价格
            fig_forecast.add_trace(go.Scatter(
                x=dates,
                y=historical_prices,
                mode='lines',
                name='历史价格',
                line=dict(color='blue', width=2)
            ))
            
            # 预测价格
            fig_forecast.add_trace(go.Scatter(
                x=future_dates,
                y=predicted_prices,
                mode='lines',
                name='预测价格',
                line=dict(color='red', width=2, dash='dash')
            ))
            
            # 置信区间
            fig_forecast.add_trace(go.Scatter(
                x=future_dates.tolist() + future_dates.tolist()[::-1],
                y=confidence_upper.tolist() + confidence_lower.tolist()[::-1],
                fill='toself',
                fillcolor='rgba(255,0,0,0.2)',
                line=dict(color='rgba(255,255,255,0)'),
                name='95%置信区间',
                showlegend=True
            ))
            
            # 保险阈值线
            fig_forecast.add_hline(
                y=3.0,
                line_dash="dot",
                annotation_text="保险阈值: ¥3.0/斤",
                line_color="orange",
                annotation_position="right"
            )
            
            fig_forecast.update_layout(
                title=f"{crop_used}价格预测 (未来{forecast_days_used}天)",
                xaxis_title="日期",
                yaxis_title="价格(元/斤)",
                hovermode='x unified',
                height=500,
                yaxis=dict(range=[1.5, 4.5])
            )
            
            st.plotly_chart(fig_forecast, use_container_width=True)
            
            # 预测统计
            col_a, col_b, col_c = st.columns(3)
            
            with col_a:
                avg_price = predicted_prices.mean()
                st.metric("预测均价", f"¥{avg_price:.2f}/斤")
            
            with col_b:
                min_price = predicted_prices.min()
                st.metric("预测最低价", f"¥{min_price:.2f}/斤")
            
            with col_c:
                # 触发理赔概率
                trigger_prob = (predicted_prices < 3.0).sum() / len(predicted_prices) * 100
                st.metric("触发理赔概率", f"{trigger_prob:.0f}%")
            
            # 风险提示
            if trigger_prob > 50:
                st.error(f"⚠️ **风险警告:** 预测期内有{trigger_prob:.0f}%的时间价格低于保险阈值,理赔风险较高!")
            elif trigger_prob > 20:
                st.warning(f"⚠️ **注意:** 预测期内有{trigger_prob:.0f}%的时间价格低于保险阈值")
            else:
                st.success("✅ 价格预测良好,理赔风险较低")
            
            # 参数影响说明
            st.divider()
            with st.expander("📊 当前参数对价格的影响分析"):
                st.markdown(f"""
                **影响因子综合分析:**
                
                - **天气系数 {weather_factor_used:.1f}**: {'恶劣天气推高价格 📈' if weather_factor_used > 0.5 else '良好天气压低价格 📉' if weather_factor_used < 0.5 else '天气正常 ➡️'}
                - **供需系数 {supply_factor_used:.1f}**: {'供不应求推高价格 📈' if supply_factor_used > 0.5 else '供过于求压低价格 📉' if supply_factor_used < 0.5 else '供需平衡 ➡️'}
                - **政策系数 {policy_factor_used:.1f}**: {'政策利好推高价格 📈' if policy_factor_used > 0.5 else '政策不利压低价格 📉' if policy_factor_used < 0.5 else '政策中性 ➡️'}
                
                **综合影响值:** {total_impact:+.2f} 元/斤
                
                💡 **建议:** {'将天气或供需系数调低可降低理赔风险' if trigger_prob > 50 else '将供需系数调高可进一步降低风险' if trigger_prob > 20 else '当前参数设置合理'}
                """)
        else:
            st.info("👈 请在左侧设置预测参数，然后点击「开始预测」按钮")
    
    st.divider()
    
    # 技术说明
    with st.expander("🔧 技术细节"):
        st.markdown("""
        ### LSTM模型架构
        
        **1. 输入特征**
        - 历史价格序列(滑动窗口: 30天)
        - 气象数据(温度、降雨量)
        - 供需指标(库存、产量预估)
        - 政策因子(补贴、进出口政策)
        
        **2. 网络结构**
