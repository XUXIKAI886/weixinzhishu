# -*- coding: utf-8 -*-
"""
微信指数项目配置文件
"""

import os

# 文件路径配置
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
DATA_FILE_PATH = os.path.join(PROJECT_ROOT, 'data', '26_Full.txt')

# 平台配置信息
PLATFORM_CONFIGS = {
    'five_platforms': [
        {'index': 0, 'name': 'JD.com', 'name_cn': '京东', 'color': '#E3002B'},
        {'index': 1, 'name': 'Meituan', 'name_cn': '美团', 'color': '#FFD100'},
        {'index': 2, 'name': 'Meituan-Delivery', 'name_cn': '美团外卖', 'color': '#FF6600'},
        {'index': 3, 'name': 'Ele.me', 'name_cn': '饿了么', 'color': '#0078FF'},
        {'index': 4, 'name': 'JD-Delivery', 'name_cn': '京东外卖', 'color': '#AA2116'}
    ],
    'delivery_platforms': [
        {'index': 2, 'name': 'Meituan-Delivery', 'name_cn': '美团外卖', 'color': '#FF6600'},
        {'index': 3, 'name': 'Ele.me', 'name_cn': '饿了么', 'color': '#0078FF'},
        {'index': 4, 'name': 'JD-Delivery', 'name_cn': '京东外卖', 'color': '#AA2116'}
    ]
}

# 图表配置
CHART_CONFIG = {
    'dpi': 150,
    'figsize': (14, 8),
    'font_family': 'SimHei',
    'line_width': 3,
    'marker_size': 8,
    'grid_alpha': 0.3,
    'legend_fontsize': 12,
    'axis_labelsize': 12,
    'title_fontsize': 16,
    'tick_labelsize': 10
}

# 输出配置
OUTPUT_CONFIG = {
    'image_format': 'png',
    'image_quality': 95,
    'output_dir': os.path.join(PROJECT_ROOT, 'output')
}