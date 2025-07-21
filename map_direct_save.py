from mas_map import merge_data
from map_draw import draw_map
import matplotlib.pyplot
import pandas
# from collections import deque
import csv


def astar(df: pandas.DataFrame, start, goal) -> list:
    max_x = df['x'].max()
    max_y = df['y'].max()

    # 그리드 생성: 1이면 이동 가능, 0이면 불가
    grid = [[1 for _ in range(max_x + 1)] for _ in range(max_y + 1)]
    for _, row in df.iterrows():
        if row['ConstructionSite'] == 1:
            grid[row['y']][row['x']] = 0

    def heuristic(a, b):
        return abs(a[0] - b[0]) + abs(a[1] - b[1])  # 맨해튼 거리

    open_list = [(start, 0, heuristic(start, goal))]  # (좌표, g, f)
    came_from = {}
    visited = set()

    while open_list:
        # f 값이 가장 낮은 노드 선택
        current, g_cost, f_cost = min(open_list, key=lambda x: x[2])
        open_list.remove((current, g_cost, f_cost))

        if current == goal:
            path = [current]
            while current in came_from:
                current = came_from[current]
                path.append(current)
            path.reverse()
            return path

        visited.add(current)

        for dx, dy in [(-1,0), (1,0), (0,-1), (0,1)]:
            nx, ny = current[0] + dx, current[1] + dy
            neighbor = (nx, ny)
            if not (1 <= nx <= max_x and 1 <= ny <= max_y):
                continue
            if grid[ny][nx] == 0 or neighbor in visited:
                continue

            new_g = g_cost + 1
            new_f = new_g + heuristic(neighbor, goal)

            # open_list에 이미 있다면 더 좋은 경로인지 확인
            found = False
            for i, (n, g_old, f_old) in enumerate(open_list):
                if n == neighbor:
                    found = True
                    if new_f < f_old:
                        open_list[i] = (neighbor, new_g, new_f)
                        came_from[neighbor] = current
                    break

            if not found:
                open_list.append((neighbor, new_g, new_f))
                came_from[neighbor] = current

    return None


# def bfs(df: pandas.DataFrame, start, goal) -> list:
#     max_x = df['x'].max()
#     max_y = df['y'].max()

#     grid = [[1 for _ in range(max_x + 1)] for _ in range(max_y + 1)]
#     for _, row in df.iterrows():
#         if row['ConstructionSite'] == 1:
#             grid[row['y']][row['x']] = 0  # 통과 불가

#     visited = [[False for _ in range(max_x + 1)] for _ in range(max_y + 1)]
#     parent = {}

#     queue = deque()
#     queue.append(start)
#     visited[start[1]][start[0]] = True

#     directions = [(-1,0),(1,0),(0,-1),(0,1)]  # 좌우상하

#     while queue:
#         x, y = queue.popleft()
#         if (x, y) == goal:
#             path = []
#             while (x, y) != start:
#                 path.append((x, y))
#                 x, y = parent[(x, y)]
#             path.append(start)
#             path.reverse()
#             return path

#         for dx, dy in directions:
#             nx, ny = x + dx, y + dy
#             if 1 <= nx <= max_x and 1 <= ny <= max_y:
#                 if not visited[ny][nx] and grid[ny][nx] == 1:
#                     visited[ny][nx] = True
#                     parent[(nx, ny)] = (x, y)
#                     queue.append((nx, ny))

#     return None  # 경로 없음


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
