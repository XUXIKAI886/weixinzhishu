import type { NextConfig } from "next";

const nextConfig: NextConfig = {
  // 启用静态导出
  output: 'export',
  
  // 关闭图片优化(GitHub Pages不支持)
  images: {
    unoptimized: true,
  },
  
  // 设置基础路径(GitHub Pages子路径)
  basePath: '/weixinzhishu',
  assetPrefix: '/weixinzhishu/',
  
  // 确保尾部斜杠一致性
  trailingSlash: true,
  
  // 禁用服务端功能(静态部署不需要)
  experimental: {
    serverActions: {
      allowedOrigins: [],
    },
  },
};

export default nextConfig;
