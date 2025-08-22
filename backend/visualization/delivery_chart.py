# -*- coding: utf-8 -*-
"""
外卖平台图表模块
专门用于生成三个外卖平台（美团外卖、饿了么、京东外卖）的可视化图表
"""

from typing import Optional
from utils.chart_utils import plot_platform_line
from visualization.base_chart import BaseChart


class DeliveryPlatformChart(BaseChart):
    """
    外卖平台图表类
    用于生成美团外卖、饿了么、京东外卖的指数趋势图
    """
    
    def __init__(self):
        """
        初始化外卖平台图表
        """
        super().__init__(platform_type='delivery_platforms')
    
    def plot_data(self):
        """
        绘制外卖平台数据线条
        """
        if self.platforms_data is None:
            raise RuntimeError("数据尚未加载，请先调用load_data方法")
        
        if self.ax is None:
            raise RuntimeError("图表尚未创建，请先调用create_chart方法")
        
        # 绘制各平台数据线条
        for platform_name, platform_data in self.platforms_data.items():
            plot_platform_line(
                self.ax,
                platform_data['dates'],
                platform_data['values'],
                platform_name,
                platform_data['color'],
                show_markers=True
            )
    
    def generate_standard_chart(self, filename: str = "delivery_platforms_chart") -> str:
        """
        生成标准的外卖平台对比图表
        
        Args:
            filename: 保存的文件名
            
        Returns:
            str: 保存的文件路径
        """
        title = "外卖平台微信指数对比分析"
        return self.generate(
            title=title,
            filename=filename,
            show_grid=True,
            show_legend=True
        )
    
    def generate_simple_chart(self, filename: str = "simple_delivery_chart") -> str:
        """
        生成简化版外卖平台图表
        
        Args:
            filename: 保存的文件名
            
        Returns:
            str: 保存的文件路径
        """
        title = "外卖平台指数趋势"
        return self.generate(
            title=title,
            filename=filename,
            show_grid=False,
            show_legend=True
        )


class StaticDeliveryChart(DeliveryPlatformChart):
    """
    静态外卖平台图表类
    用于生成静态样式的外卖平台图表
    """
    
    def plot_data(self):
        """
        绘制静态样式的外卖平台数据
        """
        if self.platforms_data is None:
            raise RuntimeError("数据尚未加载，请先调用load_data方法")
        
        if self.ax is None:
            raise RuntimeError("图表尚未创建，请先调用create_chart方法")
        
        # 绘制各平台数据线条，不显示标记点
        for platform_name, platform_data in self.platforms_data.items():
            plot_platform_line(
                self.ax,
                platform_data['dates'],
                platform_data['values'],
                platform_name,
                platform_data['color'],
                show_markers=False  # 静态图表不显示标记点
            )


def create_delivery_chart(chart_type: str = "standard") -> DeliveryPlatformChart:
    """
    工厂函数：创建外卖平台图表实例
    
    Args:
        chart_type: 图表类型 ("standard" 或 "static")
        
    Returns:
        DeliveryPlatformChart: 图表实例
    """
    if chart_type == "static":
        return StaticDeliveryChart()
    else:
        return DeliveryPlatformChart()


# 便捷函数
def generate_delivery_chart(title: str = "", filename: str = "", 
                          chart_type: str = "standard") -> Optional[str]:
    """
    快速生成外卖平台图表的便捷函数
    
    Args:
        title: 图表标题
        filename: 保存文件名
        chart_type: 图表类型
        
    Returns:
        Optional[str]: 保存路径（如果指定了filename）
    """
    chart = create_delivery_chart(chart_type)
    try:
        if not title:
            title = "外卖平台微信指数分析"
        
        return chart.generate(
            title=title,
            filename=filename,
            show_grid=True,
            show_legend=True
        )
    finally:
        chart.close()