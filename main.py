import streamlit as st
import pandas as pd
import plotly.express as px

# ========================================
# 기본 설정
# ========================================

st.set_page_config(
    page_title="영화 데이터 그래프 도감 1 - 시간",
    page_icon="🎬",
    layout="wide"
)

st.title("🎬 영화 데이터 그래프 도감 1 - 시간")

st.write(
    "일별 박스오피스 데이터를 이용하여 영화의 시간에 따른 변화를 살펴봅니다."
)


# ========================================
# 데이터 불러오기
# ========================================

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
# 영화별 날짜에 따른 일관객 변화
# ========================================

st.header("📊 그래프 1. 영화별 날짜에 따른 일관객 변화")

st.write(
    "영화를 선택하면 해당 영화의 날짜별 일관객 변화를 확인할 수 있습니다."
)


# 영화 목록
movie_list = sorted(
    df["영화명"].dropna().unique()
)


# 영화 선택
selected_movie = st.selectbox(
    "영화를 선택하세요.",
    movie_list
)


# 선택한 영화 데이터
movie_df = df[
    df["영화명"] == selected_movie
].copy()

movie_df = movie_df.sort_values("날짜")


# ----------------------------------------
# 그래프 1 그리기
# ----------------------------------------

fig1 = px.line(
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


fig1.update_traces(
    hovertemplate=
    "날짜: %{x|%Y-%m-%d}<br>"
    "일관객: %{y:,}명"
    "<extra></extra>"
)


fig1.update_layout(
    height=500,
    hovermode="x unified",
    xaxis_title="날짜",
    yaxis_title="일관객 수(명)"
)


st.plotly_chart(
    fig1,
    use_container_width=True
)


# ----------------------------------------
# 그래프 1 설명 입력
# ----------------------------------------

st.subheader("💡 이 그래프로 알 수 있는 것")

graph1_comment = st.text_area(
    "이 그래프를 보고 알 수 있는 내용을 직접 작성하세요.",
    placeholder="여기에 직접 작성하세요.",
    height=100,
    key="graph1_comment"
)


if graph1_comment:

    st.info(graph1_comment)


# ========================================
# 그래프 2
# 일관객 합계 상위 5편
# ========================================

st.divider()

st.header("📈 그래프 2. 기간 내 일관객 합계 상위 5편 비교")

st.write(
    "전체 기간 동안의 일관객 합계를 기준으로 "
    "관객 수가 가장 많은 5편을 선정하여 날짜별 변화를 비교합니다."
)


# ----------------------------------------
# 영화별 일관객 합계
# ----------------------------------------

movie_total = (
    df.groupby("영화명", as_index=False)["일관객"]
    .sum()
    .sort_values(
        "일관객",
        ascending=False
    )
    .head(5)
)


# 상위 5편 영화 이름
top5_movies = movie_total["영화명"].tolist()


# 상위 5편 데이터
top5_df = df[
    df["영화명"].isin(top5_movies)
].copy()

top5_df = top5_df.sort_values(
    ["영화명", "날짜"]
)


# ----------------------------------------
# 그래프 2 그리기
# ----------------------------------------

fig2 = px.line(
    top5_df,
    x="날짜",
    y="일관객",
    color="영화명",
    markers=True,
    title="일관객 합계 상위 5편의 날짜별 일관객 변화",
    labels={
        "날짜": "날짜",
        "일관객": "일관객 수",
        "영화명": "영화"
    }
)


fig2.update_traces(
    hovertemplate=
    "영화: %{fullData.name}<br>"
    "날짜: %{x|%Y-%m-%d}<br>"
    "일관객: %{y:,}명"
    "<extra></extra>"
)


fig2.update_layout(
    height=600,
    hovermode="x unified",
    xaxis_title="날짜",
    yaxis_title="일관객 수(명)",
    legend_title="영화"
)


st.plotly_chart(
    fig2,
    use_container_width=True
)


# ----------------------------------------
# 상위 5편 표
# ----------------------------------------

st.write("### 🏆 이 기간 일관객 합계 상위 5편")


ranking_df = movie_total.copy()

ranking_df["순위"] = range(
    1,
    len(ranking_df) + 1
)

ranking_df = ranking_df[
    ["순위", "영화명", "일관객"]
]

ranking_df = ranking_df.rename(
    columns={
        "영화명": "영화",
        "일관객": "기간 내 일관객 합계"
    }
)


st.dataframe(
    ranking_df,
    hide_index=True,
    use_container_width=True
)


# ----------------------------------------
# 그래프 2 설명 입력
# ----------------------------------------

st.subheader("💡 이 그래프로 알 수 있는 것")

graph2_comment = st.text_area(
    "이 그래프로 알 수 있는 내용을 직접 작성하세요.",
    placeholder="여기에 직접 작성하세요.",
    height=100,
    key="graph2_comment"
)


if graph2_comment:

    st.info(graph2_comment)


# ========================================
# 그래프 3
# 날짜별 10위권 일관객 합계
# ========================================

st.divider()

st.header("📊 그래프 3. 날짜별 10위권 일관객 합계")

st.write(
    "각 날짜의 박스오피스 10위권 영화들의 일관객을 모두 합산하여 "
    "날짜별 전체 관객 규모의 변화를 확인합니다."
)


# ----------------------------------------
# 날짜별 일관객 합계
# ----------------------------------------

daily_total = (
    df.groupby("날짜", as_index=False)["일관객"]
    .sum()
    .sort_values("날짜")
)


# ----------------------------------------
# 일관객 합계가 가장 큰 3일
# ----------------------------------------

top3_days = (
    daily_total
    .sort_values(
        "일관객",
        ascending=False
    )
    .head(3)
)


# ----------------------------------------
# 영역 그래프
# ----------------------------------------

fig3 = px.area(
    daily_total,
    x="날짜",
    y="일관객",
    title="날짜별 박스오피스 10위권 일관객 합계",
    labels={
        "날짜": "날짜",
        "일관객": "10위권 일관객 합계"
    }
)


# ----------------------------------------
# 가장 관객이 많았던 3일 표시
# ----------------------------------------

for _, row in top3_days.iterrows():

    fig3.add_annotation(

        x=row["날짜"],

        y=row["일관객"],

        text=(
            f"<b>{row['날짜'].strftime('%Y-%m-%d')}</b><br>"
            f"{row['일관객']:,}명"
        ),

        showarrow=True,

        arrowhead=2,

        ax=0,

        ay=-60
    )


fig3.update_traces(
    hovertemplate=
    "날짜: %{x|%Y-%m-%d}<br>"
    "10위권 일관객 합계: %{y:,}명"
    "<extra></extra>"
)


fig3.update_layout(
    height=600,
    hovermode="x unified",
    xaxis_title="날짜",
    yaxis_title="10위권 일관객 합계(명)"
)


st.plotly_chart(
    fig3,
    use_container_width=True
)


# ----------------------------------------
# 관객 합계가 가장 많았던 3일 표
# ----------------------------------------

st.write("### 🏆 일관객 합계가 가장 컸던 3일")


top3_display = top3_days.copy()

top3_display["날짜"] = (
    top3_display["날짜"]
    .dt.strftime("%Y-%m-%d")
)

top3_display = top3_display.rename(
    columns={
        "일관객": "10위권 일관객 합계"
    }
)


st.dataframe(
    top3_display,
    hide_index=True,
    use_container_width=True
)


# ----------------------------------------
# 그래프 3 설명 입력
# ----------------------------------------

st.subheader("💡 이 그래프로 알 수 있는 것")

graph3_comment = st.text_area(
    "이 그래프로 알 수 있는 내용을 직접 작성하세요.",
    placeholder="여기에 직접 작성하세요.",
    height=100,
    key="graph3_comment"
)


if graph3_comment:

    st.info(graph3_comment)


# ========================================
# 그래프 4
# 영화별 기간 내 일관객 TOP 10
# ========================================

st.divider()

st.header("🏆 그래프 4. 영화별 기간 내 일관객 TOP 10")

st.write(
    "이 기간 동안 각 영화의 일관객을 모두 더해 "
    "관객 수가 가장 많은 영화 10편을 비교합니다."
)


# ----------------------------------------
# 영화별 일관객 합계 + 10위권에 든 날수 계산
# ----------------------------------------

movie_summary = (
    df.groupby("영화명")
    .agg(
        기간_일관객_합계=("일관객", "sum"),
        10위권_등장_일수=("날짜", "nunique")
    )
    .reset_index()
)


# ----------------------------------------
# 일관객 합계 기준 TOP 10
# ----------------------------------------

top10_movies = (
    movie_summary
    .sort_values(
        "기간_일관객_합계",
        ascending=False
    )
    .head(10)
    .copy()
)


# ----------------------------------------
# 그래프용 순서 설정
# ----------------------------------------
# Plotly 가로 막대그래프에서
# 관객이 많은 영화가 위에 오도록
# 작은 값부터 정렬한 뒤 reversed 사용

top10_movies = top10_movies.sort_values(
    "기간_일관객_합계",
    ascending=True
)


# ----------------------------------------
# 가로 막대그래프
# ----------------------------------------

fig4 = px.bar(
    top10_movies,
    x="기간_일관객_합계",
    y="영화명",
    orientation="h",
    title="영화별 기간 내 일관객 TOP 10",
    labels={
        "기간_일관객_합계": "기간 내 일관객 합계",
        "영화명": "영화"
    },
    custom_data=[
        "10위권_등장_일수"
    ]
)


# ----------------------------------------
# 마우스를 올렸을 때 표시되는 정보
# ----------------------------------------

fig4.update_traces(
    hovertemplate=
    "영화: %{y}<br>"
    "기간 내 일관객 합계: %{x:,}명<br>"
    "개봉 후 10위권에 든 날수: %{customdata[0]}일"
    "<extra></extra>"
)


fig4.update_layout(
    height=600,
    xaxis_title="기간 내 일관객 합계(명)",
    yaxis_title="영화",
    yaxis={
        "categoryorder": "array",
        "categoryarray": top10_movies["영화명"].tolist()
    }
)


st.plotly_chart(
    fig4,
    use_container_width=True
)


# ----------------------------------------
# TOP 10 표
# ----------------------------------------

st.write("### 🏆 영화별 TOP 10")


top10_display = top10_movies.copy()

top10_display["순위"] = range(
    10,
    0,
    -1
)

top10_display = top10_display.sort_values(
    "순위"
)

top10_display = top10_display[
    [
        "순위",
        "영화명",
        "기간_일관객_합계",
        "10위권_등장_일수"
    ]
]

top10_display = top10_display.rename(
    columns={
        "영화명": "영화",
        "기간_일관객_합계": "기간 내 일관객 합계",
        "10위권_등장_일수": "10위권에 든 날수"
    }
)


st.dataframe(
    top10_display,
    hide_index=True,
    use_container_width=True
)


# ----------------------------------------
# 그래프 4 설명 입력
# ----------------------------------------

st.subheader("💡 이 그래프로 알 수 있는 것")

graph4_comment = st.text_area(
    "이 그래프로 알 수 있는 내용을 직접 작성하세요.",
    placeholder="여기에 직접 작성하세요.",
    height=100,
    key="graph4_comment"
)


if graph4_comment:

    st.info(graph4_comment)


# ========================================
# 그래프 5
# 앞으로 추가할 공간
# ========================================

st.divider()

st.header("📉 그래프 5")

st.write(
    "앞으로 새로운 그래프를 추가할 수 있는 공간입니다."
)


graph5_comment = st.text_area(
    "이 그래프로 알 수 있는 것",
    placeholder="그래프를 추가한 뒤 이곳에 내용을 직접 작성하세요.",
    height=100,
    key="graph5_comment"
)


if graph5_comment:

    st.info(graph5_comment)
