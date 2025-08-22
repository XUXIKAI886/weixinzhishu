# 📊 输出文件目录

这个目录用于存放生成的图表和数据报告。

## 📁 文件类型

- **PNG文件**: 静态图表文件
- **HTML文件**: 交互式图表
- **JSON文件**: 数据分析报告

## 🚀 如何生成

```bash
# 生成所有图表
python backend/scripts/main.py

# 生成特定图表
python backend/scripts/main_simple_chart.py
python backend/scripts/main_five_platforms.py
python backend/scripts/main_interactive.py
```

## 📋 注意事项

- 此目录中的输出文件会被.gitignore忽略
- 只有此README.md文件会被提交到版本控制
- 所有图表可以通过运行相应的脚本重新生成