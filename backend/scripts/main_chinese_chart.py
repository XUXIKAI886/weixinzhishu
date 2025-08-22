# -*- coding: utf-8 -*-
"""
中文图表生成主脚本
替换原fixed_chinese_chart.py和chinese_delivery_chart.py，使用新的模块化架构
"""

import sys
import os

# 添加项目根目录到Python路径
backend_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, backend_dir)

from visualization.delivery_chart import create_delivery_chart


def main():
    """
    主函数：生成完全中文化的外卖平台图表
    """
    try:
        print("开始生成中文外卖平台图表...")
        
        # 创建标准外卖图表
        chart = create_delivery_chart("standard")
        
        try:
            # 生成标准中文图表
            standard_path = chart.generate_standard_chart("chinese_delivery_standard")
            print(f"标准中文图表生成成功: {standard_path}")
            
        finally:
            chart.close()
        
        # 创建静态样式图表
        static_chart = create_delivery_chart("static")
        
        try:
            # 生成静态中文图表
            static_path = static_chart.generate(
                title="外卖平台微信指数静态分析",
                filename="chinese_delivery_static",
                show_grid=True,
                show_legend=True
            )
            print(f"静态中文图表生成成功: {static_path}")
            
        finally:
            static_chart.close()
            
        print("所有中文图表生成完成！")
            
    except Exception as e:
        print(f"生成图表时发生错误: {str(e)}")
        import traceback
        traceback.print_exc()
        return 1
    
    return 0


if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)