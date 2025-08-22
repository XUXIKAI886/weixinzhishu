# -*- coding: utf-8 -*-
"""
交互式图表生成主脚本
替换原interactive_visualization.py，使用新的模块化架构
"""

import sys
import os
import json

# 添加项目根目录到Python路径
backend_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, backend_dir)

from visualization.interactive_chart import create_interactive_chart, generate_platform_comparison


def generate_comparison_charts():
    """
    生成多种对比图表
    """
    print("生成平台对比图表...")
    
    # 外卖平台对比
    delivery_comparison = generate_platform_comparison(
        platforms=['美团外卖', '饿了么', '京东外卖'],
        filename="delivery_platforms_comparison",
        platform_type='delivery_platforms'
    )
    print(f"外卖平台对比图表: {delivery_comparison}")
    
    # 美团系对比
    meituan_comparison = generate_platform_comparison(
        platforms=['美团', '美团外卖'],
        filename="meituan_platforms_comparison",
        platform_type='five_platforms'
    )
    print(f"美团系对比图表: {meituan_comparison}")


def generate_trend_analysis():
    """
    生成趋势分析图表
    """
    print("生成趋势分析图表...")
    
    # 创建交互式图表实例
    chart = create_interactive_chart('five_platforms')
    
    try:
        # 生成趋势分析
        trend_path = chart.generate_trend_analysis("platforms_trend_analysis")
        print(f"趋势分析图表: {trend_path}")
        
        # 生成数据摘要报告
        report = chart.create_summary_report()
        
        # 保存报告到JSON文件
        report_path = os.path.join(os.path.dirname(__file__), 'output', 'data_summary_report.json')
        os.makedirs(os.path.dirname(report_path), exist_ok=True)
        
        with open(report_path, 'w', encoding='utf-8') as f:
            json.dump(report, f, ensure_ascii=False, indent=2, default=str)
        
        print(f"数据摘要报告: {report_path}")
        
        # 打印关键统计信息
        print("\n=== 平台排名统计 ===")
        print("按平均指数排名:")
        for i, (platform, stats) in enumerate(report['rankings']['by_average'], 1):
            print(f"{i}. {platform}: 平均指数 {stats['mean']:.0f}")
        
    finally:
        chart.close()


def main():
    """
    主函数：生成交互式图表和分析报告
    """
    try:
        print("开始生成交互式图表分析...")
        
        # 生成对比图表
        generate_comparison_charts()
        
        print()
        
        # 生成趋势分析
        generate_trend_analysis()
        
        print("\n所有交互式图表生成完成！")
            
    except Exception as e:
        print(f"生成图表时发生错误: {str(e)}")
        import traceback
        traceback.print_exc()
        return 1
    
    return 0


if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)