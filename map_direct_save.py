from mas_map import merge_data
from map_draw import draw_map
import matplotlib.pyplot
import pandas
from collections import deque
import csv


def bfs(df: pandas.DataFrame, start, goal) -> list:
    max_x = df['x'].max()
    max_y = df['y'].max()

    grid = [[1 for _ in range(max_x + 1)] for _ in range(max_y + 1)]
    for _, row in df.iterrows():
        if row['ConstructionSite'] == 1:
            grid[row['y']][row['x']] = 0  # 통과 불가

    visited = [[False for _ in range(max_x + 1)] for _ in range(max_y + 1)]
    parent = {}

    queue = deque()
    queue.append(start)
    visited[start[1]][start[0]] = True

    directions = [(-1,0),(1,0),(0,-1),(0,1)]  # 좌우상하

    while queue:
        x, y = queue.popleft()
        if (x, y) == goal:
            path = []
            while (x, y) != start:
                path.append((x, y))
                x, y = parent[(x, y)]
            path.append(start)
            path.reverse()
            return path

        for dx, dy in directions:
            nx, ny = x + dx, y + dy
            if 1 <= nx <= max_x and 1 <= ny <= max_y:
                if not visited[ny][nx] and grid[ny][nx] == 1:
                    visited[ny][nx] = True
                    parent[(nx, ny)] = (x, y)
                    queue.append((nx, ny))

    return None  # 경로 없음



def save_path_to_csv(path):
    try:
        with open('home_to_cafe.csv', 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(['x', 'y'])
            for x, y in path:
                writer.writerow([x, y])
    except Exception as e:
        raise e


def visualize():
    df_merge = merge_data()
    starts = df_merge[df_merge['category'] == 'MyHome']
    goals = df_merge[df_merge['category'] == 'BandalgomCoffee']

    paths = []
    for _, start_row in starts.iterrows():
        start = (start_row['x'], start_row['y'])

        for _, goal_row in goals.iterrows():
            goal = (goal_row['x'], goal_row['y'])
            path = bfs(df_merge, start, goal)
            if path:
                paths.append(path)

    if paths:
        shortest_path = min(paths, key=len)
        if shortest_path:
            save_path_to_csv(shortest_path)
            fig, ax = draw_map(df_merge, shortest_path)
            fig.savefig('map_final.png', dpi = 300)

    matplotlib.pyplot.show()

    print('')


def main():
    try:
        visualize()
    except Exception as e:
        print(f'Error: {str(e)}')


if __name__ == '__main__':
    main()
