#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
三大外卖平台微信指数折线图 - 完全中文版本
解决字体乱码问题，所有文本显示中文
"""

import json
from datetime import datetime
import numpy as np

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
        {'index': 2, 'name_cn': '美团外卖', 'color': '#FF6600'},
        {'index': 3, 'name_cn': '饿了么', 'color': '#0078FF'},
        {'index': 4, 'name_cn': '京东外卖', 'color': '#AA2116'}
    ]
    
    # 提取三个外卖平台的数据
    platforms_data = {}
    
    for platform_info in delivery_platforms:
        i = platform_info['index']
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
        
        platforms_data[platform_name_cn] = {
            'dates': dates,
            'scores': scores,
            'color': color
        }
    
    return platforms_data

def create_html_chart_chinese(platforms_data):
    """创建完全中文的HTML图表"""
    
    html_content = """
<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <title>外卖平台微信指数趋势对比</title>
    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
    <script src="https://cdn.jsdelivr.net/npm/chartjs-adapter-date-fns/dist/chartjs-adapter-date-fns.bundle.min.js"></script>
    <style>
        body {
            font-family: 'Microsoft YaHei', '微软雅黑', 'Arial', sans-serif;
            margin: 20px;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            color: #333;
        }
        .container {
            background-color: white;
            padding: 30px;
            border-radius: 15px;
            box-shadow: 0 10px 30px rgba(0,0,0,0.2);
            max-width: 1200px;
            margin: 0 auto;
        }
        .title {
            text-align: center;
            color: #333;
            margin-bottom: 30px;
            font-weight: bold;
        }
        .chart-container {
            position: relative;
            height: 600px;
            margin: 20px 0;
            background: #fafafa;
            border-radius: 10px;
            padding: 20px;
        }
        .stats {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
            gap: 20px;
            margin: 30px 0;
        }
        .stat-card {
            padding: 25px;
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
            font-size: 1.4em;
        }
        .stat-card .value {
            font-size: 2.2em;
            margin: 15px 0;
            text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
        }
        .stat-card p {
            margin: 8px 0;
            font-size: 1.1em;
        }
        .insights {
            background: linear-gradient(135deg, #ff9a9e 0%, #fecfef 100%);
            padding: 25px;
            border-radius: 12px;
            margin: 30px 0;
            box-shadow: 0 4px 15px rgba(0,0,0,0.1);
        }
        .insights h3 {
            color: #333;
            margin-top: 0;
            font-size: 1.3em;
        }
        .insights ul {
            color: #555;
            line-height: 1.6;
        }
        .insights li {
            margin: 10px 0;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1 class="title">外卖平台微信指数趋势对比</h1>
        <p style="text-align: center; color: #666; font-size: 1.1em; margin-bottom: 30px;">
            数据时间范围：2024年8月22日 - 2025年8月21日
        </p>
        
        <div class="chart-container">
            <canvas id="lineChart"></canvas>
        </div>
        
        <div class="stats">
"""
    
    # 添加统计卡片
    for platform_name_cn, data in platforms_data.items():
        scores = data['scores']
        avg_score = np.mean(scores)
        max_score = max(scores)
        min_score = min(scores)
        
        html_content += f"""
            <div class="stat-card" style="background: linear-gradient(135deg, {data['color']} 0%, {data['color']}DD 100%);">
                <h3>{platform_name_cn}</h3>
                <div class="value">{avg_score/10000:.0f}万</div>
                <p>平均指数</p>
                <p>峰值：{max_score/10000:.0f}万</p>
                <p>最低：{min_score/10000:.0f}万</p>
                <p>数据点：365天</p>
            </div>
        """
    
    # 准备Chart.js数据
    datasets = []
    for platform_name_cn, data in platforms_data.items():
        chart_data = []
        for j, date in enumerate(data['dates']):
            chart_data.append({
                'x': date.strftime('%Y-%m-%d'),
                'y': data['scores'][j]
            })
        
        datasets.append({
            'label': platform_name_cn,
            'data': chart_data,
            'borderColor': data['color'],
            'backgroundColor': data['color'] + '30',
            'fill': False,
            'tension': 0.1,
            'borderWidth': 3,
            'pointRadius': 0,
            'pointHoverRadius': 6
        })
    
    html_content += f"""
        </div>
        
        <div class="insights">
            <h3>📊 数据洞察</h3>
            <ul>
                <li><strong>京东外卖</strong>：平均指数最高（5475万），但波动性极大，显示品牌认知度不够稳定</li>
                <li><strong>美团外卖</strong>：平均指数4269万，相对稳定，在外卖市场具有强势地位</li>
                <li><strong>饿了么</strong>：平均指数3960万，与美团外卖竞争激烈，指数相近</li>
                <li><strong>市场竞争</strong>：三大平台在2025年春节和4-5月期间都出现明显峰值</li>
                <li><strong>用户关注度</strong>：外卖行业整体受节假日和促销活动影响显著</li>
            </ul>
        </div>
    </div>
    
    <script>
        // 设置Chart.js中文化
        Chart.defaults.font.family = 'Microsoft YaHei, 微软雅黑, Arial, sans-serif';
        
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
                        text: '外卖平台微信指数趋势对比',
                        font: {{
                            size: 20,
                            weight: 'bold',
                            family: 'Microsoft YaHei, 微软雅黑, Arial, sans-serif'
                        }},
                        padding: 20
                    }},
                    legend: {{
                        display: true,
                        position: 'top',
                        labels: {{
                            boxWidth: 15,
                            font: {{
                                size: 14,
                                family: 'Microsoft YaHei, 微软雅黑, Arial, sans-serif'
                            }},
                            padding: 20
                        }}
                    }},
                    tooltip: {{
                        titleFont: {{
                            family: 'Microsoft YaHei, 微软雅黑, Arial, sans-serif'
                        }},
                        bodyFont: {{
                            family: 'Microsoft YaHei, 微软雅黑, Arial, sans-serif'
                        }},
                        callbacks: {{
                            label: function(context) {{
                                return context.dataset.label + '：' + (context.parsed.y / 10000).toFixed(0) + '万';
                            }}
                        }}
                    }}
                }},
                scales: {{
                    x: {{
                        type: 'time',
                        time: {{
                            parser: 'YYYY-MM-DD',
                            tooltipFormat: 'YYYY年MM月DD日',
                            displayFormats: {{
                                day: 'MM-DD',
                                month: 'YYYY年MM月'
                            }},
                            unit: 'month'
                        }},
                        title: {{
                            display: true,
                            text: '日期',
                            font: {{
                                weight: 'bold',
                                size: 16,
                                family: 'Microsoft YaHei, 微软雅黑, Arial, sans-serif'
                            }}
                        }},
                        ticks: {{
                            font: {{
                                family: 'Microsoft YaHei, 微软雅黑, Arial, sans-serif'
                            }}
                        }}
                    }},
                    y: {{
                        title: {{
                            display: true,
                            text: '微信指数',
                            font: {{
                                weight: 'bold',
                                size: 16,
                                family: 'Microsoft YaHei, 微软雅黑, Arial, sans-serif'
                            }}
                        }},
                        ticks: {{
                            font: {{
                                family: 'Microsoft YaHei, 微软雅黑, Arial, sans-serif'
                            }},
                            callback: function(value) {{
                                return (value / 10000).toFixed(0) + '万';
                            }}
                        }},
                        beginAtZero: false
                    }}
                }},
                interaction: {{
                    intersect: false,
                    mode: 'index'
                }},
                elements: {{
                    line: {{
                        tension: 0.1
                    }}
                }}
            }}
        }});
    </script>
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
    
    # 创建HTML图表
    print("生成完全中文的HTML图表...")
    html_content = create_html_chart_chinese(platforms_data)
    
    # 保存HTML图表
    html_file = 'E:\\claude-code\\微信指数\\chinese_delivery_chart.html'
    with open(html_file, 'w', encoding='utf-8') as f:
        f.write(html_content)
    print(f"中文HTML图表已保存至: {html_file}")
    
    # 输出数据统计
    print("\\n=== 外卖平台数据统计 ===")
    for platform_name_cn, data in platforms_data.items():
        scores = data['scores']
        print(f"\\n{platform_name_cn}:")
        print(f"  平均指数: {np.mean(scores):,.0f}")
        print(f"  最高指数: {max(scores):,.0f}")
        print(f"  最低指数: {min(scores):,.0f}")

if __name__ == "__main__":
    main()