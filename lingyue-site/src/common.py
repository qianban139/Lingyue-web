"""
凌越智缆 - 公用函数与类模块
包含: 配色配置、CSS样式、通用组件、工具函数
"""

import streamlit as st
from datetime import datetime
import base64
from pathlib import Path

# ======================================
# 配色体系配置
# ======================================
COLORS = {
    'primary': '#165DFF',
    'secondary': '#0F172A',
    'tertiary': '#1E293B',
    'success': '#00B42A',
    'warning': '#FF7D00',
    'danger': '#F53F3F',
    'dark': '#0A0F1F',
    'light': '#E2E8F0',
    'electric': '#0099FF',
    'ice': '#E0F7FF',
    'gray_400': '#94A3B8',
    'gray_500': '#64748B',
    'gray_700': '#334155',
    'gray_800': '#1E293B',
}

# ======================================
# 自定义CSS样式
# ======================================
def get_custom_css():
    """获取自定义CSS样式"""
    return f"""
    <style>
    /* 全局样式 */
    .stApp {{
        background-color: {COLORS['dark']};
        color: {COLORS['light']};
        font-family: 'Inter', system-ui, sans-serif;
    }}
    
    # /* 隐藏Streamlit默认元素 */
    # #MainMenu {{visibility: hidden;}}
    # header {{visibility: hidden;}}
    # .stDeployButton {{display: none;}}
    # footer {{visibility: hidden;}}
    
    /* 自定义滚动条 */
    ::-webkit-scrollbar {{
        width: 6px;
        height: 6px;
    }}
    ::-webkit-scrollbar-track {{
        background: rgba(30, 41, 59, 0.3);
        border-radius: 10px;
    }}
    ::-webkit-scrollbar-thumb {{
        background: rgba(22, 93, 255, 0.5);
        border-radius: 10px;
    }}
    ::-webkit-scrollbar-thumb:hover {{
        background: rgba(22, 93, 255, 0.7);
    }}
    
    /* 玻璃效果 */
    .glass-effect {{
        background: rgba(15, 23, 42, 0.85);
        backdrop-filter: blur(10px);
        -webkit-backdrop-filter: blur(10px);
    }}
    
    /* 卡片阴影 */
    .card-shadow {{
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.3);
    }}
    
    /* 渐变文字 */
    .gradient-text {{
        background: linear-gradient(90deg, {COLORS['primary']}, #60A5FA);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
    }}
    
    /* Banner渐变 */
    .banner-gradient {{
        background: linear-gradient(90deg, rgba(10,15,31,0.9) 0%, rgba(22,93,255,0.7) 100%);
    }}
    
    /* 技术卡片渐变 */
    .tech-card-gradient {{
        background: linear-gradient(180deg, rgba(15,23,42,1) 0%, rgba(30,41,59,1) 100%);
    }}
    
    /* 导航栏激活状态 */
    .nav-active {{
        background: rgba(22, 93, 255, 0.1);
        color: {COLORS['primary']};
        border-left: 4px solid {COLORS['primary']};
    }}
    
    /* 卡片悬停效果 */
    .hover-card {{
        transition: all 0.3s ease;
    }}
    .hover-card:hover {{
        transform: translateY(-4px);
    }}
    
    /* 图片悬停效果 */
    .hover-image {{
        transition: transform 0.5s ease;
    }}
    .hover-image:hover {{
        transform: scale(1.05);
    }}
    
    /* 按钮样式 */
    .custom-btn {{
        background-color: {COLORS['primary']};
        color: white;
        border: none;
        border-radius: 8px;
        padding: 8px 16px;
        font-size: 14px;
        cursor: pointer;
        transition: all 0.3s ease;
    }}
    .custom-btn:hover {{
        background-color: rgba(22, 93, 255, 0.9);
        transform: translateY(-2px);
    }}
    
    /* 状态标签 */
    .status-online {{
        background-color: rgba(0, 180, 42, 0.2);
        color: {COLORS['success']};
        padding: 2px 8px;
        border-radius: 4px;
        font-size: 12px;
    }}
    .status-offline {{
        background-color: rgba(245, 63, 63, 0.2);
        color: {COLORS['danger']};
        padding: 2px 8px;
        border-radius: 4px;
        font-size: 12px;
    }}
    .status-alarm {{
        background-color: rgba(255, 125, 0, 0.2);
        color: {COLORS['warning']};
        padding: 2px 8px;
        border-radius: 4px;
        font-size: 12px;
    }}
    .status-maintenance {{
        background-color: rgba(100, 116, 139, 0.2);
        color: {COLORS['gray_400']};
        padding: 2px 8px;
        border-radius: 4px;
        font-size: 12px;
    }}
    
    /* 进度条样式 */
    .progress-bar {{
        background-color: {COLORS['gray_800']};
        border-radius: 9999px;
        height: 8px;
        overflow: hidden;
    }}
    .progress-fill {{
        height: 100%;
        border-radius: 9999px;
        transition: width 0.3s ease;
    }}
    
    /* 表格样式 */
    .custom-table {{
        width: 100%;
        border-collapse: collapse;
        font-size: 13px;
    }}
    .custom-table th {{
        background-color: {COLORS['tertiary']};
        color: {COLORS['light']};
        padding: 12px 16px;
        text-align: left;
        font-weight: 500;
        border-bottom: 1px solid {COLORS['gray_800']};
    }}
    .custom-table td {{
        padding: 12px 16px;
        border-bottom: 1px solid {COLORS['gray_800']};
    }}
    .custom-table tr:hover {{
        background-color: rgba(30, 41, 59, 0.5);
    }}
    
    /* 分页按钮 */
    .page-btn {{
        width: 32px;
        height: 32px;
        display: flex;
        align-items: center;
        justify-content: center;
        border-radius: 8px;
        background: {COLORS['tertiary']};
        color: {COLORS['gray_400']};
        border: none;
        cursor: pointer;
        transition: all 0.2s;
    }}
    .page-btn:hover {{
        background: {COLORS['primary']};
        color: white;
    }}
    .page-btn.active {{
        background: {COLORS['primary']};
        color: white;
    }}
    
    /* 动画 */
    @keyframes pulse {{
        0%, 100% {{ opacity: 1; }}
        50% {{ opacity: 0.5; }}
    }}
    .animate-pulse {{
        animation: pulse 2s cubic-bezier(0.4, 0, 0.6, 1) infinite;
    }}
    
    @keyframes float {{
        0%, 100% {{ transform: translateY(0); }}
        50% {{ transform: translateY(-10px); }}
    }}
    .animate-float {{
        animation: float 6s ease-in-out infinite;
    }}
    
    @keyframes spin {{
        from {{ transform: rotate(0deg); }}
        to {{ transform: rotate(360deg); }}
    }}
    .animate-spin {{
        animation: spin 1s linear infinite;
    }}
    
    @keyframes slideIn {{
        from {{ transform: translateX(100%); opacity: 0; }}
        to {{ transform: translateX(0); opacity: 1; }}
    }}
    .animate-slideIn {{
        animation: slideIn 0.3s ease-out;
    }}
    
    /* 侧边栏样式 */
    [data-testid="stSidebar"] {{
        background-color: {COLORS['secondary']};
    }}
    [data-testid="stSidebar"] .stMarkdown {{
        color: {COLORS['light']};
    }}
    
    /* 输入框样式 */
    .stTextInput > div > div > input {{
        background-color: rgba(30, 41, 59, 0.5);
        color: {COLORS['light']};
        border: 1px solid rgba(100, 116, 139, 0.3);
        border-radius: 8px;
    }}
    
    /* 选择框样式 */
    .stSelectbox > div > div > div {{
        background-color: {COLORS['secondary']};
        color: {COLORS['light']};
        border: 1px solid rgba(100, 116, 139, 0.3);
        border-radius: 8px;
    }}
    </style>
    """

def apply_custom_css():
    """应用自定义CSS样式"""
    st.markdown(get_custom_css(), unsafe_allow_html=True)

# ======================================
# 通用组件函数
# ======================================
def render_card(title, value, trend, trend_up, icon, icon_color, chart=None):
    """渲染数据卡片"""
    trend_icon = "📈" if trend_up else "📉"
    trend_color = COLORS['success'] if trend_up else COLORS['warning']
    
    card_html = f"""
    <div style="background: {COLORS['secondary']}; border-radius: 12px; padding: 16px;
                border: 1px solid rgba(100, 116, 139, 0.2); transition: all 0.3s ease;" class="hover-card">
        <div style="display: flex; align-items: flex-start; justify-content: space-between;">
            <div>
                <p style="margin: 0 0 4px 0; font-size: 13px; color: {COLORS['gray_400']}; display: flex; align-items: center; gap: 8px;">
                    <span>{title}</span>
                    <span style="font-size: 8px; color: {icon_color};">●</span>
                </p>
                <h3 style="margin: 0; font-size: 28px; font-weight: bold; color: white;">{value}</h3>
                <p style="margin: 8px 0 0 0; font-size: 12px; color: {trend_color}; display: flex; align-items: center;">
                    <span>{trend_icon}</span>
                    <span style="margin-left: 4px;">{trend} 较昨日</span>
                </p>
            </div>
            <div style="width: 48px; height: 48px; border-radius: 8px;
                        background: {icon_color}33; display: flex; align-items: center; justify-content: center;">
                <span style="font-size: 24px;">{icon}</span>
            </div>
        </div>
    </div>
    """
    st.markdown(card_html, unsafe_allow_html=True)
    if chart:
        st.plotly_chart(chart, use_container_width=True, config={'displayModeBar': False}, height=60)

def render_status_badge(status):
    """渲染状态标签"""
    status_config = {
        '在线': ('status-online', COLORS['success']),
        '离线': ('status-offline', COLORS['danger']),
        '告警': ('status-alarm', COLORS['warning']),
        '维护中': ('status-maintenance', COLORS['gray_400'])
    }
    class_name, color = status_config.get(status, ('status-maintenance', COLORS['gray_400']))
    return f'<span class="{class_name}">{status}</span>'

def render_progress_bar(value, max_value, color, label_left, label_right):
    """渲染进度条"""
    percentage = min(100, (value / max_value) * 100)
    return f"""
    <div style="background: {COLORS['gray_800']}; border-radius: 9999px; height: 8px; overflow: hidden;">
        <div style="background: linear-gradient(90deg, {color}, #60A5FA); height: 100%; 
                    border-radius: 9999px; width: {percentage}%;"></div>
    </div>
    <div style="display: flex; justify-content: space-between; font-size: 11px; color: {COLORS['gray_400']}; margin-top: 8px;">
        <span>{label_left}</span>
        <span style="color: {color};">{label_right}</span>
    </div>
    """

def render_section_header(title, subtitle=None, actions=None):
    """渲染区块标题"""
    subtitle_html = f'<p style="margin: 4px 0 0 0; font-size: 11px; color: {COLORS["gray_400"]};">{subtitle}</p>' if subtitle else ''
    actions_html = f'<div style="display: flex; gap: 8px;">{actions}</div>' if actions else ''
    
    return f"""
    <div style="display: flex; align-items: center; justify-content: space-between; margin-bottom: 16px;">
        <div>
            <h3 style="margin: 0; font-size: 16px; font-weight: 600; color: white;">{title}</h3>
            {subtitle_html}
        </div>
        {actions_html}
    </div>
    """

# ======================================
# 工具函数
# ======================================
def format_datetime(dt):
    """格式化日期时间"""
    if isinstance(dt, str):
        dt = datetime.fromisoformat(dt.replace('Z', '+00:00'))
    return dt.strftime('%Y-%m-%d %H:%M:%S')

def get_current_time():
    """获取当前时间字符串"""
    return datetime.now().strftime('%Y-%m-%d %H:%M:%S')

def get_image_base64(image_path):
    """将图片转换为base64编码"""
    try:
        with open(image_path, "rb") as img_file:
            return base64.b64encode(img_file.read()).decode()
    except Exception as e:
        return None

def get_status_color(status):
    """获取状态对应的颜色"""
    status_colors = {
        '在线': COLORS['success'],
        '离线': COLORS['danger'],
        '告警': COLORS['warning'],
        '维护中': COLORS['gray_400']
    }
    return status_colors.get(status, COLORS['gray_400'])

def get_ice_thickness_color(thickness):
    """获取覆冰厚度对应的颜色"""
    if thickness > 15:
        return COLORS['danger']
    elif thickness > 10:
        return COLORS['warning']
    return COLORS['light']

def truncate_string(s, max_length=50):
    """截断字符串"""
    if len(s) > max_length:
        return s[:max_length] + '...'
    return s

def format_number(num, decimal_places=1):
    """格式化数字"""
    return f"{num:.{decimal_places}f}"
