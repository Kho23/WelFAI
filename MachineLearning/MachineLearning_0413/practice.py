from cProfile import label
from pathlib import Path
import pandas as pd
import tarfile
import urllib.request
import matplotlib.pyplot as plt
import numpy as np
from scipy.stats import alpha


def load_housing_data():
    """
    인터넷 서버에서 tgz 압축파일을 가져와서 압축 해제 후 데이터프레임으로 변환
    :return: 변환된 데이터프레임 반환
    """
    tarball_path = Path('datasets/housing.tgz') # 운영체제에 상관없이 파일 경로 관리
    if not tarball_path.is_file():
        Path('datasets').mkdir(parents=True, exist_ok=True)
        url = 'https://github.com/ageron/data/raw/main/housing.tgz'
        urllib.request.urlretrieve(url, tarball_path) # 인터넷 서버에서 파일을 가져옴
        with tarfile.open(tarball_path) as housing_tarball: # 가저온 압축파일을 압축 해제
            housing_tarball.extractall(path='datasets')

    return pd.read_csv(Path('datasets/housing/housing.csv')) # 데이터프레임 형태도 데이터 변환

housing = load_housing_data()
print(f'head 함수 결과 : {housing.head()}\n========================')
print(housing.info())
print(housing.value_counts())
print(housing.describe()) # % 붙어있는 행은 백분위수를 나타낸다

housing.hist(bins=50, figsize=(12, 8))
plt.show()

def shuffle_and_split_data(data, test_ratio):
    """
    데이터프레임과 x% 를 받아서 데이터프레임의 x% 는 테스트용 데이터로, 나머지는 머신러닝용 데이터로 쪼개어 반환
    :param data: 테스트용/머신러닝용 으로 쪼갤 데이터
    :param test_ratio: 테스트용 데이터의 비율
    :return: test_ratio 기준으로 나눠진 테스트용, 머신러닝용 데이터
    """
    shuffled_indices = np.random.permutation(len(data)) # 인덱스 무작위 설정
    test_set_size = int(len(data) * test_ratio) # 테스트 세트 크기 계산
    test_indices = shuffled_indices[:test_set_size] # 슬라이싱 20%
    train_indices = shuffled_indices[test_set_size:] # 슬라이싱 20%~끝까지
    return data.iloc[train_indices], data.iloc[test_indices] # 테스트용 데이터와 학습용 데이터를 분리하여 반환

train_set, test_set = shuffle_and_split_data(housing, 0.2)
print(len(train_set))
print(len(test_set))

from zlib import crc32

def is_id_in_test_set(identifier, test_ratio):
    """
    shuffle_and_split_data 함수가 만드는 테스트 세트는 랜덤이라 계속 변하는데
    반복해서 테스트 시 머신러닝 알고리즘이 전체 데이터를 모두 보게 되기 때문에 테스트/머신러닝용 데이터를 나누는 의미가 없어짐
    이를 방지하기 위해 각 샘플의 식별자로 해시값을 계산하여 최댓값의 20% 이하의 샘플만 테스트 세트로 보낸다.
    :param identifier:
    :param test_ratio:
    :return:
    """
    return crc32(np.int64(identifier)) < test_ratio * 2 ** 32

def split_data_with_id_hash(data, test_ratio, id_columns):
    ids = data[id_columns] # 인자로 신규 컬럼 생성
    in_test_set = ids.apply(lambda id_ : is_id_in_test_set(id_, test_ratio))
    return data.loc[~in_test_set], data.loc[in_test_set]
housing_with_id = housing.reset_index()
housing_with_id['id'] = housing['longitude'] * 1000 + housing['latitude']
train_set, test_set = split_data_with_id_hash(housing_with_id, 0.2, 'id')

from sklearn.model_selection import train_test_split

train_set, test_set = train_test_split(housing, test_size=0.2, random_state=42)

housing['income_cat'] = pd.cut(housing['median_income'],
                               bins=[0., 1.5, 3.0, 4.5, 6, np.inf],
                               labels=([1, 2, 3, 4, 5])
                               )
housing['income_cat'].value_counts().sort_index().plot.bar(rot = 0, grid = True)
plt.xlabel("소득 카테고리")
plt.ylabel('구역 개수')
plt.show()

from sklearn.model_selection import StratifiedShuffleSplit

splitter = StratifiedShuffleSplit(n_splits=10, test_size=0.2, random_state=42)
strat_split = []
for train_index, test_index in splitter.split(housing, housing['income_cat']):
    strat_train_set_n = housing.iloc[train_index]
    strat_test_set_n = housing.iloc[test_index]
    strat_split.append([strat_train_set_n, strat_test_set_n])

strat_train_set, strat_test_set = strat_split[0]

strat_test_set, strat_test_set = train_test_split(
    housing, test_size=0.2, stratify=housing['income_cat'], random_state=42
)
print(strat_test_set['income_cat'].value_counts() / len(strat_test_set))

housing = strat_train_set.copy()
housing.plot(kind = 'scatter', x = 'longitude', y = 'latitude', grid = True, alpha = 0.2)
plt.xlabel('경도')
plt.ylabel('위도')
plt.show()

housing.plot(kind='scatter', x='longitude', y='latitude', grid=True,
             s=housing['population']/100, label = '인구',
             c='median_house_value', cmap='jet', colorbar = True,
             legend = True, figsize = (10, 7)
             )
cax = plt.gcf().get_axes()[1]
plt.xlabel('경도')
plt.ylabel('위도')
plt.show()