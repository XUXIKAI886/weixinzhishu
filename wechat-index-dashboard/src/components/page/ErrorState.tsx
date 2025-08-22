'use client';

import { Card, CardContent } from '../ui/card';
import { AlertCircle } from 'lucide-react';

interface ErrorStateProps {
  error: string;
  onDismiss?: () => void;
}

/**
 * 错误状态组件
 * 显示错误信息和处理选项
 */
export function ErrorState({ error, onDismiss }: ErrorStateProps) {
  return (
    <Card className="mb-6 border-red-200 bg-red-50">
      <CardContent className="flex items-center gap-3 py-4">
        <AlertCircle className="w-5 h-5 text-red-500" />
        <div className="flex-1">
          <p className="text-red-700 font-medium">数据处理错误</p>
          <p className="text-red-600 text-sm">{error}</p>
        </div>
        {onDismiss && (
          <button
            onClick={onDismiss}
            className="text-red-500 hover:text-red-700 p-1"
            aria-label="关闭错误提示"
          >
            ✕
          </button>
        )}
      </CardContent>
    </Card>
  );
}