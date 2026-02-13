"""
凌越智缆 - GPRS定位页面 (Page 3)
展示设备GPS定位、信号强度、实时追踪等功能
"""

import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime
import random

from common import COLORS, apply_custom_css
from session_state import init_session_state, set_state, get_state
from algorithm import MockDataGenerator

# ======================================
# 图表创建函数
# ======================================
def create_map_scatter(gps_data):
    """创建GPS定位散点图"""
    # 提取坐标数据
    lats = [d['latitude'] for d in gps_data]
    lons = [d['longitude'] for d in gps_data]
    texts = [f"{d['device_id']}<br>{d['region']}<br>信号: {d['signal_strength']}%" for d in gps_data]
    colors = [COLORS['success'] if d['status'] == '正常' else COLORS['warning'] if d['status'] == '弱信号' else COLORS['danger'] for d in gps_data]
    
    fig = go.Figure()
    
    fig.add_trace(go.Scattermapbox(
        lat=lats,
        lon=lons,
        mode='markers',
        marker=dict(
            size=12,
            color=colors,
            opacity=0.8
        ),
        text=texts,
        hovertemplate='%{text}<extra></extra>'
    ))
    
    fig.update_layout(
        mapbox=dict(
            style='carto-darkmatter',
            center=dict(lat=30.5, lon=110.5),
            zoom=5
        ),
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        margin=dict(l=0, r=0, t=0, b=0),
        height=400,
        showlegend=False
    )
    
    return fig

def create_signal_chart():
    """创建信号强度趋势图"""
    hours = [f'{i}:00' for i in range(24)]
    signal = [80 + random.randint(-15, 15) for _ in range(24)]
    
    fig = go.Figure()
    
    fig.add_trace(go.Scatter(
        x=hours,
        y=signal,
        mode='lines+markers',
        name='平均信号强度',
        line=dict(color=COLORS['success'], width=2),
        marker=dict(size=4),
        fill='tozeroy',
        fillcolor='rgba(0, 180, 42, 0.1)'
    ))
    
    # 添加阈值线
    fig.add_hline(y=50, line_dash="dash", line_color=COLORS['warning'], annotation_text="弱信号阈值")
    fig.add_hline(y=30, line_dash="dash", line_color=COLORS['danger'], annotation_text="离线阈值")
    
    fig.update_layout(
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font=dict(color=COLORS['light']),
        showlegend=False,
        xaxis=dict(showgrid=True, gridcolor='rgba(255,255,255,0.1)', tickfont=dict(color=COLORS['gray_400'])),
        yaxis=dict(showgrid=True, gridcolor='rgba(255,255,255,0.1)', tickfont=dict(color=COLORS['gray_400']),
                   title='信号强度 (%)', titlefont=dict(color=COLORS['gray_400'])),
        margin=dict(l=60, r=20, t=20, b=40),
        height=250
    )
    
    return fig

def create_region_distribution(gps_data):
    """创建地区分布饼图"""
    region_counts = {}
    for d in gps_data:
        region = d['region']
        region_counts[region] = region_counts.get(region, 0) + 1
    
    fig = go.Figure(data=[go.Pie(
        labels=list(region_counts.keys()),
        values=list(region_counts.values()),
        hole=0.4,
        marker=dict(colors=[COLORS['primary'], COLORS['success'], COLORS['warning'], COLORS['electric'], COLORS['gray_500']]),
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

# ======================================
# 页面渲染函数
# ======================================
def render_page():
    """渲染GPRS定位页面"""
    
    # 初始化GPS数据
    if not get_state('gps_data'):
        gps_data = MockDataGenerator.generate_gps_data(50)
        set_state('gps_data', gps_data)
    
    gps_data = get_state('gps_data', [])
    
    # 页面标题
    st.markdown(f"""
    <div style="margin-bottom: 24px;">
        <h2 style="margin: 0; font-size: 22px; font-weight: bold; color: white;">GPRS定位</h2>
        <p style="margin: 4px 0 0 0; font-size: 13px; color: {COLORS['gray_400']};">
            实时追踪设备位置，监控信号强度，突破GPS信号限制
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # ======================================
    # 定位统计卡片
    # ======================================
    stat_cols = st.columns(4)
    
    normal_count = len([d for d in gps_data if d['status'] == '正常'])
    weak_count = len([d for d in gps_data if d['status'] == '弱信号'])
    offline_count = len([d for d in gps_data if d['status'] == '离线'])
    avg_signal = sum([d['signal_strength'] for d in gps_data]) / len(gps_data) if gps_data else 0
    
    stat_data = [
        ('正常设备', normal_count, COLORS['success'], '📡'),
        ('弱信号', weak_count, COLORS['warning'], '📶'),
        ('离线设备', offline_count, COLORS['danger'], '🚫'),
        ('平均信号', f'{avg_signal:.1f}%', COLORS['electric'], '📊')
    ]
    
    for i, (label, value, color, icon) in enumerate(stat_data):
        with stat_cols[i]:
            st.markdown(f"""
            <div style="background: {COLORS['secondary']}; border-radius: 12px; padding: 20px;
                        border: 1px solid rgba(100, 116, 139, 0.2); text-align: center;">
                <div style="font-size: 28px; margin-bottom: 8px;">{icon}</div>
                <div style="font-size: 28px; font-weight: bold; color: {color};">{value}</div>
                <div style="font-size: 13px; color: {COLORS['gray_400']}; margin-top: 4px;">{label}</div>
            </div>
            """, unsafe_allow_html=True)
    
    st.markdown("<div style='margin-bottom: 24px;'></div>", unsafe_allow_html=True)
    
    # ======================================
    # 地图和筛选
    # ======================================
    map_filter_cols = st.columns([3, 1, 1, 1])
    
    with map_filter_cols[1]:
        region_filter = st.selectbox(
            '地区筛选',
            ['all', '鄂西', '川东', '云贵', '西北', '华北'],
            format_func=lambda x: {
                'all': '全部地区',
                '鄂西': '鄂西地区',
                '川东': '川东地区',
                '云贵': '云贵地区',
                '西北': '西北地区',
                '华北': '华北地区'
            }[x],
            key='gps_region_filter'
        )
    
    with map_filter_cols[2]:
        status_filter = st.selectbox(
            '状态筛选',
            ['all', 'normal', 'weak', 'offline'],
            format_func=lambda x: {
                'all': '全部状态',
                'normal': '正常',
                'weak': '弱信号',
                'offline': '离线'
            }[x],
            key='gps_status_filter'
        )
    
    with map_filter_cols[3]:
        if st.button('🔄 刷新', use_container_width=True):
            gps_data = MockDataGenerator.generate_gps_data(50)
            set_state('gps_data', gps_data)
            st.rerun()
    
    st.markdown("<div style='margin-bottom: 16px;'></div>", unsafe_allow_html=True)
    
    # ======================================
    # 地图展示
    # ======================================
    map_cols = st.columns([2, 1])
    
    with map_cols[0]:
        st.markdown(f"<h4 style='color: white; font-size: 14px; margin-bottom: 12px;'>设备位置分布</h4>", unsafe_allow_html=True)
        
        # 筛选GPS数据
        filtered_gps = gps_data
        if region_filter != 'all':
            region_map = {'鄂西': '鄂西地区', '川东': '川东地区', '云贵': '云贵地区', '西北': '西北地区', '华北': '华北地区'}
            filtered_gps = [d for d in filtered_gps if d['region'] == region_map.get(region_filter, '')]
        if status_filter != 'all':
            status_map = {'normal': '正常', 'weak': '弱信号', 'offline': '离线'}
            filtered_gps = [d for d in filtered_gps if d['status'] == status_map.get(status_filter, '')]
        
        if filtered_gps:
            fig = create_map_scatter(filtered_gps)
            st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})
        else:
            st.info('暂无数据')
    
    with map_cols[1]:
        st.markdown(f"<h4 style='color: white; font-size: 14px; margin-bottom: 12px;'>地区分布</h4>", unsafe_allow_html=True)
        fig = create_region_distribution(gps_data)
        st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})
        
        st.markdown(f"<h4 style='color: white; font-size: 14px; margin: 16px 0 12px 0;'>信号强度趋势</h4>", unsafe_allow_html=True)
        fig = create_signal_chart()
        st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})
    
    st.markdown("<div style='margin-bottom: 24px;'></div>", unsafe_allow_html=True)
    
    # ======================================
    # GPS设备列表
    # ======================================
    st.markdown(f"<h3 style='color: white; font-size: 16px; margin-bottom: 16px;'>GPS设备列表</h3>", unsafe_allow_html=True)
    
    # 表格头部
    table_html = f"""
    <div style="overflow-x: auto; border-radius: 8px; border: 1px solid {COLORS['gray_800']};">
        <table style="width: 100%; border-collapse: collapse; font-size: 13px;">
            <thead>
                <tr style="background: {COLORS['tertiary']};">
                    <th style="padding: 12px 16px; text-align: left; color: {COLORS['light']}; font-weight: 500;">GPS编号</th>
                    <th style="padding: 12px 16px; text-align: left; color: {COLORS['light']}; font-weight: 500;">设备编号</th>
                    <th style="padding: 12px 16px; text-align: left; color: {COLORS['light']}; font-weight: 500;">地区</th>
                    <th style="padding: 12px 16px; text-align: left; color: {COLORS['light']}; font-weight: 500;">经度</th>
                    <th style="padding: 12px 16px; text-align: left; color: {COLORS['light']}; font-weight: 500;">纬度</th>
                    <th style="padding: 12px 16px; text-align: left; color: {COLORS['light']}; font-weight: 500;">海拔(m)</th>
                    <th style="padding: 12px 16px; text-align: left; color: {COLORS['light']}; font-weight: 500;">信号强度</th>
                    <th style="padding: 12px 16px; text-align: left; color: {COLORS['light']}; font-weight: 500;">状态</th>
                    <th style="padding: 12px 16px; text-align: left; color: {COLORS['light']}; font-weight: 500;">更新时间</th>
                </tr>
            </thead>
            <tbody>
    """
    
    for gps in filtered_gps[:10]:
        # 状态样式
        status_colors = {
            '正常': ('rgba(0, 180, 42, 0.2)', '#00B42A'),
            '弱信号': ('rgba(255, 125, 0, 0.2)', '#FF7D00'),
            '离线': ('rgba(245, 63, 63, 0.2)', '#F53F3F')
        }
        status_bg, status_color = status_colors.get(gps['status'], ('rgba(100, 116, 139, 0.2)', '#64748B'))
        
        # 信号强度颜色
        signal_color = COLORS['success'] if gps['signal_strength'] >= 70 else COLORS['warning'] if gps['signal_strength'] >= 40 else COLORS['danger']
        
        table_html += f"""
                <tr style="border-bottom: 1px solid {COLORS['gray_800']}; transition: background 0.2s;" 
                    onmouseover="this.style.background='rgba(30, 41, 59, 0.5)'" 
                    onmouseout="this.style.background='transparent'">
                    <td style="padding: 12px 16px; font-weight: 500; color: {COLORS['light']};">{gps['id']}</td>
                    <td style="padding: 12px 16px; color: {COLORS['light']};">{gps['device_id']}</td>
                    <td style="padding: 12px 16px; color: {COLORS['light']};">{gps['region']}</td>
                    <td style="padding: 12px 16px; color: {COLORS['gray_400']};">{gps['longitude']}</td>
                    <td style="padding: 12px 16px; color: {COLORS['gray_400']};">{gps['latitude']}</td>
                    <td style="padding: 12px 16px; color: {COLORS['light']};">{gps['altitude']}</td>
                    <td style="padding: 12px 16px;">
                        <div style="display: flex; align-items: center; gap: 8px;">
                            <div style="width: 60px; height: 6px; background: {COLORS['gray_800']}; border-radius: 3px; overflow: hidden;">
                                <div style="width: {gps['signal_strength']}%; height: 100%; background: {signal_color};"></div>
                            </div>
                            <span style="font-size: 12px; color: {signal_color};">{gps['signal_strength']}%</span>
                        </div>
                    </td>
                    <td style="padding: 12px 16px;">
                        <span style="background: {status_bg}; color: {status_color}; padding: 2px 8px; border-radius: 4px; font-size: 12px;">{gps['status']}</span>
                    </td>
                    <td style="padding: 12px 16px; color: {COLORS['gray_400']}; font-size: 12px;">{gps['last_update']}</td>
                </tr>
        """
    
    table_html += """
            </tbody>
        </table>
    </div>
    """
    
    st.markdown(table_html, unsafe_allow_html=True)

# ======================================
# 页面入口
# ======================================
def show():
    """页面入口函数"""
    init_session_state()
    apply_custom_css()
    render_page()
