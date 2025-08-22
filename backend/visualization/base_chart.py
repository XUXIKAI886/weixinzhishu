# -*- coding: utf-8 -*-
"""
基础图表类
提供所有图表的基础功能和通用接口
"""

from abc import ABC, abstractmethod
from typing import Dict, List, Optional, Any
import matplotlib.pyplot as plt
from datetime import datetime

from utils.chart_utils import (
    setup_matplotlib, create_figure, format_date_axis,
    apply_chart_styling, add_legend, save_chart, close_figure
)
from core.data_parser import parse_platforms_data, calculate_statistics


class BaseChart(ABC):
    """
    基础图表抽象类
    定义所有图表的通用接口和基础功能
    """
    
    def __init__(self, platform_type: str = 'delivery_platforms'):
        """
        初始化图表
        
        Args:
            platform_type: 平台类型
        """
        self.platform_type = platform_type
        self.platforms_data = None
        self.fig = None
        self.ax = None
        
        # 初始化matplotlib设置
        setup_matplotlib()
    
    def load_data(self) -> Dict[str, Dict]:
        """
        加载平台数据
        
        Returns:
            Dict[str, Dict]: 平台数据字典
        """
        if self.platforms_data is None:
            self.platforms_data = parse_platforms_data(self.platform_type)
        return self.platforms_data
    
    def create_chart(self, title: str = "") -> tuple:
        """
        创建图表对象
        
        Args:
            title: 图表标题
            
        Returns:
            tuple: (fig, ax) matplotlib图表对象
        """
        self.fig, self.ax = create_figure(title)
        return self.fig, self.ax
    
    @abstractmethod
    def plot_data(self):
        """
        绘制数据（抽象方法，子类必须实现）
        """
        pass
    
    def format_chart(self, show_grid: bool = True, show_legend: bool = True):
        """
        格式化图表样式
        
        Args:
            show_grid: 是否显示网格
            show_legend: 是否显示图例
        """
        if self.ax is None:
            raise RuntimeError("图表尚未创建，请先调用create_chart方法")
        
        # 获取所有日期用于格式化x轴
        all_dates = []
        for platform_data in self.platforms_data.values():
            all_dates.extend(platform_data['dates'])
        
        if all_dates:
            format_date_axis(self.ax, all_dates)
        
        apply_chart_styling(self.ax, show_grid)
        
        if show_legend:
            add_legend(self.ax)
    
    def save(self, filename: str) -> str:
        """
        保存图表
        
        Args:
            filename: 文件名
            
        Returns:
            str: 保存的文件路径
        """
        if self.fig is None:
            raise RuntimeError("图表尚未创建，请先调用create_chart方法")
        
        file_path = save_chart(self.fig, filename)
        return file_path
    
    def close(self):
        """
        关闭图表释放内存
        """
        if self.fig is not None:
            close_figure(self.fig)
            self.fig = None
            self.ax = None
    
    def generate(self, title: str = "", filename: str = "", 
                show_grid: bool = True, show_legend: bool = True) -> Optional[str]:
        """
        完整的图表生成流程
        
        Args:
            title: 图表标题
            filename: 保存文件名
            show_grid: 是否显示网格
            show_legend: 是否显示图例
            
        Returns:
            Optional[str]: 如果指定filename则返回保存路径，否则返回None
        """
        try:
            # 加载数据
            self.load_data()
            
            # 创建图表
            self.create_chart(title)
            
            # 绘制数据
            self.plot_data()
            
            # 格式化图表
            self.format_chart(show_grid, show_legend)
            
            # 保存图表
            if filename:
                return self.save(filename)
            
            return None
            
        finally:
            # 确保释放资源
            self.close()
    
    def get_statistics(self) -> Dict[str, Dict[str, float]]:
        """
        获取各平台数据的统计信息
        
        Returns:
            Dict[str, Dict[str, float]]: 各平台统计信息
        """
        if self.platforms_data is None:
            self.load_data()
        
        stats = {}
        for platform_name, platform_data in self.platforms_data.items():
            stats[platform_name] = calculate_statistics(platform_data['values'])
        
        return stats