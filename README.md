# ⚡ 凌越智缆 - 智能运维平台

> 高压电缆维护机器人智能运维平台 | 让电力运维更智能、更高效、更安全

[![Python](https://img.shields.io/badge/Python-3.9+-blue.svg)](https://python.org)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.28+-red.svg)](https://streamlit.io)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

## 📋 项目简介

凌越智缆是一款基于Streamlit开发的高压电缆维护机器人智能运维平台，提供全方位的电缆运维监控、设备管理、数据分析与可视化功能。

### ✨ 核心功能

| 模块 | 功能描述 |
|------|----------|
| 🏠 **项目介绍** | 视频介绍，核心功能 |
| 📊 **数据仪表盘** | 核心数据概览、设备运行状态趋势、覆冰监测、告警统计 |
| 🔧 **设备管理** | 机器人与传感器设备管理、状态监控、参数配置 |
| ❄️ **覆冰监测** | 实时覆冰数据监测、厚度分析、预警提醒 |
| 📍 **GPRS定位** | 设备位置追踪、地图展示、轨迹回放 |
| 🏗️ **数字孪生** | 3D可视化、虚拟仿真、场景模拟 |
| 🔔 **告警中心** | 告警管理、通知设置、历史记录 |

## 🚀 快速开始

### 环境要求

- Python 3.9+
- pip 或 conda

### 安装步骤

1. **克隆项目**
```bash
git clone <repository-url>
cd lingyue-site
```

2. **创建虚拟环境（推荐）**
```bash
python -m venv venv

# Windows
venv\Scripts\activate

# macOS/Linux
source venv/bin/activate
```

3. **安装依赖**
```bash
pip install -r requirements.txt
```

4. **配置Streamlit**
```bash
# 复制配置文件到Streamlit配置目录
mkdir -p ~/.streamlit
cp backend/config.toml ~/.streamlit/config.toml
cp backend/secrets.toml ~/.streamlit/secrets.toml
```

5. **启动应用**
```bash
cd src
streamlit run main.py
```

6. **访问应用**
打开浏览器访问: http://localhost:8501

## 📁 项目结构

```
lingyue-site/
├── src/                    # 源代码目录
│   ├── main.py            # 主入口文件
│   ├── page_0.py          # 项目介绍
│   ├── page_1.py          # 数据仪表盘
│   ├── page_2.py          # 设备管理
│   ├── page_3.py          # 覆冰监测
│   ├── page_4.py          # GPRS定位
│   ├── page_5.py          # 数字孪生
│   ├── page_6.py          # 告警中心
│   ├── common.py          # 公用函数与样式
│   ├── session_state.py   # 状态管理
│   └── algorithm.py       # 算法与数据生成
├── backend/               # 后端配置
│   ├── config.toml        # Streamlit主题配置
│   └── secrets.toml       # 密钥配置
├── assets/                # 静态资源
│   ├── images/            # 图片资源
│   └── videos/            # 视频资源
├── requirements.txt       # 依赖列表
└── README.md             # 项目说明
```

## 🎨 界面预览

### 项目介绍
- 视频介绍
- 核心功能
- 创新点


### 数据仪表盘
- 核心指标卡片展示
- 设备运行状态趋势图
- 覆冰监测实时数据
- 告警统计与分布

### 设备管理
- 设备列表与筛选
- 设备状态监控
- 参数配置与管理

### 覆冰监测
- 实时覆冰数据
- 厚度趋势分析
- 预警提醒

### GPRS定位
- 设备位置地图展示
- 实时位置追踪
- 历史轨迹回放

### 数字孪生
- 3D场景可视化
- 虚拟仿真
- 实时数据映射

### 告警中心
- 告警列表管理
- 告警级别分类
- 通知设置

## ⚙️ 配置说明

### 主题配置 (backend/config.toml)
```toml
[theme]
primaryColor = "#165DFF"
backgroundColor = "#0A0F1F"
secondaryBackgroundColor = "#0F172A"
textColor = "#E2E8F0"
```

### 密钥配置 (backend/secrets.toml)
```toml
[api_keys]
map_key = "your_map_api_key"
```

## 🔧 开发指南

### 添加新页面

1. 在 `src/` 目录创建 `page_X.py`
2. 实现 `show()` 函数作为页面入口
3. 在 `main.py` 中导入并添加路由

```python
# page_X.py
def show():
    st.title("新页面")
    # 页面内容

# main.py
import page_X

def route_page():
    # ...
    elif current_page == 'page_X':
        page_X.show()
```

### 自定义组件

使用 `common.py` 中的组件函数：

```python
from common import render_card, render_status_badge, COLORS

# 渲染数据卡片
render_card(
    title="在线设备",
    value="108",
    trend="+5.2%",
    trend_up=True,
    icon="🔧",
    icon_color=COLORS['success']
)

# 渲染状态标签
status_html = render_status_badge("在线")
st.markdown(status_html, unsafe_allow_html=True)
```

## 📊 技术栈

- **前端框架**: [Streamlit](https://streamlit.io/)
- **可视化**: [Plotly](https://plotly.com/)
- **地图**: [Folium](https://python-visualization.github.io/folium/)
- **数据处理**: [Pandas](https://pandas.pydata.org/), [NumPy](https://numpy.org/)

## 🤝 贡献指南

1. Fork 本仓库
2. 创建特性分支 (`git checkout -b feature/AmazingFeature`)
3. 提交更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送分支 (`git push origin feature/AmazingFeature`)
5. 创建 Pull Request

## 📄 许可证

本项目采用 MIT 许可证 - 详见 [LICENSE](LICENSE) 文件

## 📞 联系我们

- 邮箱: admin@lingyue.com
- 官网: https://lingyue.com
- 技术支持: 智能运维团队

---

<p align="center">
  <strong>⚡ 凌越智缆 - 让电力运维更智能、更高效、更安全</strong>
</p>
