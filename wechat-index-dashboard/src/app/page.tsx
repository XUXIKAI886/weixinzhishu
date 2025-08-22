'use client';

// 引入重构后的组件和hooks
import { useDataLoader } from '@/hooks/useDataLoader';
import EnhancedChart from '@/components/EnhancedChart';
import { DataUploader } from '@/components/page/DataUploader';
import { LoadingState } from '@/components/page/LoadingState';
import { ErrorState } from '@/components/page/ErrorState';
import { EmptyState } from '@/components/page/EmptyState';
import { PageFooter } from '@/components/page/PageFooter';

/**
 * 首页组件 - 重构版本
 * 职责：协调页面布局，管理数据状态，处理用户交互
 */
export default function Home() {
  
  // 使用数据加载Hook管理所有数据相关状态
  const {
    data,
    loading,
    error,
    handleFileUpload,
    loadSampleData,
    clearError
  } = useDataLoader();

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-50 via-blue-50 to-indigo-50">
      <div className="container mx-auto px-4 py-8 max-w-7xl">
        {/* 头部区域 */}
        <div className="mb-8">
          <div className="text-center mb-6">
            <h1 className="text-4xl font-bold bg-gradient-to-r from-blue-600 via-purple-600 to-blue-800 bg-clip-text text-transparent mb-3">
              微信指数数据可视化分析平台 - 增强版
            </h1>
            <p className="text-gray-600 text-lg">
              支持缩放、筛选、全屏的专业交互式数据分析工具
            </p>
          </div>

            {/* 数据上传区域 */}
          <DataUploader
            onFileUpload={handleFileUpload}
            onLoadSample={loadSampleData}
            loading={loading}
          />

          {/* 加载状态 */}
          {loading && <LoadingState />}

          {/* 错误状态 */}
          {error && (
            <ErrorState 
              error={error} 
              onDismiss={clearError}
            />
          )}
        </div>

        {/* 图表展示区域 */}
        {data && !loading && (
          <EnhancedChart 
            platforms={data.platforms} 
            dateRange={data.dateRange} 
          />
        )}

        {/* 空状态 */}
        {!data && !loading && !error && (
          <EmptyState onLoadSample={loadSampleData} />
        )}

        {/* 页脚信息 */}
        <PageFooter />
      </div>
    </div>
  );
}