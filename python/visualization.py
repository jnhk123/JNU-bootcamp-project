import matplotlib.pyplot as plt
import pandas as pd

plt.rcParams['font.family'] = 'Malgun Gothic'
plt.rcParams['axes.unicode_minus'] = False


def group_by_gu_and_draw_bar(df):
    # '요금정보' 컬럼의 '-' 값을 '정보없음'으로 변경
    df = df.copy()
    df['요금정보'] = df['요금정보'].replace('-', '정보없음')

    # '구'별로 '요금정보'의 갯수를 피벗 테이블로 만듭니다.
    pivot = df.pivot_table(index='구', columns='요금정보', aggfunc='size', fill_value=0)
    # 총 갯수 계산
    pivot['총갯수'] = pivot.sum(axis=1)
    # 총갯수를 기준으로 정렬
    pivot = pivot.sort_values('총갯수', ascending=False)

    # Figure와 Axes 생성
    fig, ax = plt.subplots(figsize=(10, 6))

    # x축: 각 '구'의 인덱스 (문자열)
    x = range(len(pivot.index))

    # '무료', '유료', '정보없음' 값 추출 (없을 경우 0으로 채움)
    free_counts = pivot.get('무료', pd.Series([0] * len(pivot.index), index=pivot.index))
    paid_counts = pivot.get('유료', pd.Series([0] * len(pivot.index), index=pivot.index))
    no_info_counts = pivot.get('정보없음', pd.Series([0] * len(pivot.index), index=pivot.index))

    # 스택형 바 차트 그리기: 먼저 무료, 그 위에 유료, 그 위에 정보없음 (누적)
    ax.bar(x, free_counts, label='무료')
    ax.bar(x, paid_counts, bottom=free_counts, label='유료')
    ax.bar(x, no_info_counts, bottom=free_counts + paid_counts, label='정보없음')

    # 각 막대 위에 총 갯수를 표기
    for i, total in enumerate(pivot['총갯수']):
        ax.text(i, total + 0.5, str(total), ha='center', va='bottom', fontsize=10)

    # x축 눈금 및 레이블 설정 (구 이름 표시)
    ax.set_xticks(x)
    ax.set_xticklabels(pivot.index, rotation=0, ha='right')

    ax.set_xlabel('구')
    ax.set_ylabel('건수')
    ax.set_title('구별 건수 및 요금정보 분포 (총갯수, 무료, 유료, 정보없음)')
    ax.legend()

    total = free_counts + paid_counts + no_info_counts;
    y = ((total.max() + 10) // 10) * 10

    ax.set_ylim(0, y)

    return fig


def fee_info_pie_chart(df):
    # '요금정보' 컬럼에서 '-' 값을 '정보 없음'으로 대체
    fee_series = df['요금정보'].replace('-', '정보 없음')
    # 각 요금정보별 건수 집계
    counts = fee_series.value_counts()
    total = counts.sum()

    # Figure와 Axes 생성
    fig, ax = plt.subplots(figsize=(8, 8))

    # autopct 함수: 비율과 실제 건수를 함께 표시
    def autopct_format(pct):
        count = int(round(pct / 100.0 * total))
        return '{:.1f}%\n({:d})'.format(pct, count)

    wedges, texts, autotexts = ax.pie(
        counts,
        labels=counts.index,
        autopct=autopct_format,
        startangle=90
    )

    # 차트 제목에 총 건수도 표기
    ax.set_title(f'요금정보 분포 (총 {total}건)', fontsize=14)

    return fig
