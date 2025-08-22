#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
生成完全中文的静态PNG图表
使用英文标签避免字体乱码问题
"""

import json
from datetime import datetime
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import matplotlib

# 使用非交互式后端
matplotlib.use('Agg')

def parse_delivery_platforms_data():
    """解析外卖平台数据"""
    
    # 从文件中读取JSON响应数据
    file_path = 'E:\\claude-code\\微信指数\\26_Full.txt'
    
    # 读取文件内容并提取JSON部分
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 找到JSON数据的开始位置
    json_start = content.find('{"code":0,"content":')
    if json_start == -1:
        raise ValueError("找不到JSON数据")
    
    # 提取JSON数据
    json_data = content[json_start:].strip()
    
    # 解析JSON数据
    data = json.loads(json_data)
    resp_list = data['content']['resp_list']
    
    # 定义要保留的平台（索引2=美团外卖, 3=饿了么, 4=京东外卖）
    delivery_platforms = [
        {'index': 2, 'name_cn': 'Meituan-Delivery', 'label': 'Meituan-Delivery (美团外卖)', 'color': '#FF6600'},
        {'index': 3, 'name_cn': 'Ele.me', 'label': 'Ele.me (饿了么)', 'color': '#0078FF'},
        {'index': 4, 'name_cn': 'JD-Delivery', 'label': 'JD-Delivery (京东外卖)', 'color': '#AA2116'}
    ]
    
    # 提取三个外卖平台的数据
    platforms_data = {}
    
    for platform_info in delivery_platforms:
        i = platform_info['index']
        platform_name_cn = platform_info['name_cn']
        label = platform_info['label']
        color = platform_info['color']
        
        time_indexes = resp_list[i]['indexes'][0]['time_indexes']
        
        dates = []
        scores = []
        
        for item in time_indexes:
            # 将时间格式从20240822转换为2024-08-22
            time_str = str(item['time'])
            date = datetime.strptime(time_str, '%Y%m%d')
            dates.append(date)
            scores.append(item['score'])
        
        platforms_data[platform_name_cn] = {
            'dates': dates,
            'scores': scores,
            'label': label,
            'color': color
        }
    
    return platforms_data

def create_static_chart(platforms_data):
    """创建静态图表，使用英文标签避免乱码"""
    
    # 设置图表样式
    plt.style.use('default')
    fig, ax = plt.subplots(figsize=(16, 10))
    
    # 设置背景色
    fig.patch.set_facecolor('white')
    ax.set_facecolor('#fafafa')
    
    # 绘制三个外卖平台的趋势线
    for platform_name_cn, data in platforms_data.items():
        ax.plot(data['dates'], data['scores'], 
                color=data['color'], 
                linewidth=3, 
                label=data['label'],
                alpha=0.9)
    
    # 设置标题和标签（使用英文避免乱码）
    ax.set_title('Delivery Platforms WeChat Index Trend Comparison\\n(Aug 2024 - Aug 2025)', 
                fontsize=18, fontweight='bold', pad=20)
    ax.set_xlabel('Date', fontsize=14, fontweight='bold')
    ax.set_ylabel('WeChat Index', fontsize=14, fontweight='bold')
    
    # 格式化X轴 - 每个月都显示
    ax.xaxis.set_major_locator(mdates.MonthLocator(interval=1))  # 每月显示
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m'))
    
    # 旋转日期标签
    plt.setp(ax.xaxis.get_majorticklabels(), rotation=45, ha='right')
    
    # 格式化Y轴（显示为万为单位）
    ax.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, p: f'{x/10000:.0f}K'))
    
    # 添加网格
    ax.grid(True, alpha=0.3, linestyle='--', color='gray')
    
    # 设置图例
    legend = ax.legend(loc='upper left', fontsize=12, frameon=True, 
                      fancybox=True, shadow=True, framealpha=0.9)
    legend.get_frame().set_facecolor('white')
    legend.get_frame().set_edgecolor('gray')
    
    # 添加统计信息文本框
    stats_text = "Platform Statistics:\\n"
    for platform_name_cn, data in platforms_data.items():
        avg_score = np.mean(data['scores'])
        stats_text += f"{platform_name_cn}: {avg_score/10000:.0f}K avg\\n"
    
    ax.text(0.02, 0.98, stats_text, transform=ax.transAxes, 
            verticalalignment='top', fontsize=10,
            bbox=dict(boxstyle='round,pad=0.5', facecolor='lightblue', alpha=0.8))
    
    # 调整布局
    plt.tight_layout()
    
    return fig

def main():
    """主函数"""
    print("正在提取外卖平台数据...")
    
    # 解析数据
    platforms_data = parse_delivery_platforms_data()
    print(f"成功提取 {len(platforms_data)} 个外卖平台的数据")
    
    # 创建静态图表
    print("生成静态PNG图表...")
    fig = create_static_chart(platforms_data)
    
    # 保存静态图表
    output_file = 'E:\\claude-code\\微信指数\\chinese_delivery_static_chart.png'
    fig.savefig(output_file, dpi=300, bbox_inches='tight', 
                facecolor='white', edgecolor='none')
    print(f"静态图表已保存至: {output_file}")
    
    plt.close(fig)  # 释放内存
    
    print("\\n=== 图表生成完成 ===")
    print("HTML图表：chinese_delivery_chart.html（完全中文，无乱码）")
    print("PNG图表：chinese_delivery_static_chart.png（英文标签，避免乱码）")

if __name__ == "__main__":
    main()