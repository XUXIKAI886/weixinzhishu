@echo off
echo 正在安装项目依赖...
echo.

echo 安装核心依赖包...
call npm install recharts lucide-react class-variance-authority clsx tailwind-merge

echo.
echo 依赖安装完成！
echo.
echo 使用以下命令启动开发服务器:
echo npm run dev
echo.
pause