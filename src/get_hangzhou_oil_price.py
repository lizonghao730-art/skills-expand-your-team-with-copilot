#!/usr/bin/env python3
"""
查询杭州市中国石化加油站98号汽油今天的价格
Query today's price of Sinopec 98# gasoline in Hangzhou, China.

Usage:
    python get_hangzhou_oil_price.py

Optional environment variable:
    TIANAPI_KEY  — API key for tianapi.com (https://www.tianapi.com/).
                   If not set the secondary data source is skipped.
"""

import json
import os
import urllib.error
import urllib.parse
import urllib.request
from datetime import date


def get_hangzhou_98_oil_price() -> None:
    """
    Query and print today's 98# gasoline price in Hangzhou (Sinopec).

    Attempts several public data sources. If all network calls fail
    (e.g., running offline), the script falls back to a recent
    reference price with a disclaimer.
    """
    today = date.today().strftime("%Y-%m-%d")
    print("===== 杭州市98号汽油价格查询 =====")
    print(f"查询日期: {today}")
    print("品牌: 中国石化 (Sinopec)")
    print()

    # ----------------------------------------------------------------
    # Primary source: jindianyoujia (free, no key required)
    # ----------------------------------------------------------------
    try:
        params = urllib.parse.urlencode({"city": "杭州", "type": "98号"})
        url = f"https://www.jindianyoujia.com/api/price/query?{params}"
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
        with urllib.request.urlopen(req, timeout=10) as resp:
            data = json.loads(resp.read().decode("utf-8"))
            price = data.get("data", {}).get("price") or data.get("price")
            if price:
                print(f"98号汽油今日价格: ¥{price} 元/升")
                print("数据来源: 金典油价")
                return
    except (urllib.error.URLError, json.JSONDecodeError, OSError) as err:
        print(f"[主数据源不可用: {err}]")

    # ----------------------------------------------------------------
    # Secondary source: tianapi oil-price endpoint (Zhejiang province)
    # Requires a free API key from https://www.tianapi.com/
    # Set the TIANAPI_KEY environment variable before running.
    # ----------------------------------------------------------------
    tianapi_key = os.environ.get("TIANAPI_KEY", "")
    if tianapi_key:
        try:
            params = urllib.parse.urlencode({"key": tianapi_key, "prov": "浙江"})
            url = f"https://apis.tianapi.com/oilprice/index?{params}"
            req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
            with urllib.request.urlopen(req, timeout=10) as resp:
                data = json.loads(resp.read().decode("utf-8"))
                items = data.get("result", {}).get("list", []) or data.get("newslist", [])
                for item in items:
                    if "98" in str(item.get("oname", "")):
                        price = item.get("price")
                        print(f"98号汽油今日价格: ¥{price} 元/升")
                        print("数据来源: 天行数据 (浙江省参考价)")
                        return
        except (urllib.error.URLError, json.JSONDecodeError, OSError) as err:
            print(f"[备用数据源不可用: {err}]")
    else:
        print("[提示: 设置 TIANAPI_KEY 环境变量可启用备用数据源]")

    # ----------------------------------------------------------------
    # Fallback: static reference price with disclaimer
    # ----------------------------------------------------------------
    reference_price = 9.38  # Zhejiang/Hangzhou 98# reference, March 2025
    print(f"\n98号汽油参考价格: ¥{reference_price} 元/升")
    print(
        "⚠️  无法连接实时数据源，以上为参考价格（2025年3月浙江省中石化指导价），"
        "实际价格请以加油站公示为准。"
    )
    print("实时价格请访问: https://www.sinopec.com 或拨打 95105888 查询。")


if __name__ == "__main__":
    get_hangzhou_98_oil_price()
