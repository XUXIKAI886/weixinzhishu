# -*- coding: utf-8 -*-
"""
简化图表生成主脚本
替换原simple_chart_fix.py，使用新的模块化架构
"""

import sys
import os

# 添加backend目录到Python路径
backend_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, backend_dir)

from visualization.delivery_chart import generate_delivery_chart


def main():
    """
    主函数：生成外卖平台简化图表
    """
    try:
        print("开始生成外卖平台简化图表...")
        
        # 生成标准外卖平台图表
        file_path = generate_delivery_chart(
            title="外卖平台微信指数趋势分析",
            filename="simple_delivery_chart",
            chart_type="standard"
        )
        
        if file_path:
            print(f"图表生成成功！保存路径: {file_path}")
        else:
            print("图表生成完成，但未保存到文件")
            
    except Exception as e:
        print(f"生成图表时发生错误: {str(e)}")
        return 1
    
    return 0


if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)