import pandas as pd
import matplotlib.pyplot as plt
from mas_map import merge_data


def draw_map(df_merge):
    fig, ax = plt.subplots(figsize=(10, 10))

    x_max = df_merge['x'].max()
    y_max = df_merge['y'].max()
    # 그리드 라인
    ax.set_xticks(range(1, x_max + 1))
    ax.set_yticks(range(1, y_max + 1))

    ax.grid(True)
    # TODO: 이거 좀 더 확인 필요함 / 운좋게 하나씩 잘려서, 0.5 씩 더해서 된 것일수도 있으니까, set_ylim 함수 역할 알아볼것
    ax.set_ylim(y_max + 0.5, 0.5)

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
    ax.set_title('locale map, visualized', fontsize=16)
    ax.set_xlabel('X coord', fontsize=12)
    ax.set_ylabel('Y coord', fontsize=12)

    # 범례
    ax.legend(fontsize=8, markerscale=.5, borderpad=1, labelspacing=1.5)
    # ax.invert_yaxis()

    # 이미지로 저장
    plt.savefig('map.png', dpi=300)
    plt.show()


def visualize() -> None:
    try:
        df_merge = merge_data()
        draw_map(df_merge)
    except Exception as e:
        print(f'Error: {str(e)}')
    


def main():
    try:
        visualize()
    except Exception as e:
        print(f'Error: {str(e)}')


if __name__ == '__main__':
    main()
