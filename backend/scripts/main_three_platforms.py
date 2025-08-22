# -*- coding: utf-8 -*-
"""
三平台图表生成主脚本
替换原three_delivery_platforms_chart.py，使用新的模块化架构
"""

import sys
import os

# 添加项目根目录到Python路径
backend_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, backend_dir)

from visualization.delivery_chart import DeliveryPlatformChart


def main():
    """
    主函数：生成三个外卖平台的对比图表
    """
    try:
        print("开始生成三平台外卖图表...")
        
        # 创建外卖平台图表实例
        chart = DeliveryPlatformChart()
        
        try:
            # 生成标准三平台图表
            standard_path = chart.generate_standard_chart("three_delivery_platforms")
            print(f"标准三平台图表: {standard_path}")
            
            # 重新创建实例生成简化版图表
            chart.close()
            chart = DeliveryPlatformChart()
            
            simple_path = chart.generate_simple_chart("three_delivery_simple")
            print(f"简化三平台图表: {simple_path}")
            
            # 获取并打印统计信息
            stats = chart.get_statistics()
            print("\n=== 三平台统计信息 ===")
            for platform, stat in stats.items():
                print(f"{platform}:")
                print(f"  平均指数: {stat['mean']:.0f}")
                print(f"  最大指数: {stat['max']:.0f}")
                print(f"  标准差: {stat['std']:.0f}")
            
        finally:
            chart.close()
            
        print("三平台图表生成完成！")
            
    except Exception as e:
        print(f"生成图表时发生错误: {str(e)}")
        import traceback
        traceback.print_exc()
        return 1
    
    return 0


if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)