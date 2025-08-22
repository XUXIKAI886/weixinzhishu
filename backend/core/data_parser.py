# -*- coding: utf-8 -*-
"""
数据解析模块
负责从原始数据文件中解析JSON数据和平台信息
"""

import json
from datetime import datetime
import numpy as np
from typing import Dict, List, Tuple, Any

from config.settings import DATA_FILE_PATH, PLATFORM_CONFIGS


def load_raw_data() -> Dict[str, Any]:
    """
    从原始文件加载JSON数据
    
    Returns:
        Dict[str, Any]: 解析后的JSON数据
        
    Raises:
        ValueError: 当找不到有效JSON数据时抛出
        FileNotFoundError: 当数据文件不存在时抛出
    """
    try:
        with open(DATA_FILE_PATH, 'r', encoding='utf-8') as f:
            content = f.read()
    except FileNotFoundError:
        raise FileNotFoundError(f"数据文件未找到: {DATA_FILE_PATH}")
    
    # 查找JSON数据起始位置
    json_start = content.find('{"code":0,"content":')
    if json_start == -1:
        raise ValueError("文件中找不到有效的JSON数据格式")
    
    # 提取并解析JSON数据
    json_data = content[json_start:].strip()
    try:
        data = json.loads(json_data)
        return data
    except json.JSONDecodeError as e:
        raise ValueError(f"JSON数据解析失败: {str(e)}")


def extract_platform_time_data(resp_list: List[Dict], platform_index: int) -> Tuple[List[datetime], List[int]]:
    """
    提取指定平台的时间序列数据
    
    Args:
        resp_list: 响应数据列表
        platform_index: 平台索引
        
    Returns:
        Tuple[List[datetime], List[int]]: 日期列表和数值列表
    """
    if platform_index >= len(resp_list):
        raise IndexError(f"平台索引超出范围: {platform_index}")
    
    time_indexes = resp_list[platform_index]['indexes'][0]['time_indexes']
    
    dates = []
    values = []
    
    for time_data in time_indexes:
        # 解析日期（YYYYMMDD格式）
        time_str = str(time_data['time'])
        date = datetime.strptime(time_str, '%Y%m%d')
        dates.append(date)
        
        # 提取数值
        value = int(time_data['score'])
        values.append(value)
    
    return dates, values


def parse_platforms_data(platform_type: str = 'delivery_platforms') -> Dict[str, Dict]:
    """
    解析指定类型的平台数据
    
    Args:
        platform_type: 平台类型 ('five_platforms' 或 'delivery_platforms')
        
    Returns:
        Dict[str, Dict]: 包含各平台数据的字典
    """
    # 加载原始数据
    raw_data = load_raw_data()
    resp_list = raw_data['content']['resp_list']
    
    # 获取平台配置
    if platform_type not in PLATFORM_CONFIGS:
        raise ValueError(f"不支持的平台类型: {platform_type}")
    
    platforms_config = PLATFORM_CONFIGS[platform_type]
    platforms_data = {}
    
    # 提取各平台数据
    for platform_info in platforms_config:
        platform_index = platform_info['index']
        platform_name = platform_info['name_cn']
        platform_color = platform_info['color']
        
        try:
            dates, values = extract_platform_time_data(resp_list, platform_index)
            
            platforms_data[platform_name] = {
                'dates': dates,
                'values': values,
                'color': platform_color,
                'name': platform_info.get('name', platform_name),
                'name_cn': platform_name
            }
        except (IndexError, KeyError) as e:
            print(f"警告: 无法解析平台 {platform_name} 的数据: {str(e)}")
            continue
    
    return platforms_data


def calculate_statistics(values: List[int]) -> Dict[str, float]:
    """
    计算数据统计信息
    
    Args:
        values: 数值列表
        
    Returns:
        Dict[str, float]: 包含统计信息的字典
    """
    if not values:
        return {'mean': 0, 'std': 0, 'min': 0, 'max': 0}
    
    np_values = np.array(values)
    return {
        'mean': float(np.mean(np_values)),
        'std': float(np.std(np_values)),
        'min': float(np.min(np_values)),
        'max': float(np.max(np_values))
    }


def get_date_range(platforms_data: Dict[str, Dict]) -> Tuple[datetime, datetime]:
    """
    获取所有平台数据的日期范围
    
    Args:
        platforms_data: 平台数据字典
        
    Returns:
        Tuple[datetime, datetime]: 开始和结束日期
    """
    all_dates = []
    for platform_data in platforms_data.values():
        all_dates.extend(platform_data['dates'])
    
    if not all_dates:
        return None, None
    
    return min(all_dates), max(all_dates)