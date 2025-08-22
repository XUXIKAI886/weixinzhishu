'use client';

import { Button } from '../ui/button';
import { Filter } from 'lucide-react';

interface QuickTimeSelectorProps {
  timeRange: 'all' | '3month' | '6month' | '1month';
  onTimeRangeChange: (range: 'all' | '3month' | '6month' | '1month') => void;
}

/**
 * 快速时间选择器组件
 * 提供预设的时间范围选择按钮
 */
export function QuickTimeSelector({ timeRange, onTimeRangeChange }: QuickTimeSelectorProps) {
  const timeRangeOptions = [
    { key: 'all', label: '全部数据' },
    { key: '6month', label: '近6个月' },
    { key: '3month', label: '近3个月' },
    { key: '1month', label: '近1个月' }
  ] as const;

  return (
    <div className="flex flex-wrap gap-2 mb-4">
      <span className="text-sm font-medium text-gray-700 flex items-center mr-2">
        <Filter className="w-4 h-4 mr-1" />
        时间范围:
      </span>
      {timeRangeOptions.map(({ key, label }) => (
        <Button
          key={key}
          variant={timeRange === key ? 'default' : 'outline'}
          size="sm"
          onClick={() => onTimeRangeChange(key)}
        >
          {label}
        </Button>
      ))}
    </div>
  );
}