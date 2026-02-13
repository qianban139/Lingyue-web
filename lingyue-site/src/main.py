"""
凌越智缆 - 主入口文件
高压电缆维护机器人智能运维平台
"""

import streamlit as st
import sys
from pathlib import Path

# 添加当前目录到路径
sys.path.insert(0, str(Path(__file__).parent))

from common import COLORS, apply_custom_css, get_current_time
from session_state import init_session_state, refresh_data

# 导入页面模块
import page_0
import page_1
import page_2
import page_3
import page_4
import page_5

# ======================================
# 页面配置
# ======================================
st.set_page_config(
    page_title="凌越智缆 - 智能运维平台",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ======================================
# 初始化
# ======================================
init_session_state()
apply_custom_css()

# ======================================
# 侧边栏导航
# ======================================
def render_sidebar():
    """渲染侧边栏导航"""
    with st.sidebar:
        # Logo区域
        st.markdown(f"""
        <div style="padding: 20px 0; text-align: center; border-bottom: 1px solid rgba(100, 116, 139, 0.2); margin-bottom: 20px;">
            <div style="display: flex; align-items: center; justify-content: center; gap: 12px;">
                <div style="width: 40px; height: 40px; background: linear-gradient(135deg, {COLORS['primary']}, #60A5FA); 
                            border-radius: 10px; display: flex; align-items: center; justify-content: center;">
                    <span style="font-size: 20px;">⚡</span>
                </div>
                <div style="text-align: left;">
                    <div style="font-size: 18px; font-weight: bold; color: white;">凌越智缆</div>
                    <div style="font-size: 11px; color: {COLORS['gray_400']};">智能运维平台</div>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        # 导航菜单
        st.markdown(f"""
        <div style="padding: 0 12px; margin-bottom: 12px;">
            <span style="font-size: 11px; color: {COLORS['gray_400']}; text-transform: uppercase; letter-spacing: 1px;">主菜单</span>
        </div>
        """, unsafe_allow_html=True)
        
        # 导航项配置
        nav_items = [
            ('page_0', '📊', '数据仪表盘', '核心数据概览'),
            ('page_1', '🔧', '设备管理', '机器人与传感器'),
            ('page_2', '❄️', '覆冰监测', '实时覆冰数据'),
            ('page_3', '📍', 'GPRS定位', '设备位置追踪'),
            ('page_4', '🏗️', '数字孪生', '3D可视化'),
            ('page_5', '🔔', '告警中心', '告警与通知'),
        ]
        
        current_page = st.session_state.current_page
        
        for page_id, icon, title, desc in nav_items:
            is_active = current_page == page_id
            active_style = f"""
                background: rgba(22, 93, 255, 0.15);
                border-left: 3px solid {COLORS['primary']};
                color: white;
            """ if is_active else f"""
                background: transparent;
                border-left: 3px solid transparent;
                color: {COLORS['gray_400']};
            """
            
            # 使用按钮实现导航
            btn_container = st.container()
            with btn_container:
                col1, col2 = st.columns([0.15, 0.85])
                with col1:
                    st.markdown(f"""
                    <div style="padding: 12px 0; text-align: center; {active_style}">
                        <span style="font-size: 18px;">{icon}</span>
                    </div>
                    """, unsafe_allow_html=True)
                with col2:
                    if st.button(
                        f"{title}",
                        key=f"nav_{page_id}",
                        use_container_width=True,
                        type="secondary" if is_active else "tertiary"
                    ):
                        st.session_state.current_page = page_id
                        st.rerun()
        
        # 系统状态
        st.markdown("---")
        st.markdown(f"""
        <div style="padding: 16px; background: rgba(15, 23, 42, 0.5); border-radius: 8px;">
            <div style="display: flex; align-items: center; justify-content: space-between; margin-bottom: 8px;">
                <span style="font-size: 12px; color: {COLORS['gray_400']};">系统状态</span>
                <span style="font-size: 11px; color: {COLORS['success']};">● 正常运行</span>
            </div>
            <div style="display: flex; align-items: center; justify-content: space-between; margin-bottom: 8px;">
                <span style="font-size: 12px; color: {COLORS['gray_400']};">数据更新</span>
                <span style="font-size: 11px; color: {COLORS['light']};">刚刚</span>
            </div>
            <div style="display: flex; align-items: center; justify-content: space-between;">
                <span style="font-size: 12px; color: {COLORS['gray_400']};">当前时间</span>
                <span style="font-size: 11px; color: {COLORS['light']};">{get_current_time()}</span>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        # 用户信息
        st.markdown("---")
        st.markdown(f"""
        <div style="padding: 12px; display: flex; align-items: center; gap: 12px;">
            <div style="width: 36px; height: 36px; background: linear-gradient(135deg, {COLORS['primary']}, #60A5FA); 
                        border-radius: 50%; display: flex; align-items: center; justify-content: center;">
                <span style="font-size: 14px;">👤</span>
            </div>
            <div>
                <div style="font-size: 13px; color: white; font-weight: 500;">管理员</div>
                <div style="font-size: 11px; color: {COLORS['gray_400']};">admin@lingyue.com</div>
            </div>
        </div>
        """, unsafe_allow_html=True)

# ======================================
# 顶部页眉
# ======================================
def render_header():
    """渲染顶部页眉"""
    page_titles = {
        'page_0': ('数据仪表盘', '核心数据概览与实时监控'),
        'page_1': ('设备管理', '机器人与传感器设备管理'),
        'page_2': ('覆冰监测', '实时覆冰数据监测分析'),
        'page_3': ('GPRS定位', '设备位置追踪与地图展示'),
        'page_4': ('数字孪生', '3D可视化与虚拟仿真'),
        'page_5': ('告警中心', '告警管理与通知设置'),
    }
    
    current_page = st.session_state.current_page
    title, subtitle = page_titles.get(current_page, ('凌越智缆', '智能运维平台'))
    
    st.markdown(f"""
    <div style="background: linear-gradient(90deg, rgba(10,15,31,0.95) 0%, rgba(22,93,255,0.2) 100%); 
                padding: 24px 32px; border-radius: 12px; margin-bottom: 24px;
                border: 1px solid rgba(100, 116, 139, 0.2);
                display: flex; align-items: center; justify-content: space-between;">
        <div>
            <h1 style="margin: 0; font-size: 24px; font-weight: bold; color: white;">{title}</h1>
            <p style="margin: 4px 0 0 0; font-size: 13px; color: {COLORS['gray_400']};">{subtitle}</p>
        </div>
        <div style="display: flex; align-items: center; gap: 16px;">
            <div style="text-align: right;">
                <div style="font-size: 12px; color: {COLORS['gray_400']};">当前时间</div>
                <div style="font-size: 14px; color: white; font-weight: 500;">{get_current_time()}</div>
            </div>
            <div style="width: 40px; height: 40px; background: rgba(22, 93, 255, 0.2); 
                        border-radius: 50%; display: flex; align-items: center; justify-content: center;">
                <span style="font-size: 18px;">⚡</span>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

# ======================================
# 底部页脚
# ======================================
def render_footer():
    """渲染底部页脚"""
    st.markdown("---")
    st.markdown(f"""
    <div style="padding: 24px 0; text-align: center;">
        <div style="display: flex; align-items: center; justify-content: center; gap: 8px; margin-bottom: 12px;">
            <span style="font-size: 16px;">⚡</span>
            <span style="font-size: 14px; font-weight: 600; color: white;">凌越智缆</span>
        </div>
        <p style="margin: 0 0 8px 0; font-size: 12px; color: {COLORS['gray_400']};">
            高压电缆维护机器人智能运维平台 | 让电力运维更智能、更高效、更安全
        </p>
        <p style="margin: 0; font-size: 11px; color: {COLORS['gray_500']};">
            © 2026 凌越智缆 版权所有 | 技术支持：智能运维团队
        </p>
    </div>
    """, unsafe_allow_html=True)

# ======================================
# 页面路由
# ======================================
def route_page():
    """根据当前页面路由到对应模块"""
    current_page = st.session_state.current_page
    
    if current_page == 'page_0':
        page_0.show()
    elif current_page == 'page_1':
        page_1.show()
    elif current_page == 'page_2':
        page_2.show()
    elif current_page == 'page_3':
        page_3.show()
    elif current_page == 'page_4':
        page_4.show()
    elif current_page == 'page_5':
        page_5.show()
    else:
        page_0.show()

# ======================================
# 主程序
# ======================================
def main():
    """主程序入口"""
    # 渲染侧边栏
    render_sidebar()
    
    # 渲染顶部页眉
    render_header()
    
    # 路由到对应页面
    route_page()
    
    # 渲染底部页脚
    render_footer()

if __name__ == "__main__":
    main()
