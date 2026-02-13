"""
凌越智缆 - 设备管理页面 (Page 1)
展示设备列表、设备详情、设备筛选和搜索功能
"""

import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime

from common import COLORS, render_status_badge, apply_custom_css
from session_state import init_session_state, set_state, get_state, get_paginated_data, get_total_pages
from algorithm import MockDataGenerator, DeviceAnalytics, DataProcessor

# ======================================
# 图表创建函数
# ======================================
def create_device_type_chart(devices):
    """创建设备类型分布图表"""
    type_stats = DeviceAnalytics.get_devices_by_type(devices)
    
    labels = list(type_stats.keys())
    values = [stats['total'] for stats in type_stats.values()]
    colors = [COLORS['primary'], COLORS['success'], COLORS['warning'], COLORS['electric'], COLORS['gray_500']]
    
    fig = go.Figure(data=[go.Pie(
        labels=labels,
        values=values,
        hole=0.4,
        marker=dict(colors=colors),
        textinfo='label+percent',
        textfont=dict(color=COLORS['light']),
        hovertemplate='%{label}: %{value}台<extra></extra>'
    )])
    
    fig.update_layout(
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font=dict(color=COLORS['light']),
        showlegend=False,
        margin=dict(l=20, r=20, t=20, b=20),
        height=250
    )
    
    return fig

def create_status_chart(devices):
    """创建设备状态分布图表"""
    status_summary = DataProcessor.get_status_summary(devices)
    
    labels = list(status_summary.keys())
    values = list(status_summary.values())
    colors = [COLORS['success'], COLORS['danger'], COLORS['warning'], COLORS['gray_400']]
    
    fig = go.Figure(data=[go.Bar(
        x=labels,
        y=values,
        marker_color=colors,
        text=values,
        textposition='auto',
        textfont=dict(color=COLORS['light'])
    )])
    
    fig.update_layout(
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font=dict(color=COLORS['light']),
        xaxis=dict(showgrid=False, tickfont=dict(color=COLORS['gray_400'])),
        yaxis=dict(showgrid=True, gridcolor='rgba(255,255,255,0.1)', tickfont=dict(color=COLORS['gray_400'])),
        margin=dict(l=40, r=20, t=20, b=40),
        height=250
    )
    
    return fig

def create_region_chart(devices):
    """创建地区分布图表"""
    region_stats = DeviceAnalytics.get_devices_by_region(devices)
    
    regions = list(region_stats.keys())
    online_counts = [stats['online'] for stats in region_stats.values()]
    alarm_counts = [stats['alarm'] for stats in region_stats.values()]
    
    fig = go.Figure()
    
    fig.add_trace(go.Bar(
        name='在线',
        x=regions,
        y=online_counts,
        marker_color=COLORS['success']
    ))
    
    fig.add_trace(go.Bar(
        name='告警',
        x=regions,
        y=alarm_counts,
        marker_color=COLORS['warning']
    ))
    
    fig.update_layout(
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font=dict(color=COLORS['light']),
        barmode='group',
        legend=dict(orientation='h', yanchor='bottom', y=1.02, xanchor='right', x=1),
        xaxis=dict(showgrid=False, tickfont=dict(color=COLORS['gray_400'])),
        yaxis=dict(showgrid=True, gridcolor='rgba(255,255,255,0.1)', tickfont=dict(color=COLORS['gray_400'])),
        margin=dict(l=40, r=20, t=60, b=40),
        height=250
    )
    
    return fig

# ======================================
# 页面渲染函数
# ======================================
def render_page():
    """渲染设备管理页面"""
    
    # 初始化设备数据
    if not get_state('all_devices'):
        devices = MockDataGenerator.generate_devices(120)
        set_state('all_devices', devices)
        set_state('filtered_devices', devices)
    
    devices = get_state('all_devices', [])
    filtered_devices = get_state('filtered_devices', devices)
    
    # 计算统计数据
    stats = DeviceAnalytics.calculate_statistics(devices)
    
    # 页面标题
    st.markdown(f"""
    <div style="margin-bottom: 24px;">
        <h2 style="margin: 0; font-size: 22px; font-weight: bold; color: white;">设备管理</h2>
        <p style="margin: 4px 0 0 0; font-size: 13px; color: {COLORS['gray_400']};">
            共管理 {stats.get('total', 0)} 台设备，在线率 {stats.get('online_rate', 0)}%
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # ======================================
    # 统计概览卡片
    # ======================================
    stat_cols = st.columns(5)
    
    stat_data = [
        ('总设备数', stats.get('total', 0), COLORS['primary'], '💻'),
        ('在线设备', stats.get('online', 0), COLORS['success'], '✅'),
        ('离线设备', stats.get('offline', 0), COLORS['danger'], '❌'),
        ('告警设备', stats.get('alarm', 0), COLORS['warning'], '⚠️'),
        ('维护中', stats.get('maintenance', 0), COLORS['gray_400'], '🔧')
    ]
    
    for i, (label, value, color, icon) in enumerate(stat_data):
        with stat_cols[i]:
            st.markdown(f"""
            <div style="background: {COLORS['secondary']}; border-radius: 12px; padding: 16px;
                        border: 1px solid rgba(100, 116, 139, 0.2); text-align: center;">
                <div style="font-size: 24px; margin-bottom: 8px;">{icon}</div>
                <div style="font-size: 24px; font-weight: bold; color: {color};">{value}</div>
                <div style="font-size: 12px; color: {COLORS['gray_400']};">{label}</div>
            </div>
            """, unsafe_allow_html=True)
    
    st.markdown("<div style='margin-bottom: 24px;'></div>", unsafe_allow_html=True)
    
    # ======================================
    # 图表分析区域
    # ======================================
    chart_cols = st.columns(3)
    
    with chart_cols[0]:
        st.markdown(f"<h4 style='color: white; font-size: 14px; margin-bottom: 12px;'>设备类型分布</h4>", unsafe_allow_html=True)
        fig = create_device_type_chart(devices)
        st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})
    
    with chart_cols[1]:
        st.markdown(f"<h4 style='color: white; font-size: 14px; margin-bottom: 12px;'>设备状态分布</h4>", unsafe_allow_html=True)
        fig = create_status_chart(devices)
        st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})
    
    with chart_cols[2]:
        st.markdown(f"<h4 style='color: white; font-size: 14px; margin-bottom: 12px;'>地区分布</h4>", unsafe_allow_html=True)
        fig = create_region_chart(devices)
        st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})
    
    st.markdown("<div style='margin-bottom: 24px;'></div>", unsafe_allow_html=True)
    
    # ======================================
    # 搜索和筛选
    # ======================================
    filter_cols = st.columns([2, 1, 1, 1])
    
    with filter_cols[0]:
        search_query = st.text_input('🔍 搜索设备', placeholder='输入设备编号或名称', key='device_search')
        if search_query != get_state('search_query', ''):
            set_state('search_query', search_query)
            set_state('current_page_num', 1)
    
    with filter_cols[1]:
        status_filter = st.selectbox(
            '状态筛选',
            ['all', 'online', 'offline', 'alarm', 'maintenance'],
            format_func=lambda x: {
                'all': '全部状态',
                'online': '在线',
                'offline': '离线',
                'alarm': '告警',
                'maintenance': '维护中'
            }[x],
            key='status_filter'
        )
    
    with filter_cols[2]:
        type_filter = st.selectbox(
            '类型筛选',
            ['all', 'high', 'low', 'terminal', 'robot', 'drone'],
            format_func=lambda x: {
                'all': '全部类型',
                'high': '高压电缆',
                'low': '低压电缆',
                'terminal': '监测终端',
                'robot': '除冰机器人',
                'drone': '巡检无人机'
            }[x],
            key='type_filter'
        )
    
    with filter_cols[3]:
        if st.button('🔄 刷新', use_container_width=True):
            devices = MockDataGenerator.generate_devices(120)
            set_state('all_devices', devices)
            set_state('filtered_devices', devices)
            st.rerun()
    
    # 应用筛选
    filtered = devices
    
    # 搜索筛选
    if search_query:
        search_lower = search_query.lower()
        filtered = [d for d in filtered if 
                   search_lower in d['id'].lower() or 
                   search_lower in d['name'].lower()]
    
    # 状态筛选
    if status_filter != 'all':
        status_map = {
            'online': '在线',
            'offline': '离线',
            'alarm': '告警',
            'maintenance': '维护中'
        }
        filtered = [d for d in filtered if d['status'] == status_map.get(status_filter, '')]
    
    # 类型筛选
    if type_filter != 'all':
        type_map = {
            'high': '高压电缆',
            'low': '低压电缆',
            'terminal': '监测终端',
            'robot': '除冰机器人',
            'drone': '巡检无人机'
        }
        filtered = [d for d in filtered if d['type'] == type_map.get(type_filter, '')]
    
    set_state('filtered_devices', filtered)
    
    st.markdown("<div style='margin-bottom: 16px;'></div>", unsafe_allow_html=True)
    
    # ======================================
    # 设备列表表格
    # ======================================
    page = get_state('current_page_num', 1)
    page_size = get_state('page_size', 10)
    total_pages = get_total_pages(len(filtered), page_size)
    
    page_devices = get_paginated_data(filtered, page, page_size)
    
    # 表格头部
    st.markdown(f"""
    <div style="display: flex; align-items: center; justify-content: space-between; margin-bottom: 16px;">
        <div>
            <h3 style="margin: 0; font-size: 16px; font-weight: 600; color: white;">设备列表</h3>
            <p style="margin: 4px 0 0 0; font-size: 11px; color: {COLORS['gray_400']};">
                显示 {(page-1)*page_size + 1}-{min(page*page_size, len(filtered))} 条，共 {len(filtered)} 条
            </p>
        </div>
        <div style="display: flex; gap: 8px;">
            <button style="background: {COLORS['tertiary']}; color: {COLORS['gray_400']}; 
                           border: none; border-radius: 8px; padding: 8px 16px; font-size: 13px;
                           cursor: pointer;">
                ⬇️ 导出数据
            </button>
            <button style="background: {COLORS['primary']}; color: white; 
                           border: none; border-radius: 8px; padding: 8px 16px; font-size: 13px;
                           cursor: pointer;">
                ➕ 添加设备
            </button>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # 渲染表格
    table_html = f"""
    <div style="overflow-x: auto; border-radius: 8px; border: 1px solid {COLORS['gray_800']};">
        <table style="width: 100%; border-collapse: collapse; font-size: 13px;">
            <thead>
                <tr style="background: {COLORS['tertiary']};">
                    <th style="padding: 12px 16px; text-align: left; color: {COLORS['light']}; font-weight: 500;">设备编号</th>
                    <th style="padding: 12px 16px; text-align: left; color: {COLORS['light']}; font-weight: 500;">设备名称</th>
                    <th style="padding: 12px 16px; text-align: left; color: {COLORS['light']}; font-weight: 500;">类型</th>
                    <th style="padding: 12px 16px; text-align: left; color: {COLORS['light']}; font-weight: 500;">状态</th>
                    <th style="padding: 12px 16px; text-align: left; color: {COLORS['light']}; font-weight: 500;">电压(kV)</th>
                    <th style="padding: 12px 16px; text-align: left; color: {COLORS['light']}; font-weight: 500;">温度(℃)</th>
                    <th style="padding: 12px 16px; text-align: left; color: {COLORS['light']}; font-weight: 500;">覆冰(mm)</th>
                    <th style="padding: 12px 16px; text-align: left; color: {COLORS['light']}; font-weight: 500;">最后上报</th>
                    <th style="padding: 12px 16px; text-align: left; color: {COLORS['light']}; font-weight: 500;">操作</th>
                </tr>
            </thead>
            <tbody>
    """
    
    for device in page_devices:
        # 状态样式
        status_colors = {
            '在线': ('rgba(0, 180, 42, 0.2)', '#00B42A'),
            '离线': ('rgba(245, 63, 63, 0.2)', '#F53F3F'),
            '告警': ('rgba(255, 125, 0, 0.2)', '#FF7D00'),
            '维护中': ('rgba(100, 116, 139, 0.2)', '#64748B')
        }
        status_bg, status_color = status_colors.get(device['status'], ('rgba(100, 116, 139, 0.2)', '#64748B'))
        
        # 覆冰厚度样式
        ice_color = '#E2E8F0'
        ice_warning = ''
        if device['ice_thickness'] > 15:
            ice_color = '#F53F3F'
            ice_warning = '⚠️'
        elif device['ice_thickness'] > 10:
            ice_color = '#FF7D00'
            ice_warning = '⚠️'
        
        # 温度图标
        temp_icon = '❄️' if device['temperature'] < 0 else ''
        
        table_html += f"""
                <tr style="border-bottom: 1px solid {COLORS['gray_800']}; transition: background 0.2s;" 
                    onmouseover="this.style.background='rgba(30, 41, 59, 0.5)'" 
                    onmouseout="this.style.background='transparent'">
                    <td style="padding: 12px 16px; font-weight: 500; color: {COLORS['light']};">{device['id']}</td>
                    <td style="padding: 12px 16px;">
                        <div style="font-weight: 500; color: {COLORS['light']};">{device['name']}</div>
                        <div style="font-size: 11px; color: {COLORS['gray_400']};">{device['region']}</div>
                    </td>
                    <td style="padding: 12px 16px;">
                        <span style="background: {COLORS['gray_800']}; padding: 2px 8px; border-radius: 4px; font-size: 12px; color: {COLORS['light']};">{device['type']}</span>
                    </td>
                    <td style="padding: 12px 16px;">
                        <span style="background: {status_bg}; color: {status_color}; padding: 2px 8px; border-radius: 4px; font-size: 12px;">{device['status']}</span>
                    </td>
                    <td style="padding: 12px 16px; font-weight: 500; color: {COLORS['light']};">{device['voltage']}</td>
                    <td style="padding: 12px 16px; color: {COLORS['light']};">
                        <span>{device['temperature']}</span> {temp_icon}
                    </td>
                    <td style="padding: 12px 16px;">
                        <span style="font-weight: 500; color: {ice_color};">{device['ice_thickness']}</span> {ice_warning}
                    </td>
                    <td style="padding: 12px 16px; color: {COLORS['gray_400']}; font-size: 12px;">{device['last_report']}</td>
                    <td style="padding: 12px 16px;">
                        <div style="display: flex; gap: 8px;">
                            <button style="width: 28px; height: 28px; border-radius: 4px; background: rgba(22, 93, 255, 0.2); 
                                           border: none; cursor: pointer; display: flex; align-items: center; justify-content: center;">
                                <span style="color: {COLORS['primary']}; font-size: 12px;">👁️</span>
                            </button>
                            <button style="width: 28px; height: 28px; border-radius: 4px; background: {COLORS['gray_800']}; 
                                           border: none; cursor: pointer; display: flex; align-items: center; justify-content: center;">
                                <span style="color: {COLORS['gray_400']}; font-size: 12px;">✏️</span>
                            </button>
                        </div>
                    </td>
                </tr>
        """
    
    table_html += """
            </tbody>
        </table>
    </div>
    """
    
    st.markdown(table_html, unsafe_allow_html=True)
    
    # 分页控件
    st.markdown("<div style='margin-top: 16px;'></div>", unsafe_allow_html=True)
    
    page_cols = st.columns([1, 2])
    
    with page_cols[0]:
        st.markdown(f"""
        <span style="font-size: 13px; color: {COLORS['gray_400']};">
            第 {page} / {total_pages} 页
        </span>
        """, unsafe_allow_html=True)
    
    with page_cols[1]:
        pagination_cols = st.columns(7)
        
        with pagination_cols[0]:
            if st.button('◀', key='page_prev', disabled=page == 1):
                set_state('current_page_num', max(1, page - 1))
                st.rerun()
        
        # 页码按钮
        page_range = range(max(1, page - 2), min(total_pages + 1, page + 3))
        for i, p in enumerate(page_range):
            with pagination_cols[i + 1]:
                if st.button(str(p), key=f'page_{p}'):
                    set_state('current_page_num', p)
                    st.rerun()
        
        with pagination_cols[6]:
            if st.button('▶', key='page_next', disabled=page == total_pages):
                set_state('current_page_num', min(total_pages, page + 1))
                st.rerun()

# ======================================
# 页面入口
# ======================================
def show():
    """页面入口函数"""
    init_session_state()
    apply_custom_css()
    render_page()
