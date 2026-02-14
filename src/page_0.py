"""
凌越智缆 - 项目介绍页面 (Page 0)
主页面，展示核心技术概览、覆冰监测等
"""

import streamlit as st
from pathlib import Path
import base64
from common import COLORS, apply_custom_css
from session_state import init_session_state


# ======================================
# 页面渲染函数
# ======================================
def render_page():
    # 自定义样式
    st.markdown("""
    <style>
        .stApp {
            background: linear-gradient(135deg, #0f172a 0%, #1e293b 100%);
        }
        .video-card {
            background: rgba(30, 41, 59, 0.6);
            backdrop-filter: blur(12px);
            border-radius: 16px;
            border: 1px solid rgba(100, 116, 139, 0.2);
            padding: 24px;
            box-shadow: 0 20px 25px -5px rgba(0, 0, 0, 0.3);
        }
        .video-item {
            background: rgba(15, 23, 42, 0.6);
            border-radius: 12px;
            padding: 16px;
            margin-bottom: 12px;
            border: 2px solid transparent;
            cursor: pointer;
            transition: all 0.3s ease;
        }
        .video-item:hover {
            background: rgba(30, 41, 59, 0.8);
            border-color: rgba(96, 165, 250, 0.3);
            transform: translateX(5px);
        }
        .video-item.active {
            background: rgba(22, 93, 255, 0.15);
            border-color: #165DFF;
            box-shadow: 0 0 20px rgba(22, 93, 255, 0.2);
        }
        .tech-badge {
            display: inline-block;
            background: rgba(22, 93, 255, 0.2);
            color: #60a5fa;
            padding: 4px 12px;
            border-radius: 20px;
            font-size: 12px;
            margin-right: 8px;
            margin-top: 8px;
            border: 1px solid rgba(22, 93, 255, 0.3);
        }
        .gradient-text {
            background: linear-gradient(135deg, #60a5fa 0%, #a78bfa 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
        }
        .image-container {
            background: rgba(15, 23, 42, 0.4);
            border-radius: 12px;
            overflow: hidden;
            border: 1px solid rgba(100, 116, 139, 0.1);
            transition: transform 0.3s ease;
        }
        .image-container:hover {
            transform: scale(1.02);
        }
        .image-caption {
            background: rgba(15, 23, 42, 0.8);
            padding: 12px;
            text-align: center;
            border-top: 1px solid rgba(100, 116, 139, 0.1);
        }
    </style>
    """, unsafe_allow_html=True)

    # 视频配置数据
    videos_config = {
        "feature": {
            "title": "核心功能",
            "subtitle": "Feature Demonstration",
            "icon": "⚙️",
            "desc": "多轴联动（双臂仿生越障）技术，结合神经网络算法实现线路越障，实现越障功能，提高除冰效率",
            "highlights": ["双臂仿生越障", "神经网络算法", "多轴联动技术"],
            "file": "../assets/videos/feature.mp4"
        },
        "innovation": {
            "title": "创新亮点",
            "subtitle": "Innovation Highlights",
            "icon": "💡",
            "desc": "线路除冰机器人，创造性的将抗干扰技术跟等电位融合到机器人除冰过程中，极大提高了除冰效果，该产品值得推广",
            "highlights": ["抗干扰技术", "等电位融合", "高效除冰"],
            "file": "../assets/videos/innovation.mp4"
        },
        "show": {
            "title": "技术展示",
            "subtitle": "Technical Showcase",
            "icon": "🔬",
            "desc": "展示除冰机器人的核心技术实现与现场作业实况，体现技术成熟度与可靠性",
            "highlights": ["现场作业", "技术实现", "可靠性验证"],
            "file": "../assets/videos/show.mp4"
        },
        "support": {
            "title": "实践支持",
            "subtitle": "Practical Support",
            "icon": "🏆",
            "desc": "产品已通过内蒙古乌海超高压供电局测试，获得实际应用验证，具备大规模推广条件",
            "highlights": ["乌海超高压供电局", "实际测试验证", "推广就绪"],
            "file": "../assets/videos/support.mp4"
        },
        "technology": {
            "title": "技术架构",
            "subtitle": "Technology Stack",
            "icon": "🔧",
            "desc": "采用多轴联动（双臂仿生越障）技术，结合神经网络算法实现线路越障，构建智能化除冰解决方案",
            "highlights": ["多轴联动", "仿生设计", "智能控制"],
            "file": "../assets/videos/technology.mp4"
        }
    }

    # 图片配置
    images_config = [
        {"path": "../assets/images/91.png", "title": "产品实景图"},
        {"path": "../assets/images/92.png", "title": "技术展示图"},
        {"path": "../assets/images/93.png", "title": "应用场景图"}
    ]

    # 初始化session state
    if 'current_video' not in st.session_state:
        st.session_state.current_video = "feature"

    # 辅助函数：安全获取视频
    def get_video_bytes(video_key):
        """获取视频字节流"""
        video_path = Path(videos_config[video_key]["file"])
        if video_path.exists():
            return open(video_path, "rb")
        return None

    # 页面头部
    st.markdown("""
    <div style="text-align: center; padding: 30px 0 40px 0;">
        <h1 style="font-size: 48px; margin-bottom: 16px;">
            <span class="gradient-text">🎬 凌越智缆 项目演示中心</span>
        </h1>
        <p style="color: #94a3b8; font-size: 18px; max-width: 800px; margin: 0 auto;">
            智能电缆除冰机器人系统 · 技术展示与功能演示
        </p>
    </div>
    """, unsafe_allow_html=True)

    # 主体布局：左侧视频播放（8列），右侧选择列表（4列）
    main_cols = st.columns([8, 4], gap="large")

    with main_cols[0]:
        current_key = st.session_state.current_video
        current_video = videos_config[current_key]
        
        # 视频播放卡片
        st.markdown(f"""
        <div class="video-card" style="margin-bottom: 20px;">
            <div style="display: flex; align-items: center; margin-bottom: 20px;">
                <div style="font-size: 40px; margin-right: 16px;">{current_video['icon']}</div>
                <div>
                    <h2 style="color: white; margin: 0; font-size: 28px; font-weight: 600;">{current_video['title']}</h2>
                    <p style="color: #64748b; margin: 4px 0 0 0; font-size: 14px; text-transform: uppercase; letter-spacing: 2px;">{current_video['subtitle']}</p>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        # 视频播放器区域
        video_file = get_video_bytes(current_key)
        
        if video_file:
            st.video(video_file, start_time=0)
        else:
            # 视频文件不存在时的占位
            st.markdown(f"""
            <div style="background: rgba(15, 23, 42, 0.8); border-radius: 12px; height: 400px; display: flex; flex-direction: column; align-items: center; justify-content: center; border: 2px dashed rgba(100, 116, 139, 0.3);">
                <div style="font-size: 64px; margin-bottom: 16px;">🎥</div>
                <p style="color: #64748b; font-size: 16px;">视频文件未找到</p>
                <p style="color: #475569; font-size: 13px; margin-top: 8px;">路径: {current_video['file']}</p>
            </div>
            """, unsafe_allow_html=True)
        
        # 视频描述信息
        st.markdown(f"""
        <div class="video-card" style="margin-top: 20px;">
            <h3 style="color: white; margin-top: 0; margin-bottom: 12px; font-size: 18px;">📋 内容摘要</h3>
            <p style="color: #cbd5e1; font-size: 15px; line-height: 1.8; margin-bottom: 16px;">
                {current_video['desc']}
            </p>
            <div style="margin-top: 16px;">
                <h4 style="color: #64748b; font-size: 13px; margin-bottom: 12px; text-transform: uppercase; letter-spacing: 1px;">技术亮点</h4>
                <div>
        """, unsafe_allow_html=True)
        
        # 显示技术标签
        for highlight in current_video['highlights']:
            st.markdown(f'<span class="tech-badge">{highlight}</span>', unsafe_allow_html=True)
        
        st.markdown("</div></div></div>", unsafe_allow_html=True)

    with main_cols[1]:
        # 右侧视频选择列表
        st.markdown("""
        <div class="video-card" style="height: 100%;">
            <h3 style="color: white; margin-top: 0; margin-bottom: 20px; font-size: 18px; display: flex; align-items: center;">
                <span style="margin-right: 8px;">📑</span> 演示目录
            </h3>
            <div style="margin-bottom: 20px; padding-bottom: 20px; border-bottom: 1px solid rgba(100, 116, 139, 0.2);">
                <p style="color: #64748b; font-size: 13px; margin: 0;">选择下方卡片切换不同主题的演示视频</p>
            </div>
        """, unsafe_allow_html=True)
        
        # 生成视频选择按钮
        for key, video in videos_config.items():
            is_active = key == st.session_state.current_video
            
            # 使用columns布局创建可点击区域
            cols = st.columns([1, 6])
            with cols[0]:
                st.markdown(f"<div style='font-size: 24px; text-align: center; margin-top: 10px;'>{video['icon']}</div>", unsafe_allow_html=True)
            with cols[1]:
                btn_type = "primary" if is_active else "secondary"
                if st.button(
                    f"{video['title']}\n\n{video['subtitle']}", 
                    key=f"btn_{key}",
                    type=btn_type,
                    use_container_width=True,
                    help=f"播放: {video['title']}"
                ):
                    st.session_state.current_video = key
                    st.rerun()
        
        st.markdown("</div>", unsafe_allow_html=True)

    # 分隔线
    st.markdown("<hr style='border: none; border-top: 1px solid rgba(100, 116, 139, 0.2); margin: 40px 0;'>", unsafe_allow_html=True)

    # 产品图片展示区
    st.markdown("""
    <div style="text-align: center; margin-bottom: 30px;">
        <h2 style="color: white; font-size: 32px; margin-bottom: 8px;">
            <span style="background: linear-gradient(135deg, #f87171 0%, #fbbf24 100%); -webkit-background-clip: text; -webkit-text-fill-color: transparent;">
                📷 产品图集
            </span>
        </h2>
        <p style="color: #64748b; font-size: 14px;">实物拍摄与技术细节展示</p>
    </div>
    """, unsafe_allow_html=True)

    # 图片网格布局（3列）- 修复版本
    img_cols = st.columns(3)

    for idx, (col, img_conf) in enumerate(zip(img_cols, images_config)):
        with col:
            img_path = Path(img_conf["path"])
            
            if img_path.exists():
                # ✅ 修复：使用 use_container_width 替代 use_column_width
                st.image(
                    str(img_path), 
                    use_container_width=True,  # 修复弃用警告
                    caption=""
                )
                # 自定义标题样式
                st.markdown(f"""
                <div style="text-align: center; margin-top: -10px; padding: 12px; background: rgba(15, 23, 42, 0.6); border-radius: 0 0 12px 12px; border: 1px solid rgba(100, 116, 139, 0.1); border-top: none;">
                    <h4 style="color: white; margin: 0; font-size: 16px; font-weight: 600;">{img_conf['title']}</h4>
                    <p style="color: #64748b; font-size: 12px; margin: 4px 0 0 0;">图 {idx+1}</p>
                </div>
                """, unsafe_allow_html=True)
            else:
                # 图片不存在时的占位
                st.markdown(f"""
                <div style="background: rgba(15, 23, 42, 0.6); border-radius: 12px; height: 280px; display: flex; flex-direction: column; align-items: center; justify-content: center; border: 2px dashed rgba(100, 116, 139, 0.2); margin-bottom: 10px;">
                    <div style="font-size: 48px; margin-bottom: 8px;">🖼️</div>
                    <div style="color: #475569; font-size: 13px;">图片未找到</div>
                    <div style="color: #64748b; font-size: 11px; margin-top: 4px;">{img_conf['title']}</div>
                </div>
                """, unsafe_allow_html=True)


    # 分隔线
    st.markdown("<hr style='border: none; border-top: 1px solid rgba(100, 116, 139, 0.2); margin: 40px 0;'>", unsafe_allow_html=True)

    # ======================================
    # 1. 电缆损坏图像识别展示
    # ======================================
    st.markdown("""
    <div style="text-align: center; margin-bottom: 30px;">
        <h2 style="color: white; font-size: 28px; margin-bottom: 8px;">
            <span style="background: linear-gradient(135deg, #ef4444 0%, #f97316 100%); -webkit-background-clip: text; -webkit-text-fill-color: transparent;">
                🔍 电缆损坏图像识别
            </span>
        </h2>
        <p style="color: #64748b; font-size: 14px;">基于深度学习的电缆表面缺陷智能检测</p>
    </div>
    """, unsafe_allow_html=True)

    # 电缆损坏图片配置（5张）
    cable_damage_images = [
        {"path": "../assets/images/11.png", "title": "孔洞、表面割伤、砸伤", "label": "多类型损伤"},
        {"path": "../assets/images/12.png", "title": "割伤", "label": "机械损伤"},
        {"path": "../assets/images/13.png", "title": "破损", "label": "表面缺陷"},
        {"path": "../assets/images/14.png", "title": "破损、4个孔洞", "label": "严重损伤"},
        {"path": "../assets/images/15.png", "title": "砸伤", "label": "冲击损伤"}
    ]

    # 5列布局展示
    damage_cols = st.columns(5)
    for idx, (col, img_conf) in enumerate(zip(damage_cols, cable_damage_images)):
        with col:
            img_path = Path(img_conf["path"])
            
            if img_path.exists():
                st.image(
                    str(img_path), 
                    use_container_width=True,
                    caption=""
                )
                st.markdown(f"""
                <div style="text-align: center; margin-top: -10px; padding: 10px; background: rgba(239, 68, 68, 0.1); border-radius: 0 0 8px 8px; border: 1px solid rgba(239, 68, 68, 0.2); border-top: none;">
                    <h4 style="color: #fca5a5; margin: 0; font-size: 13px; font-weight: 600;">{img_conf['title']}</h4>
                    <span style="display: inline-block; background: rgba(239, 68, 68, 0.2); color: #ef4444; padding: 2px 8px; border-radius: 12px; font-size: 11px; margin-top: 6px;">{img_conf['label']}</span>
                </div>
                """, unsafe_allow_html=True)
            else:
                st.markdown(f"""
                <div style="background: rgba(15, 23, 42, 0.6); border-radius: 8px; height: 200px; display: flex; flex-direction: column; align-items: center; justify-content: center; border: 2px dashed rgba(239, 68, 68, 0.3); margin-bottom: 10px;">
                    <div style="font-size: 32px; margin-bottom: 4px;">🔍</div>
                    <div style="color: #ef4444; font-size: 11px;">{img_conf['title']}</div>
                </div>
                """, unsafe_allow_html=True)

    # 技术说明
    st.markdown("""
    <div style="background: rgba(239, 68, 68, 0.05); border-left: 4px solid #ef4444; padding: 16px 20px; margin: 24px 0 40px 0; border-radius: 0 8px 8px 0;">
        <p style="color: #cbd5e1; font-size: 14px; line-height: 1.6; margin: 0;">
            <strong style="color: #fca5a5;">识别能力：</strong>系统可自动识别电缆表面的孔洞、割伤、砸伤、破损等缺陷类型，识别精度达到像素级，支持多目标同时检测与分类。
        </p>
    </div>
    """, unsafe_allow_html=True)

    # ======================================
    # 2. 覆雪电缆与设备识别展示
    # ======================================
    st.markdown("""
    <div style="text-align: center; margin-bottom: 30px; margin-top: 50px;">
        <h2 style="color: white; font-size: 28px; margin-bottom: 8px;">
            <span style="background: linear-gradient(135deg, #06b6d4 0%, #3b82f6 100%); -webkit-background-clip: text; -webkit-text-fill-color: transparent;">
                ❄️ 覆雪电缆与设备识别
            </span>
        </h2>
        <p style="color: #64748b; font-size: 14px;">覆冰监测、抗冰环检测与绝缘子状态识别</p>
    </div>
    """, unsafe_allow_html=True)

    # 覆雪与设备图片配置（6张）
    snow_equipment_images = [
        {"path": "../assets/images/21.png", "title": "覆雪电缆", "label": "积雪识别", "type": "snow"},
        {"path": "../assets/images/22.png", "title": "覆雪电缆", "label": "积雪覆盖", "type": "snow"},
        {"path": "../assets/images/23.png", "title": "覆雪电缆和抗冰环", "label": "复合识别", "type": "mixed"},
        {"path": "../assets/images/24.png", "title": "抗冰环", "label": "设备识别", "type": "equipment"},
        {"path": "../assets/images/25.png", "title": "绝缘子损坏", "label": "故障检测", "type": "defect"},
        {"path": "../assets/images/26.png", "title": "覆雪电缆", "label": "覆冰监测", "type": "snow"}
    ]

    # 6张图使用3列2行布局
    for row_idx in range(2):
        cols = st.columns(3)
        start_idx = row_idx * 3
        end_idx = start_idx + 3
        
        for idx, img_conf in enumerate(snow_equipment_images[start_idx:end_idx]):
            with cols[idx]:
                img_path = Path(img_conf["path"])
                
                # 根据类型设置颜色主题
                color_map = {
                    "snow": ("#06b6d4", "rgba(6, 182, 212, 0.1)", "rgba(6, 182, 212, 0.2)"),      # 青色
                    "equipment": ("#3b82f6", "rgba(59, 130, 246, 0.1)", "rgba(59, 130, 246, 0.2)"), # 蓝色
                    "mixed": ("#8b5cf6", "rgba(139, 92, 246, 0.1)", "rgba(139, 92, 246, 0.2)"),     # 紫色
                    "defect": ("#ef4444", "rgba(239, 68, 68, 0.1)", "rgba(239, 68, 68, 0.2)")       # 红色
                }
                text_color, bg_color, badge_bg = color_map.get(img_conf["type"], ("#64748b", "rgba(100, 116, 139, 0.1)", "rgba(100, 116, 139, 0.2)"))
                
                if img_path.exists():
                    st.image(
                        str(img_path), 
                        use_container_width=True,
                        caption=""
                    )
                    st.markdown(f"""
                    <div style="text-align: center; margin-top: -10px; padding: 10px; background: {bg_color}; border-radius: 0 0 8px 8px; border: 1px solid {badge_bg}; border-top: none;">
                        <h4 style="color: {text_color}; margin: 0; font-size: 13px; font-weight: 600;">{img_conf['title']}</h4>
                        <span style="display: inline-block; background: {badge_bg}; color: {text_color}; padding: 2px 8px; border-radius: 12px; font-size: 11px; margin-top: 6px;">{img_conf['label']}</span>
                    </div>
                    """, unsafe_allow_html=True)
                else:
                    st.markdown(f"""
                    <div style="background: rgba(15, 23, 42, 0.6); border-radius: 8px; height: 200px; display: flex; flex-direction: column; align-items: center; justify-content: center; border: 2px dashed {text_color}; margin-bottom: 10px;">
                        <div style="font-size: 32px; margin-bottom: 4px;">❄️</div>
                        <div style="color: {text_color}; font-size: 11px;">{img_conf['title']}</div>
                    </div>
                    """, unsafe_allow_html=True)

    # 技术说明
    st.markdown("""
    <div style="background: rgba(6, 182, 212, 0.05); border-left: 4px solid #06b6d4; padding: 16px 20px; margin: 24px 0 40px 0; border-radius: 0 8px 8px 0;">
        <p style="color: #cbd5e1; font-size: 14px; line-height: 1.6; margin: 0;">
            <strong style="color: #67e8f9;">识别能力：</strong>支持覆雪/覆冰电缆检测、抗冰环等防冰设备识别、绝缘子破损检测，可自动评估覆冰厚度与设备状态，为除冰决策提供数据支持。
        </p>
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