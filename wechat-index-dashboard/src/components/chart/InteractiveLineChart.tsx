'use client';

import { 
  LineChart, 
  Line, 
  XAxis, 
  YAxis, 
  CartesianGrid, 
  Tooltip, 
  Legend, 
  ResponsiveContainer,
  ReferenceLine,
  Brush
} from 'recharts';
import { ChartTooltip } from './ChartTooltip';
import { PlatformData, formatNumber } from '@/data/dataParser';
import { ChartDataPoint } from '@/hooks/useChartData';

interface InteractiveLineChartProps {
  data: ChartDataPoint[];
  platforms: PlatformData[];
  selectedPlatforms: string[];
  yAxisDomain: [number, number];
  isFullscreen: boolean;
  brushStartIndex?: number;
  brushEndIndex?: number;
  onBrushChange: (brushData: { startIndex?: number; endIndex?: number } | null) => void;
}

/**
 * 交互式折线图组件
 * 核心的图表渲染逻辑，支持缩放、画刷等交互功能
 */
export function InteractiveLineChart({
  data,
  platforms,
  selectedPlatforms,
  yAxisDomain,
  isFullscreen,
  brushStartIndex,
  brushEndIndex,
  onBrushChange
}: InteractiveLineChartProps) {
  
  return (
    <div className={`w-full ${isFullscreen ? 'h-[calc(100vh-300px)]' : 'h-[700px]'}`}>
      <ResponsiveContainer width="100%" height="100%">
        <LineChart
          data={data}
          margin={{
            top: 20,
            right: 30,
            left: 20,
            bottom: 100
          }}
        >
          <CartesianGrid strokeDasharray="3 3" opacity={0.3} />
          
          {/* X轴配置 */}
          <XAxis 
            dataKey="date"
            tickFormatter={(value) => {
              const date = new Date(value);
              return `${date.getFullYear()}-${String(date.getMonth() + 1).padStart(2, '0')}`;
            }}
            interval="preserveStartEnd"
            angle={-45}
            textAnchor="end"
            height={80}
            tick={{ fontSize: 12 }}
          />
          
          {/* Y轴配置 */}
          <YAxis 
            domain={yAxisDomain}
            tickFormatter={(value) => formatNumber(value)}
            tick={{ fontSize: 12 }}
          />
          
          {/* 工具提示 */}
          <Tooltip 
            content={<ChartTooltip selectedPlatforms={selectedPlatforms} />} 
          />
          
          {/* 图例 */}
          <Legend 
            verticalAlign="top" 
            height={36}
            iconType="line"
          />
          
          {/* 绘制选中平台的折线 */}
          {platforms
            .filter(platform => selectedPlatforms.includes(platform.name))
            .map((platform, index) => (
            <Line
              key={index}
              type="monotone"
              dataKey={platform.name}
              stroke={platform.color}
              strokeWidth={3}
              dot={{ r: 0 }}
              activeDot={{ r: 6, stroke: platform.color, strokeWidth: 2 }}
              connectNulls={false}
            />
          ))}
          
          {/* 重要时间点参考线 */}
          <ReferenceLine 
            x="2025-02-10" 
            stroke="#ff7300" 
            strokeDasharray="4 4" 
            label={{ value: "春节", position: "top" }}
          />

          {/* 缩放画刷 */}
          <Brush 
            dataKey="date"
            height={30}
            stroke="#8884d8"
            onChange={onBrushChange}
            startIndex={brushStartIndex}
            endIndex={brushEndIndex}
            tickFormatter={(value) => {
              const date = new Date(value);
              return `${date.getMonth() + 1}/${date.getDate()}`;
            }}
          />
        </LineChart>
      </ResponsiveContainer>
    </div>
  );
}