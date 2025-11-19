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
            
            area = st.slider("受灾面积(亩)", 1, 50, 10, key="受灾面积")
            unit_amount = 5000  # 每亩保额
            
            suggested_amount = area * unit_amount * (damage_level / 100)
            
            st.success(f"### 建议理赔: ¥{suggested_amount:,.0f}")
    
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
```
        Input Layer (多变量时间序列)
            ↓
        LSTM Layer 1 (128 units, return_sequences=True)
            ↓
        Dropout (0.2)
            ↓
        LSTM Layer 2 (64 units)
            ↓
        Dropout (0.2)
            ↓
        Dense Layer (32 units, ReLU)
            ↓
        Output Layer (1 unit, Linear)
```
        
        **3. 训练参数**
        - 损失函数: MSE (均方误差)
        - 优化器: Adam (learning_rate=0.001)
        - Batch Size: 32
        - Epochs: 100
        
        **4. 性能指标**
        - MAE (平均绝对误差): ¥0.15/斤
        - RMSE (均方根误差): ¥0.21/斤
        - R² Score: 0.87
        """)

# ==================== Tab3: 自动化理赔流程 ====================
with tab3:
    st.header("⚡ 自动化理赔流程演示")
    
    st.markdown("""
    展示从理赔申请到赔付到账的全自动化流程,突出AI技术在各环节的作用。
    """)
    
    # 模拟案例数据
    demo_case = {
        "农户姓名": "李明",
        "保单号": "ZNBX2024001237",
        "作物类型": "沃柑",
        "种植面积": "15亩",
        "投保金额": "¥75,000",
        "受灾类型": "洪涝灾害",
        "受损程度": "65%",
        "理赔金额": "¥48,750"
    }
    
    # 显示案例信息
    with st.expander("📋 查看演示案例详情", expanded=True):
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("农户姓名", demo_case["农户姓名"])
            st.metric("保单号", demo_case["保单号"])
        with col2:
            st.metric("作物类型", demo_case["作物类型"])
            st.metric("种植面积", demo_case["种植面积"])
        with col3:
            st.metric("投保金额", demo_case["投保金额"])
            st.metric("受灾类型", demo_case["受灾类型"])
        with col4:
            st.metric("受损程度", demo_case["受损程度"])
            st.metric("预计理赔", demo_case["理赔金额"])
    
    st.divider()
    
    # 初始化session state
    if 'demo_running' not in st.session_state:
        st.session_state.demo_running = False
    if 'demo_paused' not in st.session_state:
        st.session_state.demo_paused = False
    if 'current_step' not in st.session_state:
        st.session_state.current_step = 0
    
    # 控制按钮
    col_btn1, col_btn2, col_btn3 = st.columns([1, 1, 2])
    
    with col_btn1:
        if st.button("▶️ 开始演示" if not st.session_state.demo_running else "🔄 重新开始", 
                     type="primary", use_container_width=True, key="开始按钮"):
            st.session_state.demo_running = True
            st.session_state.demo_paused = False
            st.session_state.current_step = 0
            st.rerun()
    
    with col_btn2:
        if st.session_state.demo_running:
            if st.button("⏸️ 暂停" if not st.session_state.demo_paused else "▶️ 继续", 
                         use_container_width=True, key="暂停按钮"):
                st.session_state.demo_paused = not st.session_state.demo_paused
                st.rerun()
    
    # 流程步骤定义
    steps = [
        {
            "title": "📝 农户提交理赔申请",
            "desc": f"农户{demo_case['农户姓名']}通过手机APP提交理赔申请",
            "data": {
                "申请时间": "2024-11-19 09:23:15",
                "申请方式": "手机APP",
                "上传照片": "3张现场照片",
                "GPS定位": "广西南宁市武鸣区"
            },
            "time": "T+0分钟"
        },
        {
            "title": "🤖 AI图像识别",
            "desc": "深度学习模型自动分析受灾照片",
            "data": {
                "识别结果": demo_case["受灾类型"],
                "置信度": "94.3%",
                "受损面积": demo_case["种植面积"],
                "受损程度": demo_case["受损程度"]
            },
            "time": "T+2分钟"
        },
        {
            "title": "🔍 多维数据交叉验证",
            "desc": "系统自动调取多源数据进行交叉验证",
            "data": {
                "气象数据": "11月18日暴雨 187mm/24h ✅",
                "卫星遥感": "检测到大面积积水区域 ✅",
                "GPS验证": "与投保地块位置吻合 ✅",
                "历史记录": "该农户无欺诈记录 ✅"
            },
            "time": "T+4分钟"
        },
        {
            "title": "✅ 智能审核决策",
            "desc": "AI综合分析,给出审核建议",
            "data": {
                "风险评分": "92分(低风险)",
                "审核结果": "✅ 建议通过",
                "理赔金额": demo_case["理赔金额"],
                "计算依据": f"{demo_case['投保金额']} × {demo_case['受损程度']}"
            },
            "time": "T+6分钟"
        },
        {
            "title": "📋 人工复核(可选)",
            "desc": "系统自动判定为低风险案件,跳过人工复核",
            "data": {
                "复核状态": "已跳过(低风险案件)",
                "审批权限": "系统自动审批",
                "节省时间": "约25分钟"
            },
            "time": "T+6分钟"
        },
        {
            "title": "💰 自动赔付",
            "desc": "通过区块链智能合约触发赔付",
            "data": {
                "赔付金额": demo_case["理赔金额"],
                "收款账户": "621098******3456(李明)",
                "交易哈希": "0x7f9fade1c0d57a7af66ab4ead7...",
                "区块高度": "#18,934,521"
            },
            "time": "T+8分钟"
        },
        {
            "title": "✅ 理赔完成",
            "desc": "农户收到赔付款和电子理赔单",
            "data": {
                "到账时间": "2024-11-19 09:31:27",
                "总耗时": "8分钟12秒",
                "理赔单号": "LP20241119092315",
                "满意度": "⭐⭐⭐⭐⭐ 5.0分"
            },
            "time": "T+8分钟"
        }
    ]
    
    # 演示执行逻辑
    if st.session_state.demo_running:
        progress_container = st.empty()
        
        # 显示当前步骤
        if st.session_state.current_step < len(steps):
            step = steps[st.session_state.current_step]
            progress = (st.session_state.current_step + 1) / len(steps)
            
            with progress_container.container():
                st.progress(progress)
                st.success(f"### {step['title']}")
                st.info(step['desc'])
                
                # 显示详细数据
                if step['data']:
                    cols = st.columns(len(step['data']))
                    for j, (key, value) in enumerate(step['data'].items()):
                        with cols[j]:
                            st.markdown(f"**{key}**")
                            st.code(value, language="text")
                
                st.caption(f"⏱️ {step['time']}")
            
            # 如果没有暂停，自动前进到下一步
            if not st.session_state.demo_paused:
                time.sleep(2)
                st.session_state.current_step += 1
                st.rerun()
        else:
            # 演示完成
            with progress_container.container():
                st.progress(1.0)
                st.balloons()
                st.success("🎉 理赔流程演示完成!")
                
                # 显示最终总结
                st.divider()
                st.markdown("### 📊 理赔效率对比")
                
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.metric("传统理赔耗时", "7-15天", "-99.5%", delta_color="inverse")
                with col2:
                    st.metric("AI智能理赔", "8分钟", "+99.5%")
                with col3:
                    st.metric("效率提升", "2,625倍", "")
            
            # 重置状态
            st.session_state.demo_running = False
            st.session_state.current_step = 0
    
    st.divider()
    
    # 对比传统流程
    st.subheader("📊 传统流程 vs AI流程对比")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### 传统理赔流程")
        st.error("""
        **⏱️ 平均耗时: 7-15天**
        
        1. 📝 农户电话/线下申请 (1天)
        2. 👨‍💼 查勘员实地勘查 (2-3天)
        3. 📋 人工资料审核 (3-5天)
        4. ✍️ 多级审批流程 (2-3天)
        5. 💰 财务转账赔付 (1-2天)
        
        **痛点:**
        - ❌ 效率低下
        - ❌ 人工成本高
        - ❌ 容易出错
        - ❌ 透明度不足
        """)
    
    with col2:
        st.markdown("### AI智能理赔流程")
        st.success("""
        **⚡ 平均耗时: 8分钟**
        
        1. 📱 在线提交申请 (即时)
        2. 🤖 AI自动识别 (2分钟)
        3. 🔍 数据交叉验证 (2分钟)
        4. ✅ 智能审核决策 (2分钟)
        5. 💰 自动化赔付 (2分钟)
        
        **优势:**
        - ✅ 效率提升**99.5%**
        - ✅ 成本降低**70%**
        - ✅ 准确率**94%+**
        - ✅ 全程可追溯
        """)
    
    st.divider()
    
    # 关键技术
    st.subheader("🔑 关键技术栈")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        **🤖 AI技术**
        - 计算机视觉(CV)
        - 自然语言处理(NLP)
        - 时间序列预测
        - 强化学习
        """)
    
    with col2:
        st.markdown("""
        **🔗 区块链技术**
        - 智能合约
        - 分布式账本
        - 数据溯源
        - 防篡改机制
        """)
    
    with col3:
        st.markdown("""
        **☁️ 云计算**
        - 微服务架构
        - API网关
        - 实时数据流
        - 自动扩展
        """)

# ==================== Tab4: 技术架构 ====================
with tab4:
    st.header("📊 系统技术架构")
    
    st.markdown("""
    ### 🏗️ 整体架构图
    
    智控农险系统采用**微服务架构**,结合AI、区块链、大数据等技术,构建全链条智能风控平台。
    """)
    
    # 架构图(用Mermaid绘制)
    st.markdown("""
```mermaid
    graph TB
        A[农户端 Mobile/Web] --> B[API网关]
        C[保险公司端 Web] --> B
        
        B --> D[微服务层]
        
        D --> E[用户服务]
        D --> F[保单服务]
        D --> G[理赔服务]
        D --> H[AI服务]
        
        H --> I[图像识别模型]
        H --> J[价格预测模型]
        H --> K[风险评估模型]
        
        G --> L[区块链层]
        L --> M[智能合约]
        L --> N[分布式账本]
        
        E --> O[数据库层]
        F --> O
        G --> O
        
        O --> P[MySQL 用户数据]
        O --> Q[MongoDB 文档数据]
        O --> R[Redis 缓存]
        
        H --> S[大数据平台]
        S --> T[气象数据]
        S --> U[遥感数据]
        S --> V[市场数据]
```
    """)
    
    st.divider()
    
    # 技术选型
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("💻 前端技术栈")
        st.code("""
        - Framework: Streamlit / React
        - UI Library: Ant Design / MUI
        - Charts: Plotly / ECharts
        - Maps: Mapbox / Leaflet
        - State: Redux / Zustand
        """, language="text")
        
        st.subheader("🔧 后端技术栈")
        st.code("""
        - Language: Python / Go
        - Framework: FastAPI / Gin
        - ORM: SQLAlchemy / GORM
        - Message Queue: RabbitMQ / Kafka
        - Cache: Redis
        """, language="text")
    
    with col2:
        st.subheader("🤖 AI/ML技术栈")
        st.code("""
        - Deep Learning: PyTorch / TensorFlow
        - CV: OpenCV / Pillow
        - NLP: Transformers / spaCy
        - Time Series: Prophet / LSTM
        - Deployment: TorchServe / ONNX
        """, language="text")
        
        st.subheader("☁️ DevOps技术栈")
        st.code("""
        - Container: Docker / Kubernetes
        - CI/CD: GitHub Actions / Jenkins
        - Monitoring: Prometheus / Grafana
        - Logging: ELK Stack
        - Cloud: AWS / Aliyun
        """, language="text")
    
    st.divider()
    
    # 数据流图
    st.subheader("📈 数据流向图")
    
    st.markdown("""
```mermaid
    sequenceDiagram
        participant 农户
        participant APP
        participant API
        participant AI模型
        participant 区块链
        participant 数据库
        
        农户->>APP: 1. 提交理赔申请
        APP->>API: 2. 上传数据
        API->>AI模型: 3. 请求AI识别
        AI模型->>API: 4. 返回识别结果
        API->>数据库: 5. 保存理赔记录
        API->>区块链: 6. 上链存证
        区块链->>API: 7. 返回交易哈希
        API->>APP: 8. 返回审核结果
        APP->>农户: 9. 显示理赔状态
```
    """)
    
    st.divider()
    
    # 性能指标
    st.subheader("⚡ 性能指标")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("API响应时间", "< 100ms", "99th percentile")
    
    with col2:
        st.metric("AI识别速度", "< 2s", "单张图片")
    
    with col3:
        st.metric("系统可用性", "99.9%", "SLA")
    
    with col4:
        st.metric("并发处理", "10,000+", "QPS")

# 页脚
st.divider()
st.info("""
💡 **技术支持:** 本系统基于最新的AI技术和金融科技实践,持续迭代优化中。
如有技术合作或咨询需求,欢迎联系我们!
""")
