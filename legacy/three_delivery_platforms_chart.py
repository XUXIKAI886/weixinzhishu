#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
三大外卖平台微信指数折线图
只显示美团外卖、饿了么、京东外卖，横坐标每月显示
"""

import json
from datetime import datetime
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

# 使用非交互式后端
import matplotlib
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
        {'index': 2, 'name': 'Meituan-Delivery', 'name_cn': '美团外卖', 'color': '#FF6600'},
        {'index': 3, 'name': 'Ele.me', 'name_cn': '饿了么', 'color': '#0078FF'},
        {'index': 4, 'name': 'JD-Delivery', 'name_cn': '京东外卖', 'color': '#AA2116'}
    ]
    
    # 提取三个外卖平台的数据
    platforms_data = {}
    
    for platform_info in delivery_platforms:
        i = platform_info['index']
        platform_name = platform_info['name']
        platform_name_cn = platform_info['name_cn']
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
        
        platforms_data[platform_name] = {
            'dates': dates,
            'scores': scores,
            'name_cn': platform_name_cn,
            'color': color
        }
    
    return platforms_data

def create_line_chart(platforms_data):
    """创建简洁的折线图"""
    
    # 设置图表样式
    plt.style.use('default')
    fig, ax = plt.subplots(figsize=(16, 10))
    
    # 绘制三个外卖平台的趋势线
    for platform_name, data in platforms_data.items():
        ax.plot(data['dates'], data['scores'], 
                color=data['color'], 
                linewidth=3, 
                label=f"{platform_name} ({data['name_cn']})",
                alpha=0.9)
    
    # 设置标题和标签
    ax.set_title('Delivery Platforms WeChat Index Trend\\n外卖平台微信指数趋势对比 (Aug 2024 - Aug 2025)', 
                fontsize=18, fontweight='bold', pad=20)
    ax.set_xlabel('Date', fontsize=14, fontweight='bold')
    ax.set_ylabel('WeChat Index', fontsize=14, fontweight='bold')
    
    # 格式化X轴 - 每个月都显示
    ax.xaxis.set_major_locator(mdates.MonthLocator(interval=1))  # 每月显示
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m'))
    ax.xaxis.set_minor_locator(mdates.WeekdayLocator())
    
    # 旋转日期标签
    plt.setp(ax.xaxis.get_majorticklabels(), rotation=45, ha='right')
    
    # 格式化Y轴（显示为万为单位）
    ax.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, p: f'{x/10000:.0f}万'))
    
    # 添加网格
    ax.grid(True, alpha=0.3, linestyle='--')
    
    # 设置图例
    legend = ax.legend(loc='upper left', fontsize=14, frameon=True, 
                      fancybox=True, shadow=True, framealpha=0.9)
    legend.get_frame().set_facecolor('white')
    
    # 调整布局
    plt.tight_layout()
    
    return fig

def create_simple_html_chart(platforms_data):
    """创建简洁的HTML图表"""
    
    html_content = """
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>外卖平台微信指数趋势对比</title>
    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
    <style>
        body {
            font-family: 'Arial', sans-serif;
            margin: 20px;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
        }
        .container {
            background-color: white;
            padding: 30px;
            border-radius: 15px;
            box-shadow: 0 10px 30px rgba(0,0,0,0.2);
        }
        .title {
            text-align: center;
            color: #333;
            margin-bottom: 30px;
        }
        .chart-container {
            position: relative;
            height: 600px;
            margin: 20px 0;
        }
        .stats {
            display: flex;
            justify-content: space-around;
            margin: 30px 0;
            flex-wrap: wrap;
        }
        .stat-card {
            padding: 20px;
            border-radius: 12px;
            text-align: center;
            color: white;
            font-weight: bold;
            min-width: 200px;
            margin: 10px;
            box-shadow: 0 4px 15px rgba(0,0,0,0.2);
        }
        .stat-card h3 {
            margin: 0 0 15px 0;
            font-size: 1.2em;
        }
        .stat-card .value {
            font-size: 1.8em;
            margin: 10px 0;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1 class="title">外卖平台微信指数趋势对比<br>Delivery Platforms WeChat Index Trend</h1>
        <p style="text-align: center; color: #666; font-size: 1.1em;">数据时间范围: 2024年8月22日 - 2025年8月21日</p>
        
        <div class="chart-container">
            <canvas id="lineChart"></canvas>
        </div>
        
        <div class="stats">
"""
    
    # 添加统计卡片
    for platform_name, data in platforms_data.items():
        scores = data['scores']
        avg_score = np.mean(scores)
        max_score = max(scores)
        min_score = min(scores)
        
        html_content += f"""
            <div class="stat-card" style="background: linear-gradient(135deg, {data['color']} 0%, {data['color']}AA 100%);">
                <h3>{data['name_cn']}<br>({platform_name})</h3>
                <div class="value">{avg_score/10000:.0f}万</div>
                <p>平均指数</p>
                <p>峰值: {max_score/10000:.0f}万</p>
                <p>最低: {min_score/10000:.0f}万</p>
            </div>
        """
    
    # 准备Chart.js数据
    datasets = []
    for platform_name, data in platforms_data.items():
        chart_data = []
        for j, date in enumerate(data['dates']):
            chart_data.append({
                'x': date.strftime('%Y-%m-%d'),
                'y': data['scores'][j]
            })
        
        datasets.append({
            'label': f"{data['name_cn']} ({platform_name})",
            'data': chart_data,
            'borderColor': data['color'],
            'backgroundColor': data['color'] + '20',
            'fill': False,
            'tension': 0.1,
            'borderWidth': 3
        })
    
    html_content += f"""
        </div>
    </div>
    
    <script>
        const ctx = document.getElementById('lineChart').getContext('2d');
        const chart = new Chart(ctx, {{
            type: 'line',
            data: {{
                datasets: {json.dumps(datasets)}
            }},
            options: {{
                responsive: true,
                maintainAspectRatio: false,
                plugins: {{
                    title: {{
                        display: true,
                        text: '外卖平台微信指数趋势对比 (Delivery Platforms WeChat Index Trend)',
                        font: {{
                            size: 18,
                            weight: 'bold'
                        }}
                    }},
                    legend: {{
                        display: true,
                        position: 'top',
                        labels: {{
                            boxWidth: 15,
                            font: {{
                                size: 14
                            }}
                        }}
                    }}
                }},
                scales: {{
                    x: {{
                        type: 'time',
                        time: {{
                            parser: 'YYYY-MM-DD',
                            tooltipFormat: 'YYYY-MM-DD',
                            displayFormats: {{
                                day: 'MM-DD',
                                month: 'YYYY-MM'
                            }},
                            unit: 'month'
                        }},
                        title: {{
                            display: true,
                            text: '日期 (Date)',
                            font: {{
                                weight: 'bold',
                                size: 14
                            }}
                        }}
                    }},
                    y: {{
                        title: {{
                            display: true,
                            text: '微信指数 WeChat Index',
                            font: {{
                                weight: 'bold',
                                size: 14
                            }}
                        }},
                        beginAtZero: false
                    }}
                }},
                interaction: {{
                    intersect: false,
                    mode: 'index'
                }}
            }}
        }});
    </script>
    <script src="https://cdn.jsdelivr.net/npm/chartjs-adapter-date-fns/dist/chartjs-adapter-date-fns.bundle.min.js"></script>
</body>
</html>
"""
    
    return html_content

def main():
    """主函数"""
    print("正在提取外卖平台数据...")
    
    # 解析数据
    platforms_data = parse_delivery_platforms_data()
    print(f"成功提取 {len(platforms_data)} 个外卖平台的数据")
    
    # 创建折线图
    print("生成折线图...")
    fig = create_line_chart(platforms_data)
    
    # 保存静态图表
    output_file = 'E:\\claude-code\\微信指数\\delivery_platforms_line_chart.png'
    fig.savefig(output_file, dpi=300, bbox_inches='tight', 
                facecolor='white', edgecolor='none')
    print(f"折线图已保存至: {output_file}")
    
    # 创建HTML图表
    print("生成HTML图表...")
    html_content = create_simple_html_chart(platforms_data)
    
    # 保存HTML图表
    html_file = 'E:\\claude-code\\微信指数\\delivery_platforms_line_chart.html'
    with open(html_file, 'w', encoding='utf-8') as f:
        f.write(html_content)
    print(f"HTML图表已保存至: {html_file}")
    
    # 输出数据统计
    print("\\n=== 外卖平台数据统计 ===")
    for platform_name, data in platforms_data.items():
        scores = data['scores']
        print(f"\\n{data['name_cn']} ({platform_name}):")
        print(f"  平均指数: {np.mean(scores):,.0f}")
        print(f"  最高指数: {max(scores):,.0f}")
        print(f"  最低指数: {min(scores):,.0f}")

if __name__ == "__main__":
    main()