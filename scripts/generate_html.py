#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
生成专业的上市公司报告 HTML 网站
"""

import json
from pathlib import Path
from datetime import datetime
from jinja2 import Template

class HTMLGenerator:
    def __init__(self):
        self.data_dir = Path(__file__).parent.parent / "data"
        self.output_dir = Path(__file__).parent.parent / "output"
        self.templates_dir = Path(__file__).parent.parent / "templates"
        self.output_dir.mkdir(parents=True, exist_ok=True)
        
    def format_number(self, num):
        """格式化数字显示"""
        if num is None or num == 0:
            return "N/A"
        if num >= 1e12:
            return f"${num/1e12:.2f}T"
        if num >= 1e9:
            return f"${num/1e9:.2f}B"
        if num >= 1e6:
            return f"${num/1e6:.2f}M"
        return f"${num:.2f}"
    
    def format_percent(self, num):
        """格式化百分比"""
        if num is None:
            return "N/A"
        return f"{num*100:.2f}%"
    
    def get_recommendation_color(self, rec):
        """获取评级颜色"""
        colors = {
            "strong_buy": "#22c55e",
            "buy": "#4ade80",
            "hold": "#fbbf24",
            "sell": "#f87171",
            "strong_sell": "#dc2626"
        }
        return colors.get(rec.lower(), "#9ca3af")
    
    def get_recommendation_text(self, rec):
        """获取评级文本"""
        texts = {
            "strong_buy": "强烈买入",
            "buy": "买入",
            "hold": "持有",
            "sell": "卖出",
            "strong_sell": "强烈卖出"
        }
        return texts.get(rec.lower(), rec)
    
    def generate_index(self, companies):
        """生成首页（公司列表）"""
        html = f'''<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>全球上市公司市值排行榜 - Global Market Report</title>
    <style>
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}
        
        body {{
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            padding: 20px;
        }}
        
        .container {{
            max-width: 1400px;
            margin: 0 auto;
        }}
        
        .header {{
            background: rgba(255,255,255,0.95);
            border-radius: 16px;
            padding: 30px;
            margin-bottom: 30px;
            box-shadow: 0 10px 40px rgba(0,0,0,0.2);
        }}
        
        .header h1 {{
            font-size: 2.5em;
            color: #1a1a2e;
            margin-bottom: 10px;
            background: linear-gradient(135deg, #667eea, #764ba2);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
        }}
        
        .header p {{
            color: #666;
            font-size: 1.1em;
        }}
        
        .update-time {{
            background: linear-gradient(135deg, #667eea, #764ba2);
            color: white;
            padding: 8px 16px;
            border-radius: 20px;
            display: inline-block;
            margin-top: 15px;
            font-size: 0.9em;
        }}
        
        .stats-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 20px;
            margin-bottom: 30px;
        }}
        
        .stat-card {{
            background: rgba(255,255,255,0.95);
            border-radius: 12px;
            padding: 20px;
            box-shadow: 0 4px 20px rgba(0,0,0,0.1);
        }}
        
        .stat-card h3 {{
            color: #666;
            font-size: 0.9em;
            margin-bottom: 8px;
            text-transform: uppercase;
            letter-spacing: 1px;
        }}
        
        .stat-card .value {{
            font-size: 2em;
            font-weight: bold;
            color: #1a1a2e;
        }}
        
        .companies-table {{
            background: rgba(255,255,255,0.95);
            border-radius: 16px;
            overflow: hidden;
            box-shadow: 0 10px 40px rgba(0,0,0,0.2);
        }}
        
        .table-header {{
            background: linear-gradient(135deg, #667eea, #764ba2);
            color: white;
            padding: 20px;
            display: grid;
            grid-template-columns: 60px 1fr 150px 150px 150px 120px 100px;
            gap: 15px;
            font-weight: 600;
            font-size: 0.9em;
            text-transform: uppercase;
            letter-spacing: 1px;
        }}
        
        .company-row {{
            display: grid;
            grid-template-columns: 60px 1fr 150px 150px 150px 120px 100px;
            gap: 15px;
            padding: 20px;
            border-bottom: 1px solid #eee;
            transition: all 0.3s ease;
            cursor: pointer;
        }}
        
        .company-row:hover {{
            background: #f8f9ff;
            transform: translateX(5px);
        }}
        
        .company-row:last-child {{
            border-bottom: none;
        }}
        
        .rank {{
            font-size: 1.5em;
            font-weight: bold;
            color: #667eea;
        }}
        
        .company-info {{
            display: flex;
            flex-direction: column;
            gap: 5px;
        }}
        
        .company-name {{
            font-weight: 600;
            color: #1a1a2e;
            font-size: 1.1em;
        }}
        
        .company-ticker {{
            color: #666;
            font-size: 0.9em;
        }}
        
        .company-sector {{
            color: #888;
            font-size: 0.85em;
        }}
        
        .metric {{
            display: flex;
            flex-direction: column;
            justify-content: center;
        }}
        
        .metric-value {{
            font-weight: 600;
            color: #1a1a2e;
            font-size: 1.1em;
        }}
        
        .metric-label {{
            color: #888;
            font-size: 0.75em;
            text-transform: uppercase;
        }}
        
        .recommendation {{
            display: inline-block;
            padding: 6px 12px;
            border-radius: 20px;
            color: white;
            font-weight: 600;
            font-size: 0.85em;
            text-align: center;
        }}
        
        .view-report {{
            background: linear-gradient(135deg, #667eea, #764ba2);
            color: white;
            border: none;
            padding: 10px 20px;
            border-radius: 8px;
            cursor: pointer;
            font-weight: 600;
            transition: transform 0.2s;
        }}
        
        .view-report:hover {{
            transform: scale(1.05);
        }}
        
        @media (max-width: 768px) {{
            .table-header, .company-row {{
                grid-template-columns: 50px 1fr 120px;
            }}
            .hide-mobile {{
                display: none;
            }}
        }}
        
        .footer {{
            text-align: center;
            color: rgba(255,255,255,0.8);
            margin-top: 40px;
            padding: 20px;
        }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🌍 全球上市公司市值排行榜</h1>
            <p>Global Market Capitalization Report - 实时追踪全球最有价值的上市公司</p>
            <div class="update-time">📊 最后更新：{datetime.now().strftime("%Y-%m-%d %H:%M:%S")}</div>
        </div>
        
        <div class="stats-grid">
            <div class="stat-card">
                <h3>跟踪公司数</h3>
                <div class="value">{len(companies)}</div>
            </div>
            <div class="stat-card">
                <h3>总市值</h3>
                <div class="value">{self.format_number(sum(c.get('marketCap', 0) for c in companies))}</div>
            </div>
            <div class="stat-card">
                <h3>平均市值</h3>
                <div class="value">{self.format_number(sum(c.get('marketCap', 0) for c in companies) / len(companies) if companies else 0)}</div>
            </div>
            <div class="stat-card">
                <h3>数据源</h3>
                <div class="value" style="font-size: 1.2em;">Yahoo Finance</div>
            </div>
        </div>
        
        <div class="companies-table">
            <div class="table-header">
                <div>排名</div>
                <div>公司信息</div>
                <div>市值</div>
                <div>股价</div>
                <div class="hide-mobile">市盈率</div>
                <div class="hide-mobile">分析师评级</div>
                <div>报告</div>
            </div>
'''
        
        for i, company in enumerate(companies, 1):
            rec_color = self.get_recommendation_color(company.get('recommendationKey', 'hold'))
            rec_text = self.get_recommendation_text(company.get('recommendationKey', 'hold'))
            
            html += f'''
            <div class="company-row" onclick="window.location.href='report_{company['ticker']}.html'">
                <div class="rank">#{i}</div>
                <div class="company-info">
                    <div class="company-name">{company.get('name', company['ticker'])}</div>
                    <div class="company-ticker">{company['ticker']}</div>
                    <div class="company-sector">{company.get('sector', 'N/A')} | {company.get('industry', 'N/A')}</div>
                </div>
                <div class="metric">
                    <div class="metric-value">{self.format_number(company.get('marketCap', 0))}</div>
                    <div class="metric-label">市值</div>
                </div>
                <div class="metric">
                    <div class="metric-value">${company.get('currentPrice', 0):.2f}</div>
                    <div class="metric-label">股价</div>
                </div>
                <div class="metric hide-mobile">
                    <div class="metric-value">{company.get('trailingPE', 0) if company.get('trailingPE') else 'N/A'}</div>
                    <div class="metric-label">市盈率</div>
                </div>
                <div class="hide-mobile">
                    <span class="recommendation" style="background: {rec_color}">{rec_text}</span>
                </div>
                <div>
                    <button class="view-report">查看报告 →</button>
                </div>
            </div>
'''
        
        html += '''
        </div>
        
        <div class="footer">
            <p>数据来源：Yahoo Finance | 每 5 分钟更新 | Generated by Global Market Report</p>
            <p style="margin-top: 10px; font-size: 0.9em;">投资有风险，决策需谨慎。本报告仅供参考，不构成投资建议。</p>
        </div>
    </div>
</body>
</html>
'''
        
        return html
    
    def generate_company_report(self, company):
        """生成单个公司详细报告"""
        ticker = company['ticker']
        name = company.get('name', ticker)
        company_info = company.get('company_info', {})
        
        html = f'''<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{name} ({ticker}) - 公司深度报告</title>
    <style>
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}
        
        body {{
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif;
            background: #f5f7fa;
            min-height: 100vh;
            padding: 20px;
        }}
        
        .container {{
            max-width: 1200px;
            margin: 0 auto;
        }}
        
        .back-link {{
            display: inline-block;
            margin-bottom: 20px;
            color: #667eea;
            text-decoration: none;
            font-weight: 600;
        }}
        
        .back-link:hover {{
            text-decoration: underline;
        }}
        
        .header {{
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            border-radius: 16px;
            padding: 40px;
            color: white;
            margin-bottom: 30px;
            box-shadow: 0 10px 40px rgba(102, 126, 234, 0.3);
        }}
        
        .header-top {{
            display: flex;
            justify-content: space-between;
            align-items: flex-start;
            margin-bottom: 20px;
        }}
        
        .ticker-badge {{
            background: rgba(255,255,255,0.2);
            padding: 8px 16px;
            border-radius: 20px;
            font-weight: 600;
            font-size: 1.2em;
        }}
        
        .header h1 {{
            font-size: 2.5em;
            margin-bottom: 10px;
        }}
        
        .header-meta {{
            display: flex;
            gap: 30px;
            flex-wrap: wrap;
            opacity: 0.9;
        }}
        
        .header-meta span {{
            display: flex;
            align-items: center;
            gap: 8px;
        }}
        
        .grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(350px, 1fr));
            gap: 25px;
            margin-bottom: 30px;
        }}
        
        .card {{
            background: white;
            border-radius: 16px;
            padding: 30px;
            box-shadow: 0 4px 20px rgba(0,0,0,0.08);
        }}
        
        .card h2 {{
            color: #1a1a2e;
            font-size: 1.4em;
            margin-bottom: 20px;
            padding-bottom: 15px;
            border-bottom: 2px solid #667eea;
            display: flex;
            align-items: center;
            gap: 10px;
        }}
        
        .metric-grid {{
            display: grid;
            grid-template-columns: repeat(2, 1fr);
            gap: 20px;
        }}
        
        .metric-item {{
            padding: 15px;
            background: #f8f9ff;
            border-radius: 12px;
            border-left: 4px solid #667eea;
        }}
        
        .metric-label {{
            color: #666;
            font-size: 0.85em;
            text-transform: uppercase;
            letter-spacing: 0.5px;
            margin-bottom: 5px;
        }}
        
        .metric-value {{
            font-size: 1.5em;
            font-weight: 700;
            color: #1a1a2e;
        }}
        
        .metric-sub {{
            color: #888;
            font-size: 0.8em;
            margin-top: 5px;
        }}
        
        .description {{
            color: #444;
            line-height: 1.8;
            font-size: 1.05em;
        }}
        
        .milestone-list {{
            list-style: none;
        }}
        
        .milestone-item {{
            display: flex;
            gap: 20px;
            padding: 15px 0;
            border-bottom: 1px solid #eee;
        }}
        
        .milestone-item:last-child {{
            border-bottom: none;
        }}
        
        .milestone-year {{
            background: linear-gradient(135deg, #667eea, #764ba2);
            color: white;
            padding: 8px 16px;
            border-radius: 20px;
            font-weight: 600;
            min-width: 80px;
            text-align: center;
        }}
        
        .milestone-event {{
            display: flex;
            align-items: center;
            color: #333;
            font-size: 1.05em;
        }}
        
        .tag-list {{
            display: flex;
            flex-wrap: wrap;
            gap: 10px;
        }}
        
        .tag {{
            background: linear-gradient(135deg, #667eea, #764ba2);
            color: white;
            padding: 8px 16px;
            border-radius: 20px;
            font-size: 0.9em;
            font-weight: 500;
        }}
        
        .analysis-section {{
            background: white;
            border-radius: 16px;
            padding: 30px;
            margin-bottom: 25px;
            box-shadow: 0 4px 20px rgba(0,0,0,0.08);
        }}
        
        .analysis-section h2 {{
            color: #1a1a2e;
            font-size: 1.4em;
            margin-bottom: 20px;
            padding-bottom: 15px;
            border-bottom: 2px solid #667eea;
        }}
        
        .analysis-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
            gap: 20px;
        }}
        
        .analysis-item {{
            padding: 20px;
            background: linear-gradient(135deg, #f8f9ff 0%, #fff 100%);
            border-radius: 12px;
            border: 1px solid #e8ecff;
        }}
        
        .analysis-item h3 {{
            color: #667eea;
            font-size: 1.1em;
            margin-bottom: 10px;
        }}
        
        .analysis-item p {{
            color: #555;
            line-height: 1.6;
        }}
        
        .rating-box {{
            background: linear-gradient(135deg, #667eea, #764ba2);
            color: white;
            padding: 25px;
            border-radius: 12px;
            text-align: center;
            margin-top: 20px;
        }}
        
        .rating-box .rating {{
            font-size: 2em;
            font-weight: 700;
            margin-bottom: 10px;
        }}
        
        .rating-box .analysts {{
            opacity: 0.9;
        }}
        
        .positive {{
            color: #22c55e;
        }}
        
        .negative {{
            color: #dc2626;
        }}
        
        .neutral {{
            color: #f59e0b;
        }}
        
        @media (max-width: 768px) {{
            .metric-grid {{
                grid-template-columns: 1fr;
            }}
            .header-top {{
                flex-direction: column;
                gap: 15px;
            }}
        }}
        
        .footer {{
            text-align: center;
            color: #666;
            padding: 30px;
            margin-top: 40px;
        }}
        
        .disclaimer {{
            background: #fff3cd;
            border: 1px solid #ffc107;
            border-radius: 8px;
            padding: 15px;
            margin-top: 20px;
            color: #856404;
            font-size: 0.9em;
        }}
    </style>
</head>
<body>
    <div class="container">
        <a href="index.html" class="back-link">← 返回排行榜</a>
        
        <div class="header">
            <div class="header-top">
                <div>
                    <h1>{name}</h1>
                    <p style="opacity: 0.9; font-size: 1.1em;">{company.get('sector', 'N/A')} | {company.get('industry', 'N/A')}</p>
                </div>
                <div class="ticker-badge">{ticker}</div>
            </div>
            <div class="header-meta">
                <span>📊 市值：{self.format_number(company.get('marketCap', 0))}</span>
                <span>💰 股价：${company.get('currentPrice', 0):.2f}</span>
                <span>📈 52 周：${company.get('fiftyTwoWeekLow', 0):.2f} - ${company.get('fiftyTwoWeekHigh', 0):.2f}</span>
                <span>🔄 更新：{datetime.now().strftime("%Y-%m-%d %H:%M")}</span>
            </div>
        </div>
        
        <div class="grid">
            <div class="card">
                <h2>📈 核心指标</h2>
                <div class="metric-grid">
                    <div class="metric-item">
                        <div class="metric-label">市值</div>
                        <div class="metric-value">{self.format_number(company.get('marketCap', 0))}</div>
                    </div>
                    <div class="metric-item">
                        <div class="metric-label">企业价值</div>
                        <div class="metric-value">{self.format_number(company.get('enterpriseValue', 0))}</div>
                    </div>
                    <div class="metric-item">
                        <div class="metric-label">市盈率 (TTM)</div>
                        <div class="metric-value">{company.get('trailingPE', 0) if company.get('trailingPE') else 'N/A'}</div>
                    </div>
                    <div class="metric-item">
                        <div class="metric-label">远期市盈率</div>
                        <div class="metric-value">{company.get('forwardPE', 0) if company.get('forwardPE') else 'N/A'}</div>
                    </div>
                    <div class="metric-item">
                        <div class="metric-label">市净率</div>
                        <div class="metric-value">{company.get('priceToBook', 0) if company.get('priceToBook') else 'N/A'}</div>
                    </div>
                    <div class="metric-item">
                        <div class="metric-label">股息率</div>
                        <div class="metric-value">{self.format_percent(company.get('dividendYield', 0))}</div>
                    </div>
                    <div class="metric-item">
                        <div class="metric-label">利润率</div>
                        <div class="metric-value">{self.format_percent(company.get('profitMargins', 0))}</div>
                    </div>
                    <div class="metric-item">
                        <div class="metric-label">Beta</div>
                        <div class="metric-value">{company.get('beta', 0) if company.get('beta') else 'N/A'}</div>
                    </div>
                </div>
            </div>
            
            <div class="card">
                <h2>💼 主营业务</h2>
                <div class="description">
                    {company_info.get('main_business', company.get('description', '暂无描述'))}
                </div>
                <div style="margin-top: 20px;">
                    <p style="color: #666; margin-bottom: 10px;">官方网站:</p>
                    <a href="{company.get('website', '#')}" target="_blank" style="color: #667eea; font-size: 1.1em;">{company.get('website', 'N/A')}</a>
                </div>
            </div>
        </div>
        
        <div class="analysis-section">
            <h2>🏆 竞争优势</h2>
            <div class="tag-list">
'''
        
        for adv in company_info.get('competitive_advantages', []):
            html += f'                <span class="tag">✓ {adv}</span>\n'
        
        html += '''
            </div>
        </div>
        
        <div class="grid">
            <div class="card">
                <h2>📅 发展里程碑</h2>
                <ul class="milestone-list">
'''
        
        for milestone in company_info.get('key_milestones', []):
            html += f'''
                    <li class="milestone-item">
                        <div class="milestone-year">{milestone['year']}</div>
                        <div class="milestone-event">{milestone['event']}</div>
                    </li>
'''
        
        html += f'''
                </ul>
            </div>
            
            <div class="card">
                <h2>💰 财务数据</h2>
                <div class="metric-grid">
                    <div class="metric-item">
                        <div class="metric-label">总营收</div>
                        <div class="metric-value">{self.format_number(company.get('totalRevenue', 0))}</div>
                    </div>
                    <div class="metric-item">
                        <div class="metric-label">毛利润</div>
                        <div class="metric-value">{self.format_number(company.get('grossProfits', 0))}</div>
                    </div>
                    <div class="metric-item">
                        <div class="metric-label">自由现金流</div>
                        <div class="metric-value">{self.format_number(company.get('freeCashflow', 0))}</div>
                    </div>
                    <div class="metric-item">
                        <div class="metric-label">经营现金流</div>
                        <div class="metric-value">{self.format_number(company.get('operatingCashflow', 0))}</div>
                    </div>
                    <div class="metric-item">
                        <div class="metric-label">总现金</div>
                        <div class="metric-value">{self.format_number(company.get('totalCash', 0))}</div>
                    </div>
                    <div class="metric-item">
                        <div class="metric-label">总债务</div>
                        <div class="metric-value">{self.format_number(company.get('totalDebt', 0))}</div>
                    </div>
                    <div class="metric-item">
                        <div class="metric-label">营收增长率</div>
                        <div class="metric-value {'positive' if company.get('revenueGrowth', 0) > 0 else 'negative'}">{self.format_percent(company.get('revenueGrowth', 0))}</div>
                    </div>
                    <div class="metric-item">
                        <div class="metric-label">盈利增长率</div>
                        <div class="metric-value {'positive' if company.get('earningsGrowth', 0) > 0 else 'negative'}">{self.format_percent(company.get('earningsGrowth', 0))}</div>
                    </div>
                </div>
            </div>
        </div>
        
        <div class="analysis-section">
            <h2>🔮 未来发展趋势</h2>
            <div class="analysis-grid">
'''
        
        for trend in company_info.get('future_trends', []):
            html += f'''
                <div class="analysis-item">
                    <h3>📈 {trend}</h3>
                    <p>公司将在这一领域持续投入资源，把握市场机遇，推动长期增长。</p>
                </div>
'''
        
        rec_color = self.get_recommendation_color(company.get('recommendationKey', 'hold'))
        rec_text = self.get_recommendation_text(company.get('recommendationKey', 'hold'))
        
        html += f'''
            </div>
        </div>
        
        <div class="analysis-section">
            <h2>📊 分析师评级</h2>
            <div class="metric-grid">
                <div class="metric-item">
                    <div class="metric-label">目标高价</div>
                    <div class="metric-value">${company.get('targetHighPrice', 0):.2f}</div>
                </div>
                <div class="metric-item">
                    <div class="metric-label">目标低价</div>
                    <div class="metric-value">${company.get('targetLowPrice', 0):.2f}</div>
                </div>
                <div class="metric-item">
                    <div class="metric-label">当前股价</div>
                    <div class="metric-value">${company.get('currentPrice', 0):.2f}</div>
                </div>
                <div class="metric-item">
                    <div class="metric-label">分析师数量</div>
                    <div class="metric-value">{company.get('numberOfAnalystOpinions', 0)}</div>
                </div>
            </div>
            <div class="rating-box" style="background: {rec_color};">
                <div class="rating">{rec_text}</div>
                <div class="analysts">基于 {company.get('numberOfAnalystOpinions', 0)} 位分析师意见</div>
            </div>
        </div>
        
        <div class="analysis-section">
            <h2>👥 持股结构</h2>
            <div class="metric-grid">
                <div class="metric-item">
                    <div class="metric-label">内部持股</div>
                    <div class="metric-value">{self.format_percent(company.get('heldPercentInsiders', 0))}</div>
                </div>
                <div class="metric-item">
                    <div class="metric-label">机构持股</div>
                    <div class="metric-value">{self.format_percent(company.get('heldPercentInstitutions', 0))}</div>
                </div>
                <div class="metric-item">
                    <div class="metric-label">流通股数</div>
                    <div class="metric-value">{company.get('sharesOutstanding', 0)/1e9:.2f}B</div>
                </div>
                <div class="metric-item">
                    <div class="metric-label">平均成交量</div>
                    <div class="metric-value">{company.get('averageVolume', 0)/1e6:.2f}M</div>
                </div>
            </div>
        </div>
        
        <div class="footer">
            <p>数据来源：Yahoo Finance | 报告生成时间：{datetime.now().strftime("%Y-%m-%d %H:%M:%S")}</p>
            <div class="disclaimer">
                ⚠️ 免责声明：本报告仅供参考，不构成投资建议。投资有风险，决策需谨慎。数据可能存在延迟，请以官方信息为准。
            </div>
        </div>
    </div>
</body>
</html>
'''
        
        return html
    
    def generate_all(self):
        """生成所有 HTML 文件"""
        # 加载最新数据
        latest_file = self.data_dir / "latest_market_data.json"
        if not latest_file.exists():
            print("错误：未找到数据文件，请先运行 fetch_data.py")
            return
        
        with open(latest_file, 'r', encoding='utf-8') as f:
            companies = json.load(f)
        
        # 生成首页
        print("生成首页...")
        index_html = self.generate_index(companies)
        index_file = self.output_dir / "index.html"
        with open(index_file, 'w', encoding='utf-8') as f:
            f.write(index_html)
        
        # 生成每个公司的详细报告
        print("生成公司报告...")
        for company in companies:
            report_html = self.generate_company_report(company)
            report_file = self.output_dir / f"report_{company['ticker']}.html"
            with open(report_file, 'w', encoding='utf-8') as f:
                f.write(report_html)
        
        # 复制 index.html 作为 GitHub Pages 入口
        print("完成！")
        print(f"共生成 {len(companies) + 1} 个 HTML 文件")
        print(f"输出目录：{self.output_dir}")

if __name__ == "__main__":
    generator = HTMLGenerator()
    generator.generate_all()
