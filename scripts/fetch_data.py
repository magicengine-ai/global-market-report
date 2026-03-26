#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
全球上市公司数据获取脚本
从 Yahoo Finance 获取市值数据并生成报告
"""

import yfinance as yf
import pandas as pd
import json
import os
from datetime import datetime
from pathlib import Path
from bs4 import BeautifulSoup
import requests

# 全球市值最大的公司列表（持续更新）
GLOBAL_MEGACAPS = [
    # 科技巨头
    "AAPL",    # Apple
    "MSFT",    # Microsoft
    "NVDA",    # NVIDIA
    "GOOGL",   # Alphabet (Google)
    "AMZN",    # Amazon
    "META",    # Meta (Facebook)
    "TSLA",    # Tesla
    "BRK-B",   # Berkshire Hathaway
    "LLY",     # Eli Lilly
    "AVGO",    # Broadcom
    # 其他巨头
    "JPM",     # JPMorgan Chase
    "V",       # Visa
    "UNH",     # UnitedHealth
    "XOM",     # Exxon Mobil
    "MA",      # Mastercard
    "PG",      # Procter & Gamble
    "JNJ",     # Johnson & Johnson
    "HD",      # Home Depot
    "CVX",     # Chevron
    "MRK",     # Merck
    # 中国公司
    "BABA",    # Alibaba
    "TCEHY",   # Tencent
    "PDD",     # PDD Holdings
    "NVO",     # Novo Nordisk
    "ORCL",    # Oracle
    "COST",    # Costco
    "ABBV",    # AbbVie
    "KO",      # Coca-Cola
    "PEP",     # PepsiCo
    "WMT",     # Walmart
]

class MarketDataFetcher:
    def __init__(self):
        self.data_dir = Path(__file__).parent.parent / "data"
        self.output_dir = Path(__file__).parent.parent / "output"
        self.logs_dir = Path(__file__).parent.parent / "logs"
        self.data_dir.mkdir(parents=True, exist_ok=True)
        self.output_dir.mkdir(parents=True, exist_ok=True)
        self.logs_dir.mkdir(parents=True, exist_ok=True)
        
    def fetch_company_info(self, ticker):
        """获取单个公司的详细信息"""
        try:
            stock = yf.Ticker(ticker)
            info = stock.info
            
            # 获取历史数据用于趋势分析
            hist = stock.history(period="1y")
            
            company_data = {
                "ticker": ticker,
                "name": info.get("longName", ticker),
                "sector": info.get("sector", "N/A"),
                "industry": info.get("industry", "N/A"),
                "website": info.get("website", "N/A"),
                "description": info.get("longBusinessSummary", "暂无描述"),
                "marketCap": info.get("marketCap", 0),
                "enterpriseValue": info.get("enterpriseValue", 0),
                "trailingPE": info.get("trailingPE", 0),
                "forwardPE": info.get("forwardPE", 0),
                "priceToBook": info.get("priceToBook", 0),
                "dividendYield": info.get("dividendYield", 0),
                "profitMargins": info.get("profitMargins", 0),
                "revenueGrowth": info.get("revenueGrowth", 0),
                "earningsGrowth": info.get("earningsGrowth", 0),
                "currentPrice": info.get("currentPrice", 0),
                "targetHighPrice": info.get("targetHighPrice", 0),
                "targetLowPrice": info.get("targetLowPrice", 0),
                "recommendationKey": info.get("recommendationKey", "N/A"),
                "numberOfAnalystOpinions": info.get("numberOfAnalystOpinions", 0),
                "totalCash": info.get("totalCash", 0),
                "totalDebt": info.get("totalDebt", 0),
                "totalRevenue": info.get("totalRevenue", 0),
                "grossProfits": info.get("grossProfits", 0),
                "freeCashflow": info.get("freeCashflow", 0),
                "operatingCashflow": info.get("operatingCashflow", 0),
                "earningsQuarterlyGrowth": info.get("earningsQuarterlyGrowth", 0),
                "52WeekChange": hist["Close"].pct_change(252).iloc[-1] if len(hist) > 252 else 0,
                "beta": info.get("beta", 0),
                "fiftyTwoWeekHigh": info.get("fiftyTwoWeekHigh", 0),
                "fiftyTwoWeekLow": info.get("fiftyTwoWeekLow", 0),
                "fiftyDayAverage": info.get("fiftyDayAverage", 0),
                "twoHundredDayAverage": info.get("twoHundredDayAverage", 0),
                "volume": info.get("volume", 0),
                "averageVolume": info.get("averageVolume", 0),
                "sharesOutstanding": info.get("sharesOutstanding", 0),
                "heldPercentInsiders": info.get("heldPercentInsiders", 0),
                "heldPercentInstitutions": info.get("heldPercentInstitutions", 0),
                "lastFetched": datetime.now().isoformat(),
            }
            
            # 获取公司信息（用于历史和发展）
            company_data["company_info"] = self._get_company_background(ticker, info)
            
            return company_data
            
        except Exception as e:
            print(f"Error fetching {ticker}: {str(e)}")
            return None
    
    def _get_company_background(self, ticker, info):
        """获取公司背景信息（主营业务、历史等）"""
        background = {
            "main_business": "",
            "history": [],
            "key_milestones": [],
            "competitive_advantages": [],
            "future_trends": []
        }
        
        description = info.get("longBusinessSummary", "")
        if description:
            # 提取主营业务
            background["main_business"] = description.split('.')[0] if '.' in description else description[:200]
            
            # 基于行业分析竞争优势
            industry = info.get("industry", "")
            sector = info.get("sector", "")
            
            if "Technology" in sector:
                background["competitive_advantages"] = [
                    "技术创新能力强",
                    "研发投入高",
                    "生态系统完善",
                    "品牌影响力大"
                ]
                background["future_trends"] = [
                    "人工智能和机器学习应用",
                    "云计算持续增长",
                    "数字化转型加速",
                    "物联网设备普及"
                ]
            elif "Healthcare" in sector:
                background["competitive_advantages"] = [
                    "研发管线丰富",
                    "专利保护强",
                    "全球化布局",
                    "监管壁垒高"
                ]
                background["future_trends"] = [
                    "精准医疗发展",
                    "生物技术创新",
                    "老龄化带来的需求增长",
                    "数字化健康服务"
                ]
            elif "Financial" in sector:
                background["competitive_advantages"] = [
                    "规模效应明显",
                    "客户基础庞大",
                    "风险管理能力强",
                    "数字化转型领先"
                ]
                background["future_trends"] = [
                    "金融科技应用",
                    "数字货币发展",
                    "监管科技升级",
                    "全球化服务扩展"
                ]
            elif "Energy" in sector:
                background["competitive_advantages"] = [
                    "资源丰富",
                    "垂直整合",
                    "成本控制能力强",
                    "全球化运营"
                ]
                background["future_trends"] = [
                    "可再生能源转型",
                    "碳中和目标驱动",
                    "能源效率提升",
                    "新技术投资"
                ]
            else:
                background["competitive_advantages"] = [
                    "市场地位稳固",
                    "品牌认知度高",
                    "运营效率高",
                    "现金流稳定"
                ]
                background["future_trends"] = [
                    "数字化转型",
                    "可持续发展",
                    "市场扩张",
                    "产品创新"
                ]
        
        # 添加公司发展历史节点（基于知名公司信息）
        background["key_milestones"] = self._get_company_milestones(ticker)
        
        return background
    
    def _get_company_milestones(self, ticker):
        """获取公司重要发展节点"""
        milestones = {
            "AAPL": [
                {"year": 1976, "event": "苹果公司成立"},
                {"year": 1984, "event": "推出 Macintosh"},
                {"year": 2001, "event": "推出 iPod"},
                {"year": 2007, "event": "推出 iPhone"},
                {"year": 2010, "event": "推出 iPad"},
                {"year": 2015, "event": "推出 Apple Watch"},
                {"year": 2020, "event": "市值突破 2 万亿美元"},
            ],
            "MSFT": [
                {"year": 1975, "event": "微软公司成立"},
                {"year": 1985, "event": "推出 Windows 1.0"},
                {"year": 1995, "event": "推出 Windows 95"},
                {"year": 2001, "event": "推出 Xbox"},
                {"year": 2014, "event": "Satya Nadella 出任 CEO"},
                {"year": 2018, "event": "市值突破 1 万亿美元"},
                {"year": 2021, "event": "市值突破 2 万亿美元"},
            ],
            "NVDA": [
                {"year": 1993, "event": "英伟达公司成立"},
                {"year": 1999, "event": "推出 GeForce GPU"},
                {"year": 2006, "event": "推出 CUDA 平台"},
                {"year": 2016, "event": "AI 和深度学习爆发"},
                {"year": 2023, "event": "AI 芯片需求激增"},
                {"year": 2024, "event": "市值突破 3 万亿美元"},
            ],
            "GOOGL": [
                {"year": 1998, "event": "Google 公司成立"},
                {"year": 2004, "event": "公司上市"},
                {"year": 2008, "event": "推出 Chrome 浏览器"},
                {"year": 2015, "event": "重组为 Alphabet"},
                {"year": 2023, "event": "推出 Bard AI"},
            ],
            "AMZN": [
                {"year": 1994, "event": "亚马逊公司成立"},
                {"year": 1997, "event": "公司上市"},
                {"year": 2006, "event": "推出 AWS 云服务"},
                {"year": 2014, "event": "推出 Alexa"},
                {"year": 2020, "event": "市值突破 1.5 万亿美元"},
            ],
            "META": [
                {"year": 2004, "event": "Facebook 成立"},
                {"year": 2012, "event": "公司上市"},
                {"year": 2014, "event": "收购 WhatsApp"},
                {"year": 2021, "event": "更名为 Meta"},
                {"year": 2023, "event": "元宇宙和 AI 投资"},
            ],
            "TSLA": [
                {"year": 2003, "event": "特斯拉公司成立"},
                {"year": 2008, "event": "推出 Roadster"},
                {"year": 2010, "event": "公司上市"},
                {"year": 2012, "event": "推出 Model S"},
                {"year": 2017, "event": "推出 Model 3"},
                {"year": 2020, "event": "加入标普 500"},
            ],
        }
        
        return milestones.get(ticker, [
            {"year": "N/A", "event": "公司发展历史数据待完善"}
        ])
    
    def fetch_all_companies(self):
        """获取所有公司的数据"""
        all_data = []
        
        print(f"开始获取 {len(GLOBAL_MEGACAPS)} 家公司的数据...")
        
        for i, ticker in enumerate(GLOBAL_MEGACAPS, 1):
            print(f"[{i}/{len(GLOBAL_MEGACAPS)}] 获取 {ticker} 数据...")
            data = self.fetch_company_info(ticker)
            if data and data.get("marketCap", 0) > 0:
                all_data.append(data)
        
        # 按市值排序
        all_data.sort(key=lambda x: x.get("marketCap", 0), reverse=True)
        
        # 保存原始数据
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        data_file = self.data_dir / f"market_data_{timestamp}.json"
        with open(data_file, 'w', encoding='utf-8') as f:
            json.dump(all_data, f, ensure_ascii=False, indent=2)
        
        # 保存最新数据
        latest_file = self.data_dir / "latest_market_data.json"
        with open(latest_file, 'w', encoding='utf-8') as f:
            json.dump(all_data, f, ensure_ascii=False, indent=2)
        
        print(f"数据已保存到 {data_file}")
        return all_data
    
    def log_fetch(self, message):
        """记录日志"""
        log_file = self.logs_dir / f"fetch_{datetime.now().strftime('%Y%m%d')}.log"
        with open(log_file, 'a', encoding='utf-8') as f:
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            f.write(f"[{timestamp}] {message}\n")

if __name__ == "__main__":
    fetcher = MarketDataFetcher()
    fetcher.log_fetch("开始数据获取任务")
    data = fetcher.fetch_all_companies()
    fetcher.log_fetch(f"成功获取 {len(data)} 家公司数据")
    print(f"\n完成！共获取 {len(data)} 家公司数据")
