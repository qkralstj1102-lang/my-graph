import streamlit as st
import pandas as pd
import plotly.express as px

# ----------------------------------------
# 기본 설정
# ----------------------------------------
st.set_page_config(
    page_title="영화 데이터 그래프 도감 1 - 시간",
    page_icon="🎬",
    layout="wide"
)

st.title("🎬 영화 데이터 그래프 도감 1 - 시간")

st.write(
    "일별 박스오피스 데이터를 이용하여 영화의 시간에 따른 변화를 살펴봅니다."
)

# ----------------------------------------
# 데이터 불러오기
# ----------------------------------------
DATA_URL = "https://raw.githubusercontent.com/greatsong/modudata/main/data/kobis_daily.csv"


@st.cache_data
def load_data():
    df = pd.read_csv(DATA_URL)

    # 날짜를 실제 날짜 형식으로 변환
    df["날짜"] = pd.to_datetime(
        df["날짜"].astype(str),
        format="%Y%m%d"
    )

    # 숫자형 데이터 변환
    numeric_columns = [
        "순위",
        "영화코드",
        "일관객",
        "누적관객",
        "스크린수",
        "상영횟수"
    ]

    for col in numeric_columns:
        df[col] = pd.to_numeric(
            df[col],
            errors="coerce"
        )

    return df


# 데이터 불러오기
try:
    df = load_data()

except Exception as e:
    st.error("데이터를 불러오는 중 문제가 발생했습니다.")
    st.code(str(e))
    st.stop()


# ========================================
# 그래프 1
# ========================================
st.header("📊 그래프 1. 영화별 날짜에 따른 일관객 변화")

st.write(
    "영화를 선택하면 해당 영화의 날짜별 일관객 변화를 확인할 수 있습니다."
)

# 영화 선택
movie_list = sorted(
    df["영화명"].dropna().unique()
)

selected_movie = st.selectbox(
    "영화를 선택하세요.",
    movie_list
)

# 선택한 영화의 데이터만 추출
movie_df = df[
    df["영화명"] == selected_movie
].copy()

movie_df = movie_df.sort_values("날짜")


# ----------------------------------------
# 선 그래프
# ----------------------------------------
fig = px.line(
    movie_df,
    x="날짜",
    y="일관객",
    markers=True,
    title=f"'{selected_movie}'의 날짜별 일관객 변화",
    labels={
        "날짜": "날짜",
        "일관객": "일관객 수"
    }
)

# 마우스를 올렸을 때 표시되는 정보
fig.update_traces(
    hovertemplate=
    "날짜: %{x|%Y-%m-%d}<br>"
    "일관객: %{y:,}명"
    "<extra></extra>"
)

fig.update_layout(
    height=500,
    hovermode="x unified",
    xaxis_title="날짜",
    yaxis_title="일관객 수(명)"
)

st.plotly_chart(
    fig,
    use_container_width=True
)


# ----------------------------------------
# 그래프로 알 수 있는 것
# ----------------------------------------
st.subheader("💡 이 그래프로 알 수 있는 것")

graph1_comment = st.text_area(
    "이 그래프를 보고 알 수 있는 내용을 직접 작성하세요.",
    placeholder="예: 영화 개봉 초기에는 관객 수가 많았지만 시간이 지나면서 점차 감소하는 것을 알 수 있다.",
    height=100,
    key="graph1_comment"
)

if graph1_comment:
    st.info(graph1_comment)


# ========================================
# 그래프 2
# ========================================
st.divider()

st.header("📈 그래프 2")

st.write(
    "두 번째 그래프를 추가할 수 있는 공간입니다."
)

graph2_comment = st.text_area(
    "이 그래프로 알 수 있는 것",
    placeholder="그래프를 추가한 뒤, 이 그래프를 통해 알 수 있는 내용을 작성하세요.",
    height=100,
    key="graph2_comment"
)

if graph2_comment:
    st.info(graph2_comment)


# ========================================
# 그래프 3
# ========================================
st.divider()

st.header("📉 그래프 3")

st.write(
    "세 번째 그래프를 추가할 수 있는 공간입니다."
)

graph3_comment = st.text_area(
    "이 그래프로 알 수 있는 것",
    placeholder="그래프를 추가한 뒤, 이 그래프를 통해 알 수 있는 내용을 작성하세요.",
    height=100,
    key="graph3_comment"
)

if graph3_comment:
    st.info(graph3_comment)
