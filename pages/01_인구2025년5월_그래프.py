import streamlit as st
import pandas as pd
import folium
from streamlit_folium import st_folium

# -------------------- 기본 설정 --------------------
st.set_page_config(page_title="2025년 5월 인구 지도 시각화", layout="wide")
st.title("2025년 5월 기준 인구 상위 5개 행정구역 지도 표시")

# -------------------- 데이터 불러오기 및 전처리 --------------------
file_path = "202505_202505_연령별인구현황_월간.csv"
df = pd.read_csv(file_path, encoding="euc-kr")

# 필요한 열 추출
population_cols = [col for col in df.columns if col.startswith("2025년05월_계_")]
age_cols = [col for col in population_cols if "총인구수" not in col]
age_mapping = {col: col.replace("2025년05월_계_", "") for col in age_cols}
df = df.rename(columns=age_mapping)
df["총인구수"] = df["2025년05월_계_총인구수"].str.replace(",", "").astype(int)
df_filtered = df[df["행정구역"].str.count(r"\(") == 1]
top5_df = df_filtered.sort_values("총인구수", ascending=False).head(5).copy()

# -------------------- 위도/경도 수동 설정 --------------------
# 각 행정구역에 대응하는 위도/경도 (샘플 - 필요시 추가 보완 가능)
location_map = {
    "경기도 수원시 (4111000000)": [37.2636, 127.0286],
    "부산광역시 해운대구 (2647000000)": [35.1631, 129.1635],
    "서울특별시 송파구 (1171000000)": [37.5145, 127.1056],
    "서울특별시 강서구 (1150000000)": [37.5509, 126.8495],
    "서울특별시 강남구 (1168000000)": [37.5172, 127.0473],
}

# -------------------- 지도 생성 --------------------
m = folium.Map(location=[36.5, 127.8], zoom_start=7)

for _, row in top5_df.iterrows():
    name = row["행정구역"]
    pop = row["총인구수"]
    coords = location_map.get(name)

    if coords:
        folium.CircleMarker(
            location=coords,
            radius=pop / 1000000,  # 인구 수에 따라 크기 조절
            color='crimson',
            fill=True,
            fill_color='crimson',
            fill_opacity=0.4,
            popup=f"{name}<br>총인구수: {pop:,}명"
        ).add_to(m)

# -------------------- Streamlit UI --------------------
st.subheader("📍 인구 상위 5개 지역 지도 시각화")
st_folium(m, width=1000, height=600)

st.subheader("📊 인구 데이터")
st.dataframe(top5_df[["행정구역", "총인구수"]])
