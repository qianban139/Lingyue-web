"""
凌越智缆 - 数字孪生页面 (Page 5)
展示三维仿真、环境还原、风险预判等功能
"""

import streamlit as st
import streamlit.components.v1 as components
import html
import plotly.graph_objects as go
from datetime import datetime
import random

from common import COLORS, apply_custom_css
from session_state import init_session_state, set_state, get_state

# ======================================
# 图表创建函数
# ======================================
def create_3d_cable_model():
    """创建3D电缆模型可视化"""
    x = [i for i in range(0, 101, 5)]
    y = [random.uniform(-5, 5) for _ in x]
    z = [random.uniform(10, 30) for _ in x]
    
    # 覆冰厚度数据
    ice_thickness = [random.uniform(0, 25) for _ in x]
    
    fig = go.Figure()
    
    # 主电缆线
    fig.add_trace(go.Scatter3d(
        x=x, y=y, z=z,
        mode='lines',
        line=dict(color=COLORS['primary'], width=4),
        name='电缆线路'
    ))
    
    # 覆冰点
    fig.add_trace(go.Scatter3d(
        x=x, y=y, z=z,
        mode='markers',
        marker=dict(
            size=[t/2 for t in ice_thickness],
            color=ice_thickness,
            colorscale=[[0, COLORS['success']], [0.5, COLORS['warning']], [1, COLORS['danger']]],
            showscale=True,
            # ✅ 修复：colorbar的titlefont改为title.font
            colorbar=dict(
                title=dict(
                    text='覆冰厚度(mm)',
                    font=dict(color=COLORS['light'])
                )
            )
        ),
        name='覆冰监测点',
        hovertemplate='覆冰厚度: %{marker.color:.1f}mm<extra></extra>'
    ))
    
    fig.update_layout(
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font=dict(color=COLORS['light']),
        scene=dict(
            # ✅ 修复：3D场景坐标轴的titlefont
            xaxis=dict(
                title=dict(text='距离(m)', font=dict(color=COLORS['gray_400'])),
                tickfont=dict(color=COLORS['gray_400'])
            ),
            yaxis=dict(
                title=dict(text='横向偏移(m)', font=dict(color=COLORS['gray_400'])),
                tickfont=dict(color=COLORS['gray_400'])
            ),
            zaxis=dict(
                title=dict(text='高度(m)', font=dict(color=COLORS['gray_400'])),
                tickfont=dict(color=COLORS['gray_400'])
            ),
            bgcolor='rgba(15, 23, 42, 0.5)'
        ),
        margin=dict(l=0, r=0, t=0, b=0),
        height=450,
        showlegend=False
    )
    
    return fig

def create_environment_simulation():
    """创建环境仿真图表"""
    hours = [f'{i}:00' for i in range(24)]
    wind_speed = [random.uniform(0, 20) for _ in range(24)]
    humidity = [random.uniform(60, 95) for _ in range(24)]
    
    fig = go.Figure()
    
    fig.add_trace(go.Scatter(
        x=hours, y=wind_speed,
        mode='lines',
        name='风速',
        line=dict(color=COLORS['electric'], width=2),
        yaxis='y'
    ))
    
    fig.add_trace(go.Scatter(
        x=hours, y=humidity,
        mode='lines',
        name='湿度',
        line=dict(color=COLORS['warning'], width=2),
        yaxis='y2'
    ))
    
    fig.update_layout(
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font=dict(color=COLORS['light']),
        xaxis=dict(showgrid=True, gridcolor='rgba(255,255,255,0.1)', tickfont=dict(color=COLORS['gray_400'])),
        # ✅ 修复：yaxis的titlefont
        yaxis=dict(
            title=dict(text='风速 (m/s)', font=dict(color=COLORS['electric'])),
            tickfont=dict(color=COLORS['gray_400']),
            showgrid=True,
            gridcolor='rgba(255,255,255,0.1)'
        ),
        # ✅ 修复：yaxis2的titlefont
        yaxis2=dict(
            title=dict(text='湿度 (%)', font=dict(color=COLORS['warning'])),
            tickfont=dict(color=COLORS['gray_400']),
            overlaying='y',
            side='right'
        ),
        legend=dict(orientation='h', yanchor='bottom', y=1.02, xanchor='right', x=1),
        margin=dict(l=60, r=60, t=60, b=40),
        height=250
    )
    
    return fig

def create_risk_prediction_chart():
    """创建风险预测图表"""
    days = ['今天', '明天', '后天', '第4天', '第5天', '第6天', '第7天']
    risk_scores = [random.randint(20, 80) for _ in range(7)]
    
    colors = [COLORS['success'] if r < 40 else COLORS['warning'] if r < 70 else COLORS['danger'] for r in risk_scores]
    
    fig = go.Figure(data=[go.Bar(
        x=days,
        y=risk_scores,
        marker_color=colors,
        text=risk_scores,
        textposition='auto',
        textfont=dict(color=COLORS['light'])
    )])
    
    fig.update_layout(
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font=dict(color=COLORS['light']),
        xaxis=dict(showgrid=False, tickfont=dict(color=COLORS['gray_400'])),
        # ✅ 修复：yaxis的titlefont
        yaxis=dict(
            title=dict(text='风险评分', font=dict(color=COLORS['gray_400'])),
            tickfont=dict(color=COLORS['gray_400']),
            showgrid=True,
            gridcolor='rgba(255,255,255,0.1)',
            range=[0, 100]
        ),
        margin=dict(l=60, r=20, t=20, b=40),
        height=250
    )
    
    return fig


# ======================================
# 页面渲染函数
# ======================================
def render_page():
    """渲染数字孪生页面"""
    
    # 页面标题
    st.markdown(f"""
    <div style="margin-bottom: 24px;">
        <h2 style="margin: 0; font-size: 22px; font-weight: bold; color: white;">数字孪生</h2>
        <p style="margin: 4px 0 0 0; font-size: 13px; color: {COLORS['gray_400']};">
            三维仿真电缆环境，实时还原覆冰状态，辅助预判风险
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # ======================================
    # 模型精度统计
    # ======================================
    stat_cols = st.columns(4)
    
    stat_data = [
        ('模型精度', '99.8%', COLORS['primary'], '🎯'),
        ('实时延迟', '<100ms', COLORS['success'], '⚡'),
        ('覆盖线路', '1,250km', COLORS['electric'], '📏'),
        ('监测点', '3,680个', COLORS['warning'], '📍')
    ]
    
    for i, (label, value, color, icon) in enumerate(stat_data):
        with stat_cols[i]:
            st.markdown(f"""
            <div style="background: {COLORS['secondary']}; border-radius: 12px; padding: 20px;
                        border: 1px solid rgba(100, 116, 139, 0.2); text-align: center;">
                <div style="font-size: 28px; margin-bottom: 8px;">{icon}</div>
                <div style="font-size: 24px; font-weight: bold; color: {color};">{value}</div>
                <div style="font-size: 13px; color: {COLORS['gray_400']}; margin-top: 4px;">{label}</div>
            </div>
            """, unsafe_allow_html=True)
    
    st.markdown("<div style='margin-bottom: 24px;'></div>", unsafe_allow_html=True)
    
    # ======================================
    # 3D模型和控制面板
    # ======================================
    model_cols = st.columns([3, 1])
    
    with model_cols[0]:
        st.markdown(f"<h4 style='color: white; font-size: 14px; margin-bottom: 12px;'>电缆线路三维仿真</h4>", unsafe_allow_html=True)
        fig = create_3d_cable_model()
        st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})
    
    with model_cols[1]:
        st.markdown(f"<h4 style='color: white; font-size: 14px; margin-bottom: 12px;'>视图控制</h4>", unsafe_allow_html=True)
        
        # 视图模式选择
        view_mode = st.radio(
            '视图模式',
            ['3D视图', '2D平面', '剖面视图'],
            key='twin_view_mode'
        )
        
        st.markdown("<div style='margin: 16px 0;'></div>", unsafe_allow_html=True)
        
        # 显示选项
        st.markdown(f"<p style='color: {COLORS['gray_400']}; font-size: 13px;'>显示选项</p>", unsafe_allow_html=True)
        st.checkbox('显示电缆线路', value=True, key='show_cable')
        st.checkbox('显示覆冰监测', value=True, key='show_ice')
        st.checkbox('显示温度分布', value=False, key='show_temp')
        st.checkbox('显示应力分析', value=False, key='show_stress')
        
        st.markdown("<div style='margin: 16px 0;'></div>", unsafe_allow_html=True)
        
        # 线路选择
        st.markdown(f"<p style='color: {COLORS['gray_400']}; font-size: 13px;'>选择线路</p>", unsafe_allow_html=True)
        st.selectbox(
            '',
            ['鄂西主干线', '川东支线A', '云贵联络线', '西北输电线', '华北配电网'],
            label_visibility='collapsed',
            key='cable_line_select'
        )
        
        st.markdown("<div style='margin: 16px 0;'></div>", unsafe_allow_html=True)
        
        if st.button('🔄 刷新模型', use_container_width=True):
            st.rerun()
    
    st.markdown("<div style='margin-bottom: 24px;'></div>", unsafe_allow_html=True)
    
    # ======================================
    # 环境仿真和风险预测
    # ======================================
    bottom_cols = st.columns([1, 1])
    
    with bottom_cols[0]:
        st.markdown(f"<h4 style='color: white; font-size: 14px; margin-bottom: 12px;'>环境参数仿真</h4>", unsafe_allow_html=True)
        fig = create_environment_simulation()
        st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})
    
    with bottom_cols[1]:
        st.markdown(f"<h4 style='color: white; font-size: 14px; margin-bottom: 12px;'>未来7天风险预测</h4>", unsafe_allow_html=True)
        fig = create_risk_prediction_chart()
        st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})
    
    st.markdown("<div style='margin-bottom: 24px;'></div>", unsafe_allow_html=True)
    
    # ======================================
    # 关键监测点列表（真实按钮版）
    # ======================================
    st.markdown(f"<h3 style='color: white; font-size: 16px; margin-bottom: 16px;'>关键监测点状态</h3>", unsafe_allow_html=True)

    # 模拟监测点数据
    monitoring_points = [
        {'id': 'MP001', 'location': '鄂西地区-塔#102', 'ice': 12.5, 'temp': -5.2, 'stress': 85, 'risk': 'low'},
        {'id': 'MP002', 'location': '川东地区-塔#245', 'ice': 18.3, 'temp': -8.1, 'stress': 92, 'risk': 'medium'},
        {'id': 'MP003', 'location': '云贵地区-塔#089', 'ice': 24.7, 'temp': -10.5, 'stress': 98, 'risk': 'high'},
        {'id': 'MP004', 'location': '西北地区-塔#156', 'ice': 8.2, 'temp': -2.3, 'stress': 72, 'risk': 'low'},
        {'id': 'MP005', 'location': '华北地区-塔#301', 'ice': 15.6, 'temp': -6.8, 'stress': 88, 'risk': 'medium'},
    ]

    # 定义列宽比例（与之前HTML表格对应）
    cols_header = st.columns([1.2, 2, 1, 1, 1, 1, 1])

    # 表头（使用markdown美化）
    headers = ['监测点编号', '位置', '覆冰厚度', '温度', '应力', '风险等级', '操作']
    for col, header in zip(cols_header, headers):
        col.markdown(f"""
        <div style="padding: 12px 0; font-weight: 600; color: {COLORS['light']}; font-size: 12px; border-bottom: 2px solid {COLORS['gray_800']};">
            {header}
        </div>
        """, unsafe_allow_html=True)

    # 数据行（每行用columns布局，包含真实按钮）
    for idx, point in enumerate(monitoring_points):
        # 定义颜色
        ice_color = COLORS['success'] if point['ice'] < 10 else COLORS['warning'] if point['ice'] < 20 else COLORS['danger']
        stress_color = COLORS['success'] if point['stress'] < 80 else COLORS['warning'] if point['stress'] < 95 else COLORS['danger']
        
        risk_config = {
            'low': ('rgba(0, 180, 42, 0.2)', '#00B42A', '低风险'),
            'medium': ('rgba(255, 125, 0, 0.2)', '#FF7D00', '中风险'),
            'high': ('rgba(245, 63, 63, 0.2)', '#F53F3F', '高风险')
        }
        risk_bg, risk_color, risk_text = risk_config.get(point['risk'], ('rgba(100, 116, 139, 0.2)', '#64748B', '未知'))
        
        # 创建行布局
        cols = st.columns([1.2, 2, 1, 1, 1, 1, 1])
        
        with cols[0]:
            st.markdown(f"<span style='font-weight: 500; color: {COLORS['light']};'>{point['id']}</span>", unsafe_allow_html=True)
        
        with cols[1]:
            st.markdown(f"<span style='color: {COLORS['light']};'>{point['location']}</span>", unsafe_allow_html=True)
        
        with cols[2]:
            st.markdown(f"<span style='color: {ice_color};'>{point['ice']}mm</span>", unsafe_allow_html=True)
        
        with cols[3]:
            st.markdown(f"<span style='color: {COLORS['light']};'>{point['temp']}℃</span>", unsafe_allow_html=True)
        
        with cols[4]:
            st.markdown(f"<span style='color: {stress_color};'>{point['stress']}%</span>", unsafe_allow_html=True)
        
        with cols[5]:
            st.markdown(f"""
            <span style="background: {risk_bg}; color: {risk_color}; padding: 2px 8px; border-radius: 4px; font-size: 12px; border: 1px solid {risk_color};">
                {risk_text}
            </span>
            """, unsafe_allow_html=True)
        
        with cols[6]:
            # ✅ 真实按钮，可触发Python回调
            if st.button('查看详情', key=f'detail_btn_{point["id"]}_{idx}', type='primary'):
                # 存储选中状态
                st.session_state.selected_point = point
                st.session_state.show_detail_modal = True
                st.rerun()

    # 显示详情弹窗（示例）
    if st.session_state.get('show_detail_modal', False):
        point = st.session_state.selected_point
        with st.container():
            st.markdown("---")
            st.subheader(f"监测点详情: {point['id']}")
            col1, col2 = st.columns(2)
            with col1:
                st.metric("覆冰厚度", f"{point['ice']}mm")
                st.metric("温度", f"{point['temp']}℃")
            with col2:
                st.metric("应力", f"{point['stress']}%")
                st.metric("风险等级", risk_text)
            
            if st.button('关闭', key='close_modal'):
                st.session_state.show_detail_modal = False
                st.rerun()
        st.markdown("---")
    

# ======================================
# 页面入口
# ======================================
def show():
    """页面入口函数"""
    init_session_state()
    apply_custom_css()
    render_page()
