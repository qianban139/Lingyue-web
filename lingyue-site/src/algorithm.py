"""
凌越智缆 - 核心算法模块
包含: 设备数据处理、覆冰检测算法、数据分析、预测算法
"""

import numpy as np
import pandas as pd
from datetime import datetime, timedelta
import random

# ======================================
# 模拟数据生成
# ======================================
class MockDataGenerator:
    """模拟数据生成器"""
    
    DEVICE_TYPES = ['高压电缆', '低压电缆', '监测终端', '除冰机器人', '巡检无人机']
    STATUSES = ['在线', '离线', '告警', '维护中']
    LOCATIONS = ['鄂西地区', '川东地区', '云贵地区', '西北地区', '华北地区']
    OPERATORS = ['自动运维', '人工巡检', '机器人作业']
    
    @classmethod
    def generate_device(cls, device_id):
        """生成单个设备数据"""
        status = random.choice(cls.STATUSES)
        location = random.choice(cls.LOCATIONS)
        device_type = random.choice(cls.DEVICE_TYPES)
        
        return {
            'id': f'DEV{str(device_id).zfill(4)}',
            'name': f'{location}设备#{device_id}',
            'type': device_type,
            'status': status,
            'voltage': round(random.uniform(100, 600), 1),
            'temperature': round(random.uniform(-20, 20), 1),
            'ice_thickness': round(random.uniform(0, 25), 1),
            'last_report': (datetime.now() - timedelta(minutes=random.randint(0, 60))).strftime('%Y-%m-%d %H:%M:%S'),
            'operator': random.choice(cls.OPERATORS),
            'region': location,
            'latitude': round(random.uniform(28.0, 35.0), 6),
            'longitude': round(random.uniform(105.0, 118.0), 6)
        }
    
    @classmethod
    def generate_devices(cls, count=120):
        """生成多个设备数据"""
        return [cls.generate_device(i) for i in range(1, count + 1)]
    
    @classmethod
    def generate_chart_data(cls, data_type='online', count=12):
        """生成图表数据"""
        labels = []
        data = []
        
        base_values = {
            'online': 80 + random.random() * 10,
            'offline': 10 + random.random() * 5,
            'alarm': 2 + random.random() * 4,
            'data': 100 + random.random() * 30
        }
        
        base_value = base_values.get(data_type, 50)
        
        for i in range(count):
            labels.append(f'{i+1}时')
            variation = (random.random() - 0.5) * 10
            data.append(max(0, base_value + variation))
        
        return {'labels': labels, 'data': data}
    
    @classmethod
    def generate_trend_data(cls, time_range='day'):
        """生成趋势数据"""
        if time_range == 'hour':
            labels = [f'{i*2}时' for i in range(12)]
            online = [80 + random.random() * 15 for _ in range(12)]
            alarm = [random.random() * 10 for _ in range(12)]
            offline = [random.random() * 8 for _ in range(12)]
        elif time_range == 'day':
            labels = [f'{i}时' for i in range(24)]
            online = [80 + random.random() * 15 for _ in range(24)]
            alarm = [random.random() * 10 for _ in range(24)]
            offline = [random.random() * 8 for _ in range(24)]
        elif time_range == 'week':
            labels = ['周一', '周二', '周三', '周四', '周五', '周六', '周日']
            online = [85, 82, 86, 88, 90, 92, 95]
            alarm = [5, 8, 12, 15, 10, 7, 5]
            offline = [10, 10, 8, 7, 5, 3, 2]
        else:  # month
            labels = ['1月', '2月', '3月', '4月', '5月', '6月', '7月', '8月', '9月', '10月', '11月', '12月']
            online = [85, 82, 86, 88, 90, 92, 95, 93, 91, 89, 87, 86]
            alarm = [5, 8, 12, 15, 10, 7, 5, 3, 4, 6, 8, 3]
            offline = [10, 10, 8, 7, 5, 3, 2, 4, 5, 5, 5, 14]
        
        return {
            'labels': labels,
            'online': online,
            'alarm': alarm,
            'offline': offline
        }
    
    @classmethod
    def generate_alarms(cls, count=15):
        """生成告警数据"""
        alarm_types = [
            ('覆冰厚度超标', 'danger'),
            ('设备离线', 'warning'),
            ('温度异常', 'warning'),
            ('电压波动', 'info'),
            ('通信中断', 'danger')
        ]
        
        alarms = []
        for i in range(count):
            alarm_type, level = random.choice(alarm_types)
            device_id = random.randint(1, 120)
            alarms.append({
                'id': f'ALM{str(i+1).zfill(4)}',
                'device_id': f'DEV{str(device_id).zfill(4)}',
                'type': alarm_type,
                'level': level,
                'message': f'{alarm_type}: 设备DEV{str(device_id).zfill(4)}',
                'time': (datetime.now() - timedelta(minutes=random.randint(0, 120))).strftime('%Y-%m-%d %H:%M:%S'),
                'status': '未处理' if random.random() > 0.3 else '已处理'
            })
        
        return alarms
    
    @classmethod
    def generate_gps_data(cls, count=50):
        """生成GPS定位数据"""
        gps_data = []
        base_coords = {
            '鄂西地区': (30.5, 110.5),
            '川东地区': (29.5, 106.5),
            '云贵地区': (25.0, 104.0),
            '西北地区': (36.0, 103.0),
            '华北地区': (39.9, 116.4)
        }
        
        for i in range(count):
            region = random.choice(list(base_coords.keys()))
            base_lat, base_lon = base_coords[region]
            
            gps_data.append({
                'id': f'GPS{str(i+1).zfill(4)}',
                'device_id': f'DEV{str(random.randint(1, 120)).zfill(4)}',
                'region': region,
                'latitude': round(base_lat + random.uniform(-2, 2), 6),
                'longitude': round(base_lon + random.uniform(-2, 2), 6),
                'altitude': round(random.uniform(500, 3000), 1),
                'speed': round(random.uniform(0, 50), 1),
                'signal_strength': random.randint(20, 100),
                'last_update': (datetime.now() - timedelta(minutes=random.randint(0, 30))).strftime('%H:%M:%S'),
                'status': random.choice(['正常', '弱信号', '离线'])
            })
        
        return gps_data

# ======================================
# 覆冰检测算法
# ======================================
class IceDetectionAlgorithm:
    """覆冰检测算法"""
    
    # 覆冰厚度阈值 (mm)
    THRESHOLDS = {
        'normal': 10,
        'warning': 15,
        'danger': 20
    }
    
    @classmethod
    def detect_ice_thickness(cls, thickness):
        """检测覆冰厚度等级"""
        if thickness >= cls.THRESHOLDS['danger']:
            return 'danger', '严重告警'
        elif thickness >= cls.THRESHOLDS['warning']:
            return 'warning', '中度告警'
        elif thickness >= cls.THRESHOLDS['normal']:
            return 'caution', '轻度告警'
        else:
            return 'normal', '正常'
    
    @classmethod
    def calculate_risk_score(cls, thickness, temperature, wind_speed=0):
        """计算覆冰风险分数 (0-100)"""
        # 基础风险分
        base_risk = min(100, (thickness / cls.THRESHOLDS['danger']) * 50)
        
        # 温度影响 (温度越低风险越高)
        temp_factor = max(0, (-temperature) / 20) * 20
        
        # 风速影响
        wind_factor = min(20, wind_speed / 5)
        
        total_risk = min(100, base_risk + temp_factor + wind_factor)
        
        return round(total_risk, 1)
    
    @classmethod
    def predict_ice_growth(cls, current_thickness, temperature, humidity, hours=24):
        """预测覆冰增长"""
        # 简化的线性增长模型
        if temperature >= 0:
            growth_rate = 0
        else:
            growth_rate = abs(temperature) * 0.1 * (humidity / 100)
        
        predicted_thickness = current_thickness + (growth_rate * hours)
        return round(min(50, predicted_thickness), 1)

# ======================================
# 设备数据分析
# ======================================
class DeviceAnalytics:
    """设备数据分析"""
    
    @classmethod
    def calculate_statistics(cls, devices):
        """计算设备统计信息"""
        if not devices:
            return {}
        
        df = pd.DataFrame(devices)
        
        stats = {
            'total': len(devices),
            'online': len([d for d in devices if d['status'] == '在线']),
            'offline': len([d for d in devices if d['status'] == '离线']),
            'alarm': len([d for d in devices if d['status'] == '告警']),
            'maintenance': len([d for d in devices if d['status'] == '维护中']),
            'avg_voltage': df['voltage'].mean(),
            'avg_temperature': df['temperature'].mean(),
            'avg_ice_thickness': df['ice_thickness'].mean(),
            'max_ice_thickness': df['ice_thickness'].max(),
            'ice_alarm_count': len([d for d in devices if d['ice_thickness'] > 10])
        }
        
        stats['online_rate'] = round((stats['online'] / stats['total']) * 100, 1) if stats['total'] > 0 else 0
        
        return stats
    
    @classmethod
    def filter_devices(cls, devices, filter_type='all', search_query=''):
        """筛选设备"""
        filtered = devices
        
        if filter_type == 'high':
            filtered = [d for d in filtered if d['type'] == '高压电缆']
        elif filter_type == 'low':
            filtered = [d for d in filtered if d['type'] == '低压电缆']
        elif filter_type == 'ice':
            filtered = [d for d in filtered if d['ice_thickness'] > 10]
        elif filter_type == 'alarm':
            filtered = [d for d in filtered if d['status'] == '告警']
        elif filter_type == 'online':
            filtered = [d for d in filtered if d['status'] == '在线']
        elif filter_type == 'offline':
            filtered = [d for d in filtered if d['status'] == '离线']
        
        if search_query:
            search_lower = search_query.lower()
            filtered = [d for d in filtered if 
                       search_lower in d['id'].lower() or 
                       search_lower in d['name'].lower() or
                       search_lower in d['type'].lower()]
        
        return filtered
    
    @classmethod
    def get_devices_by_region(cls, devices):
        """按地区分组统计设备"""
        region_stats = {}
        for device in devices:
            region = device['region']
            if region not in region_stats:
                region_stats[region] = {'total': 0, 'online': 0, 'alarm': 0}
            region_stats[region]['total'] += 1
            if device['status'] == '在线':
                region_stats[region]['online'] += 1
            if device['status'] == '告警':
                region_stats[region]['alarm'] += 1
        
        return region_stats
    
    @classmethod
    def get_devices_by_type(cls, devices):
        """按类型分组统计设备"""
        type_stats = {}
        for device in devices:
            device_type = device['type']
            if device_type not in type_stats:
                type_stats[device_type] = {'total': 0, 'online': 0, 'alarm': 0}
            type_stats[device_type]['total'] += 1
            if device['status'] == '在线':
                type_stats[device_type]['online'] += 1
            if device['status'] == '告警':
                type_stats[device_type]['alarm'] += 1
        
        return type_stats

# ======================================
# 预测算法
# ======================================
class PredictionAlgorithm:
    """预测算法"""
    
    @classmethod
    def predict_device_failure(cls, device_data):
        """预测设备故障概率"""
        # 简化的故障预测模型
        risk_factors = 0
        
        # 温度异常
        if device_data['temperature'] > 40 or device_data['temperature'] < -15:
            risk_factors += 20
        
        # 电压异常
        if device_data['voltage'] > 550 or device_data['voltage'] < 120:
            risk_factors += 15
        
        # 覆冰厚度
        if device_data['ice_thickness'] > 15:
            risk_factors += 25
        
        # 离线时间 (模拟)
        if device_data['status'] == '离线':
            risk_factors += 30
        
        failure_probability = min(100, risk_factors + random.randint(0, 10))
        
        if failure_probability >= 70:
            return 'high', failure_probability
        elif failure_probability >= 40:
            return 'medium', failure_probability
        else:
            return 'low', failure_probability
    
    @classmethod
    def predict_maintenance_time(cls, device_data):
        """预测维护时间"""
        _, failure_prob = cls.predict_device_failure(device_data)
        
        if failure_prob >= 70:
            return '24小时内'
        elif failure_prob >= 40:
            return '7天内'
        else:
            return '30天内'

# ======================================
# 数据处理工具
# ======================================
class DataProcessor:
    """数据处理工具"""
    
    @staticmethod
    def paginate(data, page, page_size):
        """分页处理"""
        start = (page - 1) * page_size
        end = start + page_size
        return data[start:end]
    
    @staticmethod
    def sort_by(data, key, reverse=False):
        """排序"""
        return sorted(data, key=lambda x: x.get(key, ''), reverse=reverse)
    
    @staticmethod
    def export_to_csv(devices, filename='devices.csv'):
        """导出为CSV"""
        df = pd.DataFrame(devices)
        return df.to_csv(index=False)
    
    @staticmethod
    def get_status_summary(devices):
        """获取状态汇总"""
        summary = {'在线': 0, '离线': 0, '告警': 0, '维护中': 0}
        for device in devices:
            status = device.get('status', '未知')
            if status in summary:
                summary[status] += 1
        return summary
