import numpy as np

A = np.array([[1,9,7,7,7,7],[0.11,1,0.14,0.33,0.14,0.14],[0.33,7,1,3,0.5,0.5],
              [0.11,3,0.33,1,0.25,0.25],[0.14,7,2,4,1,1],[0.14,7,1,4,1,1]]) #输入判断矩阵
(n,n) = np.shape(A)

# 算术平均法求权重
sum_1 = A.sum(axis=0) #对每一列求和
B = A/sum_1  #归一化处理
sum_2 = B.sum(axis=1) #对每一行求和
suan = sum_2/n #除N得权重
print('算术平均法所得权重为：')
print(suan)
print('\n')

#几何平均法求权重
multiply_1 = A.prod(axis=1) #按行相乘
C = np.power(multiply_1,1/n) # 开n次方
sum_1 = C.sum(axis=0)
jihe = C /sum_1
print('几何平均法所得权重为：')
print(jihe)
print('\n')

#特征值法求权重
D = np.linalg.eig(A)
max_eig = np.max(D[0]) #最大特征值
position = np.argmax(D[0]) #最大特征值位置
E = D[1]  #特征向量
E = E[:,position]
tezheng = E/sum(E) #归一化处理
print('特征法所求权重为：')
print(tezheng)
print('\n')

#计算一致性比例
CI = (max_eig - n) / (n-1)
RI = [0,0,0.52,0.89,1.12,1.26,1.36,1.41,1.46,1.49,1.52,1.54,1.56,1.58,1.59]
CR = CI / RI[n-1]
print('一致性指标CI：')
print(CI)
print('一致性比例CR：')
print(CR)
if CR<0.1:
    print('一致性可以接受')
else:
    print('一致性不可接受')
