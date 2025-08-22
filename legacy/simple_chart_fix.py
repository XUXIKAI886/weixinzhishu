#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
最简化的图表修复版本 - 移除复杂的时间处理
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

def create_simple_html_chart(platforms_data):
    """创建最简化的HTML图表 - 移除复杂的时间处理"""
    
    # 准备标签数组 - 简化为月份索引
    first_platform = list(platforms_data.values())[0]
    labels = []
    monthly_data = {}
    
    # 初始化月度数据
    for platform_name, data in platforms_data.items():
        monthly_data[platform_name] = []
    
    # 按月聚合数据，每月取一个代表性数据点
    current_month = None
    month_scores = {name: [] for name in platforms_data.keys()}
    
    for i, date in enumerate(first_platform['dates']):
        month_key = date.strftime('%Y-%m')
        
        if current_month != month_key:
            # 如果是新月份，保存上个月的平均值
            if current_month is not None:
                labels.append(current_month)
                for platform_name in platforms_data.keys():
                    if month_scores[platform_name]:
                        avg_score = sum(month_scores[platform_name]) / len(month_scores[platform_name])
                        monthly_data[platform_name].append(avg_score)
                    else:
                        monthly_data[platform_name].append(0)
            
            # 重置月份数据
            current_month = month_key
            for name in month_scores:
                month_scores[name] = []
        
        # 添加当前数据到对应月份
        for platform_name, data in platforms_data.items():
            if i < len(data['scores']):
                month_scores[platform_name].append(data['scores'][i])
    
    # 处理最后一个月
    if current_month is not None:
        labels.append(current_month)
        for platform_name in platforms_data.keys():
            if month_scores[platform_name]:
                avg_score = sum(month_scores[platform_name]) / len(month_scores[platform_name])
                monthly_data[platform_name].append(avg_score)
            else:
                monthly_data[platform_name].append(0)

    html_content = f"""
<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>外卖平台微信指数趋势对比</title>
    <style>
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}
        
        body {{
            font-family: 'Microsoft YaHei', '微软雅黑', 'SimHei', Arial, sans-serif;
            margin: 20px;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            color: #333;
        }}
        
        .container {{
            background-color: white;
            padding: 30px;
            border-radius: 15px;
            box-shadow: 0 10px 30px rgba(0,0,0,0.2);
            max-width: 1400px;
            margin: 0 auto;
        }}
        
        .title {{
            text-align: center;
            color: #333;
            margin-bottom: 10px;
            font-weight: bold;
            font-size: 24px;
        }}
        
        .subtitle {{
            text-align: center;
            color: #666;
            font-size: 14px;
            margin-bottom: 30px;
        }}
        
        .chart-container {{
            position: relative;
            height: 500px;
            margin: 30px 0;
            background: #fafafa;
            border-radius: 10px;
            padding: 20px;
            border: 1px solid #ddd;
        }}
        
        .stats {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
            gap: 20px;
            margin: 30px 0;
        }}
        
        .stat-card {{
            padding: 25px;
            border-radius: 12px;
            text-align: center;
            color: white;
            font-weight: bold;
            box-shadow: 0 4px 15px rgba(0,0,0,0.2);
            transition: transform 0.3s ease;
        }}
        
        .stat-card:hover {{
            transform: translateY(-5px);
        }}
        
        .stat-card h3 {{
            margin: 0 0 15px 0;
            font-size: 20px;
        }}
        
        .stat-card .value {{
            font-size: 32px;
            margin: 15px 0;
            text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
        }}
        
        .stat-card p {{
            margin: 8px 0;
            font-size: 14px;
        }}
        
        .loading {{
            text-align: center;
            color: #666;
            font-size: 16px;
            padding: 50px;
        }}
        
        canvas {{
            max-width: 100%;
            height: auto;
        }}
    </style>
</head>
<body>
    <div class="container">
        <h1 class="title">外卖平台微信指数趋势对比</h1>
        <p class="subtitle">数据时间范围：2024年8月 - 2025年8月 (月度平均值)</p>
        
        <div class="chart-container">
            <div class="loading" id="loading">正在加载图表...</div>
            <canvas id="lineChart" style="display: none;"></canvas>
        </div>
        
        <div class="stats">"""
    
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
                <p>数据点：{len(monthly_data[platform_name_cn])}个月</p>
            </div>
        """
    
    html_content += f"""
        </div>
    </div>
    
    <!-- Chart.js 3.9.1 稳定版本 -->
    <script src="https://cdn.jsdelivr.net/npm/chart.js@3.9.1/dist/chart.min.js"></script>
    
    <script>
        console.log('开始初始化图表...');
        
        // 等待页面完全加载
        document.addEventListener('DOMContentLoaded', function() {{
            console.log('DOM已加载，开始创建图表');
            
            // 图表数据
            const labels = {json.dumps(labels)};
            const datasets = [
                {{
                    label: '美团外卖',
                    data: {json.dumps(monthly_data['美团外卖'])},
                    borderColor: '#FF6600',
                    backgroundColor: 'rgba(255, 102, 0, 0.1)',
                    fill: false,
                    tension: 0.1,
                    borderWidth: 3,
                    pointRadius: 4,
                    pointHoverRadius: 8
                }},
                {{
                    label: '饿了么',
                    data: {json.dumps(monthly_data['饿了么'])},
                    borderColor: '#0078FF',
                    backgroundColor: 'rgba(0, 120, 255, 0.1)',
                    fill: false,
                    tension: 0.1,
                    borderWidth: 3,
                    pointRadius: 4,
                    pointHoverRadius: 8
                }},
                {{
                    label: '京东外卖',
                    data: {json.dumps(monthly_data['京东外卖'])},
                    borderColor: '#AA2116',
                    backgroundColor: 'rgba(170, 33, 22, 0.1)',
                    fill: false,
                    tension: 0.1,
                    borderWidth: 3,
                    pointRadius: 4,
                    pointHoverRadius: 8
                }}
            ];
            
            console.log('数据准备完成:', {{labels: labels.length, datasets: datasets.length}});
            
            // 获取图表元素
            const ctx = document.getElementById('lineChart');
            const loading = document.getElementById('loading');
            
            if (!ctx) {{
                console.error('找不到画布元素');
                loading.innerHTML = '错误：找不到图表容器';
                return;
            }}
            
            try {{
                console.log('开始创建Chart.js实例...');
                
                // 创建图表
                const chart = new Chart(ctx, {{
                    type: 'line',
                    data: {{
                        labels: labels,
                        datasets: datasets
                    }},
                    options: {{
                        responsive: true,
                        maintainAspectRatio: false,
                        plugins: {{
                            title: {{
                                display: true,
                                text: '外卖平台微信指数月度趋势对比',
                                font: {{
                                    size: 18,
                                    weight: 'bold'
                                }},
                                padding: 20
                            }},
                            legend: {{
                                display: true,
                                position: 'top',
                                labels: {{
                                    boxWidth: 15,
                                    font: {{
                                        size: 14
                                    }},
                                    padding: 20
                                }}
                            }},
                            tooltip: {{
                                callbacks: {{
                                    label: function(context) {{
                                        return context.dataset.label + '：' + (context.parsed.y / 10000).toFixed(0) + '万';
                                    }}
                                }}
                            }}
                        }},
                        scales: {{
                            x: {{
                                title: {{
                                    display: true,
                                    text: '月份',
                                    font: {{
                                        weight: 'bold',
                                        size: 14
                                    }}
                                }}
                            }},
                            y: {{
                                title: {{
                                    display: true,
                                    text: '微信指数',
                                    font: {{
                                        weight: 'bold',
                                        size: 14
                                    }}
                                }},
                                ticks: {{
                                    callback: function(value) {{
                                        return (value / 10000).toFixed(0) + '万';
                                    }}
                                }}
                            }}
                        }},
                        interaction: {{
                            intersect: false,
                            mode: 'index'
                        }}
                    }}
                }});
                
                console.log('图表创建成功！', chart);
                
                // 隐藏加载提示，显示图表
                loading.style.display = 'none';
                ctx.style.display = 'block';
                
            }} catch (error) {{
                console.error('创建图表时出错:', error);
                loading.innerHTML = '图表加载失败：' + error.message;
                loading.style.color = 'red';
            }}
        }});
        
        // 备用检查
        window.addEventListener('load', function() {{
            console.log('页面完全加载完成');
            setTimeout(function() {{
                const canvas = document.getElementById('lineChart');
                const loading = document.getElementById('loading');
                if (canvas && canvas.style.display === 'none' && loading && loading.style.display !== 'none') {{
                    console.log('图表仍未显示，显示错误信息');
                    loading.innerHTML = '图表加载超时，请刷新页面重试';
                    loading.style.color = 'orange';
                }}
            }}, 5000);
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
    
    # 创建简化版HTML图表
    print("生成简化版HTML图表...")
    html_content = create_simple_html_chart(platforms_data)
    
    # 保存HTML图表
    html_file = 'E:\\claude-code\\微信指数\\simple_delivery_chart.html'
    with open(html_file, 'w', encoding='utf-8') as f:
        f.write(html_content)
    print(f"简化版HTML图表已保存至: {html_file}")
    
    print("\n=== 简化版修复说明 ===")
    print("1. 使用Chart.js 3.9.1稳定版本")
    print("2. 移除复杂的时间适配器依赖")
    print("3. 改为月度聚合数据，减少数据点")
    print("4. 添加详细的调试日志")
    print("5. 简化数据格式，避免解析错误")

if __name__ == "__main__":
    main()