// 数据解析工具
export interface WeChatIndexData {
  time: string;
  score: number;
}

export interface PlatformData {
  name: string;
  color: string;
  data: WeChatIndexData[];
  avgScore: number;
  maxScore: number;
  minScore: number;
}

export interface ParsedData {
  platforms: PlatformData[];
  dateRange: {
    start: string;
    end: string;
  };
}

/**
 * 解析微信指数原始数据
 */
export function parseWeChatIndexData(rawContent: string): ParsedData {
  // 找到JSON数据的开始位置
  const jsonStart = rawContent.indexOf('{"code":0,"content":');
  if (jsonStart === -1) {
    throw new Error("找不到JSON数据");
  }
  
  // 提取JSON数据
  const jsonData = rawContent.substring(jsonStart).trim();
  
  // 解析JSON数据
  const data = JSON.parse(jsonData);
  const respList = data.content.resp_list;
  
  // 定义要保留的外卖平台（索引2=美团外卖, 3=饿了么, 4=京东外卖）
  const deliveryPlatforms = [
    { index: 2, name: '美团外卖', color: '#FF6600' },
    { index: 3, name: '饿了么', color: '#0078FF' },
    { index: 4, name: '京东外卖', color: '#E53E3E' }
  ];
  
  const platforms: PlatformData[] = [];
  let startDate = '';
  let endDate = '';
  
  for (const platform of deliveryPlatforms) {
    const platformIndex = platform.index;
    const timeIndexes = respList[platformIndex].indexes[0].time_indexes;
    
    const platformData: WeChatIndexData[] = [];
    let totalScore = 0;
    let maxScore = 0;
    let minScore = Infinity;
    
    for (const item of timeIndexes) {
      // 将时间格式从20240822转换为2024-08-22
      const timeStr = item.time.toString();
      const formattedDate = `${timeStr.slice(0, 4)}-${timeStr.slice(4, 6)}-${timeStr.slice(6, 8)}`;
      
      if (!startDate || formattedDate < startDate) {
        startDate = formattedDate;
      }
      if (!endDate || formattedDate > endDate) {
        endDate = formattedDate;
      }
      
      const score = item.score;
      platformData.push({
        time: formattedDate,
        score: score
      });
      
      totalScore += score;
      maxScore = Math.max(maxScore, score);
      minScore = Math.min(minScore, score);
    }
    
    platforms.push({
      name: platform.name,
      color: platform.color,
      data: platformData.sort((a, b) => a.time.localeCompare(b.time)),
      avgScore: Math.round(totalScore / platformData.length),
      maxScore: maxScore,
      minScore: minScore
    });
  }
  
  return {
    platforms,
    dateRange: {
      start: startDate,
      end: endDate
    }
  };
}

/**
 * 格式化数字为万为单位
 */
export function formatNumber(num: number): string {
  if (num >= 10000) {
    return `${Math.round(num / 10000)}万`;
  }
  return num.toString();
}

/**
 * 获取月份标签（用于图表x轴）
 */
export function getMonthlyLabels(data: WeChatIndexData[]): string[] {
  const monthSet = new Set<string>();
  
  for (const item of data) {
    const month = item.time.substring(0, 7); // 获取 YYYY-MM 格式
    monthSet.add(month);
  }
  
  return Array.from(monthSet).sort();
}