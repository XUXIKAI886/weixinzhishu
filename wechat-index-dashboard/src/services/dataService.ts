'use client';

import { parseWeChatIndexData, ParsedData } from '@/data/dataParser';

/**
 * 数据服务层
 * 负责数据的加载、处理和缓存
 */
export class DataService {
  
  /**
   * 从文件加载数据
   */
  static async loadFromFile(file: File): Promise<ParsedData> {
    try {
      const content = await file.text();
      return parseWeChatIndexData(content);
    } catch (error) {
      throw new Error(`文件解析失败: ${error instanceof Error ? error.message : '未知错误'}`);
    }
  }

  /**
   * 加载示例数据
   */
  static async loadSampleData(): Promise<ParsedData> {
    try {
      // 首先尝试从API获取数据
      const response = await fetch('/api/sample-data');
      if (response.ok) {
        const content = await response.text();
        return parseWeChatIndexData(content);
      }
      
      // 如果API不可用，使用内嵌示例数据
      const { rawDataContent } = await import('@/data/sampleData');
      return parseWeChatIndexData(rawDataContent);
    } catch (error) {
      throw new Error(`示例数据加载失败: ${error instanceof Error ? error.message : '未知错误'}`);
    }
  }

  /**
   * 验证数据格式
   */
  static validateDataFormat(content: string): boolean {
    try {
      // 检查是否包含预期的JSON结构
      const jsonStart = content.indexOf('{"code":0,"content":');
      if (jsonStart === -1) {
        return false;
      }
      
      const jsonData = content.substring(jsonStart).trim();
      const data = JSON.parse(jsonData);
      
      // 验证必需的字段
      return !!(data.content && data.content.resp_list);
    } catch {
      return false;
    }
  }

  /**
   * 获取数据摘要信息
   */
  static getDataSummary(data: ParsedData) {
    const totalDataPoints = data.platforms.reduce((total, platform) => total + platform.data.length, 0);
    const dateRange = data.dateRange;
    
    return {
      platformCount: data.platforms.length,
      totalDataPoints,
      dateRange,
      avgScoreOverall: Math.round(
        data.platforms.reduce((sum, platform) => sum + platform.avgScore, 0) / data.platforms.length
      )
    };
  }
}