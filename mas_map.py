import pandas as pd
from typing import Optional
from pandas.api.types import is_integer_dtype, is_string_dtype


def read_file_to_dataframe(
    path: str,
    skipinitialspace: bool = True,
    expected_columns: Optional[list[str]] = None,
    column_types: Optional[dict[str, type]] = None
) -> pd.DataFrame:
    '''CSV 파일을 읽고 컬럼 이름의 공백을 제거한 후, 기대하는 컬럼과 타입을 검증합니다.'''
    try:
        data_frame = pd.read_csv(path, skipinitialspace = skipinitialspace)
        data_frame.columns = data_frame.columns.str.strip()

        # 기대하는 컬럼 확인
        if expected_columns:
            missing_columns = [col for col in expected_columns if col not in data_frame.columns]
            if missing_columns:
                raise ValueError(f'Missing expected columns in {path}: {missing_columns}')

        # 타입 확인
        if column_types:
            for col, expected_type in column_types.items():
                if col in data_frame.columns:
                    if expected_type == int and not is_integer_dtype(data_frame[col]):
                        raise TypeError(f'Column "{col}" in {path} is not of type int')
                    elif expected_type == str and not is_string_dtype(data_frame[col]):
                        raise TypeError(f'Column "{col}" in {path} is not of type str')

        return data_frame

    except FileNotFoundError as e:
        raise ValueError(f'File not found: {path}') from e
    except Exception as e:
        raise ValueError(f'Error while reading and validating CSV at {path}: {e}') from e


def merge_data() -> pd.DataFrame:
    '''여러 데이터를 읽고 병합하여 최종 DataFrame을 반환합니다.'''
    try:
        df_category = read_file_to_dataframe(
            'data/csv/area_category.csv',
            expected_columns = ['category', 'struct'],
            column_types = {'category': int, 'struct': str}
        )
        df_struct = read_file_to_dataframe(
            'data/csv/area_struct.csv',
            expected_columns = ['x', 'y', 'category', 'area'],
            column_types = {'x': int, 'y': int, 'category': int, 'area': int}
        )
        df_map = read_file_to_dataframe(
            'data/csv/area_map.csv',
            expected_columns = ['x', 'y', 'ConstructionSite'],
            column_types = {'x': int, 'y': int, 'ConstructionSite': int}
        )

        try:
            category_map = dict(zip(df_category['category'], df_category['struct']))
        except KeyError as e:
            raise ValueError(f'Missing expected key in category DataFrame: {e}') from e

        df_struct['category'] = df_struct['category'].apply(lambda x: category_map.get(x, x))

        df_merge = df_struct.merge(df_map, on = ['x', 'y'], how = 'left')

        # 병합 후 컬럼 확인
        if 'ConstructionSite' not in df_merge.columns:
            raise ValueError('Merged DataFrame does not contain "ConstructionSite" column.')

        df_merge = df_merge[['x', 'y', 'area', 'category', 'ConstructionSite']]

        return df_merge

    except (ValueError, TypeError):
        raise
    except Exception as e:
        raise RuntimeError(f'Unexpected error during merge: {e}') from e


def main():
    '''메인 진입점'''
    try:
        data = merge_data()
        filtered_area_1 = data[data['area'] == 1]

        if filtered_area_1.empty:
            print('⚠️  Warning: No data found for area == 1')

    except Exception as e:
        print(f'❌ Error: {e}')
    else:
        print(filtered_area_1)
        return data


if __name__ == '__main__':
    main()
