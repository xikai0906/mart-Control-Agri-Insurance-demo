import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
from scipy.stats import norm
from datetime import datetime, timedelta

st.set_page_config(page_title="量化模型后台", page_icon="📊", layout="wide")

st.title("📊 量化模型后台 - 金融工程与精算分析")
st.markdown("---")

# Tab导航
tab1, tab2, tab3, tab4 = st.tabs([
    "💰 保险+期权损益分析", 
    "📈 波动率与保费精算",
    "🎯 智能核保演示",
    "⚡ 智能理赔演示"
])

# ==================== Tab1: 保险+亚式看跌期权损益分析 ====================
with tab1:
    st.header("💰 保险+亚式看跌期权 损益分析模型")
    
    st.markdown("""
    ### 模型说明
    
    **亚式看跌期权（Asian Put Option）**是一种路径依赖型期权，其收益取决于标的资产在一段时间内的平均价格，
    而非到期时的即时价格。相比欧式期权，亚式期权能更好地平滑价格波动，降低被操纵风险。
    
    **"保险+亚式看跌期权"结构：**
    1. 农户向保险公司购买价格保险（保障最低收购价 K）
    2. 保险公司向风险管理公司买入亚式看跌期权对冲风险
    3. 风险管理公司在期货市场进行动态对冲
    """)
    
    st.divider()
    
    # 参数设置
    st.subheader("⚙️ 参数设置")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        S0 = st.number_input("当前市场价格 S₀ (元/斤)", min_value=1.0, max_value=10.0, value=3.0, step=0.1)
        K = st.number_input("保险约定价格 K (元/斤)", min_value=1.0, max_value=10.0, value=3.0, step=0.1)
        T = st.slider("保险期限 T (月)", min_value=1, max_value=12, value=6)
    
    with col2:
        sigma = st.slider("价格波动率 σ", min_value=0.1, max_value=0.8, value=0.25, step=0.05,key="sigma_volatility")
        r = st.slider("无风险利率 r", min_value=0.01, max_value=0.10, value=0.03, step=0.01,key="risk_free_rate")
        Q = st.number_input("承保数量 Q (吨)", min_value=1, max_value=1000, value=100, step=10,key="quantity_insured")
    
    with col3:
        premium_rate = st.slider("保费率 (%)", min_value=1.0, max_value=20.0, value=8.0, step=0.5)
        option_premium_rate = st.slider("期权费率 (%)", min_value=1.0, max_value=15.0, value=6.0, step=0.5)
    
    # 计算保费和期权费
    insurance_premium = K * Q * 1000 * (premium_rate / 100)  # 转换为公斤
    option_premium = K * Q * 1000 * (option_premium_rate / 100)
    
    st.divider()
    
    # 模拟价格路径
    st.subheader("📈 价格路径模拟（蒙特卡洛）")
    
    n_simulations = st.slider("模拟路径数量", 100, 1000, 500, 100)
    n_steps = T * 30  # 每月30天
    
    # 生成价格路径
    dt = T / n_steps
    paths = np.zeros((n_simulations, n_steps + 1))
    paths[:, 0] = S0
    
    for t in range(1, n_steps + 1):
        z = np.random.standard_normal(n_simulations)
        paths[:, t] = paths[:, t-1] * np.exp((r - 0.5 * sigma**2) * dt + sigma * np.sqrt(dt) * z)
    
    # 计算亚式平均价格
    asian_prices = paths.mean(axis=1)
    
    # 绘制部分路径
    fig_paths = go.Figure()
    
    # 显示前50条路径
    for i in range(min(50, n_simulations)):
        fig_paths.add_trace(go.Scatter(
            x=np.arange(n_steps + 1),
            y=paths[i],
            mode='lines',
            line=dict(width=0.5),
            opacity=0.3,
            showlegend=False,
            hoverinfo='skip'
        ))
    
    # 添加平均路径
    avg_path = paths.mean(axis=0)
    fig_paths.add_trace(go.Scatter(
        x=np.arange(n_steps + 1),
        y=avg_path,
        mode='lines',
        name='平均路径',
        line=dict(color='red', width=3)
    ))
    
    # 添加保险价格线
    fig_paths.add_hline(y=K, line_dash="dash", line_color="orange",
                       annotation_text=f"保险价格 K={K}")
    
    fig_paths.update_layout(
        title=f"价格路径模拟 (n={n_simulations}条)",
        xaxis_title="时间步",
        yaxis_title="价格(元/斤)",
        height=500
    )
    
    st.plotly_chart(fig_paths, use_container_width=True)
    
    st.divider()
    
    # 损益分析
    st.subheader("💸 损益分析")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("#### 🏢 保险公司视角")
        
        # 保险公司收入
        st.success(f"**保费收入:** ¥{insurance_premium:,.2f}")
        
        # 保险公司支出
        # 1. 期权费支出
        st.error(f"**期权费支出:** ¥{option_premium:,.2f}")
        
        # 2. 赔付支出（对农户）
        # 当市场平均价格 < K 时，保险公司需要赔付
        insurance_payouts = np.maximum(K - asian_prices, 0) * Q * 1000
        avg_insurance_payout = insurance_payouts.mean()
        
        st.error(f"**预期赔付支出:** ¥{avg_insurance_payout:,.2f}")
        
        # 3. 期权收入（从风险管理公司）
        # 当市场平均价格 < K 时，看跌期权行权
        option_payoffs = np.maximum(K - asian_prices, 0) * Q * 1000
        avg_option_payoff = option_payoffs.mean()
        
        st.success(f"**期权行权收入:** ¥{avg_option_payoff:,.2f}")
        
        # 保险公司净利润
        insurance_profit = insurance_premium - option_premium - avg_insurance_payout + avg_option_payoff
        
        if insurance_profit > 0:
            st.success(f"### 💰 **预期净利润:** ¥{insurance_profit:,.2f}")
        else:
            st.error(f"### 📉 **预期净亏损:** ¥{abs(insurance_profit):,.2f}")
        
        # 利润率
        profit_margin = (insurance_profit / insurance_premium) * 100 if insurance_premium > 0 else 0
        st.metric("利润率", f"{profit_margin:.2f}%")
    
    with col2:
        st.markdown("#### 👨‍🌾 农户视角")
        
        # 农户支出
        st.error(f"**保费支出:** ¥{insurance_premium:,.2f}")
        
        # 农户收入（无保险情况）
        # 假设产量固定为 Q * 1000 公斤
        revenue_no_insurance = asian_prices * Q * 1000
        avg_revenue_no_insurance = revenue_no_insurance.mean()
        
        st.info(f"**无保险预期收入:** ¥{avg_revenue_no_insurance:,.2f}")
        
        # 农户收入（有保险情况）
        # 收入 = max(市场价, 保险价) * 数量
        protected_prices = np.maximum(asian_prices, K)
        revenue_with_insurance = protected_prices * Q * 1000
        avg_revenue_with_insurance = revenue_with_insurance.mean()
        
        st.info(f"**有保险预期收入:** ¥{avg_revenue_with_insurance:,.2f}")
        
        # 获得的保险赔付
        st.success(f"**预期获赔金额:** ¥{avg_insurance_payout:,.2f}")
        
        # 农户净收益（扣除保费）
        net_revenue = avg_revenue_with_insurance - insurance_premium
        
        st.success(f"### 💰 **净收益（扣除保费）:** ¥{net_revenue:,.2f}")
        
        # 保险保障效果
        income_protection = ((avg_revenue_with_insurance - avg_revenue_no_insurance) / avg_revenue_no_insurance) * 100
        st.metric("收入保障提升", f"{income_protection:.2f}%")
    
    st.divider()
    
    # 损益分布图
    st.subheader("📊 损益分布分析")
    
    col1, col2 = st.columns(2)
    
    with col1:
        # 保险公司利润分布
        insurance_profits = insurance_premium - option_premium - insurance_payouts + option_payoffs
        
        fig_profit_dist = go.Figure()
        fig_profit_dist.add_trace(go.Histogram(
            x=insurance_profits,
            nbinsx=50,
            name='利润分布',
            marker_color='lightblue'
        ))
        
        fig_profit_dist.add_vline(x=insurance_profits.mean(), 
                                 line_dash="dash", line_color="red",
                                 annotation_text=f"平均: ¥{insurance_profits.mean():,.0f}")
        
        fig_profit_dist.update_layout(
            title="保险公司利润分布",
            xaxis_title="利润(元)",
            yaxis_title="频数",
            height=400
        )
        
        st.plotly_chart(fig_profit_dist, use_container_width=True)
        
        # 风险指标
        st.markdown("**风险指标:**")
        st.write(f"- VaR(95%): ¥{np.percentile(insurance_profits, 5):,.2f}")
        st.write(f"- CVaR(95%): ¥{insurance_profits[insurance_profits <= np.percentile(insurance_profits, 5)].mean():,.2f}")
        st.write(f"- 亏损概率: {(insurance_profits < 0).sum() / n_simulations * 100:.2f}%")
    
    with col2:
        # 农户收益分布
        farmer_net_revenue = revenue_with_insurance - insurance_premium
        
        fig_farmer_dist = go.Figure()
        fig_farmer_dist.add_trace(go.Histogram(
            x=farmer_net_revenue,
            nbinsx=50,
            name='收益分布',
            marker_color='lightgreen'
        ))
        
        fig_farmer_dist.add_vline(x=farmer_net_revenue.mean(),
                                 line_dash="dash", line_color="red",
                                 annotation_text=f"平均: ¥{farmer_net_revenue.mean():,.0f}")
        
        fig_farmer_dist.update_layout(
            title="农户净收益分布",
            xaxis_title="净收益(元)",
            yaxis_title="频数",
            height=400
        )
        
        st.plotly_chart(fig_farmer_dist, use_container_width=True)
        
        # 保障效果
        st.markdown("**保障效果:**")
        st.write(f"- 最低收益: ¥{farmer_net_revenue.min():,.2f}")
        st.write(f"- 最高收益: ¥{farmer_net_revenue.max():,.2f}")
        st.write(f"- 收益标准差: ¥{farmer_net_revenue.std():,.2f}")
    
    st.divider()
    
    # 敏感性分析
    st.subheader("🎯 敏感性分析 - 不同市场价格下的损益")
    
    # 生成不同终值价格的损益
    final_prices = np.linspace(1.5, 4.5, 100)
    
    # 农户损益（有保险 vs 无保险）
    farmer_revenue_no_ins = final_prices * Q * 1000
    farmer_revenue_with_ins = np.maximum(final_prices, K) * Q * 1000 - insurance_premium
    
    # 保险公司损益
    insurance_payout_curve = np.maximum(K - final_prices, 0) * Q * 1000
    option_payoff_curve = np.maximum(K - final_prices, 0) * Q * 1000
    insurance_company_profit = insurance_premium - option_premium - insurance_payout_curve + option_payoff_curve
    
    fig_sensitivity = go.Figure()
    
    # 农户收益线
    fig_sensitivity.add_trace(go.Scatter(
        x=final_prices,
        y=farmer_revenue_no_ins,
        mode='lines',
        name='农户收益(无保险)',
        line=dict(color='gray', dash='dash', width=2)
    ))
    
    fig_sensitivity.add_trace(go.Scatter(
        x=final_prices,
        y=farmer_revenue_with_ins,
        mode='lines',
        name='农户收益(有保险)',
        line=dict(color='green', width=3)
    ))
    
    # 保险公司利润线
    fig_sensitivity.add_trace(go.Scatter(
        x=final_prices,
        y=insurance_company_profit,
        mode='lines',
        name='保险公司利润',
        line=dict(color='blue', width=3),
        yaxis='y2'
    ))
    
    fig_sensitivity.add_vline(x=K, line_dash="dot", line_color="red",
                             annotation_text=f"执行价 K={K}")
    
    fig_sensitivity.update_layout(
        title="价格敏感性分析",
        xaxis_title="市场平均价格(元/斤)",
        yaxis_title="农户收益(元)",
        yaxis2=dict(
            title="保险公司利润(元)",
            overlaying='y',
            side='right'
        ),
        height=500,
        hovermode='x unified'
    )
    
    st.plotly_chart(fig_sensitivity, use_container_width=True)

# ==================== Tab2: 波动率与保费精算 ====================
with tab2:
    st.header("📈 波动率分析与保费动态精算")
    
    st.markdown("""
    ### Black-Scholes-Merton 期权定价模型
    
    亚式看跌期权的理论价格受多个因素影响，其中**波动率(σ)**是最关键的参数之一。
    波动率越高，期权价值越大，因此保费也需要相应调整。
    """)
    
    st.divider()
    
    # 参数设置
    col1, col2 = st.columns([1, 3])
    
    with col1:
        st.subheader("⚙️ 定价参数")
        
        S_base = st.number_input("现货价格 S₀", min_value=1.0, value=3.0, step=0.1,key="spot_price_base")
        K_base = st.number_input("执行价格 K", min_value=1.0, value=3.0, step=0.1,key="strike_price_base")
        T_base = st.slider("到期时间 T (年)", 0.1, 2.0, 0.5, 0.1,key="time_to_maturity_base")
        r_base = st.slider("无风险利率 r", 0.01, 0.10, 0.03, 0.01,key="risk_free_rate_base")
        
        st.divider()
        
        st.markdown("**市场状况选择:**")
        market_condition = st.radio(
            "选择市场波动情景",
            ["低波动(σ=15%)", "正常波动(σ=25%)", "高波动(σ=40%)", "极端波动(σ=60%)"],
            index=1
        )
        
        sigma_map = {
            "低波动(σ=15%)": 0.15,
            "正常波动(σ=25%)": 0.25,
            "高波动(σ=40%)": 0.40,
            "极端波动(σ=60%)": 0.60
        }
        sigma_current = sigma_map[market_condition]
    
    with col2:
        st.subheader("📊 波动率对期权价格的影响")
        
        # 计算不同波动率下的期权价格（简化的Black-Scholes公式）
        sigma_range = np.linspace(0.05, 0.80, 100)
        
        def asian_put_approx(S, K, T, r, sigma):
            """亚式期权近似定价（Kemna-Vorst方法）"""
            # 调整参数
            sigma_adj = sigma / np.sqrt(3)
            b = 0.5 * (r - 0.5 * sigma**2)
            
            d1 = (np.log(S / K) + (b + 0.5 * sigma_adj**2) * T) / (sigma_adj * np.sqrt(T))
            d2 = d1 - sigma_adj * np.sqrt(T)
            
            put_price = K * np.exp(-r * T) * norm.cdf(-d2) - S * np.exp(b * T) * norm.cdf(-d1)
            return max(put_price, 0)
        
        option_prices = [asian_put_approx(S_base, K_base, T_base, r_base, sig) for sig in sigma_range]
        
        # 当前波动率对应的价格
        current_price = asian_put_approx(S_base, K_base, T_base, r_base, sigma_current)
        
        fig_vol = go.Figure()
        
        fig_vol.add_trace(go.Scatter(
            x=sigma_range * 100,
            y=option_prices,
            mode='lines',
            name='期权价格',
            line=dict(color='blue', width=3),
            fill='tozeroy',
            fillcolor='rgba(0,100,255,0.2)'
        ))
        
        # 标注当前波动率
        fig_vol.add_vline(x=sigma_current * 100, line_dash="dash", line_color="red",
                         annotation_text=f"当前波动率: {sigma_current*100:.0f}%")
        
        fig_vol.add_trace(go.Scatter(
            x=[sigma_current * 100],
            y=[current_price],
            mode='markers',
            name='当前价格',
            marker=dict(color='red', size=15, symbol='star')
        ))
        
        fig_vol.update_layout(
            title="波动率 vs 亚式看跌期权价格",
            xaxis_title="波动率 σ (%)",
            yaxis_title="期权价格(元)",
            height=400
        )
        
        st.plotly_chart(fig_vol, use_container_width=True)
        
        # 显示当前定价
        col_a, col_b, col_c = st.columns(3)
        
        with col_a:
            st.metric("当前期权价格", f"¥{current_price:.4f}/斤")
        
        with col_b:
            # Vega: 期权价格对波动率的敏感度
            vega = asian_put_approx(S_base, K_base, T_base, r_base, sigma_current + 0.01) - current_price
            st.metric("Vega (敏感度)", f"¥{vega:.4f}")
        
        with col_c:
            # 建议保费率
            suggested_premium_rate = (current_price / K_base) * 100 * 1.3  # 加30%风险溢价
            st.metric("建议保费率", f"{suggested_premium_rate:.2f}%")
    
    st.divider()
    
    # Greeks 分析
    st.subheader("🔢 期权Greeks分析")
    
    st.markdown("""
    **Greeks**是衡量期权价格对各种市场参数敏感度的指标：
    - **Delta (Δ)**: 对标的资产价格的敏感度
    - **Gamma (Γ)**: Delta的变化率
    - **Vega (ν)**: 对波动率的敏感度
    - **Theta (Θ)**: 对时间流逝的敏感度
    - **Rho (ρ)**: 对利率的敏感度
    """)
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Delta曲线
        S_range = np.linspace(S_base * 0.7, S_base * 1.3, 100)
        prices_S = [asian_put_approx(s, K_base, T_base, r_base, sigma_current) for s in S_range]
        delta_approx = np.gradient(prices_S, S_range)
        
        fig_delta = go.Figure()
        fig_delta.add_trace(go.Scatter(
            x=S_range,
            y=delta_approx,
            mode='lines',
            name='Delta',
            line=dict(color='purple', width=3)
        ))
        
        fig_delta.add_vline(x=K_base, line_dash="dot", line_color="red",
                           annotation_text=f"执行价 K={K_base}")
        
        fig_delta.update_layout(
            title="Delta曲线",
            xaxis_title="标的资产价格(元)",
            yaxis_title="Delta",
            height=350
        )
        
        st.plotly_chart(fig_delta, use_container_width=True)
    
    with col2:
        # Vega曲线
        vega_values = []
        for sig in sigma_range:
            base_price = asian_put_approx(S_base, K_base, T_base, r_base, sig)
            up_price = asian_put_approx(S_base, K_base, T_base, r_base, sig + 0.01)
            vega_values.append(up_price - base_price)
        
        fig_vega = go.Figure()
        fig_vega.add_trace(go.Scatter(
            x=sigma_range * 100,
            y=vega_values,
            mode='lines',
            name='Vega',
            line=dict(color='orange', width=3)
        ))
        
        fig_vega.add_vline(x=sigma_current * 100, line_dash="dot", line_color="red",
                          annotation_text=f"当前波动率: {sigma_current*100:.0f}%")
        
        fig_vega.update_layout(
            title="Vega曲线",
            xaxis_title="波动率(%)",
            yaxis_title="Vega",
            height=350
        )
        
        st.plotly_chart(fig_vega, use_container_width=True)
    
    st.divider()
    
    # 动态保费精算表
    st.subheader("📋 不同波动率情景下的保费精算")
    
    volatility_scenarios = [0.15, 0.20, 0.25, 0.30, 0.35, 0.40, 0.50, 0.60]
    
    pricing_table = []
    for vol in volatility_scenarios:
        opt_price = asian_put_approx(S_base, K_base, T_base, r_base, vol)
        
        # 保费率 = (期权价格 / 执行价) * (1 + 风险溢价) * 100%
        risk_premium = 0.20 + vol * 0.3  # 风险溢价随波动率增加
        premium_rate = (opt_price / K_base) * (1 + risk_premium) * 100
        
        # 每吨保费
        premium_per_ton = premium_rate / 100 * K_base * 1000
        
        pricing_table.append({
            '波动率': f"{vol*100:.0f}%",
            '期权价格(元/斤)': f"¥{opt_price:.4f}",
            '风险溢价': f"{risk_premium*100:.1f}%",
            '建议保费率': f"{premium_rate:.2f}%",
            '保费(元/吨)': f"¥{premium_per_ton:.2f}",
            '市场情景': '低波动' if vol < 0.2 else ('正常' if vol < 0.35 else '高波动')
        })
    
    df_pricing = pd.DataFrame(pricing_table)
    
    # 高亮显示当前波动率
    def highlight_current(row):
        if row['波动率'] == f"{sigma_current*100:.0f}%":
            return ['background-color: #ffffcc'] * len(row)
        return [''] * len(row)
    
    st.dataframe(
        df_pricing.style.apply(highlight_current, axis=1),
        use_container_width=True,
        hide_index=True
    )
    
    st.info("💡 **说明**: 黄色高亮行为当前市场波动率对应的建议保费")

# ==================== Tab3: 智能核保演示 ====================
with tab3:
    st.header("🎯 智能核保演示 - AI风险评估")
    
    st.markdown("""
    ### 核保流程
    智能核保系统通过AI技术自动评估投保风险，综合考虑：
    - 📍 地理位置风险
    - 🌦️ 历史气象数据
    - 📊 作物种植历史
    - 💰 历史理赔记录
    - 🛰️ 卫星遥感数据
    """)
    
    st.divider()
    
    col1, col2 = st.columns([1, 2])
    
    with col1:
        st.subheader("📝 投保申请信息")
        
        farmer_name = st.text_input("农户姓名", value="张三")
        farm_location = st.selectbox("农田位置", 
            ["广西南宁-武鸣", "广西钦州-灵山", "广西崇左-扶绥"])
        crop_type_ins = st.selectbox("投保作物", 
            ["沃柑", "甘蔗", "荔枝"])
        area_ins = st.number_input("种植面积(亩)", min_value=1, max_value=500, value=50)
        insured_value = st.number_input("保险金额(万元)", min_value=1, max_value=500, value=25)
        
        has_history = st.checkbox("是否有历史投保记录", value=True)
        
        if has_history:
            claim_history = st.slider("过去3年理赔次数", 0, 10, 2,key="claim_history_count")
        else:
            claim_history = 0
        
        st.divider()
        
        if st.button("🚀 提交核保申请", type="primary", use_container_width=True):
            st.session_state.underwriting_submitted = True
    
    with col2:
        st.subheader("🤖 AI核保分析")
        
        if 'underwriting_submitted' in st.session_state and st.session_state.underwriting_submitted:
            
            # 模拟核保过程
            with st.spinner("AI正在分析风险..."):
                import time
                
                progress_bar = st.progress(0)
                status_text = st.empty()
                
                steps = [
                    ("📍 分析地理位置风险...", 0.2),
                    ("🌦️ 调取历史气象数据...", 0.4),
                    ("🛰️ 获取卫星遥感影像...", 0.6),
                    ("📊 评估历史理赔情况...", 0.8),
                    ("🎯 计算综合风险评分...", 1.0)
                ]
                
                for step_name, progress in steps:
                    status_text.text(step_name)
                    progress_bar.progress(progress)
                    time.sleep(0.8)
            
            st.success("✅ 核保分析完成!")
            
            st.divider()
            
            # 风险评估结果
            st.subheader("📊 风险评估报告")
            
            # 模拟风险评分
            location_risk = np.random.randint(60, 85)
            weather_risk = np.random.randint(50, 80)
            crop_risk = np.random.randint(65, 90)
            history_risk = 100 - (claim_history * 8)  # 理赔次数越多风险越高
            
            综合评分 = (location_risk * 0.3 + weather_risk * 0.3 + 
                       crop_risk * 0.2 + history_risk * 0.2)
            
            col_a, col_b, col_c = st.columns(3)
            
            with col_a:
                st.metric("地理位置风险", f"{location_risk}分", 
                         help="基于历史灾害数据")
            
            with col_b:
                st.metric("气象风险", f"{weather_risk}分",
                         help="基于未来30天天气预测")
            
            with col_c:
                st.metric("作物风险", f"{crop_risk}分",
                         help="基于作物特性和市场波动")
            
            st.divider()
            
            # 综合评分显示
            col1, col2 = st.columns([1, 2])
            
            with col1:
                st.metric("综合风险评分", f"{综合评分:.1f}分", 
                         help="满分100分，分数越高风险越低")
                
                if 综合评分 >= 80:
                    risk_level = "🟢 低风险"
                    st.success(risk_level)
                elif 综合评分 >= 60:
                    risk_level = "🟡 中等风险"
                    st.warning(risk_level)
                else:
                    risk_level = "🔴 高风险"
                    st.error(risk_level)
            
            with col2:
                # 雷达图展示各维度风险
                categories = ['地理位置', '气象条件', '作物类型', '历史记录']
                values = [location_risk, weather_risk, crop_risk, history_risk]
                
                fig_radar = go.Figure()
                
                fig_radar.add_trace(go.Scatterpolar(
                    r=values + [values[0]],  # 闭合图形
                    theta=categories + [categories[0]],
                    fill='toself',
                    name='风险评分',
                    line_color='blue'
                ))
                
                fig_radar.update_layout(
                    polar=dict(
                        radialaxis=dict(
                            visible=True,
                            range=[0, 100]
                        )
                    ),
                    showlegend=False,
                    height=300
                )
                
                st.plotly_chart(fig_radar, use_container_width=True)
            
            st.divider()
            
            # 核保决策
            st.subheader("✅ 核保决策")
            
            if 综合评分 >= 70:
                st.success("### 🎉 核保通过")
                
                # 计算保费
                base_rate = 0.08  # 基础费率8%
                risk_adjustment = (100 - 综合评分) / 1000  # 风险调整
                final_rate = base_rate + risk_adjustment
                
                premium = insured_value * 10000 * final_rate
                
                col_a, col_b = st.columns(2)
                
                with col_a:
                    st.info(f"""
                    **保险方案:**
                    - 保险金额: ¥{insured_value}万元
                    - 保费率: {final_rate*100:.2f}%
                    - 应缴保费: ¥{premium:,.2f}
                    - 保险期限: 1年
                    """)
                
                with col_b:
                    st.info(f"""
                    **风险提示:**
                    - 注意防范极端天气
                    - 建议安装监测设备
                    - 及时关注天气预警
                    - 做好田间管理记录
                    """)
                
                if st.button("📋 生成电子保单", type="primary"):
                    st.balloons()
                    st.success("✅ 保单已生成并发送至手机!")
            
            elif 综合评分 >= 50:
                st.warning("### ⚠️ 附条件承保")
                st.info("""
                **承保条件:**
                - 需要增加保费10%
                - 需要实地查勘
                - 建议安装IoT监测设备
                - 限制部分高风险区域
                """)
            
            else:
                st.error("### ❌ 拒绝承保")
                st.warning("""
                **拒保原因:**
                - 综合风险评分过低
                - 历史理赔次数过多
                - 该区域近期灾害频发
                
                **建议:**
                - 改善种植管理
                - 一年后重新申请
                - 或考虑其他保险产品
                """)

# ==================== Tab4: 智能理赔演示 ====================
with tab4:
    st.header("⚡ 智能理赔演示 - AI自动审核")
    
    st.markdown("""
    ### 理赔流程
    通过AI图像识别、卫星遥感和区块链智能合约，实现全自动化理赔：
    1. 📷 农户上传受灾照片
    2. 🤖 AI自动识别灾害类型和受损程度
    3. 🛰️ 卫星数据交叉验证
    4. ✅ 智能合约自动触发赔付
    5. 💰 理赔款即时到账
    """)
    
    st.divider()
    
    col1, col2 = st.columns([1, 2])
    
    with col1:
        st.subheader("📤 上传受灾照片")
        
        uploaded_img = st.file_uploader(
            "选择受灾照片",
            type=['jpg', 'png', 'jpeg'],
            help="支持jpg/png格式"
        )
        
        if uploaded_img:
            st.image(uploaded_img, caption="受灾现场照片", use_container_width=True)
        else:
            # 显示示例图片占位符
            st.info("👆 请上传受灾作物照片进行AI识别")
        
        st.divider()
        
        st.subheader("📝 理赔申请信息")
        
        claim_farmer = st.text_input("农户姓名", value="李四")
        claim_location = st.selectbox("受灾位置", 
            ["广西钦州-灵山", "广西南宁-武鸣", "广西崇左-扶绥"])
        claim_date = st.date_input("灾害发生日期", value=datetime.now())
        claim_area = st.number_input("受灾面积(亩)", min_value=1, max_value=100, value=10)
        
        st.divider()
        
        if uploaded_img and st.button("🚀 提交理赔申请", type="primary", use_container_width=True):
            st.session_state.claim_submitted = True
    
    with col2:
        st.subheader("🤖 AI智能审核")
        
        if 'claim_submitted' in st.session_state and st.session_state.claim_submitted and uploaded_img:
            
            # 模拟AI识别过程
            with st.spinner("AI正在分析照片..."):
                import time
                
                progress_bar = st.progress(0)
                status_text = st.empty()
                
                steps = [
                    ("🖼️ 图像预处理...", 0.15),
                    ("🤖 AI模型识别中...", 0.35),
                    ("🛰️ 调取卫星遥感数据...", 0.55),
                    ("🌦️ 交叉验证气象数据...", 0.75),
                    ("📊 计算赔付金额...", 0.90),
                    ("✅ 分析完成!", 1.0)
                ]
                
                for step_name, progress in steps:
                    status_text.text(step_name)
                    progress_bar.progress(progress)
                    time.sleep(0.6)
            
            st.success("✅ AI识别完成!")
            
            st.divider()
            
            # AI识别结果
            st.subheader("📊 AI识别结果")
            
            disaster_types = ['洪涝', '干旱', '病虫害', '暴雨', '台风']
            probabilities = np.random.dirichlet(np.ones(5)) * 100
            
            main_disaster = disaster_types[np.argmax(probabilities)]
            main_prob = np.max(probabilities)
            
            damage_level = np.random.randint(45, 85)
            
            col_a, col_b = st.columns(2)
            
            with col_a:
                st.success(f"### 🎯 识别结果: **{main_disaster}**")
                st.metric("AI置信度", f"{main_prob:.1f}%")
            
            with col_b:
                st.error(f"### 📉 受损程度: **{damage_level}%**")
                st.metric("评估面积", f"{claim_area}亩")
            
            # 各类灾害概率
            with st.expander("📈 详细识别概率"):
                prob_df = pd.DataFrame({
                    '灾害类型': disaster_types,
                    '识别概率(%)': probabilities
                }).sort_values('识别概率(%)', ascending=False)
                
                fig_prob = px.bar(
                    prob_df,
                    x='识别概率(%)',
                    y='灾害类型',
                    orientation='h',
                    color='识别概率(%)',
                    color_continuous_scale='Blues'
                )
                
                st.plotly_chart(fig_prob, use_container_width=True)
            
            st.divider()
            
            # 卫星数据交叉验证
            st.subheader("🛰️ 卫星遥感数据交叉验证")
            
            col_sat1, col_sat2, col_sat3 = st.columns(3)
            
            with col_sat1:
                sat_verified = np.random.choice([True, False], p=[0.92, 0.08])
                if sat_verified:
                    st.success("✅ 卫星影像验证通过")
                else:
                    st.warning("⚠️ 卫星影像待人工复核")
                st.caption(f"灾害发生日期: {claim_date}")
            
            with col_sat2:
                weather_verified = np.random.choice([True, False], p=[0.89, 0.11])
                if weather_verified:
                    st.success("✅ 气象数据验证通过")
                else:
                    st.warning("⚠️ 气象数据待人工复核")
                st.caption(f"当日降雨: {np.random.randint(50, 150)}mm")
            
            with col_sat3:
                ndvi_verified = np.random.choice([True, False], p=[0.87, 0.13])
                if ndvi_verified:
                    st.success("✅ NDVI指数验证通过")
                else:
                    st.warning("⚠️ NDVI指数待人工复核")
                st.caption("植被健康度: 异常")
            
            # 综合验证评分
            verification_score = (sat_verified + weather_verified + ndvi_verified) / 3
            
            st.divider()
            
            # 智能合约触发
            st.subheader("⚡ 区块链智能合约触发")
            
            if verification_score >= 0.66:  # 至少2项验证通过
                st.success("### 🎉 验证通过，触发智能合约自动理赔!")
                
                # 计算赔付金额
                unit_amount = 5000  # 每亩保额
                compensation = claim_area * unit_amount * (damage_level / 100)
                
                col1, col2 = st.columns(2)
                
                with col1:
                    st.info(f"""
                    **理赔详情:**
                    - 受灾面积: {claim_area}亩
                    - 受损程度: {damage_level}%
                    - 每亩保额: ¥{unit_amount:,}
                    - 理赔金额: ¥{compensation:,.2f}
                    """)
                
                with col2:
                    # 模拟区块链信息
                    tx_hash = "0x" + "".join(np.random.choice(list('0123456789abcdef'), 64))
                    block_number = np.random.randint(1000000, 2000000)
                    
                    st.code(f"""
# 区块链交易信息
Transaction Hash: {tx_hash[:20]}...
Block Number: {block_number}
Status: ✅ Success
Gas Used: 21000
                    """, language="python")
                
                st.divider()
                
                # 赔付进度
                st.subheader("💰 理赔进度追踪")
                
                # 模拟赔付流程
                with st.spinner("正在处理赔付..."):
                    import time
                    
                    timeline_steps = [
                        ("📝 理赔申请已提交", "已完成", True),
                        ("🤖 AI审核通过", "已完成", True),
                        ("🛰️ 数据交叉验证完成", "已完成", True),
                        ("⚡ 智能合约已触发", "已完成", True),
                        ("💰 款项已转入农户账户", "处理中...", False)
                    ]
                    
                    for i, (step_name, status, completed) in enumerate(timeline_steps):
                        time.sleep(0.5)
                        if completed:
                            st.success(f"✅ {step_name} - {status}")
                        else:
                            st.info(f"⏳ {step_name} - {status}")
                    
                    time.sleep(1)
                
                st.success("### ✅ 理赔完成!")
                st.balloons()
                
                st.success(f"""
                ### 💰 理赔款已到账: ¥{compensation:,.2f}
                
                **到账信息:**
                - 到账账户: {claim_farmer} (尾号1234)
                - 到账时间: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
                - 理赔周期: **仅用时2分钟!**
                
                📱 短信通知已发送
                📧 电子理赔单已发送至邮箱
                """)
                
                # 效率对比
                st.divider()
                st.subheader("⚡ 效率对比")
                
                col_old, col_new = st.columns(2)
                
                with col_old:
                    st.error("""
                    **传统理赔流程:**
                    - ⏰ 平均耗时: 7-15天
                    - 📞 电话申请
                    - 🚗 查勘员实地勘查(2-3天)
                    - 📋 人工审核(3-5天)
                    - ✍️ 多级审批(2-3天)
                    - 💰 财务转账(1-2天)
                    """)
                
                with col_new:
                    st.success("""
                    **AI智能理赔:**
                    - ⚡ 耗时: **2分钟**
                    - 📱 在线提交
                    - 🤖 AI自动识别(秒级)
                    - 🛰️ 自动交叉验证(秒级)
                    - ⚡ 智能合约触发(即时)
                    - 💰 自动到账(即时)
                    
                    **效率提升: 99.5%!**
                    """)
            
            else:
                st.warning("### ⚠️ 验证未完全通过，需要人工复核")
                st.info("""
                **处理建议:**
                - 补充更多受灾照片
                - 提供气象局证明
                - 或等待人工审核(预计1-2个工作日)
                """)

# 页脚
st.divider()
st.info("""
💡 **技术说明:** 
- 亚式期权定价采用 Kemna-Vorst 近似方法
- AI识别基于ResNet-50卷积神经网络
- 卫星数据来自Sentinel-2遥感影像
- 智能合约部署在以太坊测试网
- 所有演示数据为模拟生成，仅供展示
""")
