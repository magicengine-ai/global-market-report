#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
主运行脚本 - 获取数据并生成报告
"""

import sys
from pathlib import Path

# 添加脚本目录到路径
script_dir = Path(__file__).parent
sys.path.insert(0, str(script_dir))

from fetch_data import MarketDataFetcher
from generate_html import HTMLGenerator

def main():
    print("=" * 60)
    print("全球上市公司报告生成系统")
    print("=" * 60)
    
    # 步骤 1: 获取数据
    print("\n[1/2] 获取市场数据...")
    fetcher = MarketDataFetcher()
    fetcher.log_fetch("=== 开始数据获取任务 ===")
    data = fetcher.fetch_all_companies()
    
    if not data:
        print("错误：未能获取到任何数据")
        fetcher.log_fetch("错误：未能获取到任何数据")
        return 1
    
    fetcher.log_fetch(f"成功获取 {len(data)} 家公司数据")
    
    # 步骤 2: 生成 HTML
    print("\n[2/2] 生成 HTML 报告...")
    generator = HTMLGenerator()
    generator.generate_all()
    
    print("\n" + "=" * 60)
    print("✅ 完成！")
    print(f"📊 处理公司数：{len(data)}")
    print(f"📁 输出目录：{generator.output_dir}")
    print("=" * 60)
    
    return 0

if __name__ == "__main__":
    sys.exit(main())
