# 🌍 全球上市公司市值报告

Global Market Capitalization Report - 专业的上市公司数据分析网站

## 📊 项目特点

- **实时数据**: 从 Yahoo Finance 获取最新市场数据
- **自动更新**: 每 5 分钟自动刷新数据
- **专业报告**: 详细的财务分析、竞争优势、发展趋势
- **响应式设计**: 完美支持桌面和移动设备
- **GitHub Pages**: 一键部署到 GitHub 展示

## 🚀 快速开始

### 1. 安装依赖

```bash
cd global-market-report
pip3 install -r requirements.txt
```

### 2. 运行一次

```bash
python3 scripts/run.py
```

### 3. 查看报告

打开 `output/index.html` 查看排行榜
打开 `output/report_AAPL.html` 查看单个公司报告

### 4. 设置定时更新

```bash
# 添加 cron 任务（每 5 分钟更新）
crontab -e

# 添加以下行
*/5 * * * * /path/to/global-market-report/scripts/update_cron.sh
```

## 📁 项目结构

```
global-market-report/
├── data/               # 数据文件目录
│   ├── latest_market_data.json    # 最新数据
│   └── market_data_*.json         # 历史数据
├── scripts/            # 脚本目录
│   ├── fetch_data.py   # 数据获取
│   ├── generate_html.py # HTML 生成
│   ├── run.py          # 主运行脚本
│   └── update_cron.sh  # Cron 更新脚本
├── output/             # 生成的 HTML 文件
│   ├── index.html      # 首页排行榜
│   └── report_*.html   # 公司报告
├── logs/               # 日志文件
├── templates/          # 模板文件（预留）
├── requirements.txt    # Python 依赖
└── README.md          # 说明文档
```

## 📈 数据指标

### 核心指标
- 市值 (Market Cap)
- 股价 (Current Price)
- 市盈率 (P/E Ratio)
- 市净率 (P/B Ratio)
- 股息率 (Dividend Yield)

### 财务数据
- 总营收 (Total Revenue)
- 毛利润 (Gross Profits)
- 自由现金流 (Free Cash Flow)
- 经营现金流 (Operating Cash Flow)
- 总现金/总债务

### 分析指标
- 营收增长率
- 盈利增长率
- 分析师评级
- 目标价格区间
- Beta 系数

### 公司信息
- 主营业务描述
- 行业发展历史
- 竞争优势分析
- 未来发展趋势

## 🌐 部署到 GitHub Pages

### 方法 1: 手动推送

```bash
# 初始化 git（如果还未初始化）
git init
git add -A
git commit -m "Initial commit"

# 添加远程仓库
git remote add origin https://github.com/yourusername/global-market-report.git

# 创建 gh-pages 分支并推送 output 目录
git subtree push --prefix output origin gh-pages
```

### 方法 2: 使用 GitHub Actions

创建 `.github/workflows/deploy.yml`:

```yaml
name: Deploy to GitHub Pages

on:
  push:
    branches: [ main ]
  schedule:
    - cron: '*/5 * * * *'  # 每 5 分钟

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      
      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.9'
      
      - name: Install dependencies
        run: pip install -r requirements.txt
      
      - name: Generate reports
        run: python scripts/run.py
      
      - name: Deploy to GitHub Pages
        uses: peaceiris/actions-gh-pages@v3
        with:
          github_token: ${{ secrets.GITHUB_TOKEN }}
          publish_dir: ./output
```

## ⚙️ Cron 配置

### 查看当前 cron 任务

```bash
crontab -l
```

### 编辑 cron 任务

```bash
crontab -e
```

### 添加以下行

```bash
# 每 5 分钟更新一次市场报告
*/5 * * * * /absolute/path/to/global-market-report/scripts/update_cron.sh
```

### 查看日志

```bash
# 查看今日日志
tail -f logs/cron_$(date +%Y%m%d).log

# 查看获取日志
tail -f logs/fetch_$(date +%Y%m%d).log
```

## 📝 注意事项

1. **API 限制**: Yahoo Finance 有请求频率限制，如需更频繁更新请考虑付费 API
2. **数据延迟**: 股市数据可能有 15-20 分钟延迟
3. **时区**: 数据基于美股交易时间
4. **免责声明**: 本报告仅供参考，不构成投资建议

## 🛠️ 自定义

### 添加新公司

编辑 `scripts/fetch_data.py` 中的 `GLOBAL_MEGACAPS` 列表：

```python
GLOBAL_MEGACAPS = [
    "AAPL",    # Apple
    "MSFT",    # Microsoft
    # 添加你的公司...
]
```

### 修改更新频率

修改 cron 表达式：
- `*/5 * * * *` - 每 5 分钟
- `*/10 * * * *` - 每 10 分钟
- `0 * * * *` - 每小时
- `0 9 * * *` - 每天早上 9 点

## 📄 许可证

MIT License

## 🙏 致谢

- 数据源：[Yahoo Finance](https://finance.yahoo.com/)
- 图标：Emoji

---

**投资有风险，决策需谨慎** ⚠️
