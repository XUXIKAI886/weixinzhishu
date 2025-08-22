'use client';

import { useState } from 'react';

/**
 * 图表状态管理自定义Hook
 * 管理时间范围、全屏模式、平台选择、缩放等状态
 */
export function useChartState(initialPlatforms: string[]) {
  // 时间范围状态
  const [timeRange, setTimeRange] = useState<'all' | '3month' | '6month' | '1month'>('all');
  
  // 全屏模式状态
  const [isFullscreen, setIsFullscreen] = useState(false);
  
  // 选中的平台状态
  const [selectedPlatforms, setSelectedPlatforms] = useState<string[]>(initialPlatforms);
  
  // 缩放画刷状态
  const [brushStartIndex, setBrushStartIndex] = useState<number | undefined>(undefined);
  const [brushEndIndex, setBrushEndIndex] = useState<number | undefined>(undefined);

  // 平台选择切换函数
  const togglePlatform = (platformName: string) => {
    setSelectedPlatforms(prev => 
      prev.includes(platformName)
        ? prev.filter(name => name !== platformName)
        : [...prev, platformName]
    );
  };

  // 重置缩放功能
  const resetZoom = () => {
    setBrushStartIndex(undefined);
    setBrushEndIndex(undefined);
    setTimeRange('all');
  };

  // 处理画刷变化
  const handleBrushChange = (brushData: { startIndex?: number; endIndex?: number } | null) => {
    if (brushData) {
      setBrushStartIndex(brushData.startIndex);
      setBrushEndIndex(brushData.endIndex);
    }
  };

  // 切换全屏模式
  const toggleFullscreen = () => {
    setIsFullscreen(!isFullscreen);
  };

  return {
    // 状态
    timeRange,
    isFullscreen,
    selectedPlatforms,
    brushStartIndex,
    brushEndIndex,
    // 操作函数
    setTimeRange,
    togglePlatform,
    resetZoom,
    handleBrushChange,
    toggleFullscreen
  };
}