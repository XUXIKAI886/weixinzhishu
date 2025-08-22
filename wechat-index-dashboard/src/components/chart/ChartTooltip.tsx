'use client';

import { formatNumber } from '@/data/dataParser';

interface TooltipPayload {
  dataKey: string;
  color: string;
  value: number;
}

interface ChartTooltipProps {
  active?: boolean;
  payload?: TooltipPayload[];
  label?: string;
  selectedPlatforms: string[];
}

/**
 * 自定义图表工具提示组件
 * 显示鼠标悬停时的数据详情
 */
export function ChartTooltip({ active, payload, label, selectedPlatforms }: ChartTooltipProps) {
  if (active && payload && payload.length) {
    return (
      <div className="bg-white p-4 border border-gray-200 rounded-lg shadow-lg min-w-48">
        <p className="font-medium text-gray-900 mb-2">{`日期: ${label}`}</p>
        {payload
          .filter((entry) => selectedPlatforms.includes(entry.dataKey))
          .map((entry, index: number) => (
          <p key={index} style={{ color: entry.color }} className="text-sm flex justify-between">
            <span>{entry.dataKey}:</span>
            <span className="font-medium ml-2">{formatNumber(entry.value)}</span>
          </p>
        ))}
      </div>
    );
  }
  return null;
}