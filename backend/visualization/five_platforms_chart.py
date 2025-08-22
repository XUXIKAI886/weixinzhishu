# -*- coding: utf-8 -*-
"""
五平台图表模块
用于生成包含五个平台（京东、美团、美团外卖、饿了么、京东外卖）的可视化图表
"""

from typing import Optional
from utils.chart_utils import plot_platform_line
from visualization.base_chart import BaseChart


class FivePlatformsChart(BaseChart):
    """
    五平台图表类
    用于生成包含所有五个平台的指数趋势图
    """
    
    def __init__(self):
        """
        初始化五平台图表
        """
        super().__init__(platform_type='five_platforms')
    
    def plot_data(self):
        """
        绘制五个平台的数据线条
        """
        if self.platforms_data is None:
            raise RuntimeError("数据尚未加载，请先调用load_data方法")
        
        if self.ax is None:
            raise RuntimeError("图表尚未创建，请先调用create_chart方法")
        
        # 按特定顺序绘制平台数据以确保视觉效果
        platform_order = ['京东', '美团', '美团外卖', '饿了么', '京东外卖']
        
        for platform_name in platform_order:
            if platform_name in self.platforms_data:
                platform_data = self.platforms_data[platform_name]
                plot_platform_line(
                    self.ax,
                    platform_data['dates'],
                    platform_data['values'],
                    platform_name,
                    platform_data['color'],
                    show_markers=True
                )
    
    def generate_comprehensive_chart(self, filename: str = "five_platforms_comprehensive") -> str:
        """
        生成综合五平台对比图表
        
        Args:
            filename: 保存的文件名
            
        Returns:
            str: 保存的文件路径
        """
        title = "五大平台微信指数综合对比分析"
        return self.generate(
            title=title,
            filename=filename,
            show_grid=True,
            show_legend=True
        )
    
    def plot_delivery_focus(self):
        """
        绘制突出外卖平台的数据
        """
        if self.platforms_data is None:
            raise RuntimeError("数据尚未加载，请先调用load_data方法")
        
        if self.ax is None:
            raise RuntimeError("图表尚未创建，请先调用create_chart方法")
        
        # 定义外卖平台
        delivery_platforms = ['美团外卖', '饿了么', '京东外卖']
        other_platforms = ['京东', '美团']
        
        # 先绘制非外卖平台（淡色显示）
        for platform_name in other_platforms:
            if platform_name in self.platforms_data:
                platform_data = self.platforms_data[platform_name]
                plot_platform_line(
                    self.ax,
                    platform_data['dates'],
                    platform_data['values'],
                    platform_name,
                    platform_data['color'],
                    show_markers=False
                )
                
                # 降低透明度
                lines = self.ax.get_lines()
                if lines:
                    lines[-1].set_alpha(0.3)
        
        # 再绘制外卖平台（高亮显示）
        for platform_name in delivery_platforms:
            if platform_name in self.platforms_data:
                platform_data = self.platforms_data[platform_name]
                plot_platform_line(
                    self.ax,
                    platform_data['dates'],
                    platform_data['values'],
                    platform_name,
                    platform_data['color'],
                    show_markers=True
                )
    
    def generate_delivery_focus_chart(self, filename: str = "five_platforms_delivery_focus") -> str:
        """
        生成突出外卖平台的五平台图表
        
        Args:
            filename: 保存的文件名
            
        Returns:
            str: 保存的文件路径
        """
        try:
            # 加载数据
            self.load_data()
            
            # 创建图表
            title = "五大平台指数对比（突出外卖平台）"
            self.create_chart(title)
            
            # 绘制突出外卖的数据
            self.plot_delivery_focus()
            
            # 格式化图表
            self.format_chart(show_grid=True, show_legend=True)
            
            # 保存图表
            return self.save(filename)
            
        finally:
            # 确保释放资源
            self.close()


def create_five_platforms_chart() -> FivePlatformsChart:
    """
    工厂函数：创建五平台图表实例
    
    Returns:
        FivePlatformsChart: 图表实例
    """
    return FivePlatformsChart()


# 便捷函数
def generate_five_platforms_chart(title: str = "", filename: str = "", 
                                focus_delivery: bool = False) -> Optional[str]:
    """
    快速生成五平台图表的便捷函数
    
    Args:
        title: 图表标题
        filename: 保存文件名
        focus_delivery: 是否突出显示外卖平台
        
    Returns:
        Optional[str]: 保存路径（如果指定了filename）
    """
    chart = create_five_platforms_chart()
    try:
        if not title:
            title = "五大平台微信指数分析" if not focus_delivery else "五大平台指数对比（突出外卖）"
        
        if focus_delivery:
            return chart.generate_delivery_focus_chart(filename or "five_platforms_delivery_focus")
        else:
            return chart.generate(
                title=title,
                filename=filename,
                show_grid=True,
                show_legend=True
            )
    finally:
        chart.close()