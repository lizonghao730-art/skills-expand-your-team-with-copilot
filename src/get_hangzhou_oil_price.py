#!/usr/bin/env python3
"""
查询浙江省汽油今天的价格
Query today's gasoline prices in Zhejiang province, China.

Usage:
    python get_hangzhou_oil_price.py

Data source: http://www.qiyoujiage.com/zhejiang.shtml
"""

import re
import urllib.error
import urllib.request
from datetime import date


def get_hangzhou_oil_price() -> None:
    """
    Query and print today's gasoline prices in Zhejiang province.

    Scrapes the latest prices from qiyoujiage.com. If the network call
    fails (e.g., running offline), the script falls back to recent
    reference prices with a disclaimer.

    The data source uses definition lists in the following format:
        <dl><dt>浙江95#汽油</dt><dd>8.09</dd></dl>
        <dl><dt>浙江98#汽油</dt><dd>9.59</dd></dl>
    """
    today = date.today().strftime("%Y-%m-%d")
    print("===== 浙江省汽油价格查询 =====")
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

        # The page renders prices in definition lists:
        #   <dl><dt>浙江95#汽油</dt><dd>8.09</dd></dl>
        #   <dl><dt>浙江98#汽油</dt><dd>9.59</dd></dl>
        matches = re.findall(
            r"<dt>\s*浙江(\d+)#汽油\s*</dt>\s*<dd>\s*(\d+\.\d+)\s*</dd>",
            html,
        )

        if matches:
            for grade, price in matches:
                print(f"{grade}号汽油今日价格: ¥{price} 元/升")
            print(f"\n数据来源: 汽油价格网 ({url})")
            return

        print(f"[未能从页面中解析到汽油价格，请访问 {url} 查看最新价格]")

    except (urllib.error.URLError, OSError) as err:
        print(f"[数据源不可用: {err}]")

    # ----------------------------------------------------------------
    # Fallback: static reference prices with disclaimer
    # ----------------------------------------------------------------
    reference_prices = {
        "95": 8.09,  # Zhejiang 95# reference, March 2025
        "98": 9.59,  # Zhejiang 98# reference, March 2025
    }
    print("\n汽油参考价格:")
    for grade, price in reference_prices.items():
        print(f"  {grade}号汽油: ¥{price} 元/升")
    print(
        "\n⚠️  无法连接实时数据源，以上为参考价格（2025年3月浙江省指导价），"
        "实际价格请以加油站公示为准。"
    )
    print(f"实时价格请访问: {url}")


# Keep backward compatibility
def get_hangzhou_98_oil_price() -> None:
    get_hangzhou_oil_price()


if __name__ == "__main__":
    get_hangzhou_oil_price()
