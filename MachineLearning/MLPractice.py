import pandas as pd
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression
from sklearn.neighbors import KNeighborsRegressor

# 데이터 다운로드 및 준비
data_root = 'https://github.com/ageron/data/raw/main/'
lifesat = pd.read_csv(data_root + 'lifesat/lifesat.csv')

x_value = "GDP per capita (USD)"
y_value = 'Life satisfaction'
X = lifesat[[x_value]].values # GDP 예측을 위한 자료 즉 특성
Y = lifesat[[y_value]].values # 찾은 정답 즉 레이블 또는 타겟

# 데이터를 그래프로 표시
lifesat.plot(kind = 'scatter', grid = True,
             x = x_value , y = y_value)

plt.axis([23_500, 62_500, 4, 9])
plt.show()

# 선형모델 선택
l_model = LinearRegression() # 선형 회귀 방식으로 데이터를 분석
# 모델 훈련
l_model.fit(X, Y)

# 키프로스에 대한 예측 생성
x_new = [[37_655.2]] # 2020년 키프로스 1인당 GDP
print(l_model.predict(x_new)) # 출력 6.30165767

K_model = KNeighborsRegressor(n_neighbors=3) # 최근접 이웃 계산 방식으로 데이터를 분석

K_model.fit(X, Y)
print(K_model.predict(x_new)) # 출력 6.33333333