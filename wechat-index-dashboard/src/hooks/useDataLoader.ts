'use client';

import { useState, useEffect } from 'react';
import { ParsedData } from '../data/dataParser';
import { DataService } from '../services/dataService';

/**
 * 数据加载状态管理Hook
 * 管理数据加载、错误处理等状态
 */
export function useDataLoader() {
  const [data, setData] = useState<ParsedData | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  // 处理文件上传
  const handleFileUpload = async (event: React.ChangeEvent<HTMLInputElement>) => {
    const file = event.target.files?.[0];
    if (!file) return;

    setLoading(true);
    setError(null);

    try {
      const parsedData = await DataService.loadFromFile(file);
      setData(parsedData);
    } catch (err) {
      setError(err instanceof Error ? err.message : '文件解析失败');
    } finally {
      setLoading(false);
    }
  };

  // 加载示例数据
  const loadSampleData = async () => {
    setLoading(true);
    setError(null);

    try {
      const parsedData = await DataService.loadSampleData();
      setData(parsedData);
    } catch (err) {
      setError(err instanceof Error ? err.message : '数据加载失败');
    } finally {
      setLoading(false);
    }
  };

  // 组件加载时自动加载示例数据
  useEffect(() => {
    loadSampleData();
  }, []);

  // 清除错误状态
  const clearError = () => {
    setError(null);
  };

  // 重置所有状态
  const resetState = () => {
    setData(null);
    setLoading(false);
    setError(null);
  };

  return {
    data,
    loading,
    error,
    handleFileUpload,
    loadSampleData,
    clearError,
    resetState
  };
}