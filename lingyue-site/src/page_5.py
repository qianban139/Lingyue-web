"""
凌越智缆 - 告警中心页面 (Page 5)
展示告警列表、告警统计、告警处理等功能
"""

import streamlit as st
import plotly.graph_objects as go
from datetime import datetime

from common import COLORS, apply_custom_css
from session_state import init_session_state, set_state, get_state
from algorithm import MockDataGenerator

# ======================================
# 图表创建函数
# ======================================
def create_alarm_trend_chart():
    """创建告警趋势图"""
    days = ['周一', '周二', '周三', '周四', '周五', '周六', '周日']
    critical = [2, 1, 3, 2, 4, 1, 2]
    warning = [5, 3, 4, 6, 5, 3, 4]
    info = [8, 6, 7, 9, 8, 5, 6]
    
    fig = go.Figure()
    
    fig.add_trace(go.Bar(
        name='紧急',
        x=days,
        y=critical,
        marker_color=COLORS['danger']
    ))
    
    fig.add_trace(go.Bar(
        name='警告',
        x=days,
        y=warning,
        marker_color=COLORS['warning']
    ))
    
    fig.add_trace(go.Bar(
        name='提示',
        x=days,
        y=info,
        marker_color=COLORS['electric']
    ))
    
    fig.update_layout(
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font=dict(color=COLORS['light']),
        barmode='stack',
        legend=dict(orientation='h', yanchor='bottom', y=1.02, xanchor='right', x=1),
        xaxis=dict(showgrid=False, tickfont=dict(color=COLORS['gray_400'])),
        yaxis=dict(showgrid=True, gridcolor='rgba(255,255,255,0.1)', tickfont=dict(color=COLORS['gray_400'])),
        margin=dict(l=40, r=20, t=60, b=40),
        height=250
    )
    
    return fig

def create_alarm_type_chart():
    """创建告警类型分布图"""
    types = ['覆冰超标', '设备离线', '温度异常', '电压波动', '通信中断']
    counts = [15, 8, 12, 6, 5]
    colors = [COLORS['danger'], COLORS['warning'], COLORS['electric'], COLORS['success'], COLORS['gray_400']]
    
    fig = go.Figure(data=[go.Pie(
        labels=types,
        values=counts,
        hole=0.5,
        marker=dict(colors=colors),
        textinfo='label+percent',
        textfont=dict(color=COLORS['light']),
        hovertemplate='%{label}: %{value}条<extra></extra>'
    )])
    
    fig.update_layout(
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font=dict(color=COLORS['light']),
        showlegend=False,
        margin=dict(l=20, r=20, t=20, b=20),
        height=250,
        annotations=[dict(text='46条', x=0.5, y=0.5, font_size=20, showarrow=False, font_color=COLORS['light'])]
    )
    
    return fig

# ======================================
# 页面渲染函数
# ======================================
def render_page():
    """渲染告警中心页面"""
    
    # 初始化告警数据
    if not get_state('alarms'):
        alarms = MockDataGenerator.generate_alarms(15)
        set_state('alarms', alarms)
    
    alarms = get_state('alarms', [])
    
    # 页面标题
    st.markdown(f"""
    <div style="margin-bottom: 24px;">
        <h2 style="margin: 0; font-size: 22px; font-weight: bold; color: white;">告警中心</h2>
        <p style="margin: 4px 0 0 0; font-size: 13px; color: {COLORS['gray_400']};">
            实时监控告警信息，快速响应处理
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # ======================================
    # 告警统计卡片
    # ======================================
    stat_cols = st.columns(4)
    
    # 统计告警数量
    unread_count = len([a for a in alarms if a['status'] == '未处理'])
    critical_count = len([a for a in alarms if a['level'] == 'danger' and a['status'] == '未处理'])
    warning_count = len([a for a in alarms if a['level'] == 'warning' and a['status'] == '未处理'])
    total_count = len(alarms)
    
    stat_data = [
        ('未处理告警', unread_count, COLORS['danger'], '🔴'),
        ('紧急告警', critical_count, COLORS['danger'], '⚠️'),
        ('警告告警', warning_count, COLORS['warning'], '⚡'),
        ('今日告警', total_count, COLORS['electric'], '📋')
    ]
    
    for i, (label, value, color, icon) in enumerate(stat_data):
        with stat_cols[i]:
            st.markdown(f"""
            <div style="background: {COLORS['secondary']}; border-radius: 12px; padding: 20px;
                        border: 1px solid rgba(100, 116, 139, 0.2); text-align: center;">
                <div style="font-size: 28px; margin-bottom: 8px;">{icon}</div>
                <div style="font-size: 32px; font-weight: bold; color: {color};">{value}</div>
                <div style="font-size: 13px; color: {COLORS['gray_400']}; margin-top: 4px;">{label}</div>
            </div>
            """, unsafe_allow_html=True)
    
    st.markdown("<div style='margin-bottom: 24px;'></div>", unsafe_allow_html=True)
    
    # ======================================
    # 告警趋势和类型分布
    # ======================================
    chart_cols = st.columns(2)
    
    with chart_cols[0]:
        st.markdown(f"<h4 style='color: white; font-size: 14px; margin-bottom: 12px;'>告警趋势统计</h4>", unsafe_allow_html=True)
        fig = create_alarm_trend_chart()
        st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})
    
    with chart_cols[1]:
        st.markdown(f"<h4 style='color: white; font-size: 14px; margin-bottom: 12px;'>告警类型分布</h4>", unsafe_allow_html=True)
        fig = create_alarm_type_chart()
        st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})
    
    st.markdown("<div style='margin-bottom: 24px;'></div>", unsafe_allow_html=True)
    
    # ======================================
    # 筛选和操作按钮
    # ======================================
    filter_cols = st.columns([1, 1, 1, 1, 1])
    
    with filter_cols[0]:
        level_filter = st.selectbox(
            '告警级别',
            ['all', 'danger', 'warning', 'info'],
            format_func=lambda x: {
                'all': '全部级别',
                'danger': '紧急',
                'warning': '警告',
                'info': '提示'
            }[x],
            key='alarm_level_filter'
        )
    
    with filter_cols[1]:
        status_filter = st.selectbox(
            '处理状态',
            ['all', 'unprocessed', 'processed'],
            format_func=lambda x: {
                'all': '全部状态',
                'unprocessed': '未处理',
                'processed': '已处理'
            }[x],
            key='alarm_status_filter'
        )
    
    with filter_cols[2]:
        if st.button('✅ 全部标记已读', use_container_width=True):
            for alarm in alarms:
                alarm['status'] = '已处理'
            set_state('alarms', alarms)
            st.rerun()
    
    with filter_cols[3]:
        if st.button('🔄 刷新', use_container_width=True):
            alarms = MockDataGenerator.generate_alarms(15)
            set_state('alarms', alarms)
            st.rerun()
    
    with filter_cols[4]:
        if st.button('⬇️ 导出', use_container_width=True):
            st.info('导出功能开发中...')
    
    st.markdown("<div style='margin-bottom: 16px;'></div>", unsafe_allow_html=True)
    
    # 应用筛选
    filtered_alarms = alarms
    
    if level_filter != 'all':
        filtered_alarms = [a for a in filtered_alarms if a['level'] == level_filter]
    
    if status_filter != 'all':
        status_map = {'unprocessed': '未处理', 'processed': '已处理'}
        filtered_alarms = [a for a in filtered_alarms if a['status'] == status_map.get(status_filter, '')]
    
    # ======================================
    # 告警列表
    # ======================================
    st.markdown(f"<h3 style='color: white; font-size: 16px; margin-bottom: 16px;'>告警列表 ({len(filtered_alarms)}条)</h3>", unsafe_allow_html=True)
    
    for alarm in filtered_alarms:
        # 级别样式
        level_config = {
            'danger': ('🔴 紧急', COLORS['danger'], 'rgba(245, 63, 63, 0.2)'),
            'warning': ('⚡ 警告', COLORS['warning'], 'rgba(255, 125, 0, 0.2)'),
            'info': ('ℹ️ 提示', COLORS['electric'], 'rgba(0, 153, 255, 0.2)')
        }
        level_text, level_color, level_bg = level_config.get(alarm['level'], ('ℹ️ 提示', COLORS['electric'], 'rgba(0, 153, 255, 0.2)'))
        
        # 状态样式
        status_color = COLORS['danger'] if alarm['status'] == '未处理' else COLORS['success']
        
        st.markdown(f"""
        <div style="background: {COLORS['secondary']}; border-radius: 12px; padding: 16px; margin-bottom: 12px;
                    border: 1px solid rgba(100, 116, 139, 0.2);">
            <div style="display: flex; justify-content: space-between; align-items: flex-start;">
                <div style="flex: 1;">
                    <div style="display: flex; align-items: center; gap: 8px; margin-bottom: 8px;">
                        <span style="background: {level_bg}; color: {level_color}; padding: 2px 8px; border-radius: 4px; font-size: 12px;">{level_text}</span>
                        <span style="font-weight: 500; color: {COLORS['light']}; font-size: 14px;">{alarm['id']}</span>
                    </div>
                    <div style="color: {COLORS['light']}; font-size: 14px; margin-bottom: 4px;">{alarm['message']}</div>
                    <div style="display: flex; gap: 16px; margin-top: 8px;">
                        <span style="font-size: 12px; color: {COLORS['gray_400']};">📍 {alarm['device_id']}</span>
                        <span style="font-size: 12px; color: {COLORS['gray_400']};">🕐 {alarm['time']}</span>
                    </div>
                </div>
                <div style="display: flex; align-items: center; gap: 8px;">
                    <span style="color: {status_color}; font-size: 12px;">{alarm['status']}</span>
                    {f'<button style="background: {COLORS["primary"]}; color: white; border: none; border-radius: 4px; padding: 4px 12px; font-size: 12px; cursor: pointer;">处理</button>' if alarm['status'] == '未处理' else ''}
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
