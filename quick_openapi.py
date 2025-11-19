import requests
import xml.etree.ElementTree as ET
import pandas as pd

SERVICE_KEY = "64427a7971616d69373370496c664f"

def get_page(start, end):
    """특정 구간(start~end) 호출해서 item 리스트 반환"""
    url = f"http://openapi.seoul.go.kr:8088/{SERVICE_KEY}/xml/getFstExit/{start}/{end}/"
    res = requests.get(url)
    res.encoding = "utf-8"
    root = ET.fromstring(res.text)

    items = root.find("body").find("items")

    if items is None:
        return []

    rows = []
    for item in items.findall("item"):
        rows.append({
            "관리번호": item.findtext("qckgffMngNo"),
            "호선": item.findtext("lineNm"),
            "역코드": item.findtext("stnCd"),
            "역명": item.findtext("stnNm"),
            "역번호": item.findtext("stnNo"),
            "기준일자": item.findtext("crtrYmd"),
            "상하행": item.findtext("upbdnbSe"),
            "방향(다음역)": item.findtext("drtnInfo"),
            "칸-문번호": item.findtext("qckgffVhclDoorNo"),
            "승하차시설": item.findtext("plfmCmgFac"),
            "시설번호": item.findtext("facNo"),
            "엘리베이터번호": item.findtext("elvtrNo"),
            "통로위치": item.findtext("fwkPstnNm"),
            "시설위치": item.findtext("facPstnNm"),
        })
    return rows


# 전체 페이지 반복
all_rows = []
start = 1
step = 1000

print("전체 데이터 수집 중...")

while True:
    end = start + step - 1
    print(f"📌 {start} ~ {end} 요청 중...")

    rows = get_page(start, end)
    if len(rows) == 0:
        print("📌 더 이상 데이터 없음 → 종료")
        break

    all_rows.extend(rows)
    start += step

# DataFrame 만들기
df = pd.DataFrame(all_rows)
print("총 데이터 개수:", len(df))

# CSV 저장
df.to_csv("전체_빠른승하차정보.csv", index=False, encoding="utf-8-sig")
print("전체 데이터 CSV 저장 완료!")
