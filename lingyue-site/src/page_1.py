"""
凌越智缆 - 数据仪表盘页面 (Page 1)
展示核心数据概览、设备运行状态趋势等
"""

import streamlit as st
from pathlib import Path
import base64
import plotly.graph_objects as go
from datetime import datetime
from streamlit.components.v1 import html as html_component  # 用于渲染复杂HTML

from common import COLORS, apply_custom_css, get_image_base64
from session_state import init_session_state, refresh_data, set_state, get_state
from algorithm import MockDataGenerator, DeviceAnalytics

# ======================================
# 图片处理辅助函数
# ======================================
def get_image_html(image_path, fallback_text, height=120):
    """将图片转为base64 HTML或返回占位符"""
    try:
        full_path = Path(image_path)
        if not full_path.exists():
            alt_paths = [Path("assets") / image_path, Path("../assets") / image_path, 
                        Path("pages") / image_path, Path(image_path).name]
            for alt in alt_paths:
                if alt.exists():
                    full_path = alt
                    break
        
        if full_path.exists():
            with open(full_path, "rb") as f:
                data = f.read()
            b64 = base64.b64encode(data).decode()
            ext = full_path.suffix.replace('.', '')
            if ext == 'jpg':
                ext = 'jpeg'
            return f'<img src="data:image/{ext};base64,{b64}" style="width: 100%; height: {height}px; object-fit: cover; border-radius: 6px;" />'
        else:
            return f'<div style="height: {height}px; background: rgba(100,116,139,0.2); border-radius: 6px; display: flex; align-items: center; justify-content: center; color: #64748b; font-size: 12px;">{fallback_text}</div>'
    except Exception as e:
        return f'<div style="height: {height}px; background: rgba(100,116,139,0.2); border-radius: 6px; display: flex; align-items: center; justify-content: center; color: #64748b; font-size: 12px;">{fallback_text}</div>'

# ======================================
# 图表创建函数（保持不变）
# ======================================
def create_mini_chart(chart_type='online', color='#00B42A'):
    """创建迷你趋势图"""
    chart_data = MockDataGenerator.generate_chart_data(chart_type, 8)
    
    fig = go.Figure()
    
    r = int(color[1:3], 16)
    g = int(color[3:5], 16)
    b = int(color[5:7], 16)
    rgba_color = f'rgba({r}, {g}, {b}, 0.2)'
    
    if chart_type == 'data':
        fig.add_trace(go.Bar(
            x=chart_data['labels'],
            y=chart_data['data'],
            marker_color=color,
            opacity=0.7
        ))
    else:
        fig.add_trace(go.Scatter(
            x=chart_data['labels'],
            y=chart_data['data'],
            mode='lines',
            line=dict(color=color, width=2),
            fill='tozeroy',
            fillcolor=rgba_color
        ))
    
    fig.update_layout(
        margin=dict(l=0, r=0, t=0, b=0),
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        showlegend=False,
        xaxis=dict(showgrid=False, showticklabels=False, zeroline=False),
        yaxis=dict(showgrid=False, showticklabels=False, zeroline=False),
        height=60,
        hovermode=False
    )
    
    return fig

def create_trend_chart(time_range='day'):
    """创建设备运行状态趋势图"""
    data = MockDataGenerator.generate_trend_data(time_range)
    
    fig = go.Figure()
    
    fig.add_trace(go.Scatter(
        x=data['labels'], y=data['online'],
        mode='lines',
        name='在线设备',
        line=dict(color=COLORS['success'], width=3),
        hovertemplate='%{y:.0f}台<extra></extra>'
    ))
    
    fig.add_trace(go.Scatter(
        x=data['labels'], y=data['alarm'],
        mode='lines',
        name='告警设备',
        line=dict(color=COLORS['warning'], width=3),
        hovertemplate='%{y:.0f}台<extra></extra>'
    ))
    
    fig.add_trace(go.Scatter(
        x=data['labels'], y=data['offline'],
        mode='lines',
        name='离线设备',
        line=dict(color=COLORS['danger'], width=3),
        hovertemplate='%{y:.0f}台<extra></extra>'
    ))
    
    fig.update_layout(
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font=dict(color=COLORS['light']),
        legend=dict(
            orientation='h',
            yanchor='bottom',
            y=1.02,
            xanchor='right',
            x=1,
            font=dict(color=COLORS['light'])
        ),
        margin=dict(l=40, r=20, t=60, b=40),
        xaxis=dict(
            showgrid=True,
            gridcolor='rgba(255,255,255,0.1)',
            tickfont=dict(color=COLORS['gray_400'])
        ),
        yaxis=dict(
            showgrid=True,
            gridcolor='rgba(255,255,255,0.1)',
            tickfont=dict(color=COLORS['gray_400'])
        ),
        height=320,
        hoverlabel=dict(
            bgcolor=COLORS['secondary'],
            bordercolor=COLORS['gray_800'],
            font=dict(color=COLORS['light'])
        )
    )
    
    return fig

# ======================================
# 页面渲染函数
# ======================================
def render_page():
    """渲染数据仪表盘页面"""
    
    # 页面头部信息
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.markdown(f"""
        <div style="margin-bottom: 8px;">
            <div style="display: flex; align-items: center; gap: 12px; margin-bottom: 4px;">
                <h2 style="margin: 0; font-size: 22px; font-weight: bold; color: white;">电缆设备实时数据仪表盘</h2>
                <span style="font-size: 11px; background: rgba(0,180,42,0.2); color: {COLORS['success']}; 
                             padding: 4px 10px; border-radius: 9999px;">运行正常</span>
            </div>
            <p style="margin: 0; font-size: 13px; color: {COLORS['gray_400']}; display: flex; align-items: center;">
                <span style="margin-right: 8px;">🔄</span>
                最后更新时间: <span style="margin-left: 4px; font-weight: 500;">{get_state('last_update', datetime.now()).strftime('%Y-%m-%d %H:%M:%S')}</span>
            </p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        filter_cols = st.columns([1.2, 1.2, 1])
        
        with filter_cols[0]:
            device_filter = st.selectbox(
                '',
                ['all', 'high', 'low', 'ice', 'alarm'],
                format_func=lambda x: {
                    'all': '🔍 全部设备',
                    'high': '⚡ 高压电缆设备',
                    'low': '🔌 低压电缆设备',
                    'ice': '❄️ 覆冰监测设备',
                    'alarm': '⚠️ 故障设备'
                }[x],
                label_visibility='collapsed',
                key='device_filter_select'
            )
            set_state('device_filter', device_filter)
        
        with filter_cols[1]:
            time_filter = st.selectbox(
                '',
                ['today', 'yesterday', '7days', '30days'],
                format_func=lambda x: {
                    'today': '📅 今日数据',
                    'yesterday': '📅 昨日数据',
                    '7days': '📅 近7天',
                    '30days': '📅 近30天'
                }[x],
                label_visibility='collapsed',
                key='time_filter_select'
            )
            set_state('time_filter', time_filter)
        
        with filter_cols[2]:
            if st.button('🔄 刷新数据', use_container_width=True, key='refresh_btn'):
                with st.spinner('刷新中...'):
                    refresh_data()
                st.rerun()
    
    if get_state('show_refresh_success', False):
        st.success('✅ 数据已更新')
        set_state('show_refresh_success', False)
    
    st.markdown("<div style='margin-bottom: 24px;'></div>", unsafe_allow_html=True)
    
    # ======================================
    # 核心数据概览卡片
    # ======================================
    card_cols = st.columns(4)
    
    cards_data = [
        {
            'title': '在线设备',
            'value': get_state('online_devices', 86),
            'trend': '2.3%',
            'trend_up': True,
            'icon': '✅',
            'icon_color': COLORS['success'],
            'chart_type': 'online'
        },
        {
            'title': '离线设备',
            'value': get_state('offline_devices', 14),
            'trend': '1.1%',
            'trend_up': True,
            'icon': '❌',
            'icon_color': COLORS['danger'],
            'chart_type': 'offline'
        },
        {
            'title': '覆冰告警设备',
            'value': get_state('alarm_devices', 3),
            'trend': '5.7%',
            'trend_up': False,
            'icon': '❄️',
            'icon_color': COLORS['warning'],
            'chart_type': 'alarm'
        },
        {
            'title': '数据采集总量',
            'value': f"{get_state('data_total', 128.7)} GB",
            'trend': '18.9%',
            'trend_up': True,
            'icon': '🗄️',
            'icon_color': COLORS['primary'],
            'chart_type': 'data'
        }
    ]
    
    for i, card in enumerate(cards_data):
        with card_cols[i]:
            trend_icon = '📈' if card['trend_up'] else '📉'
            trend_color = COLORS['success'] if card['trend_up'] else COLORS['warning']
            
            st.markdown(f"""
            <div style="background: {COLORS['secondary']}; border-radius: 12px; padding: 16px;
                        border: 1px solid rgba(100, 116, 139, 0.2);">
                <div style="display: flex; align-items: flex-start; justify-content: space-between;">
                    <div>
                        <p style="margin: 0 0 4px 0; font-size: 13px; color: {COLORS['gray_400']}; display: flex; align-items: center; gap: 8px;">
                            <span>{card['title']}</span>
                            <span style="font-size: 8px; color: {card['icon_color']};">●</span>
                        </p>
                        <h3 style="margin: 0; font-size: 28px; font-weight: bold; color: white;">{card['value']}</h3>
                        <p style="margin: 8px 0 0 0; font-size: 12px; color: {trend_color}; display: flex; align-items: center;">
                            <span>{trend_icon}</span>
                            <span style="margin-left: 4px;">{card['trend']} 较昨日</span>
                        </p>
                    </div>
                    <div style="width: 48px; height: 48px; border-radius: 8px;
                                background: {card['icon_color']}33; display: flex; align-items: center; justify-content: center;">
                        <span style="font-size: 24px;">{card['icon']}</span>
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)
            
            fig = create_mini_chart(card['chart_type'], card['icon_color'])
            st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})
    
    st.markdown("<div style='margin-bottom: 24px;'></div>", unsafe_allow_html=True)
    
    # ======================================
    # 技术创新板块
    # ======================================
    tech_cols = st.columns([2, 1])

    with tech_cols[0]:
        time_buttons = ['hour', 'day', 'week', 'month']
        time_labels = ['小时', '天', '周', '月']
        
        button_cols = st.columns([4, 1, 1, 1, 1])
        with button_cols[0]:
            st.markdown("<h3 style='margin: 0; font-size: 16px; font-weight: 600; color: white;'>设备运行状态趋势</h3>", unsafe_allow_html=True)
        
        for i, (btn_val, btn_label) in enumerate(zip(time_buttons, time_labels)):
            with button_cols[i + 1]:
                is_active = st.session_state.get('trend_time_range', 'day') == btn_val
                btn_type = "primary" if is_active else "secondary"
                if st.button(btn_label, key=f'trend_btn_{btn_val}', use_container_width=True, type=btn_type):
                    st.session_state['trend_time_range'] = btn_val
                    st.rerun()
        
        trend_fig = create_trend_chart(st.session_state.get('trend_time_range', 'day'))
        st.plotly_chart(trend_fig, use_container_width=True, config={'displayModeBar': False})

    with tech_cols[1]:
        # 核心技术支撑卡片 - 使用 st.html (Streamlit 1.37+) 或 html_component
        tech_html_content = f"""
        <div style="background: linear-gradient(180deg, {COLORS['secondary']} 0%, {COLORS['tertiary']} 100%);
                    border-radius: 12px; padding: 16px; border: 1px solid rgba(100, 116, 139, 0.2); color: white; font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;">
            <div style="display: flex; align-items: center; justify-content: space-between; margin-bottom: 16px;">
                <h3 style="margin: 0; font-size: 16px; font-weight: 600;">核心技术支撑</h3>
                <div style="display: flex; gap: 8px;">
                    <div style="width: 32px; height: 32px; border-radius: 50%;
                                background: linear-gradient(135deg, {COLORS['primary']}, #2563EB);
                                display: flex; align-items: center; justify-content: center;">
                        <span style="color: white; font-size: 14px;">🤖</span>
                    </div>
                    <div style="width: 32px; height: 32px; border-radius: 50%;
                                background: linear-gradient(135deg, {COLORS['electric']}, #60A5FA);
                                display: flex; align-items: center; justify-content: center;">
                        <span style="color: white; font-size: 14px;">❄️</span>
                    </div>
                </div>
            </div>
            
            <div style="border-bottom: 1px solid {COLORS['gray_800']}; padding-bottom: 16px; margin-bottom: 16px;">
                <div style="display: flex; align-items: center; gap: 12px; margin-bottom: 12px;">
                    <div style="width: 40px; height: 40px; border-radius: 8px;
                                background: rgba(0, 153, 255, 0.1); display: flex; align-items: center; justify-content: center;">
                        <span style="font-size: 20px;">📍</span>
                    </div>
                    <div>
                        <h4 style="margin: 0; font-size: 14px; font-weight: 500;">GPRS通讯定位数据</h4>
                        <p style="margin: 0; font-size: 11px; color: {COLORS['gray_400']};">实时追踪 · 精准定位</p>
                    </div>
                </div>
                <p style="margin: 0 0 12px 0; font-size: 13px; color: {COLORS['gray_400']}; line-height: 1.5;">
                    突破GPS信号限制，在高压线路下方等弱信号区域稳定回传设备位置
                </p>
                {get_image_html("../assets/images/t_3.png", "📍 GPRS定位示意图", 100)}
                <div style="margin-top: 8px; display: flex; align-items: center; gap: 6px;">
                    <span style="font-size: 11px; color: {COLORS['electric']};">●</span>
                    <span style="font-size: 11px; color: {COLORS['gray_400']};">实时定位精度 ±2m</span>
                </div>
            </div>
            
            <div>
                <div style="display: flex; align-items: center; gap: 12px; margin-bottom: 12px;">
                    <div style="width: 40px; height: 40px; border-radius: 8px;
                                background: rgba(139, 92, 246, 0.1); display: flex; align-items: center; justify-content: center;">
                        <span style="font-size: 20px;">🧊</span>
                    </div>
                    <div>
                        <h4 style="margin: 0; font-size: 14px; font-weight: 500;">数字孪生电缆环境仿真</h4>
                        <p style="margin: 0; font-size: 11px; color: {COLORS['gray_400']};">三维仿真 · 风险预判</p>
                    </div>
                </div>
                <p style="margin: 0 0 12px 0; font-size: 13px; color: {COLORS['gray_400']}; line-height: 1.5;">
                    结合定位数据构建虚拟仿真界面，实时还原覆冰状态
                </p>
                {get_image_html("../assets/images/t_4.png", "🧊 数字孪生示意图", 100)}
                <div style="margin-top: 8px; display: flex; align-items: center; gap: 6px;">
                    <span style="font-size: 11px; color: #a78bfa;">●</span>
                    <span style="font-size: 11px; color: {COLORS['gray_400']};">模型精度 99.8%</span>
                </div>
            </div>
        </div>
        """
        
        # 使用 html_component 渲染复杂HTML，避免Markdown解析问题
        html_component(tech_html_content, height=600, scrolling=False)

    st.markdown("<div style='margin-bottom: 24px;'></div>", unsafe_allow_html=True)
    
    # ======================================
    # 覆冰监测专题板块（修复版）
    # ======================================
    ice_cols = st.columns(2)

    with ice_cols[0]:
        ice_thickness = st.session_state.get('ice_thickness', 12.7)
        env_temp = st.session_state.get('env_temp', -5.3)
        
        ice_percent = min((ice_thickness / 20) * 100, 100)
        temp_percent = min((abs(env_temp) / 20) * 100, 100)
        
        ice_monitor_html = f"""
        <div style="background: {COLORS['secondary']}; border-radius: 12px; padding: 16px; border: 1px solid rgba(100, 116, 139, 0.2); color: white; font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;">
            <div style="display: flex; align-items: center; justify-content: space-between; margin-bottom: 16px;">
                <div>
                    <h3 style="margin: 0; font-size: 16px; font-weight: 600;">电缆覆冰参数实时监测</h3>
                    <p style="margin: 4px 0 0 0; font-size: 11px; color: {COLORS['gray_400']};">实时监控 · 智能预警</p>
                </div>
                <span style="background: rgba(224, 247, 255, 0.1); color: {COLORS['electric']}; border-radius: 8px; padding: 8px 16px; font-size: 13px; display: flex; align-items: center; gap: 8px; cursor: pointer;">
                    📊 查看历史曲线
                </span>
            </div>
            
            <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 16px; margin-bottom: 24px;">
                <div style="background: linear-gradient(135deg, {COLORS['tertiary']}, #111827); border-radius: 8px; padding: 16px; border: 1px solid rgba(100, 116, 139, 0.3);">
                    <div style="display: flex; justify-content: space-between; align-items: flex-start; margin-bottom: 8px;">
                        <p style="margin: 0; font-size: 11px; color: {COLORS['gray_400']};">覆冰厚度 (mm)</p>
                        <span style="width: 8px; height: 8px; border-radius: 50%; background: {COLORS['warning']};"></span>
                    </div>
                    <p style="margin: 0; font-size: 24px; font-weight: bold;">{ice_thickness}</p>
                    <div style="background: {COLORS['gray_800']}; border-radius: 9999px; height: 8px; overflow: hidden; margin-top: 12px;">
                        <div style="background: linear-gradient(90deg, {COLORS['warning']}, #FB923C); height: 100%; border-radius: 9999px; width: {ice_percent}%;"></div>
                    </div>
                    <div style="display: flex; justify-content: space-between; font-size: 11px; color: {COLORS['gray_400']}; margin-top: 8px;">
                        <span>0mm</span>
                        <span style="color: {COLORS['warning']};">告警阈值：20mm</span>
                    </div>
                </div>
                <div style="background: linear-gradient(135deg, {COLORS['tertiary']}, #111827); border-radius: 8px; padding: 16px; border: 1px solid rgba(100, 116, 139, 0.3);">
                    <div style="display: flex; justify-content: space-between; align-items: flex-start; margin-bottom: 8px;">
                        <p style="margin: 0; font-size: 11px; color: {COLORS['gray_400']};">环境温度 (℃)</p>
                        <span style="width: 8px; height: 8px; border-radius: 50%; background: {COLORS['electric']};"></span>
                    </div>
                    <p style="margin: 0; font-size: 24px; font-weight: bold;">{env_temp}</p>
                    <div style="background: {COLORS['gray_800']}; border-radius: 9999px; height: 8px; overflow: hidden; margin-top: 12px;">
                        <div style="background: linear-gradient(90deg, {COLORS['electric']}, #60A5FA); height: 100%; border-radius: 9999px; width: {temp_percent}%;"></div>
                    </div>
                    <div style="display: flex; justify-content: space-between; font-size: 11px; color: {COLORS['gray_400']}; margin-top: 8px;">
                        <span>-20℃</span>
                        <span style="color: {COLORS['electric']};">冰点阈值：0℃</span>
                    </div>
                </div>
            </div>
            
            <div>
                <h4 style="margin: 0 0 12px 0; font-size: 14px; font-weight: 500;">AI识别技术对比</h4>
                <div style="display: flex; gap: 12px;">
                    <div style="flex: 1;">
                        <div style="background: {COLORS['tertiary']}; color: {COLORS['gray_400']}; border-radius: 8px; padding: 8px; margin-bottom: 8px; text-align: center; font-size: 13px;">
                            传统参数提取
                        </div>
                        {get_image_html("../assets/images/t_1.png", "传统方法示例", 120)}
                        <p style="margin: 4px 0 0 0; font-size: 11px; color: {COLORS['gray_400']}; text-align: center;">准确率 85%</p>
                    </div>
                    <div style="flex: 1;">
                        <div style="background: rgba(22, 93, 255, 0.1); color: {COLORS['primary']}; font-weight: 500; border-radius: 8px; padding: 8px; margin-bottom: 8px; text-align: center; font-size: 13px;">
                            凌越AI语义分割
                        </div>
                        {get_image_html("../assets/images/26.png", "AI识别示例", 120)}
                        <p style="margin: 4px 0 0 0; font-size: 11px; color: {COLORS['primary']}; text-align: center;">准确率 98.2%</p>
                    </div>
                </div>
            </div>
        </div>
        """
        
        html_component(ice_monitor_html, height=450, scrolling=False)

    with ice_cols[1]:
        ops_html = f"""
        <div style="background: {COLORS['secondary']}; border-radius: 12px; padding: 16px; border: 1px solid rgba(100, 116, 139, 0.2); color: white; font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;">
            <div style="display: flex; align-items: center; justify-content: space-between; margin-bottom: 16px;">
                <div>
                    <h3 style="margin: 0; font-size: 16px; font-weight: 600;">一线运维现场</h3>
                    <p style="margin: 4px 0 0 0; font-size: 11px; color: {COLORS['gray_400']};">实时作业 · 现场直击</p>
                </div>
                <span style="background: rgba(22, 93, 255, 0.1); color: {COLORS['primary']}; border-radius: 8px; padding: 8px 16px; font-size: 13px; display: flex; align-items: center; gap: 8px; cursor: pointer;">
                    📷 查看更多
                </span>
            </div>
            
            <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 12px; margin-bottom: 16px;">
                <div>
                    {get_image_html("../assets/images/t_2.jpg", "人工除冰现场", 150)}
                    <p style="margin: 6px 0 0 0; font-size: 11px; color: {COLORS['gray_400']}; text-align: center;">人工除冰作业 · 鄂西地区</p>
                </div>
                <div>
                    {get_image_html("../assets/images/64.png", "机器人作业现场", 150)}
                    <p style="margin: 6px 0 0 0; font-size: 11px; color: {COLORS['gray_400']}; text-align: center;">机器人除冰作业 · 实时</p>
                </div>
            </div>
            
            <div style="background: linear-gradient(90deg, rgba(255, 125, 0, 0.1), rgba(255, 125, 0, 0.05)); border: 1px solid rgba(255, 125, 0, 0.2); border-radius: 8px; padding: 16px;">
                <div style="display: flex; align-items: center; gap: 12px; margin-bottom: 12px;">
                    <div style="width: 40px; height: 40px; border-radius: 50%; background: rgba(255, 125, 0, 0.2); display: flex; align-items: center; justify-content: center; font-size: 20px;">⚠️</div>
                    <div>
                        <p style="margin: 0; font-size: 14px; font-weight: 500;">紧急运维提示</p>
                        <p style="margin: 0; font-size: 11px; color: {COLORS['warning']};">需立即处理</p>
                    </div>
                </div>
                <p style="margin: 0 0 12px 0; font-size: 13px; color: {COLORS['gray_400']}; line-height: 1.5;">
                    今日鄂西地区3条高压线路覆冰厚度超过10mm，已派发除冰作业工单，建议优先调度凌越®高压电缆维护机器人前往作业
                </p>
                <div style="display: flex; align-items: center; justify-content: space-between;">
                    <span style="font-size: 11px; color: {COLORS['gray_400']};">工单编号: #20251231003</span>
                    <button style="background: {COLORS['warning']}; color: white; border: none; border-radius: 4px; padding: 6px 12px; font-size: 11px; cursor: pointer;">
                        处理工单
                    </button>
                </div>
            </div>
        </div>
        """
        
        html_component(ops_html, height=420, scrolling=False)
    

# ======================================
# 页面入口
# ======================================
def show():
    """页面入口函数"""
    init_session_state()
    apply_custom_css()
    render_page()
