# -*- coding: utf-8 -*-
"""
간단 웹 크롤러 예제
- 대상: https://quotes.toscrape.com (연습용으로 공개 허용된 사이트)
- 기능: 페이지를 다음(next) 버튼이 사라질 때까지 순회하며
        문구, 작가, 태그를 수집한 뒤 CSV로 저장
"""

import time
import csv
import sys
from typing import List, Dict, Optional

import requests
from bs4 import BeautifulSoup

BASE_URL = "https://quotes.toscrape.com"
START_URL = f"{BASE_URL}/page/1/"
HEADERS = {
    # 기본 User-Agent 지정 (너무 짧게 요청하지 않도록 예의)
    "User-Agent": "Mozilla/5.0 (compatible; SimpleCrawler/1.0; +https://example.com/bot)"
}

def fetch_html(url: str, timeout: int = 10) -> Optional[str]:
    try:
        res = requests.get(url, headers=HEADERS, timeout=timeout)
        res.raise_for_status()
        return res.text
    except requests.RequestException as e:
        print(f"[에러] 요청 실패: {url} -> {e}", file=sys.stderr)
        return None

def parse_quotes(html: str) -> List[Dict[str, str]]:
    soup = BeautifulSoup(html, "html.parser")
    out = []
    for box in soup.select(".quote"):
        text = box.select_one(".text")
        author = box.select_one(".author")
        tags = [t.get_text(strip=True) for t in box.select(".tags .tag")]
        out.append({
            "quote": text.get_text(strip=True) if text else "",
            "author": author.get_text(strip=True) if author else "",
            "tags": ", ".join(tags)
        })
    return out

def find_next_page(html: str) -> Optional[str]:
    soup = BeautifulSoup(html, "html.parser")
    next_link = soup.select_one("li.next > a")
    if next_link and next_link.get("href"):
        # 상대 경로를 절대 경로로 변환
        return BASE_URL + next_link.get("href")
    return None

def crawl(start_url: str, delay_sec: float = 1.0) -> List[Dict[str, str]]:
    url = start_url
    collected: List[Dict[str, str]] = []

    while url:
        print(f"[크롤링] {url}")
        html = fetch_html(url)
        if not html:
            break

        items = parse_quotes(html)
        print(f"  - {len(items)}개 수집")
        collected.extend(items)

        url = find_next_page(html)
        time.sleep(delay_sec)  # 매너 타임(과도한 요청 방지)
    return collected

def save_csv(rows: List[Dict[str, str]], path: str = "quotes.csv") -> None:
    if not rows:
        print("[안내] 저장할 데이터가 없습니다.")
        return
    fieldnames = ["quote", "author", "tags"]
    with open(path, "w", newline="", encoding="utf-8-sig") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)
    print(f"[완료] CSV 저장: {path} (총 {len(rows)}행)")

if __name__ == "__main__":
    data = crawl(START_URL, delay_sec=0.8)
    save_csv(data, "quotes.csv")
