'use client';

import { Card, CardContent, CardDescription, CardHeader, CardTitle } from './ui/card';
import { Button } from './ui/button';
import { 
  TrendingUp, 
  Calendar, 
  RotateCcw,
  Maximize2,
  ZoomIn
} from 'lucide-react';
import { PlatformData } from '@/data/dataParser';

// 引入重构后的组件和hooks
import { useChartState } from '@/hooks/useChartState';
import { useChartData } from '@/hooks/useChartData';
import { QuickTimeSelector } from './chart/QuickTimeSelector';
import { PlatformSelector } from './chart/PlatformSelector';
import { StatisticsCards } from './chart/StatisticsCards';
import { InteractiveLineChart } from './chart/InteractiveLineChart';

interface EnhancedChartProps {
  platforms: PlatformData[];
  dateRange: {
    start: string;
    end: string;
  };
}

/**
 * 增强版图表组件 - 重构版本
 * 职责：协调各个子组件，管理整体布局和交互
 */
export default function EnhancedChart({ platforms, dateRange }: EnhancedChartProps) {
  
  // 使用自定义hooks管理状态
  const {
    timeRange,
    isFullscreen,
    selectedPlatforms,
    brushStartIndex,
    brushEndIndex,
    setTimeRange,
    togglePlatform,
    resetZoom,
    handleBrushChange,
    toggleFullscreen
  } = useChartState(platforms.map(p => p.name));

  // 使用自定义hooks处理数据
  const { filteredChartData, yAxisDomain } = useChartData(platforms, timeRange, selectedPlatforms);

  return (
    <div className="w-full space-y-6">
      {/* 标题和概览区域 */}
      <div className="text-center space-y-2">
        <h1 className="text-3xl font-bold bg-gradient-to-r from-blue-600 to-purple-600 bg-clip-text text-transparent">
          外卖平台微信指数趋势分析 - 增强版
        </h1>
        <p className="text-gray-600 flex items-center justify-center gap-2">
          <Calendar className="w-4 h-4" />
          数据范围: {dateRange.start} 至 {dateRange.end} | 
          显示数据: {filteredChartData.length} 天 | 
          选中平台: {selectedPlatforms.length} 个
        </p>
      </div>

      {/* 统计卡片区域 */}
      <StatisticsCards 
        platforms={platforms}
        selectedPlatforms={selectedPlatforms}
      />

      {/* 交互式图表区域 */}
      <Card className={`transition-all duration-300 ${isFullscreen ? 'fixed inset-4 z-50 bg-white' : 'p-6'}`}>
        <CardHeader>
          <div className="flex items-center justify-between">
            <div>
              <CardTitle className="flex items-center gap-2">
                <TrendingUp className="w-5 h-5" />
                交互式趋势图表
              </CardTitle>
              <CardDescription>
                支持缩放、筛选和全屏查看的专业数据可视化
              </CardDescription>
            </div>
            <div className="flex gap-2">
              <Button
                variant="outline"
                size="sm"
                onClick={resetZoom}
                disabled={timeRange === 'all' && !brushStartIndex}
              >
                <RotateCcw className="w-4 h-4 mr-1" />
                重置
              </Button>
              <Button
                variant="outline"
                size="sm"
                onClick={toggleFullscreen}
              >
                <Maximize2 className="w-4 h-4 mr-1" />
                {isFullscreen ? '退出全屏' : '全屏'}
              </Button>
            </div>
          </div>
        </CardHeader>
        
        <CardContent className="space-y-4">
          {/* 控制面板 */}
          <div className="bg-gray-50 p-4 rounded-lg space-y-3">
            <QuickTimeSelector
              timeRange={timeRange}
              onTimeRangeChange={setTimeRange}
            />
            <PlatformSelector
              platforms={platforms}
              selectedPlatforms={selectedPlatforms}
              onTogglePlatform={togglePlatform}
            />
          </div>

          {/* 主图表 */}
          <InteractiveLineChart
            data={filteredChartData}
            platforms={platforms}
            selectedPlatforms={selectedPlatforms}
            yAxisDomain={yAxisDomain}
            isFullscreen={isFullscreen}
            brushStartIndex={brushStartIndex}
            brushEndIndex={brushEndIndex}
            onBrushChange={handleBrushChange}
          />
          
          {/* 使用说明 */}
          <div className="mt-4 p-4 bg-blue-50 rounded-lg">
            <h4 className="font-medium text-blue-900 mb-2 flex items-center gap-2">
              <ZoomIn className="w-4 h-4" />
              交互功能说明
            </h4>
            <ul className="space-y-1 text-sm text-blue-800">
              <li>• <strong>时间筛选</strong>：点击上方时间范围按钮快速筛选</li>
              <li>• <strong>平台切换</strong>：点击平台按钮显示/隐藏对应数据线</li>
              <li>• <strong>缩放功能</strong>：拖拽底部滑块选择查看范围</li>
              <li>• <strong>全屏模式</strong>：点击全屏按钮获得更大的查看空间</li>
              <li>• <strong>重置视图</strong>：点击重置按钮恢复默认显示</li>
            </ul>
          </div>
        </CardContent>
      </Card>
    </div>
  );
}