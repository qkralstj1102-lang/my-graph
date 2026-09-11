import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go


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


movie_list = sorted(
    df["영화명"].dropna().unique()
)


selected_movie = st.selectbox(
    "영화를 선택하세요.",
    movie_list
)


movie_df = df[
    df["영화명"] == selected_movie
].copy()

movie_df = movie_df.sort_values("날짜")


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


st.subheader("💡 이 그래프로 알 수 있는 것")

graph1_comment = st.text_area(
    "이 그래프로 알 수 있는 내용을 직접 작성하세요.",
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


movie_total = (
    df.groupby("영화명", as_index=False)["일관객"]
    .sum()
    .sort_values(
        "일관객",
        ascending=False
    )
    .head(5)
)


top5_movies = movie_total["영화명"].tolist()


top5_df = df[
    df["영화명"].isin(top5_movies)
].copy()

top5_df = top5_df.sort_values(
    ["영화명", "날짜"]
)


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


daily_total = (
    df.groupby("날짜", as_index=False)["일관객"]
    .sum()
    .sort_values("날짜")
)


top3_days = (
    daily_total
    .sort_values(
        "일관객",
        ascending=False
    )
    .head(3)
)


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


# 영화별 일관객 합계
movie_sum = (
    df.groupby("영화명")["일관객"]
    .sum()
    .reset_index()
)

movie_sum = movie_sum.rename(
    columns={
        "일관객": "기간_일관객_합계"
    }
)


# 영화별 10위권 등장 일수
movie_days = (
    df.groupby("영화명")["날짜"]
    .nunique()
    .reset_index()
)

movie_days = movie_days.rename(
    columns={
        "날짜": "10위권_등장_일수"
    }
)


# 두 데이터 합치기
movie_summary = pd.merge(
    movie_sum,
    movie_days,
    on="영화명"
)


# TOP 10
top10_movies = (
    movie_summary
    .sort_values(
        "기간_일관객_합계",
        ascending=False
    )
    .head(10)
    .copy()
)


# 그래프에서는 관객 적은 순 → 많은 순
top10_movies = top10_movies.sort_values(
    "기간_일관객_합계",
    ascending=True
)


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


fig4.update_traces(
    hovertemplate=
    "영화: %{y}<br>"
    "기간 내 일관객 합계: %{x:,}명<br>"
    "10위권에 든 날수: %{customdata[0]}일"
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


# TOP 10 표
st.write("### 🏆 영화별 TOP 10")

top10_display = top10_movies.copy()

top10_display = top10_display.sort_values(
    "기간_일관객_합계",
    ascending=False
)

top10_display["순위"] = range(
    1,
    len(top10_display) + 1
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
# 월 × 요일별 일관객 합계 히트맵
# ========================================

st.divider()

st.header("🔥 그래프 5. 월 × 요일별 일관객 합계")

st.write(
    "날짜에서 월과 요일을 추출하여 "
    "각 월·요일에 기록된 일관객의 합계를 히트맵으로 나타냅니다."
)


# ----------------------------------------
# 월과 요일 추출
# ----------------------------------------

heatmap_df = df.copy()

# 월 추출
heatmap_df["월"] = heatmap_df["날짜"].dt.month

# 요일 순서
weekday_order = [
    "월요일",
    "화요일",
    "수요일",
    "목요일",
    "금요일",
    "토요일",
    "일요일"
]

# 요일 추출
heatmap_df["요일"] = heatmap_df["날짜"].dt.weekday.map(
    lambda x: weekday_order[x]
)


# ----------------------------------------
# 월 × 요일별 일관객 합계
# ----------------------------------------

monthly_weekday = (
    heatmap_df
    .groupby(
        ["월", "요일"],
        as_index=False
    )["일관객"]
    .sum()
)


# ----------------------------------------
# 히트맵용 피벗
# ----------------------------------------

heatmap_pivot = monthly_weekday.pivot(
    index="월",
    columns="요일",
    values="일관객"
)


# 월요일 → 일요일 순서
heatmap_pivot = heatmap_pivot.reindex(
    columns=weekday_order
)


# 1월 → 12월 순서
heatmap_pivot = heatmap_pivot.sort_index()


# ----------------------------------------
# 히트맵
# ----------------------------------------

fig5 = go.Figure(
    data=go.Heatmap(
        z=heatmap_pivot.values,
        x=heatmap_pivot.columns,
        y=[
            f"{month}월"
            for month in heatmap_pivot.index
        ],
        colorscale="Blues",
        colorbar=dict(
            title="일관객 합계"
        ),
        hovertemplate=
        "월: %{y}<br>"
        "요일: %{x}<br>"
        "일관객 합계: %{z:,}명"
        "<extra></extra>"
    )
)


fig5.update_layout(
    title="월 × 요일별 일관객 합계",
    height=600,
    xaxis_title="요일",
    yaxis_title="월"
)


st.plotly_chart(
    fig5,
    use_container_width=True
)


# ----------------------------------------
# 그래프 5 설명
# ----------------------------------------

st.subheader("💡 이 그래프로 알 수 있는 것")

graph5_comment = st.text_area(
    "이 그래프로 알 수 있는 내용을 직접 작성하세요.",
    placeholder="예: 특정 월의 주말에 관객 수가 많은 것을 확인할 수 있다.",
    height=100,
    key="graph5_comment"
)

if graph5_comment:
    st.info(graph5_comment)
