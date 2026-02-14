"""
凌越智缆 - 覆冰监测页面 (Page 3)
展示覆冰监测数据、AI识别结果、历史趋势等
"""

import streamlit as st
import plotly.graph_objects as go

from common import COLORS, apply_custom_css,get_asset_path
from session_state import init_session_state,get_state

# ======================================
# 图表创建函数
# ======================================
def create_ice_thickness_chart():
    """创建覆冰厚度趋势图"""
    hours = [f'{i}:00' for i in range(24)]
    thickness = [5 + i * 0.5 + (i % 5) * 0.3 for i in range(24)]
    threshold = [20] * 24
    
    fig = go.Figure()
    
    fig.add_trace(go.Scatter(
        x=hours,
        y=thickness,
        mode='lines+markers',
        name='覆冰厚度',
        line=dict(color=COLORS['electric'], width=2),
        marker=dict(size=6)
    ))
    
    fig.add_trace(go.Scatter(
        x=hours,
        y=threshold,
        mode='lines',
        name='告警阈值',
        line=dict(color=COLORS['danger'], width=2, dash='dash')
    ))
    
    fig.update_layout(
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font=dict(color=COLORS['light']),
        legend=dict(orientation='h', yanchor='bottom', y=1.02, xanchor='right', x=1),
        xaxis=dict(showgrid=True, gridcolor='rgba(255,255,255,0.1)', tickfont=dict(color=COLORS['gray_400'])),
        yaxis=dict(
            showgrid=True, 
            gridcolor='rgba(255,255,255,0.1)', 
            tickfont=dict(color=COLORS['gray_400']),
            title=dict(
                text='厚度 (mm)', 
                font=dict(color=COLORS['gray_400'])
            )
        ),
        margin=dict(l=60, r=20, t=60, b=40),
        height=300
    )
    
    return fig

def create_temperature_chart():
    """创建温度趋势图"""
    hours = [f'{i}:00' for i in range(24)]
    temp = [-5 - (i % 10) * 0.3 for i in range(24)]
    
    fig = go.Figure()
    
    fig.add_trace(go.Scatter(
        x=hours,
        y=temp,
        mode='lines+markers',
        name='环境温度',
        line=dict(color=COLORS['warning'], width=2),
        marker=dict(size=6),
        fill='tozeroy',
        fillcolor='rgba(255, 125, 0, 0.1)'
    ))
    
    # 添加0度线
    fig.add_hline(y=0, line_dash="dash", line_color=COLORS['danger'], annotation_text="冰点")
    
    fig.update_layout(
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font=dict(color=COLORS['light']),
        showlegend=False,
        xaxis=dict(showgrid=True, gridcolor='rgba(255,255,255,0.1)', tickfont=dict(color=COLORS['gray_400'])),
        yaxis=dict(
            showgrid=True, 
            gridcolor='rgba(255,255,255,0.1)', 
            tickfont=dict(color=COLORS['gray_400']),
            title=dict(
                text='温度 (℃)', 
                font=dict(color=COLORS['gray_400'])
            )
        ),
        margin=dict(l=60, r=20, t=20, b=40),
        height=250
    )
    
    return fig

def create_risk_heatmap():
    """创建风险热力图"""
    import random
    
    regions = ['鄂西地区', '川东地区', '云贵地区', '西北地区', '华北地区']
    hours = [f'{i}:00' for i in range(0, 24, 4)]
    
    # 模拟风险数据
    risk_data = [[random.randint(10, 90) for _ in range(len(hours))] for _ in range(len(regions))]
    
    fig = go.Figure(data=go.Heatmap(
        z=risk_data,
        x=hours,
        y=regions,
        colorscale=[
            [0, COLORS['success']],
            [0.5, COLORS['warning']],
            [1, COLORS['danger']]
        ],
        showscale=True,
        colorbar=dict(
            title=dict(
                text='风险等级', 
                font=dict(color=COLORS['light'])
            ),
            tickfont=dict(color=COLORS['light'])
        )
    ))
    
    fig.update_layout(
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font=dict(color=COLORS['light']),
        xaxis=dict(tickfont=dict(color=COLORS['gray_400'])),
        yaxis=dict(tickfont=dict(color=COLORS['gray_400'])),
        margin=dict(l=80, r=100, t=20, b=40),
        height=250
    )
    
    return fig


# ======================================
# 页面渲染函数
# ======================================
def render_page():
    """渲染覆冰监测页面"""
    
    # 页面标题
    st.markdown(f"""
    <div style="margin-bottom: 24px;">
        <h2 style="margin: 0; font-size: 22px; font-weight: bold; color: white;">覆冰监测</h2>
        <p style="margin: 4px 0 0 0; font-size: 13px; color: {COLORS['gray_400']};">
            实时监控电缆覆冰状态，AI智能识别，精准预警
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # ======================================
    # 实时监测数据卡片
    # ======================================
    monitor_cols = st.columns(4)
    
    monitor_data = [
        ('当前覆冰厚度', f"{get_state('ice_thickness', 12.7)} mm", COLORS['warning'], '❄️'),
        ('环境温度', f"{get_state('env_temp', -5.3)} ℃", COLORS['electric'], '🌡️'),
        ('覆冰告警设备', '3 台', COLORS['danger'], '⚠️'),
        ('监测覆盖率', '98.5%', COLORS['success'], '📊')
    ]
    
    for i, (label, value, color, icon) in enumerate(monitor_data):
        with monitor_cols[i]:
            st.markdown(f"""
            <div style="background: {COLORS['secondary']}; border-radius: 12px; padding: 20px;
                        border: 1px solid rgba(100, 116, 139, 0.2); text-align: center;">
                <div style="font-size: 32px; margin-bottom: 12px;">{icon}</div>
                <div style="font-size: 28px; font-weight: bold; color: {color};">{value}</div>
                <div style="font-size: 13px; color: {COLORS['gray_400']}; margin-top: 4px;">{label}</div>
            </div>
            """, unsafe_allow_html=True)
    
    st.markdown("<div style='margin-bottom: 24px;'></div>", unsafe_allow_html=True)
    
    # ======================================
    # 覆冰趋势图表
    # ======================================
    trend_cols = st.columns([2, 1])
    
    with trend_cols[0]:
        st.markdown(f"<h4 style='color: white; font-size: 14px; margin-bottom: 12px;'>24小时覆冰厚度趋势</h4>", unsafe_allow_html=True)
        fig = create_ice_thickness_chart()
        st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})
    
    with trend_cols[1]:
        st.markdown(f"<h4 style='color: white; font-size: 14px; margin-bottom: 12px;'>温度变化趋势</h4>", unsafe_allow_html=True)
        fig = create_temperature_chart()
        st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})
    
    st.markdown("<div style='margin-bottom: 24px;'></div>", unsafe_allow_html=True)
    
    # ======================================
    # AI识别结果展示（修复路径）
    # ======================================

    st.markdown("<h3 style='color: white; font-size: 18px; margin-bottom: 20px; font-weight: 600;'>🤖 AI智能识别结果对比</h3>", unsafe_allow_html=True)

    ai_cols = st.columns(2)

    with ai_cols[0]:
        st.markdown("""
        <style>
            .ai-card-traditional {
                background: linear-gradient(145deg, rgba(30, 41, 59, 0.9) 0%, rgba(15, 23, 42, 0.9) 100%);
                border-radius: 16px;
                padding: 20px;
                border: 1px solid rgba(100, 116, 139, 0.2);
            }
            .metric-box-traditional {
                background: rgba(30, 41, 59, 0.8);
                border-radius: 10px;
                padding: 12px;
                text-align: center;
                border: 1px solid rgba(100, 116, 139, 0.1);
            }
        </style>
        <div class="ai-card-traditional">
            <div style="display: flex; align-items: center; justify-content: space-between; margin-bottom: 16px;">
                <div style="display: flex; align-items: center; gap: 8px;">
                    <span style="font-size: 20px;">📊</span>
                    <h4 style="margin: 0; font-size: 15px; font-weight: 600; color: #e2e8f0;">传统参数提取</h4>
                </div>
                <span style="background: rgba(100, 116, 139, 0.2); padding: 4px 10px; border-radius: 20px; font-size: 12px; color: #94a3b8;">准确率 85%</span>
            </div>
        """, unsafe_allow_html=True)
        
        # ✅ 修复：使用动态路径
        img_path_1 = get_asset_path("assets/images/t_1.png")
        if img_path_1.exists():
            st.image(str(img_path_1), use_container_width=True)
        else:
            st.markdown(f'<div style="height: 200px; background: rgba(100,116,139,0.1); border-radius: 8px; display: flex; align-items: center; justify-content: center; color: #64748b; flex-direction: column;"><span>传统方法示例图</span><span style="font-size: 10px; margin-top: 8px;">{img_path_1}</span></div>', unsafe_allow_html=True)
        
        st.markdown("""
            <div style="display: flex; gap: 12px; margin-top: 16px;">
                <div class="metric-box-traditional" style="flex: 1;">
                    <div style="font-size: 20px; font-weight: bold; color: #e2e8f0; margin-bottom: 4px;">12.3mm</div>
                    <div style="font-size: 11px; color: #64748b;">识别厚度</div>
                </div>
                <div class="metric-box-traditional" style="flex: 1;">
                    <div style="font-size: 20px; font-weight: bold; color: #e2e8f0; margin-bottom: 4px;">320ms</div>
                    <div style="font-size: 11px; color: #64748b;">处理时间</div>
                </div>
            </div>
            <div style="margin-top: 12px; padding-top: 12px; border-top: 1px solid rgba(100, 116, 139, 0.1);">
                <div style="display: flex; align-items: center; gap: 6px; font-size: 12px; color: #64748b;">
                    <span>⚠️</span>
                    <span>边缘检测算法，易受光照干扰</span>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)

    with ai_cols[1]:
        # 右侧：凌越AI
        st.markdown(f"""
        <style>
            .ai-card-premium {{
                background: linear-gradient(145deg, rgba(22, 93, 255, 0.05) 0%, rgba(30, 41, 59, 0.95) 100%);
                border-radius: 16px;
                padding: 20px;
                border: 1px solid rgba(22, 93, 255, 0.3);
                box-shadow: 0 0 20px rgba(22, 93, 255, 0.1);
            }}
            .metric-box-premium {{
                background: rgba(22, 93, 255, 0.1);
                border-radius: 10px;
                padding: 12px;
                text-align: center;
                border: 1px solid rgba(22, 93, 255, 0.2);
            }}
        </style>
        <div class="ai-card-premium">
            <div style="display: flex; align-items: center; justify-content: space-between; margin-bottom: 16px;">
                <div style="display: flex; align-items: center; gap: 8px;">
                    <span style="font-size: 20px;">🚀</span>
                    <h4 style="margin: 0; font-size: 15px; font-weight: 600; color: {COLORS['primary']};">凌越AI语义分割</h4>
                </div>
                <span style="background: rgba(22, 93, 255, 0.2); color: #60a5fa; padding: 4px 10px; border-radius: 20px; font-size: 12px; font-weight: 600; border: 1px solid rgba(22, 93, 255, 0.3);">准确率 98.2%</span>
            </div>
        """, unsafe_allow_html=True)
        
        # ✅ 修复：使用动态路径
        img_path_2 = get_asset_path("assets/images/26.png")
        if img_path_2.exists():
            st.image(str(img_path_2), use_container_width=True)
        else:
            st.markdown(f'<div style="height: 200px; background: rgba(22,93,255,0.1); border-radius: 8px; display: flex; align-items: center; justify-content: center; color: #60a5fa; flex-direction: column;"><span>AI识别示例图</span><span style="font-size: 10px; margin-top: 8px;">{img_path_2}</span></div>', unsafe_allow_html=True)
        
        st.markdown(f"""
            <div style="display: flex; gap: 12px; margin-top: 16px;">
                <div class="metric-box-premium" style="flex: 1;">
                    <div style="font-size: 20px; font-weight: bold; color: {COLORS['primary']}; margin-bottom: 4px;">12.7mm</div>
                    <div style="font-size: 11px; color: #94a3b8;">识别厚度</div>
                </div>
                <div class="metric-box-premium" style="flex: 1;">
                    <div style="font-size: 20px; font-weight: bold; color: {COLORS['primary']}; margin-bottom: 4px;">85ms</div>
                    <div style="font-size: 11px; color: #94a3b8;">处理时间</div>
                </div>
            </div>
            <div style="margin-top: 12px; padding-top: 12px; border-top: 1px solid rgba(22, 93, 255, 0.1);">
                <div style="display: flex; align-items: center; gap: 6px; font-size: 12px; color: {COLORS['primary']};">
                    <span>✓</span>
                    <span>深度学习语义分割，像素级精度</span>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<div style='margin-bottom: 32px;'></div>", unsafe_allow_html=True)


    
    # ======================================
    # 风险热力图和告警列表
    # ======================================
    bottom_cols = st.columns([1, 1])
    
    with bottom_cols[0]:
        st.markdown(f"<h4 style='color: white; font-size: 14px; margin-bottom: 12px;'>各地区覆冰风险热力图</h4>", unsafe_allow_html=True)
        fig = create_risk_heatmap()
        st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})
    
    with bottom_cols[1]:
        st.markdown(f"<h4 style='color: white; font-size: 14px; margin-bottom: 12px;'>覆冰告警列表</h4>", unsafe_allow_html=True)
        
        # 告警列表
        alarms = [
            {'device': 'DEV1023', 'location': '鄂西地区', 'thickness': 25.3, 'level': 'danger', 'time': '2分钟前'},
            {'device': 'DEV0845', 'location': '川东地区', 'thickness': 18.7, 'level': 'warning', 'time': '15分钟前'},
            {'device': 'DEV0567', 'location': '云贵地区', 'thickness': 16.2, 'level': 'warning', 'time': '32分钟前'},
        ]
        
        for alarm in alarms:
            level_color = COLORS['danger'] if alarm['level'] == 'danger' else COLORS['warning']
            level_text = '严重' if alarm['level'] == 'danger' else '警告'
            
            st.markdown(f"""
            <div style="background: {COLORS['secondary']}; border-radius: 8px; padding: 12px; margin-bottom: 8px;
                        border-left: 4px solid {level_color};">
                <div style="display: flex; justify-content: space-between; align-items: center;">
                    <div>
                        <div style="font-weight: 500; color: {COLORS['light']}; font-size: 13px;">{alarm['device']} · {alarm['location']}</div>
                        <div style="font-size: 12px; color: {COLORS['gray_400']}; margin-top: 4px;">覆冰厚度: {alarm['thickness']}mm</div>
                    </div>
                    <div style="text-align: right;">
                        <span style="background: {level_color}33; color: {level_color}; padding: 2px 8px; border-radius: 4px; font-size: 11px;">{level_text}</span>
                        <div style="font-size: 11px; color: {COLORS['gray_400']}; margin-top: 4px;">{alarm['time']}</div>
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)

# ======================================
# 页面入口
# ======================================
def show():
    """页面入口函数"""
    init_session_state()
    apply_custom_css()
    render_page()
