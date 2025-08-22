# -*- coding: utf-8 -*-
"""
五平台图表生成主脚本
替换原five_platforms_visualization.py，使用新的模块化架构
"""

import sys
import os

# 添加项目根目录到Python路径
backend_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, backend_dir)

from visualization.five_platforms_chart import generate_five_platforms_chart


def main():
    """
    主函数：生成五平台综合图表
    """
    try:
        print("开始生成五平台综合图表...")
        
        # 生成标准五平台图表
        file_path1 = generate_five_platforms_chart(
            title="五大平台微信指数综合对比分析",
            filename="five_platforms_comprehensive",
            focus_delivery=False
        )
        
        print(f"综合图表生成成功！保存路径: {file_path1}")
        
        # 生成突出外卖平台的图表
        file_path2 = generate_five_platforms_chart(
            title="五大平台指数对比（突出外卖平台）",
            filename="five_platforms_delivery_focus",
            focus_delivery=True
        )
        
        print(f"外卖突出图表生成成功！保存路径: {file_path2}")
            
    except Exception as e:
        print(f"生成图表时发生错误: {str(e)}")
        return 1
    
    return 0


if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)