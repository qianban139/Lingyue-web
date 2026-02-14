"""
凌越智缆 - Session State 管理模块
用于管理应用状态、缓存数据和用户会话
"""

import streamlit as st
from datetime import datetime, timedelta
import random

# ======================================
# Session State 初始化
# ======================================
def init_session_state():
    """初始化所有Session State变量"""
    
    # 基础状态
    if 'initialized' not in st.session_state:
        st.session_state.initialized = True
    
    # 页面导航状态
    if 'current_page' not in st.session_state:
        st.session_state.current_page = 'page_0'
    
    # 时间相关状态
    if 'last_update' not in st.session_state:
        st.session_state.last_update = datetime.now()
    
    # 刷新状态
    if 'refreshing' not in st.session_state:
        st.session_state.refreshing = False
    
    if 'show_refresh_success' not in st.session_state:
        st.session_state.show_refresh_success = False
    
    # 图表时间范围状态
    if 'trend_time_range' not in st.session_state:
        st.session_state.trend_time_range = 'day'
    
    # 筛选器状态
    if 'device_filter' not in st.session_state:
        st.session_state.device_filter = 'all'
    
    if 'time_filter' not in st.session_state:
        st.session_state.time_filter = 'today'
    
    # 分页状态
    if 'current_page_num' not in st.session_state:
        st.session_state.current_page_num = 1
    
    if 'page_size' not in st.session_state:
        st.session_state.page_size = 10
    
    # 设备数据状态
    if 'online_devices' not in st.session_state:
        st.session_state.online_devices = 86
    
    if 'offline_devices' not in st.session_state:
        st.session_state.offline_devices = 14
    
    if 'alarm_devices' not in st.session_state:
        st.session_state.alarm_devices = 3
    
    if 'data_total' not in st.session_state:
        st.session_state.data_total = 128.7
    
    # 覆冰监测状态
    if 'ice_thickness' not in st.session_state:
        st.session_state.ice_thickness = 12.7
    
    if 'env_temp' not in st.session_state:
        st.session_state.env_temp = -5.3
    
    # 告警状态
    if 'show_alert' not in st.session_state:
        st.session_state.show_alert = False
    
    if 'unread_alarms' not in st.session_state:
        st.session_state.unread_alarms = 3
    
    # 设备列表数据（缓存）
    if 'all_devices' not in st.session_state:
        st.session_state.all_devices = []
    
    if 'filtered_devices' not in st.session_state:
        st.session_state.filtered_devices = []
    
    # 告警列表数据
    if 'alarms' not in st.session_state:
        st.session_state.alarms = []
    
    # 用户设置
    if 'user_settings' not in st.session_state:
        st.session_state.user_settings = {
            'theme': 'dark',
            'language': 'zh-CN',
            'notifications': True,
            'auto_refresh': True,
            'refresh_interval': 30
        }
    
    # 搜索状态
    if 'search_query' not in st.session_state:
        st.session_state.search_query = ''
    
    # 选中设备
    if 'selected_device' not in st.session_state:
        st.session_state.selected_device = None
    
    # 模态框状态
    if 'show_modal' not in st.session_state:
        st.session_state.show_modal = False
    
    if 'modal_content' not in st.session_state:
        st.session_state.modal_content = None
    
    # GPS定位状态
    if 'selected_region' not in st.session_state:
        st.session_state.selected_region = 'all'
    
    if 'map_zoom' not in st.session_state:
        st.session_state.map_zoom = 10
    
    # 数字孪生状态
    if 'twin_view_mode' not in st.session_state:
        st.session_state.twin_view_mode = '3d'
    
    if 'selected_model' not in st.session_state:
        st.session_state.selected_model = None

# ======================================
# 状态获取函数
# ======================================
def get_state(key, default=None):
    """获取Session State值"""
    return st.session_state.get(key, default)

def set_state(key, value):
    """设置Session State值"""
    st.session_state[key] = value

def update_state(key, updater):
    """更新Session State值（使用函数）"""
    current = st.session_state.get(key)
    if current is not None:
        st.session_state[key] = updater(current)

# ======================================
# 状态重置函数
# ======================================
def reset_filters():
    """重置筛选器状态"""
    st.session_state.device_filter = 'all'
    st.session_state.time_filter = 'today'
    st.session_state.current_page_num = 1
    st.session_state.search_query = ''

def reset_device_data():
    """重置设备数据状态"""
    st.session_state.online_devices = 86
    st.session_state.offline_devices = 14
    st.session_state.alarm_devices = 3
    st.session_state.data_total = 128.7
    st.session_state.ice_thickness = 12.7
    st.session_state.env_temp = -5.3

def clear_cache():
    """清除所有缓存数据"""
    st.session_state.all_devices = []
    st.session_state.filtered_devices = []
    st.session_state.selected_device = None

# ======================================
# 数据刷新函数
# ======================================
def refresh_data():
    """刷新所有数据"""
    st.session_state.refreshing = True
    
    # 模拟数据刷新
    st.session_state.online_devices = random.randint(80, 90)
    st.session_state.offline_devices = random.randint(10, 15)
    st.session_state.alarm_devices = random.randint(2, 5)
    st.session_state.data_total = round(100 + random.random() * 30, 1)
    st.session_state.ice_thickness = round(random.random() * 25, 1)
    st.session_state.env_temp = round(random.random() * 40 - 20, 1)
    st.session_state.last_update = datetime.now()
    
    st.session_state.refreshing = False
    st.session_state.show_refresh_success = True

# ======================================
# 分页相关函数
# ======================================
def get_paginated_data(data, page, page_size):
    """获取分页数据"""
    start = (page - 1) * page_size
    end = start + page_size
    return data[start:end]

def get_total_pages(total_items, page_size):
    """获取总页数"""
    return (total_items + page_size - 1) // page_size

def next_page():
    """下一页"""
    st.session_state.current_page_num += 1

def prev_page():
    """上一页"""
    st.session_state.current_page_num = max(1, st.session_state.current_page_num - 1)

def go_to_page(page):
    """跳转到指定页"""
    st.session_state.current_page_num = page

# ======================================
# 筛选相关函数
# ======================================
def set_device_filter(filter_value):
    """设置设备筛选器"""
    st.session_state.device_filter = filter_value
    st.session_state.current_page_num = 1

def set_time_filter(filter_value):
    """设置时间筛选器"""
    st.session_state.time_filter = filter_value
    st.session_state.current_page_num = 1

def set_search_query(query):
    """设置搜索查询"""
    st.session_state.search_query = query
    st.session_state.current_page_num = 1

# ======================================
# 告警相关函数
# ======================================
def mark_alarm_read():
    """标记告警为已读"""
    st.session_state.unread_alarms = max(0, st.session_state.unread_alarms - 1)

def clear_all_alarms():
    """清除所有告警"""
    st.session_state.unread_alarms = 0

def add_alarm():
    """添加新告警"""
    st.session_state.unread_alarms += 1

# ======================================
# 用户设置函数
# ======================================
def update_user_setting(key, value):
    """更新用户设置"""
    if 'user_settings' in st.session_state:
        st.session_state.user_settings[key] = value

def get_user_setting(key, default=None):
    """获取用户设置"""
    settings = st.session_state.get('user_settings', {})
    return settings.get(key, default)

# ======================================
# 模态框函数
# ======================================
def show_modal(content):
    """显示模态框"""
    st.session_state.show_modal = True
    st.session_state.modal_content = content

def hide_modal():
    """隐藏模态框"""
    st.session_state.show_modal = False
    st.session_state.modal_content = None

# ======================================
# 设备选择函数
# ======================================
def select_device(device):
    """选择设备"""
    st.session_state.selected_device = device

def clear_selected_device():
    """清除选中的设备"""
    st.session_state.selected_device = None

# ======================================
# 页面导航函数
# ======================================
def navigate_to(page):
    """导航到指定页面"""
    st.session_state.current_page = page

def get_current_page():
    """获取当前页面"""
    return st.session_state.get('current_page', 'page_0')
