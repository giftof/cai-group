import pandas as pd
import matplotlib.pyplot as plt
# from coffe_map import Serching_Analysis
from mas_map import merge_data

def setup_coordinate_system(ax, data):
    """
    좌표계 설정: 좌측 상단이 (1,1), 우측 하단이 가장 큰 좌표
    """
    
    # 데이터 범위 확인
    x_min, x_max = data['x'].min(), data['x'].max()
    y_min, y_max = data['y'].min(), data['y'].max()
    
    # y축을 뒤집어서 작은 값이 위쪽에 오도록 설정
    ax.invert_yaxis()
    
    # 축 범위 설정 (여백 0.5 추가)
    ax.set_xlim(x_min - 0.5, x_max + 0.5)
    ax.set_ylim(y_max + 0.5, y_min - 0.5)
    
    # 축 라벨 및 제목 설정
    ax.set_title('map Area-1')
    ax.set_xlabel('X position (WEST ← → EAST)')
    ax.set_ylabel('Y position (NORTH ↑ ↓ SOUTH)')
    
    # 격자 표시
    ax.set_xticks(range(int(data['x'].min()), int(data['x'].max())+1))
    ax.set_yticks(range(int(data['y'].min()), int(data['y'].max())+1))
    ax.grid(which='major', linestyle='--', color='gray', linewidth=0.5)
    
    return x_min, x_max, y_min, y_max

def mask_overlap(data):
    overlap_data = data[data['ConstructionSite'] == 1][['x', 'y']]
    mask = data.set_index(['x', 'y']).index.isin(overlap_data.set_index(['x', 'y']).index)
    data.loc[mask, 'ConstructionSite'] = 1
    data.loc[mask, 'category'] = ' etc'
    return data

def visualize_map(data):
    
    # 플롯 생성
    fig, ax = plt.subplots(figsize=(10, 10))
    
    # 좌표계 설정
    x_min, x_max, y_min, y_max = setup_coordinate_system(ax, data)
    
    # 카테고리별 데이터 저장
    apartments_buildings = data[data['category'].isin(['Apartment', 'Building'])]
    shops = data[data['category']=='BandalgomCoffee']
    home = data[data['category']=='MyHome']
    construction_sites = data[data['ConstructionSite']==1]

    # 겹치는 구조물 건설 현장으로 변경
    data = mask_overlap(data)
    
    # 아파트·빌딩 -> 갈색 원형
    ax.scatter(apartments_buildings['x'], apartments_buildings['y'],
               c='saddlebrown', marker='o', s=100, label=f"apartments and bulidings ({len(apartments_buildings)})")
    
    # 반달곰 커피점 -> 녹색 사각형
    ax.scatter(shops['x'], shops['y'],
               c='limegreen', marker='s', s=120, label=f"bandalgom coffee ({len(shops)})")
    
    # 집 -> 녹색 삼각형
    ax.scatter(home['x'], home['y'],
               c='green', marker='^', s=120, label="my_home")

    # 건설현장 -> 회색 사각형
    ax.scatter(construction_sites['x'], construction_sites['y'], 
              c='lightgrey', s=140, alpha=0.8, marker='s',
              label=f'construction_sites ({len(construction_sites)})', zorder=5)
    
    # 좌표계 확인용 모서리 점 표시
    corners = [(x_min, y_min), (x_max, y_min), (x_min, y_max), (x_max, y_max)]
    corner_labels = ['left_top', 'right_top', 'left_bottom', 'right_bottom']
    
    for i, (x, y) in enumerate(corners):
        ax.plot(x, y, 'ko', markersize=8)
        ax.annotate(f'{corner_labels[i]}\n({x},{y})', 
                   (x, y), xytext=(10, 10), 
                   textcoords='offset points', 
                   fontsize=8, ha='left')
    
    # 범례 표시
    ax.legend(loc='upper right', bbox_to_anchor=(1.0, 1.0))
    
    # 이미지 저장
    fig.savefig('map.png', bbox_inches='tight', dpi=300)

    # 레이아웃 조정
    plt.tight_layout()
    plt.show()
    return fig, ax

def main():
    ori_data = merge_data()
    visualize_map(ori_data)

if __name__ == '__main__':
    main()
