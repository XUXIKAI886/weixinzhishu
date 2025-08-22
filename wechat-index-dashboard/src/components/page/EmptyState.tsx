'use client';

import { Card, CardContent } from '../ui/card';
import { FileText } from 'lucide-react';

interface EmptyStateProps {
  onLoadSample: () => void;
}

/**
 * 空状态组件
 * 当没有数据时显示的欢迎界面
 */
export function EmptyState({ onLoadSample }: EmptyStateProps) {
  return (
    <Card>
      <CardContent className="text-center py-16">
        <FileText className="w-16 h-16 text-gray-400 mx-auto mb-4" />
        <h3 className="text-xl font-medium text-gray-700 mb-2">
          欢迎使用微信指数分析平台
        </h3>
        <p className="text-gray-500 mb-6">
          请上传数据文件或点击&quot;使用示例数据&quot;开始分析
        </p>
        <button
          onClick={onLoadSample}
          className="px-6 py-3 bg-blue-600 text-white rounded-lg hover:bg-blue-700 
                   transition-colors flex items-center gap-2 mx-auto"
        >
          <FileText className="w-4 h-4" />
          加载示例数据
        </button>
      </CardContent>
    </Card>
  );
}