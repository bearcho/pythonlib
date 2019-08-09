from sklearn import svm, metrics
import pandas as pd
from sklearn.model_selection import train_test_split

#1. classifire 선택 머신 러닝 알고리즘 선택
clf = svm.LinearSVC()

#2. 데이터 준비하기(정제, 분리)
csv = pd.read_csv('data/iris.csv')
# train_data = csv.iloc[0:120, 0:-1]
# train_label = csv.iloc[0:120, [-1]]
# test_data = csv.iloc[120:, 0:-1]
# test_label = csv.iloc[120:, [-1]]
data = csv.iloc[:, 0:-1]
label = csv.iloc[:, [-1]]

train_data, test_data, train_label, test_label = \
    train_test_split(data, label)


#3. 데이터로 훈련시키기
clf.fit(train_data,train_label.values.ravel())

#4. 정답률(신뢰도)를 확인하기
result = clf.predict(test_data)
score = metrics.accuracy_score(result,test_label)
print('정답률 : ' , '{0:.2f}%'.format(score*100))
#5. 길거리의 곷을 꺽어서 물어보기


myIris = [4.1, 3.3, 1.5 , 0.2]
result = clf.predict([myIris])
print(result)