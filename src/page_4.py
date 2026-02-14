"""
凌越智缆 - GPRS定位页面 (Page 4)
展示设备GPS定位、信号强度、实时追踪等功能
"""

import streamlit as st
import pandas as pd
import streamlit.components.v1 as components
import html
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
    """创建设备位置分布地图（修复版）"""
    
    if not gps_data:
        return go.Figure()
    
    # 转换为DataFrame便于处理
    df = pd.DataFrame(gps_data)
    
    # 根据状态设置颜色
    color_map = {
        '正常': '#00B42A',
        '弱信号': '#FF7D00',
        '离线': '#F53F3F'
    }
    
    # 为每个状态创建独立的trace（便于图例显示）
    fig = go.Figure()
    
    for status in ['正常', '弱信号', '离线']:
        mask = df['status'] == status
        if mask.any():
            subset = df[mask]
            fig.add_trace(go.Scattergeo(
                lon=subset['longitude'],
                lat=subset['latitude'],
                mode='markers',
                name=status,
                marker=dict(
                    size=12,
                    color=color_map.get(status, '#64748B'),
                    opacity=0.8,
                    line=dict(width=1, color='white')
                ),
                text=subset.apply(lambda x: f"设备: {x['device_id']}<br>状态: {x['status']}<br>信号: {x['signal_strength']}%", axis=1),
                hoverinfo='text'
            ))
    
    # 配置地理投影（聚焦中国区域）
    fig.update_layout(
        geo=dict(
            scope='asia',  # 亚洲范围
            projection=dict(type='mercator'),  # 墨卡托投影
            center=dict(lat=35, lon=105),  # 中国中心
            fitbounds="locations",  # 自动适应数据点范围
            showland=True,
            landcolor="rgb(30, 41, 59)",  # 深色地图背景
            showocean=True,
            oceancolor="rgb(15, 23, 42)",  # 海洋颜色
            showcountries=True,
            countrycolor="rgb(100, 116, 139)",
            countrywidth=0.5,
            showsubunits=True,
            subunitcolor="rgb(100, 116, 139)",
            subunitwidth=0.5,
            bgcolor='rgba(0,0,0,0)'
        ),
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        margin=dict(l=0, r=0, t=0, b=0),
        showlegend=True,
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1,
            font=dict(color='white')
        ),
        height=400
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

    # 构建表格行
    table_rows = []
    for gps in filtered_gps[:10]:
        # 转义所有动态内容
        gps_id = html.escape(str(gps.get('id', '')))
        device_id = html.escape(str(gps.get('device_id', '')))
        region = html.escape(str(gps.get('region', '')))
        longitude = html.escape(str(gps.get('longitude', '')))
        latitude = html.escape(str(gps.get('latitude', '')))
        altitude = html.escape(str(gps.get('altitude', '')))
        signal = gps.get('signal_strength', 0)
        status = html.escape(str(gps.get('status', '')))
        last_update = html.escape(str(gps.get('last_update', '')))
        
        # 状态样式
        status_colors = {
            '正常': ('rgba(0, 180, 42, 0.2)', '#00B42A'),
            '弱信号': ('rgba(255, 125, 0, 0.2)', '#FF7D00'),
            '离线': ('rgba(245, 63, 63, 0.2)', '#F53F3F')
        }
        status_bg, status_color = status_colors.get(gps['status'], ('rgba(100, 116, 139, 0.2)', '#64748B'))
        
        # 信号强度颜色
        signal_color = COLORS['success'] if signal >= 70 else COLORS['warning'] if signal >= 40 else COLORS['danger']
        
        # 构建行（使用format避免引号冲突）
        row = """
        <tr style="border-bottom: 1px solid {border_color};">
            <td style="padding: 12px 16px; font-weight: 500; color: {light};">{gps_id}</td>
            <td style="padding: 12px 16px; color: {light};">{device_id}</td>
            <td style="padding: 12px 16px; color: {light};">{region}</td>
            <td style="padding: 12px 16px; color: {gray_400};">{longitude}</td>
            <td style="padding: 12px 16px; color: {gray_400};">{latitude}</td>
            <td style="padding: 12px 16px; color: {light};">{altitude}</td>
            <td style="padding: 12px 16px;">
                <div style="display: flex; align-items: center; gap: 8px;">
                    <div style="width: 60px; height: 6px; background: {gray_800}; border-radius: 3px; overflow: hidden;">
                        <div style="width: {signal}%; height: 100%; background: {signal_color};"></div>
                    </div>
                    <span style="font-size: 12px; color: {signal_color};">{signal}%</span>
                </div>
            </td>
            <td style="padding: 12px 16px;">
                <span style="background: {status_bg}; color: {status_color}; padding: 2px 8px; border-radius: 4px; font-size: 12px; border: 1px solid {status_color};">{status}</span>
            </td>
            <td style="padding: 12px 16px; color: {gray_400}; font-size: 12px;">{last_update}</td>
        </tr>
        """.format(
            border_color=COLORS['gray_800'],
            light=COLORS['light'],
            gray_400=COLORS['gray_400'],
            gray_800=COLORS['gray_800'],
            gps_id=gps_id,
            device_id=device_id,
            region=region,
            longitude=longitude,
            latitude=latitude,
            altitude=altitude,
            signal=signal,
            signal_color=signal_color,
            status_bg=status_bg,
            status_color=status_color,
            status=status,
            last_update=last_update
        )
        table_rows.append(row)

    # 完整表格HTML
    table_html = """
    <div style="overflow-x: auto; border-radius: 8px; border: 1px solid {border_color}; background: {secondary};">
        <table style="width: 100%; border-collapse: collapse; font-size: 13px; font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;">
            <thead>
                <tr style="background: {tertiary}; border-bottom: 2px solid {border_color};">
                    <th style="padding: 12px 16px; text-align: left; color: {light}; font-weight: 600; font-size: 12px;">GPS编号</th>
                    <th style="padding: 12px 16px; text-align: left; color: {light}; font-weight: 600; font-size: 12px;">设备编号</th>
                    <th style="padding: 12px 16px; text-align: left; color: {light}; font-weight: 600; font-size: 12px;">地区</th>
                    <th style="padding: 12px 16px; text-align: left; color: {light}; font-weight: 600; font-size: 12px;">经度</th>
                    <th style="padding: 12px 16px; text-align: left; color: {light}; font-weight: 600; font-size: 12px;">纬度</th>
                    <th style="padding: 12px 16px; text-align: left; color: {light}; font-weight: 600; font-size: 12px;">海拔(m)</th>
                    <th style="padding: 12px 16px; text-align: left; color: {light}; font-weight: 600; font-size: 12px;">信号强度</th>
                    <th style="padding: 12px 16px; text-align: left; color: {light}; font-weight: 600; font-size: 12px;">状态</th>
                    <th style="padding: 12px 16px; text-align: left; color: {light}; font-weight: 600; font-size: 12px;">更新时间</th>
                </tr>
            </thead>
            <tbody>
                {rows}
            </tbody>
        </table>
    </div>
    """.format(
        border_color=COLORS['gray_800'],
        secondary=COLORS['secondary'],
        tertiary=COLORS['tertiary'],
        light=COLORS['light'],
        rows='\n'.join(table_rows)
    )

    # 使用 components.html 渲染（最稳定）
    components.html(table_html, height=500, scrolling=True)

# ======================================
# 页面入口
# ======================================
def show():
    """页面入口函数"""
    init_session_state()
    apply_custom_css()
    render_page()
