from typing import List, Tuple, Optional
import pandas as pd
import matplotlib.pyplot as plt
import csv

from caffee_map import merge_data
from map_draw import draw_map


def astar(df: pd.DataFrame, start: Tuple[int, int], goal: Tuple[int, int]) -> Optional[List[Tuple[int, int]]]:
    '''A* 알고리즘으로 최단 경로를 탐색합니다.'''
    max_x = df['x'].max()
    max_y = df['y'].max()

    # 모든 칸을 0(막힘)으로 초기화
    grid = [[0 for _ in range(max_x + 1)] for _ in range(max_y + 1)]

    # df에 있는 좌표 중 ConstructionSite == 0 인 곳만 1(통과 가능)으로 설정
    for _, row in df.iterrows():
        if row['ConstructionSite'] == 0:
            grid[row['y']][row['x']] = 1

    def heuristic(a: Tuple[int, int], b: Tuple[int, int]) -> int:
        return abs(a[0] - b[0]) + abs(a[1] - b[1])

    open_list = [(start, 0, heuristic(start, goal))]  # (좌표, g, f)
    came_from = {}
    visited = set()

    while open_list:
        # f 값이 가장 작은 노드 선택
        current, g_cost, f_cost = min(open_list, key = lambda x: x[2])
        open_list.remove((current, g_cost, f_cost))

        if current == goal:
            path = [current]
            while current in came_from:
                current = came_from[current]
                path.append(current)
            path.reverse()
            return path

        visited.add(current)

        for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            nx, ny = current[0] + dx, current[1] + dy
            neighbor = (nx, ny)

            if not (0 <= nx <= max_x and 0 <= ny <= max_y):
                continue
            if grid[ny][nx] == 0 or neighbor in visited:
                continue

            new_g = g_cost + 1
            new_f = new_g + heuristic(neighbor, goal)

            # 기존보다 더 나은 경로면 갱신
            for i, (n, g_old, f_old) in enumerate(open_list):
                if n == neighbor:
                    if new_f < f_old:
                        open_list[i] = (neighbor, new_g, new_f)
                        came_from[neighbor] = current
                    break
            else:
                open_list.append((neighbor, new_g, new_f))
                came_from[neighbor] = current

    return None


def save_path_to_csv(path: List[Tuple[int, int]]) -> None:
    '''경로 데이터를 CSV 파일로 저장합니다.'''
    try:
        with open('home_to_cafe.csv', 'w', newline = '') as f:
            writer = csv.writer(f)
            writer.writerow(['x', 'y'])
            for x, y in path:
                writer.writerow([x, y])
    except Exception as e:
        raise RuntimeError(f'Error saving CSV: {e}') from e


def visualize() -> None:
    '''지도 데이터 시각화 및 경로 탐색 실행'''
    try:
        df_merge = merge_data()
    except Exception as e:
        print(f'Error loading and merging data: {e}')
        return

    starts = df_merge[df_merge['category'] == 'MyHome']
    goals = df_merge[df_merge['category'] == 'BandalgomCoffee']

    if starts.empty:
        print('Warning: No start points (MyHome) found.')
        return
    if goals.empty:
        print('Warning: No goal points (BandalgomCoffee) found.')
        return

    paths = []

    for _, start_row in starts.iterrows():
        start = (start_row['x'], start_row['y'])

        for _, goal_row in goals.iterrows():
            goal = (goal_row['x'], goal_row['y'])
            path = astar(df_merge, start, goal)
            if path and len(path) > 0:
                paths.append(path)

    if not paths:
        print('No valid paths found between start and goal points.')
        return

    shortest_path = min(paths, key = len)

    try:
        save_path_to_csv(shortest_path)
    except RuntimeError as e:
        print(f'Failed to save path CSV: {e}')

    try:
        fig, ax = draw_map(df_merge, shortest_path)
        fig.savefig('map_final.png', dpi = 300)
    except Exception as e:
        print(f'Failed to save or draw map: {e}')

    try:
        plt.show()
    except Exception as e:
        print(f'Failed to display plot: {e}')


def main() -> None:
    try:
        visualize()
    except Exception as e:
        print(f'Error: {e}')


if __name__ == '__main__':
    main()
