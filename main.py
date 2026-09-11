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

# 요일 추출
# weekday()는 월요일=0, 일요일=6
weekday_order = [
    "월요일",
    "화요일",
    "수요일",
    "목요일",
    "금요일",
    "토요일",
    "일요일"
]

heatmap_df["요일"] = (
    heatmap_df["날짜"]
    .dt.weekday
    .map(lambda x: weekday_order[x])
)


# ----------------------------------------
# 월 × 요일별 일관객 합계 계산
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
# 히트맵용 피벗 테이블
# ----------------------------------------

heatmap_pivot = monthly_weekday.pivot(
    index="월",
    columns="요일",
    values="일관객"
)

# 요일을 월요일 → 일요일 순서로 정렬
heatmap_pivot = heatmap_pivot.reindex(
    columns=weekday_order
)

# 월을 1월 → 12월 순서로 정렬
heatmap_pivot = heatmap_pivot.sort_index()


# ----------------------------------------
# Plotly 히트맵
# ----------------------------------------

import plotly.graph_objects as go

fig5 = go.Figure(
    data=go.Heatmap(
        z=heatmap_pivot.values,
        x=heatmap_pivot.columns,
        y=[f"{month}월" for month in heatmap_pivot.index],
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
