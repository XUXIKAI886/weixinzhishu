'use client';

import { useMemo } from 'react';
import { PlatformData } from '@/data/dataParser';

/**
 * 图表数据点接口
 */
export interface ChartDataPoint {
  date: string;
  dateObj: Date;
  [key: string]: string | number | Date;
}

/**
 * 图表数据处理自定义Hook
 * 负责数据转换、筛选和计算
 */
export function useChartData(platforms: PlatformData[], timeRange: string, selectedPlatforms: string[]) {
  
  // 准备完整的图表数据
  const fullChartData: ChartDataPoint[] = useMemo(() => {
    if (platforms.length === 0) return [];
    
    const dateSet = new Set<string>();
    platforms.forEach(platform => {
      platform.data.forEach(item => dateSet.add(item.time));
    });
    
    const sortedDates = Array.from(dateSet).sort();
    
    return sortedDates.map(date => {
      const dataPoint: ChartDataPoint = { 
        date,
        dateObj: new Date(date)
      };
      
      platforms.forEach(platform => {
        const dayData = platform.data.find(item => item.time === date);
        dataPoint[platform.name] = dayData ? dayData.score : 0;
      });
      
      return dataPoint;
    });
  }, [platforms]);

  // 根据时间范围筛选数据
  const filteredChartData = useMemo(() => {
    if (timeRange === 'all') return fullChartData;
    
    const now = new Date();
    let startDate: Date;
    
    switch (timeRange) {
      case '1month':
        startDate = new Date(now.getTime() - 30 * 24 * 60 * 60 * 1000);
        break;
      case '3month':
        startDate = new Date(now.getTime() - 90 * 24 * 60 * 60 * 1000);
        break;
      case '6month':
        startDate = new Date(now.getTime() - 180 * 24 * 60 * 60 * 1000);
        break;
      default:
        return fullChartData;
    }
    
    return fullChartData.filter(item => item.dateObj >= startDate);
  }, [fullChartData, timeRange]);

  // 计算Y轴的范围
  const yAxisDomain = useMemo(() => {
    const allValues = filteredChartData.flatMap(item => 
      platforms
        .filter(platform => selectedPlatforms.includes(platform.name))
        .map(platform => item[platform.name] as number || 0)
    );
    
    if (allValues.length === 0) return [0, 100] as [number, number];
    
    const minValue = Math.min(...allValues);
    const maxValue = Math.max(...allValues);
    const padding = (maxValue - minValue) * 0.1;
    
    return [minValue - padding, maxValue + padding] as [number, number];
  }, [filteredChartData, platforms, selectedPlatforms]);

  return {
    fullChartData,
    filteredChartData,
    yAxisDomain
  };
}