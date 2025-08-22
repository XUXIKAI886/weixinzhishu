'use client';

import { Card, CardContent, CardDescription, CardHeader, CardTitle } from './ui/card';
import { TrendingUp, Calendar } from 'lucide-react';
import { PlatformData } from '@/data/dataParser';

// 引入重构后的组件和hooks
import { useChartData } from '@/hooks/useChartData';
import { StatisticsCards } from './chart/StatisticsCards';
import { InteractiveLineChart } from './chart/InteractiveLineChart';

interface WeChatIndexChartProps {
  platforms: PlatformData[];
  dateRange: {
    start: string;
    end: string;
  };
}

// interface ChartDataPoint {
//   date: string;
//   [key: string]: string | number;
// }

/**
 * 微信指数图表组件 - 重构版本（简化版）
 * 职责：展示基础的趋势对比图表，无复杂交互功能
 */
export default function WeChatIndexChart({ platforms, dateRange }: WeChatIndexChartProps) {
  
  // 使用所有平台，显示全部数据
  const selectedPlatforms = platforms.map(p => p.name);
  
  // 使用数据处理hook，固定显示所有数据
  const { filteredChartData, yAxisDomain } = useChartData(platforms, 'all', selectedPlatforms);

  // 简单的空函数用于满足组件接口
  const handleBrushChange = () => {};

  return (
    <div className="w-full space-y-6">
      {/* 标题和概览 */}
      <div className="text-center space-y-2">
        <h1 className="text-3xl font-bold bg-gradient-to-r from-blue-600 to-purple-600 bg-clip-text text-transparent">
          外卖平台微信指数趋势分析
        </h1>
        <p className="text-gray-600 flex items-center justify-center gap-2">
          <Calendar className="w-4 h-4" />
          数据范围: {dateRange.start} 至 {dateRange.end}
        </p>
      </div>

      {/* 统计卡片区域 */}
      <StatisticsCards 
        platforms={platforms}
        selectedPlatforms={selectedPlatforms}
      />

      {/* 主图表区域 */}
      <Card className="p-6">
        <CardHeader>
          <CardTitle className="flex items-center gap-2">
            <TrendingUp className="w-5 h-5" />
            趋势对比图表
          </CardTitle>
          <CardDescription>
            显示三大外卖平台的微信指数变化趋势，每月在X轴显示刻度
          </CardDescription>
        </CardHeader>
        <CardContent>
          <div className="h-[600px] w-full">
            <InteractiveLineChart
              data={filteredChartData}
              platforms={platforms}
              selectedPlatforms={selectedPlatforms}
              yAxisDomain={yAxisDomain}
              isFullscreen={false}
              onBrushChange={handleBrushChange}
            />
          </div>
          
          {/* 图表说明 */}
          <div className="mt-4 p-4 bg-blue-50 rounded-lg">
            <h4 className="font-medium text-blue-900 mb-2">📊 数据洞察</h4>
            <ul className="space-y-1 text-sm text-blue-800">
              <li>• <strong>美团外卖</strong>：市场占有率稳定，指数波动相对平缓</li>
              <li>• <strong>饿了么</strong>：与美团竞争激烈，指数趋势相似</li>
              <li>• <strong>京东外卖</strong>：指数波动较大，在特定时期出现显著峰值</li>
              <li>• 三大平台在节假日期间都会出现明显的指数上升</li>
            </ul>
          </div>
        </CardContent>
      </Card>
    </div>
  );
}