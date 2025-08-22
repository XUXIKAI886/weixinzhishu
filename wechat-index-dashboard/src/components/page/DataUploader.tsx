'use client';

import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '../ui/card';
import { Upload, FileText } from 'lucide-react';

interface DataUploaderProps {
  onFileUpload: (event: React.ChangeEvent<HTMLInputElement>) => void;
  onLoadSample: () => void;
  loading: boolean;
}

/**
 * 数据上传器组件
 * 负责文件上传和示例数据加载的UI
 */
export function DataUploader({ onFileUpload, onLoadSample, loading }: DataUploaderProps) {
  return (
    <Card className="mb-6">
      <CardHeader>
        <CardTitle className="flex items-center gap-2">
          <Upload className="w-5 h-5" />
          数据源管理
        </CardTitle>
        <CardDescription>
          上传微信指数数据文件或使用示例数据进行分析
        </CardDescription>
      </CardHeader>
      <CardContent>
        <div className="flex flex-col sm:flex-row gap-4">
          <div className="flex-1">
            <label className="block text-sm font-medium text-gray-700 mb-2">
              上传数据文件 (.txt)
            </label>
            <input
              type="file"
              accept=".txt"
              onChange={onFileUpload}
              className="block w-full text-sm text-gray-500
                file:mr-4 file:py-2 file:px-4
                file:rounded-lg file:border-0
                file:text-sm file:font-medium
                file:bg-blue-50 file:text-blue-700
                hover:file:bg-blue-100
                cursor-pointer"
            />
          </div>
          <div className="flex items-end">
            <button
              onClick={onLoadSample}
              disabled={loading}
              className="px-6 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 
                       disabled:opacity-50 disabled:cursor-not-allowed
                       flex items-center gap-2 transition-colors"
            >
              <FileText className="w-4 h-4" />
              使用示例数据
            </button>
          </div>
        </div>
      </CardContent>
    </Card>
  );
}