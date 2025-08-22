#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
5平台微信指数数据可视化脚本
分析京东、美团、美团外卖、饿了么、京东外卖的指数趋势
"""

import json
from datetime import datetime
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

# 使用非交互式后端
import matplotlib
matplotlib.use('Agg')

def parse_five_platforms_data():
    """解析包含5个平台的HTTP响应数据"""
    
    # 从文件中读取JSON响应数据
    file_path = 'E:\\claude-code\\微信指数\\26_Full.txt'
    
    # 读取文件内容并提取JSON部分
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 找到JSON数据的开始位置
    json_start = content.find('{"code":0,"content":')
    if json_start == -1:
        raise ValueError("找不到JSON数据")
    
    # 提取JSON数据（到文件末尾）
    json_data = content[json_start:].strip()
    
    # 解析JSON数据
    data = json.loads(json_data)
    resp_list = data['content']['resp_list']
    
    # 定义平台信息
    platform_info = [
        {'name': 'JD.com', 'name_cn': '京东', 'color': '#E3002B'},
        {'name': 'Meituan', 'name_cn': '美团', 'color': '#FFD100'},
        {'name': 'Meituan-Delivery', 'name_cn': '美团外卖', 'color': '#FF6600'},
        {'name': 'Ele.me', 'name_cn': '饿了么', 'color': '#0078FF'},
        {'name': 'JD-Delivery', 'name_cn': '京东外卖', 'color': '#AA2116'}
    ]
    
    # 提取五个平台的数据
    platforms_data = {}
    
    for i, platform in enumerate(resp_list):
        platform_name = platform_info[i]['name']
        platform_name_cn = platform_info[i]['name_cn']
        color = platform_info[i]['color']
        time_indexes = platform['indexes'][0]['time_indexes']
        
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

def create_comprehensive_visualization(platforms_data):
    """创建综合可视化图表"""
    
    # 创建图表布局
    fig = plt.figure(figsize=(20, 16))
    
    # 主趋势图
    ax1 = plt.subplot(2, 2, (1, 2))
    
    # 绘制所有平台的趋势线
    for platform_name, data in platforms_data.items():
        ax1.plot(data['dates'], data['scores'], 
                color=data['color'], 
                linewidth=2.5, 
                label=f"{platform_name} ({data['name_cn']})",
                alpha=0.9)
    
    ax1.set_title('Five-Platform WeChat Index Trend Comparison\\n5大平台微信指数趋势对比 (Aug 2024 - Aug 2025)', 
                 fontsize=16, fontweight='bold', pad=20)
    ax1.set_xlabel('Date', fontsize=12, fontweight='bold')
    ax1.set_ylabel('WeChat Index', fontsize=12, fontweight='bold')
    
    # 格式化X轴
    ax1.xaxis.set_major_locator(mdates.MonthLocator(interval=2))
    ax1.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m'))
    plt.setp(ax1.xaxis.get_majorticklabels(), rotation=45, ha='right')
    
    # 格式化Y轴
    ax1.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, p: f'{x/100000000:.1f}B'))
    
    # 添加网格和图例
    ax1.grid(True, alpha=0.3, linestyle='--')
    ax1.legend(loc='upper left', fontsize=10, frameon=True, fancybox=True, shadow=True)
    
    # 子图2：平台对比柱状图（平均指数）
    ax2 = plt.subplot(2, 2, 3)
    
    platform_names = []
    avg_scores = []
    colors = []
    
    for platform_name, data in platforms_data.items():
        platform_names.append(f"{platform_name}\\n({data['name_cn']})")
        avg_scores.append(np.mean(data['scores']) / 100000000)  # 转换为亿
        colors.append(data['color'])
    
    bars = ax2.bar(platform_names, avg_scores, color=colors, alpha=0.7, edgecolor='black')
    ax2.set_title('Average WeChat Index Comparison\\n平均微信指数对比', fontweight='bold')
    ax2.set_ylabel('Average Index (100M)', fontweight='bold')
    ax2.tick_params(axis='x', rotation=45)
    
    # 在柱状图上添加数值标签
    for bar, score in zip(bars, avg_scores):
        height = bar.get_height()
        ax2.text(bar.get_x() + bar.get_width()/2., height + 0.1,
                f'{score:.1f}B', ha='center', va='bottom', fontweight='bold')
    
    # 子图3：波动性分析（标准差）
    ax3 = plt.subplot(2, 2, 4)
    
    volatility_scores = []
    for platform_name, data in platforms_data.items():
        volatility_scores.append(np.std(data['scores']) / 100000000)  # 转换为亿
    
    bars2 = ax3.bar(platform_names, volatility_scores, color=colors, alpha=0.7, edgecolor='black')
    ax3.set_title('Volatility Comparison (Standard Deviation)\\n波动性对比（标准差）', fontweight='bold')
    ax3.set_ylabel('Standard Deviation (100M)', fontweight='bold')
    ax3.tick_params(axis='x', rotation=45)
    
    # 在波动性图上添加数值标签
    for bar, score in zip(bars2, volatility_scores):
        height = bar.get_height()
        ax3.text(bar.get_x() + bar.get_width()/2., height + 0.05,
                f'{score:.1f}B', ha='center', va='bottom', fontweight='bold')
    
    # 调整布局
    plt.tight_layout()
    
    return fig

def create_html_visualization(platforms_data):
    """创建HTML交互式可视化图表"""
    
    html_content = """
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>5大平台微信指数对比 - Five Platforms WeChat Index Comparison</title>
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
            margin-bottom: 20px;
        }
        .title {
            text-align: center;
            color: #333;
            margin-bottom: 20px;
            text-shadow: 2px 2px 4px rgba(0,0,0,0.1);
        }
        .stats-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
            gap: 20px;
            margin: 20px 0;
        }
        .stat-card {
            padding: 20px;
            border-radius: 12px;
            text-align: center;
            color: white;
            font-weight: bold;
            box-shadow: 0 4px 15px rgba(0,0,0,0.2);
            transition: transform 0.3s ease;
        }
        .stat-card:hover {
            transform: translateY(-5px);
        }
        .stat-card h3 {
            margin: 0 0 15px 0;
            font-size: 1.2em;
        }
        .stat-card .value {
            font-size: 2em;
            margin: 10px 0;
        }
        .chart-container {
            position: relative;
            height: 600px;
            margin: 30px 0;
            background: white;
            border-radius: 10px;
            padding: 20px;
            box-shadow: 0 4px 15px rgba(0,0,0,0.1);
        }
        .insights {
            background: linear-gradient(135deg, #ff9a9e 0%, #fecfef 100%);
            padding: 20px;
            border-radius: 10px;
            margin: 20px 0;
        }
        .insights h3 {
            color: #333;
            margin-top: 0;
        }
        .insights ul {
            color: #555;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1 class="title">5大平台微信指数对比分析<br>Five Platforms WeChat Index Analysis</h1>
        <h2 class="title">京东 vs 美团 vs 美团外卖 vs 饿了么 vs 京东外卖</h2>
        <p style="text-align: center; color: #666; font-size: 1.1em;">数据时间范围: 2024年8月22日 - 2025年8月21日</p>
        
        <div class="chart-container">
            <canvas id="trendChart"></canvas>
        </div>
        
        <div class="stats-grid">
"""
    
    # 添加统计卡片
    for platform_name, data in platforms_data.items():
        scores = data['scores']
        avg_score = np.mean(scores)
        max_score = max(scores)
        min_score = min(scores)
        
        html_content += f"""
            <div class="stat-card" style="background: linear-gradient(135deg, {data['color']} 0%, {data['color']}AA 100%);">
                <h3>{platform_name}<br>({data['name_cn']})</h3>
                <div class="value">{avg_score/100000000:.1f}亿</div>
                <p>平均指数</p>
                <p>峰值: {max_score/100000000:.1f}亿</p>
                <p>最低: {min_score/100000000:.1f}亿</p>
            </div>
        """
    
    # 准备Chart.js数据
    datasets = []
    for platform_name, data in platforms_data.items():
        chart_data = []
        for j, date in enumerate(data['dates']):
            chart_data.append({
                'x': date.strftime('%Y-%m-%d'),
                'y': data['scores'][j] / 100000000  # 转换为亿为单位
            })
        
        datasets.append({
            'label': f"{platform_name} ({data['name_cn']})",
            'data': chart_data,
            'borderColor': data['color'],
            'backgroundColor': data['color'] + '20',
            'fill': False,
            'tension': 0.1
        })
    
    html_content += f"""
        </div>
        
        <div class="insights">
            <h3>🔍 关键洞察</h3>
            <ul>
                <li><strong>外卖市场细分</strong>：美团外卖和京东外卖作为专门的外卖业务，展现了与主平台不同的指数特征</li>
                <li><strong>平台生态对比</strong>：主平台（京东、美团）vs 垂直业务（外卖专门平台）的用户关注度差异</li>
                <li><strong>市场竞争格局</strong>：5大平台在不同时期的热度变化反映了电商和外卖市场的竞争态势</li>
                <li><strong>业务独立性</strong>：外卖业务的独立品牌运营效果在微信指数中的体现</li>
            </ul>
        </div>
    </div>
    
    <script>
        const ctx = document.getElementById('trendChart').getContext('2d');
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
                        text: '5大平台微信指数趋势对比 (Five Platforms WeChat Index Trend)',
                        font: {{
                            size: 18,
                            weight: 'bold'
                        }}
                    }},
                    legend: {{
                        display: true,
                        position: 'top',
                        labels: {{
                            boxWidth: 12,
                            font: {{
                                size: 11
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
                            }}
                        }},
                        title: {{
                            display: true,
                            text: '日期 (Date)',
                            font: {{
                                weight: 'bold'
                            }}
                        }}
                    }},
                    y: {{
                        title: {{
                            display: true,
                            text: '微信指数 (亿) WeChat Index (100M)',
                            font: {{
                                weight: 'bold'
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
    print("正在解析5个平台的微信指数数据...")
    
    # 解析数据
    platforms_data = parse_five_platforms_data()
    print(f"成功提取 {len(platforms_data)} 个平台的数据")
    
    # 创建静态图表
    print("生成综合可视化图表...")
    fig = create_comprehensive_visualization(platforms_data)
    
    # 保存静态图表
    output_file = 'E:\\claude-code\\微信指数\\five_platforms_comprehensive_chart.png'
    fig.savefig(output_file, dpi=300, bbox_inches='tight', 
                facecolor='white', edgecolor='none')
    print(f"综合图表已保存至: {output_file}")
    
    # 创建HTML交互式图表
    print("生成交互式HTML图表...")
    html_content = create_html_visualization(platforms_data)
    
    # 保存HTML图表
    html_file = 'E:\\claude-code\\微信指数\\five_platforms_interactive_chart.html'
    with open(html_file, 'w', encoding='utf-8') as f:
        f.write(html_content)
    print(f"交互式图表已保存至: {html_file}")
    
    # 输出数据统计摘要
    print("\\n=== 5大平台数据统计摘要 ===")
    for platform_name, data in platforms_data.items():
        scores = data['scores']
        print(f"\\n{platform_name} ({data['name_cn']}):")
        print(f"  数据点数: {len(scores)}")
        print(f"  平均指数: {np.mean(scores):,.0f}")
        print(f"  最高指数: {max(scores):,.0f}")
        print(f"  最低指数: {min(scores):,.0f}")
        print(f"  标准差: {np.std(scores):,.0f}")
        print(f"  变异系数: {np.std(scores)/np.mean(scores):.2f}")

if __name__ == "__main__":
    main()