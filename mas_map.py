import pandas as pd


def read_file_to_dataframe(path: str, skipinitialspace: bool = True) -> pd.DataFrame:
    try:
        data_frame = pd.read_csv(path, skipinitialspace=skipinitialspace)
        data_frame.columns = data_frame.columns.str.strip()
    except:
        raise ValueError(f'Error: while read_csv at {path}')
    else:
        return data_frame


def merge_data() -> pd.DataFrame:
    try:
        df_category = read_file_to_dataframe('data/csv/area_category.csv')
        df_struct = read_file_to_dataframe('data/csv/area_struct.csv')
        df_map = read_file_to_dataframe('data/csv/area_map.csv')

        category_map = dict(zip(df_category['category'], df_category['struct']))
        df_struct['category'] = df_struct['category'].apply(lambda x: category_map.get(x, x))

        df_merge = df_struct.merge(df_map, on=['x', 'y'], how='left')
        df_merge = df_merge[['x', 'y', 'area', 'category', 'ConstructionSite']]

        return df_merge
    except ValueError as e:
        raise e
    except BaseException as e:
        raise e
    except:
        raise ValueError('빵꾸똥꾸')


def main():
    try:
        data = merge_data()
        filtered_area_1 = data[data['area'] == 1]
    except ValueError as e:
        print(e)
    except Exception as e:
        print(e)
    else:
        print(filtered_area_1)
        return data


if __name__ == '__main__':
    main()
