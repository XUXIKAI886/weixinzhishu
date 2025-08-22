'use client';

import { Button } from '../ui/button';
import { BarChart3 } from 'lucide-react';
import { PlatformData } from '../../data/dataParser';

interface PlatformSelectorProps {
  platforms: PlatformData[];
  selectedPlatforms: string[];
  onTogglePlatform: (platformName: string) => void;
}

/**
 * 平台选择器组件
 * 允许用户选择或取消选择特定平台的数据显示
 */
export function PlatformSelector({ platforms, selectedPlatforms, onTogglePlatform }: PlatformSelectorProps) {
  return (
    <div className="flex flex-wrap gap-2 mb-4">
      <span className="text-sm font-medium text-gray-700 flex items-center mr-2">
        <BarChart3 className="w-4 h-4 mr-1" />
        显示平台:
      </span>
      {platforms.map((platform) => (
        <Button
          key={platform.name}
          variant={selectedPlatforms.includes(platform.name) ? 'default' : 'outline'}
          size="sm"
          onClick={() => onTogglePlatform(platform.name)}
          style={{
            backgroundColor: selectedPlatforms.includes(platform.name) ? platform.color : 'transparent',
            borderColor: platform.color,
            color: selectedPlatforms.includes(platform.name) ? 'white' : platform.color
          }}
        >
          {platform.name}
        </Button>
      ))}
    </div>
  );
}