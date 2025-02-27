import matplotlib.pyplot as plt

plt.rcParams['font.family'] = 'Malgun Gothic'
plt.rcParams['axes.unicode_minus'] = False


def group_by_gu_and_draw_bar(df):
    grouped = df.groupby('구').size()

    # Figure와 Axes 생성
    fig, ax = plt.subplots(figsize=(8, 6))

    # 막대 차트
    bars = ax.bar(grouped.index, grouped.values)

    # 막대 위에 텍스트 표시
    for bar in bars:
        height = bar.get_height()
        ax.text(
            bar.get_x() + bar.get_width() / 2,  # x 위치: 막대 중앙
            height,  # y 위치: 막대 높이
            f'{height}',  # 표시할 텍스트
            ha='center',  # 수평 중앙 정렬
            va='bottom'  # 텍스트가 막대 위에 위치하도록 설정
        )

    ax.set_xlabel('구')
    ax.set_ylabel('건수')
    ax.set_title('구별 건수 분포')

    # fig 반환
    return fig