import streamlit as st
import pandas as pd

# 페이지 기본 설정
st.set_page_config(page_title="2025년 5월 연령별 인구 분석", layout="wide")

# 제목
st.title("2025년 5월 기준 연령별 인구 현황 분석")

# 데이터 불러오기
file_path = "202505_202505_연령별인구현황_월간.csv"
df = pd.read_csv(file_path, encoding="euc-kr")

# '2025년05월_계_'로 시작하는 열 중 '총인구수' 외 연령만 추출
population_cols = [col for col in df.columns if col.startswith("2025년05월_계_")]
age_cols = [col for col in population_cols if "총인구수" not in col]
age_mapping = {col: col.replace("2025년05월_계_", "") for col in age_cols}
df = df.rename(columns=age_mapping)

# 총인구수 처리
df["총인구수"] = df["2025년05월_계_총인구수"].str.replace(",", "").astype(int)

# '구' 단위만 필터링 (괄호가 한 번 나오는 행정구역만)
df_filtered = df[df["행정구역"].str.count(r"\(") == 1]

# 총인구수 기준 상위 5개 행정구역 추출
top5_df = df_filtered.sort_values("총인구수", ascending=False).head(5)

# 연령별 인구 데이터 정제
age_df = top5_df[["행정구역"] + list(age_mapping.values())].copy()
for age in age_mapping.values():
    age_df[age] = age_df[age].astype(str).str.replace(",", "").astype(int)

# 연령을 행으로, 행정구역을 열로 변경
age_df = age_df.set_index("행정구역").T
age_df.index.name = "연령"

# -------------------- UI --------------------

st.subheader("📊 상위 5개 행정구역 데이터 (총인구수 기준)")
st.dataframe(top5_df[["행정구역", "총인구수"] + list(age_mapping.values())])

st.subheader("📈 연령별 인구 분포 (선 그래프)")
st.line_chart(age_df)

