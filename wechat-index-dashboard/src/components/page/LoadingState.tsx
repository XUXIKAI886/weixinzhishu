'use client';

import { Card, CardContent } from '../ui/card';
import { Loader2 } from 'lucide-react';

/**
 * 加载状态组件
 * 显示数据加载时的loading状态
 */
export function LoadingState() {
  return (
    <Card className="mb-6">
      <CardContent className="flex items-center justify-center py-8">
        <div className="flex items-center gap-3 text-blue-600">
          <Loader2 className="w-5 h-5 animate-spin" />
          <span>正在解析数据...</span>
        </div>
      </CardContent>
    </Card>
  );
}