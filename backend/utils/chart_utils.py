# -*- coding: utf-8 -*-
"""
图表工具函数模块
提供图表通用功能和样式配置
"""

import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import matplotlib.font_manager as fm
from datetime import datetime
from typing import List, Dict, Any, Optional
import os

from config.settings import CHART_CONFIG, OUTPUT_CONFIG


def setup_matplotlib():
    """
    配置matplotlib的基本设置
    """
    # 使用非交互式后端避免GUI依赖
    plt.switch_backend('Agg')
    
    # 设置中文字体
    plt.rcParams['font.sans-serif'] = [CHART_CONFIG['font_family']]
    plt.rcParams['axes.unicode_minus'] = False
    
    # 设置默认字体大小
    plt.rcParams['font.size'] = CHART_CONFIG['tick_labelsize']


def create_figure(title: str = "") -> tuple:
    """
    创建标准化的图表对象
    
    Args:
        title: 图表标题
        
    Returns:
        tuple: (fig, ax) matplotlib图表对象
    """
    fig, ax = plt.subplots(
        figsize=CHART_CONFIG['figsize'],
        dpi=CHART_CONFIG['dpi']
    )
    
    if title:
        ax.set_title(title, fontsize=CHART_CONFIG['title_fontsize'], fontweight='bold')
    
    return fig, ax


def format_date_axis(ax, dates: List[datetime]):
    """
    格式化日期轴显示
    
    Args:
        ax: matplotlib轴对象
        dates: 日期列表
    """
    # 设置日期格式
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%m-%d'))
    ax.xaxis.set_major_locator(mdates.DayLocator(interval=2))
    
    # 旋转日期标签避免重叠
    plt.setp(ax.xaxis.get_majorticklabels(), rotation=45, ha='right')
    
    # 设置x轴范围
    if dates:
        ax.set_xlim(min(dates), max(dates))


def apply_chart_styling(ax, show_grid: bool = True):
    """
    应用标准化的图表样式
    
    Args:
        ax: matplotlib轴对象
        show_grid: 是否显示网格
    """
    if show_grid:
        ax.grid(True, alpha=CHART_CONFIG['grid_alpha'], linestyle='--')
    
    # 设置轴标签字体大小
    ax.tick_params(labelsize=CHART_CONFIG['tick_labelsize'])
    
    # 设置坐标轴标签
    ax.set_xlabel('日期', fontsize=CHART_CONFIG['axis_labelsize'])
    ax.set_ylabel('微信指数', fontsize=CHART_CONFIG['axis_labelsize'])


def add_legend(ax, loc: str = 'upper left'):
    """
    添加标准化的图例
    
    Args:
        ax: matplotlib轴对象
        loc: 图例位置
    """
    ax.legend(
        loc=loc,
        fontsize=CHART_CONFIG['legend_fontsize'],
        frameon=True,
        fancybox=True,
        shadow=True,
        framealpha=0.9
    )


def save_chart(fig, filename: str, tight_layout: bool = True) -> str:
    """
    保存图表到文件
    
    Args:
        fig: matplotlib图表对象
        filename: 文件名（不含路径和扩展名）
        tight_layout: 是否使用紧密布局
        
    Returns:
        str: 保存的文件完整路径
    """
    if tight_layout:
        fig.tight_layout()
    
    # 确保输出目录存在
    output_dir = OUTPUT_CONFIG['output_dir']
    os.makedirs(output_dir, exist_ok=True)
    
    # 构建完整文件路径
    file_path = os.path.join(
        output_dir,
        f"{filename}.{OUTPUT_CONFIG['image_format']}"
    )
    
    # 保存文件
    fig.savefig(
        file_path,
        format=OUTPUT_CONFIG['image_format'],
        dpi=CHART_CONFIG['dpi'],
        bbox_inches='tight',
        facecolor='white',
        edgecolor='none'
    )
    
    return file_path


def plot_platform_line(ax, dates: List[datetime], values: List[int], 
                      label: str, color: str, show_markers: bool = True):
    """
    绘制单个平台的数据线条
    
    Args:
        ax: matplotlib轴对象
        dates: 日期列表
        values: 数值列表
        label: 线条标签
        color: 线条颜色
        show_markers: 是否显示数据点标记
    """
    line_style = {
        'linewidth': CHART_CONFIG['line_width'],
        'color': color,
        'label': label,
        'alpha': 0.8
    }
    
    if show_markers:
        line_style.update({
            'marker': 'o',
            'markersize': CHART_CONFIG['marker_size'],
            'markerfacecolor': color,
            'markeredgecolor': 'white',
            'markeredgewidth': 1
        })
    
    ax.plot(dates, values, **line_style)


def close_figure(fig):
    """
    安全关闭图表对象释放内存
    
    Args:
        fig: matplotlib图表对象
    """
    plt.close(fig)