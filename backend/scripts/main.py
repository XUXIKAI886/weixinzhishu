# -*- coding: utf-8 -*-
"""
微信指数项目主入口脚本
提供统一的命令行接口调用各种图表生成功能
"""

import sys
import os
import argparse

# 添加项目根目录到Python路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))


def run_simple_chart():
    """运行简化图表生成"""
    from main_simple_chart import main as simple_main
    return simple_main()


def run_five_platforms():
    """运行五平台图表生成"""
    from main_five_platforms import main as five_main
    return five_main()


def run_interactive():
    """运行交互式图表生成"""
    from main_interactive import main as interactive_main
    return interactive_main()


def run_chinese_chart():
    """运行中文图表生成"""
    from main_chinese_chart import main as chinese_main
    return chinese_main()


def run_three_platforms():
    """运行三平台图表生成"""
    from main_three_platforms import main as three_main
    return three_main()


def run_all_charts():
    """运行所有图表生成"""
    print("=== 开始生成所有图表 ===\n")
    
    modules = [
        ("简化图表", run_simple_chart),
        ("五平台图表", run_five_platforms),
        ("中文图表", run_chinese_chart),
        ("三平台图表", run_three_platforms),
        ("交互式图表", run_interactive)
    ]
    
    success_count = 0
    total_count = len(modules)
    
    for name, func in modules:
        print(f"--- 生成{name} ---")
        try:
            result = func()
            if result == 0:
                print(f"[成功] {name}生成成功")
                success_count += 1
            else:
                print(f"[失败] {name}生成失败")
        except Exception as e:
            print(f"[异常] {name}生成异常: {str(e)}")
        print()
    
    print(f"=== 生成完成 {success_count}/{total_count} ===")
    return 0 if success_count == total_count else 1


def main():
    """
    主函数：解析命令行参数并调用相应功能
    """
    parser = argparse.ArgumentParser(
        description='微信指数可视化图表生成工具',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例用法:
  python main.py simple        # 生成简化图表
  python main.py five          # 生成五平台图表
  python main.py interactive   # 生成交互式图表
  python main.py chinese       # 生成中文图表
  python main.py three         # 生成三平台图表
  python main.py all           # 生成所有图表
        """
    )
    
    parser.add_argument(
        'mode',
        choices=['simple', 'five', 'interactive', 'chinese', 'three', 'all'],
        help='图表生成模式'
    )
    
    args = parser.parse_args()
    
    # 确保输出目录存在
    output_dir = os.path.join(os.path.dirname(__file__), 'output')
    os.makedirs(output_dir, exist_ok=True)
    
    # 根据模式调用相应功能
    mode_functions = {
        'simple': run_simple_chart,
        'five': run_five_platforms,
        'interactive': run_interactive,
        'chinese': run_chinese_chart,
        'three': run_three_platforms,
        'all': run_all_charts
    }
    
    try:
        return mode_functions[args.mode]()
    except KeyboardInterrupt:
        print("\n用户中断操作")
        return 1
    except Exception as e:
        print(f"执行过程中发生错误: {str(e)}")
        import traceback
        traceback.print_exc()
        return 1


if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)