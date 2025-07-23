from typing import Tuple, Optional
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.figure import Figure
from matplotlib.axes import Axes

from caffee_map import merge_data


def draw_map(df_merge: pd.DataFrame, path: Optional[list[Tuple[int, int]]] = None) -> Tuple[Figure, Axes]:
    '''지도 위에 구조물 정보를 시각화하고, 경로가 주어지면 함께 표시합니다.'''
    if df_merge.empty:
        raise ValueError('❌ df_merge is empty. Cannot draw map.')

    required_columns = {'x', 'y', 'category', 'ConstructionSite'}
    if not required_columns.issubset(df_merge.columns):
        missing = required_columns - set(df_merge.columns)
        raise ValueError(f'❌ draw_map: Missing required columns: {missing}')

    fig, ax = plt.subplots(figsize = (10, 10))

    # 그리드 라인
    ax.set_xticks(range(1, df_merge['x'].max() + 1))
    ax.set_yticks(range(1, df_merge['y'].max() + 1))
    ax.grid(True)

    ax.set_xlim(0.5, df_merge['x'].max() + 0.5)
    ax.set_ylim(df_merge['y'].max() + 0.5, 0.5)

    # 구조물 종류별 표시
    apartment_building = df_merge[df_merge['category'].isin(['Apartment', 'Building'])]
    ax.scatter(apartment_building['x'], apartment_building['y'],
               color = 'brown', marker = 'o', label = 'Apartment/Building', s = 200)

    bandalgom_coffee = df_merge[df_merge['category'] == 'BandalgomCoffee']
    ax.scatter(bandalgom_coffee['x'], bandalgom_coffee['y'],
               color = 'green', marker = 's', label = 'BandalgomCoffee', s = 200)

    my_home = df_merge[df_merge['category'] == 'MyHome']
    ax.scatter(my_home['x'], my_home['y'],
               color = 'green', marker = '^', label = 'MyHome', s = 200)

    construction_sites = df_merge[df_merge['ConstructionSite'] == 1]
    ax.scatter(construction_sites['x'], construction_sites['y'],
               color = 'grey', marker = 's', label = 'ConstructionSite', s = 200)

    # 경로 표시
    if path is not None:
        path_x = [p[0] for p in path]
        path_y = [p[1] for p in path]
        ax.plot(path_x, path_y, color = 'red', linewidth = 3, label = 'Path')

    # 레이블, 타이틀, 범례
    ax.set_title('Locale Map, Visualized', fontsize = 16)
    ax.set_xlabel('X Coord', fontsize = 12)
    ax.set_ylabel('Y Coord', fontsize = 12)
    ax.legend(fontsize = 8, markerscale = 0.5, borderpad = 1, labelspacing = 1.5)

    return fig, ax


def visualize() -> None:
    '''데이터를 병합하고 시각화 이미지를 생성한 뒤 화면에 출력합니다.'''
    try:
        df_merge = merge_data()
        fig, ax = draw_map(df_merge)
        try:
            fig.savefig('map.png', dpi = 300)
        except IOError as e:
            print(f'❌ Failed to save image: {e}')

        try:
            plt.show()
        except Exception as e:
            print(f'❌ Failed to display image: {e}')

    except ValueError as ve:
        print(f'Validation Error: {ve}')
    except Exception as e:
        print(f'❌ Unexpected error during visualization: {e}')


def main() -> None:
    '''메인 진입점'''
    try:
        visualize()
    except Exception as e:
        print(f'Error: {e}')


if __name__ == '__main__':
    main()
