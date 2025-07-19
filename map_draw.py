from matplotlib.axes import Axes
from matplotlib.figure import Figure
# import matplotlib.pyplot as plt
import matplotlib.pyplot
from mas_map import merge_data


def draw_map(df_merge) -> tuple[Figure, Axes]:
    fig, ax = matplotlib.pyplot.subplots(figsize=(10, 10))
    # 그리드 라인
    ax.set_xticks(range(1, df_merge['x'].max() + 1))
    ax.set_yticks(range(1, df_merge['y'].max() + 1))

    ax.grid(True)
    ax.set_ylim(df_merge['y'].max() + .5, .5)

    # 구조물 종류별 표시
    # 아파트와 빌딩 - 갈색 원형
    apartment_building = df_merge[df_merge['category'].isin(['Apartment', 'Building'])]
    ax.scatter(apartment_building['x'], apartment_building['y'], color = 'brown', marker = 'o', label = 'Apartment/Building', s = 200)

    # 반달곰 커피점 - 녹색 사각형
    bandalgom_coffee = df_merge[df_merge['category'] == 'BandalgomCoffee']
    ax.scatter(bandalgom_coffee['x'], bandalgom_coffee['y'], color = 'green', marker = 's', label = 'BandalgomCoffee', s = 200)

    # 내 집 - 녹색 삼각형
    myhome = df_merge[df_merge['category'] == 'MyHome']
    ax.scatter(myhome['x'], myhome['y'], color = 'green', marker = '^', label = 'MyHome', s = 200)

    # 건설 현장 - 회색 사각형 (겹쳐서 표시)
    construction_sites = df_merge[df_merge['ConstructionSite'] == 1]
    ax.scatter(construction_sites['x'], construction_sites['y'], color = 'grey', marker = 's', label = 'ConstructionSite', s = 200)

    # 레이블, 타이틀 추가
    ax.set_title('locale map, visualized', fontsize = 16)
    ax.set_xlabel('X coord', fontsize = 12)
    ax.set_ylabel('Y coord', fontsize = 12)

    # 범례
    ax.legend(fontsize = 8, markerscale = .5, borderpad = 1, labelspacing = 1.5)

    return (fig, ax)


def visualize() -> None:
    try:
        df_merge = merge_data()
        fig, ax = draw_map(df_merge)
        fig.savefig('map.png', dpi = 300)
        matplotlib.pyplot.show()
    except Exception as e:
        print(f'Error: {str(e)}')


def main():
    try:
        visualize()
    except Exception as e:
        print(f'Error: {str(e)}')


if __name__ == '__main__':
    main()
