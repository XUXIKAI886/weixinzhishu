'use client';

import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '../ui/card';
import { BarChart3 } from 'lucide-react';
import { PlatformData, formatNumber } from '../../data/dataParser';

interface StatisticsCardsProps {
  platforms: PlatformData[];
  selectedPlatforms: string[];
}

/**
 * 统计卡片组件
 * 展示选中平台的统计信息
 */
export function StatisticsCards({ platforms, selectedPlatforms }: StatisticsCardsProps) {
  const visiblePlatforms = platforms.filter(platform => selectedPlatforms.includes(platform.name));

  return (
    <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
      {visiblePlatforms.map((platform, index) => (
        <Card key={index} className="overflow-hidden">
          <CardHeader className="pb-3">
            <div className="flex items-center justify-between">
              <CardTitle 
                className="text-lg" 
                style={{ color: platform.color }}
              >
                {platform.name}
              </CardTitle>
              <div 
                className="w-4 h-4 rounded-full" 
                style={{ backgroundColor: platform.color }}
              />
            </div>
            <CardDescription>微信指数统计</CardDescription>
          </CardHeader>
          <CardContent className="space-y-3">
            <div className="flex items-center justify-between">
              <span className="text-sm text-gray-600">平均指数</span>
              <span className="font-bold text-lg">{formatNumber(platform.avgScore)}</span>
            </div>
            <div className="flex items-center justify-between">
              <span className="text-sm text-gray-600">最高峰值</span>
              <span className="font-medium text-green-600">{formatNumber(platform.maxScore)}</span>
            </div>
            <div className="flex items-center justify-between">
              <span className="text-sm text-gray-600">最低值</span>
              <span className="font-medium text-red-600">{formatNumber(platform.minScore)}</span>
            </div>
            <div className="pt-2 border-t">
              <div className="flex items-center gap-2 text-sm text-gray-600">
                <BarChart3 className="w-4 h-4" />
                <span>共 {platform.data.length} 个数据点</span>
              </div>
            </div>
          </CardContent>
        </Card>
      ))}
    </div>
  );
}