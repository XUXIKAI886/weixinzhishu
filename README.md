# 📊 微信指数数据分析与可视化平台

## 🎯 项目概述

微信指数数据分析与可视化平台是一个现代化的数据处理和展示系统，专门用于分析和可视化微信指数数据，支持多平台对比、趋势分析和交互式图表展示。

## 🏗️ 项目架构

```
微信指数/
├── 📁 backend/                     # Python数据处理后端
│   ├── 📁 config/                  # 配置管理
│   ├── 📁 core/                    # 核心数据处理
│   ├── 📁 utils/                   # 工具函数
│   ├── 📁 visualization/           # 可视化模块
│   ├── 📁 scripts/                 # 主执行脚本
│   └── 📁 output/                  # 生成的图表和报告
│
├── 📁 frontend/                    # Next.js Web仪表盘
│   └── wechat-index-dashboard/     # React应用 (需要移动)
│
├── 📁 data/                        # 数据文件
│   ├── 26_Full.txt                 # 主要数据文件
│   └── 3_Full.txt                  # 辅助数据文件
│
├── 📁 legacy/                      # 旧版本代码归档
│   └── ...                        # 重构前的原始文件
│
└── 📁 docs/                        # 项目文档
    ├── PROJECT_STRUCTURE.md       # 项目结构说明
    └── REFACTOR_SUMMARY.md        # 重构总结
```

## 🚀 功能特性

### 后端 (Python)
- ✅ **模块化架构**: 符合现代Python开发规范
- ✅ **多图表类型**: 支持静态图表、交互式图表、对比图表
- ✅ **数据处理**: 智能数据解析和格式化
- ✅ **配置化管理**: 集中式配置，易于维护
- ✅ **错误处理**: 完善的异常处理机制

### 前端 (React + Next.js)
- ✅ **现代化UI**: 基于React和Next.js 15.5
- ✅ **组件化设计**: 可复用的图表组件
- ✅ **自定义Hooks**: 状态管理和业务逻辑分离
- ✅ **TypeScript**: 完整的类型安全支持
- ✅ **响应式设计**: 适配多种屏幕尺寸

## 📋 快速开始

### 环境要求
- **Python**: 3.8+
- **Node.js**: 18+
- **npm**: 9+

### 后端运行

```bash
# 进入后端目录
cd backend

# 安装依赖
pip install matplotlib numpy

# 生成所有图表
python scripts/main.py

# 生成特定图表
python scripts/main_simple_chart.py    # 简化图表
python scripts/main_five_platforms.py  # 五平台对比
python scripts/main_interactive.py     # 交互式图表
```

### 前端运行

```bash
# 进入前端目录 (目前仍在根目录，需要移动到frontend/)
cd wechat-index-dashboard

# 安装依赖
npm install

# 启动开发服务器
npm run dev
```

访问 http://localhost:3000 查看Web仪表盘

## 📊 支持的图表类型

| 图表类型 | 文件名 | 功能描述 |
|---------|--------|----------|
| 🏃 简化图表 | `main_simple_chart.py` | 基础的平台对比图表 |
| 🎯 中文图表 | `main_chinese_chart.py` | 中文字体支持的图表 |
| 📈 三平台对比 | `main_three_platforms.py` | 外卖三大平台数据对比 |
| 🌟 五平台综合 | `main_five_platforms.py` | 五个平台的综合分析 |
| 🎮 交互式图表 | `main_interactive.py` | 支持交互的HTML图表 |

## 🔧 配置说明

### 后端配置 (`backend/config/settings.py`)
- 数据文件路径配置
- 平台信息和颜色配置
- 图表样式配置
- 输出路径配置

### 前端配置
- Next.js配置: `next.config.ts`
- TypeScript配置: `tsconfig.json`
- ESLint配置: `eslint.config.mjs`

## 📈 输出文件

生成的文件保存在 `backend/output/` 目录中：
- **PNG图表**: 静态图表文件
- **HTML报告**: 交互式图表
- **JSON数据**: 数据分析报告

## 🛠️ 开发指南

### 代码质量标准
- **Python文件**: 每个文件 ≤ 200行
- **TypeScript文件**: 每个文件 ≤ 250行
- **中文注释**: 所有函数和类都有中文注释
- **模块化设计**: 单一职责原则

### 添加新功能
1. **后端**: 在对应的visualization模块中添加新的图表类
2. **前端**: 在components/chart目录添加新组件
3. **配置**: 在config/settings.py中添加相关配置

## 🎨 重构成果

本项目已完成全面重构：

### 文件规模优化
- **重构前**: 最大452行，6个文件超标
- **重构后**: 所有文件符合规范，最大230行

### 代码重复消除
- **重构前**: 7处重复的数据解析逻辑
- **重构后**: 统一的数据处理模块

### 架构现代化
- **重构前**: 单体式代码，难以维护
- **重构后**: 模块化架构，职责清晰

## 📞 支持与反馈

- 📁 **项目结构**: 详见 `docs/PROJECT_STRUCTURE.md`
- 📋 **重构总结**: 详见 `docs/REFACTOR_SUMMARY.md`
- 🏛️ **旧版代码**: 已归档至 `legacy/` 目录

## 📄 许可证

本项目采用 MIT 许可证 - 详见 LICENSE 文件

---

⭐ **如果这个项目对你有帮助，请给一个Star！**