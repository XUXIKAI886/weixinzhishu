# -*- coding: utf-8 -*-
"""
交互式图表模块
用于生成具有交互功能的图表和数据分析
"""

from typing import Optional, Dict, List, Tuple
import matplotlib.pyplot as plt
from datetime import datetime

from visualization.base_chart import BaseChart
from utils.chart_utils import plot_platform_line
from core.data_parser import get_date_range


class InteractiveChart(BaseChart):
    """
    交互式图表类
    支持动态数据筛选和多种显示模式
    """
    
    def __init__(self, platform_type: str = 'delivery_platforms'):
        """
        初始化交互式图表
        
        Args:
            platform_type: 平台类型
        """
        super().__init__(platform_type)
        self.selected_platforms = None
        self.date_range = None
    
    def set_platform_filter(self, platform_names: List[str]):
        """
        设置要显示的平台筛选
        
        Args:
            platform_names: 要显示的平台名称列表
        """
        self.selected_platforms = platform_names
    
    def set_date_range(self, start_date: datetime, end_date: datetime):
        """
        设置日期范围筛选
        
        Args:
            start_date: 开始日期
            end_date: 结束日期
        """
        self.date_range = (start_date, end_date)
    
    def filter_data_by_date(self, dates: List[datetime], values: List[int]) -> Tuple[List[datetime], List[int]]:
        """
        根据日期范围筛选数据
        
        Args:
            dates: 原始日期列表
            values: 原始数值列表
            
        Returns:
            Tuple[List[datetime], List[int]]: 筛选后的日期和数值
        """
        if self.date_range is None:
            return dates, values
        
        start_date, end_date = self.date_range
        filtered_dates = []
        filtered_values = []
        
        for date, value in zip(dates, values):
            if start_date <= date <= end_date:
                filtered_dates.append(date)
                filtered_values.append(value)
        
        return filtered_dates, filtered_values
    
    def plot_data(self):
        """
        绘制经过筛选的平台数据
        """
        if self.platforms_data is None:
            raise RuntimeError("数据尚未加载，请先调用load_data方法")
        
        if self.ax is None:
            raise RuntimeError("图表尚未创建，请先调用create_chart方法")
        
        # 确定要绘制的平台
        platforms_to_plot = self.selected_platforms or list(self.platforms_data.keys())
        
        # 绘制选定的平台数据
        for platform_name in platforms_to_plot:
            if platform_name in self.platforms_data:
                platform_data = self.platforms_data[platform_name]
                
                # 应用日期筛选
                filtered_dates, filtered_values = self.filter_data_by_date(
                    platform_data['dates'],
                    platform_data['values']
                )
                
                if filtered_dates:  # 确保有数据可绘制
                    plot_platform_line(
                        self.ax,
                        filtered_dates,
                        filtered_values,
                        platform_name,
                        platform_data['color'],
                        show_markers=True
                    )
    
    def generate_comparison_chart(self, platforms: List[str], filename: str = "") -> Optional[str]:
        """
        生成指定平台的对比图表
        
        Args:
            platforms: 要对比的平台列表
            filename: 保存文件名
            
        Returns:
            Optional[str]: 保存路径
        """
        self.set_platform_filter(platforms)
        
        title = f"微信指数对比分析 - {' vs '.join(platforms)}"
        return self.generate(
            title=title,
            filename=filename,
            show_grid=True,
            show_legend=True
        )
    
    def generate_trend_analysis(self, filename: str = "") -> Optional[str]:
        """
        生成趋势分析图表
        
        Args:
            filename: 保存文件名
            
        Returns:
            Optional[str]: 保存路径
        """
        # 加载数据获取统计信息
        self.load_data()
        stats = self.get_statistics()
        
        # 根据平均值排序平台
        sorted_platforms = sorted(stats.items(), key=lambda x: x[1]['mean'], reverse=True)
        platform_names = [name for name, _ in sorted_platforms]
        
        self.set_platform_filter(platform_names)
        
        # 构建标题包含排名信息
        title = "微信指数趋势分析（按平均指数排序）"
        
        return self.generate(
            title=title,
            filename=filename,
            show_grid=True,
            show_legend=True
        )
    
    def create_summary_report(self) -> Dict[str, any]:
        """
        创建数据摘要报告
        
        Returns:
            Dict[str, any]: 包含统计信息的摘要报告
        """
        if self.platforms_data is None:
            self.load_data()
        
        stats = self.get_statistics()
        date_range = get_date_range(self.platforms_data)
        
        # 计算总体统计
        all_values = []
        for platform_data in self.platforms_data.values():
            all_values.extend(platform_data['values'])
        
        report = {
            'overview': {
                'total_platforms': len(self.platforms_data),
                'date_range': {
                    'start': date_range[0].strftime('%Y-%m-%d') if date_range[0] else None,
                    'end': date_range[1].strftime('%Y-%m-%d') if date_range[1] else None
                },
                'total_data_points': len(all_values)
            },
            'platform_statistics': stats,
            'rankings': {
                'by_average': sorted(stats.items(), key=lambda x: x[1]['mean'], reverse=True),
                'by_maximum': sorted(stats.items(), key=lambda x: x[1]['max'], reverse=True),
                'by_volatility': sorted(stats.items(), key=lambda x: x[1]['std'], reverse=True)
            }
        }
        
        return report


def create_interactive_chart(platform_type: str = 'delivery_platforms') -> InteractiveChart:
    """
    工厂函数：创建交互式图表实例
    
    Args:
        platform_type: 平台类型
        
    Returns:
        InteractiveChart: 图表实例
    """
    return InteractiveChart(platform_type)


# 便捷函数
def generate_platform_comparison(platforms: List[str], filename: str = "", 
                               platform_type: str = 'delivery_platforms') -> Optional[str]:
    """
    快速生成平台对比图表的便捷函数
    
    Args:
        platforms: 要对比的平台列表
        filename: 保存文件名
        platform_type: 平台类型
        
    Returns:
        Optional[str]: 保存路径
    """
    chart = create_interactive_chart(platform_type)
    try:
        return chart.generate_comparison_chart(platforms, filename)
    finally:
        chart.close()