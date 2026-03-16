#!/usr/bin/env python3
"""
查询浙江省98号汽油今天的价格
Query today's price of 98# gasoline in Zhejiang province, China.

Usage:
    python get_hangzhou_oil_price.py

Data source: http://www.qiyoujiage.com/zhejiang.shtml
"""

import re
import urllib.error
import urllib.request
from datetime import date


def get_hangzhou_98_oil_price() -> None:
    """
    Query and print today's 98# gasoline price in Zhejiang province.

    Scrapes the latest price from qiyoujiage.com. If the network call
    fails (e.g., running offline), the script falls back to a recent
    reference price with a disclaimer.
    """
    today = date.today().strftime("%Y-%m-%d")
    print("===== 浙江省98号汽油价格查询 =====")
    print(f"查询日期: {today}")
    print()

    # ----------------------------------------------------------------
    # Primary source: qiyoujiage.com (free, no key required)
    # ----------------------------------------------------------------
    url = "http://www.qiyoujiage.com/zhejiang.shtml"
    try:
        req = urllib.request.Request(
            url,
            headers={
                "User-Agent": (
                    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                    "AppleWebKit/537.36 (KHTML, like Gecko) "
                    "Chrome/120.0.0.0 Safari/537.36"
                )
            },
        )
        with urllib.request.urlopen(req, timeout=10) as resp:
            html = resp.read().decode("utf-8", errors="replace")

        # The page renders a price table; each row looks like:
        #   <td ...>98号汽油</td> ... <td ...>9.50</td>
        # Match the price that appears after the "98号" fuel label.
        match = re.search(
            r"98\s*号[^<]{0,30}?</td>\s*(?:<td[^>]*>\s*[\d.]+\s*</td>\s*)*"
            r"<td[^>]*>\s*(\d+\.\d+)\s*</td>",
            html,
        )
        if not match:
            # Broader fallback pattern: find any decimal number immediately
            # following the text "98号" within 200 characters.
            match = re.search(r"98\s*号.{0,200}?(\d+\.\d{2})", html, re.DOTALL)

        if match:
            price = match.group(1)
            print(f"98号汽油今日价格: ¥{price} 元/升")
            print(f"数据来源: 汽油价格网 ({url})")
            return

        print(f"[未能从页面中解析到98号汽油价格，请访问 {url} 查看最新价格]")

    except (urllib.error.URLError, OSError) as err:
        print(f"[数据源不可用: {err}]")

    # ----------------------------------------------------------------
    # Fallback: static reference price with disclaimer
    # ----------------------------------------------------------------
    reference_price = 9.38  # Zhejiang 98# reference, March 2025
    print(f"\n98号汽油参考价格: ¥{reference_price} 元/升")
    print(
        "⚠️  无法连接实时数据源，以上为参考价格（2025年3月浙江省指导价），"
        "实际价格请以加油站公示为准。"
    )
    print(f"实时价格请访问: {url}")


if __name__ == "__main__":
    get_hangzhou_98_oil_price()
