'use client';

/**
 * 页面底部组件
 * 显示技术栈信息和版权信息
 */
export function PageFooter() {
  return (
    <footer className="mt-16 text-center text-gray-500 text-sm">
      <p>© 2024 微信指数数据分析平台 | 基于现代技术栈构建</p>
      <div className="flex items-center justify-center gap-4 mt-2 text-xs">
        <span>Next.js 15</span>
        <span>•</span>
        <span>TypeScript</span>
        <span>•</span>
        <span>Tailwind CSS</span>
        <span>•</span>
        <span>Recharts</span>
      </div>
    </footer>
  );
}