from PIL import Image  # 이미지 처리 라이브러리
import numpy as np  # 수치 라이브러리
import matplotlib.pyplot as plt  # 그래프를 그리기 위한 라이브러리

imgCtrl = Image.open("Expression_ctrl.png")
imgL5 = Image.open("Expression_L5.png")

plt.imshow(imgCtrl)
plt.show()

plt.imshow(imgL5)
plt.show()

imgCtrlGray = imgCtrl.convert('L')
imgL5Gray = imgL5.convert('L')

print(imgCtrlGray.size)
print(imgL5Gray.size)

singleImgSize = (32, 32)
imgCount = 6
multipleImgSize = (singleImgSize[0]*imgCount, singleImgSize[1])

imgCtrlGray = imgCtrlGray.resize(multipleImgSize)  # 이미지 크기를 (32*6, 32)로 변환
imgL5Gray = imgL5Gray.resize(multipleImgSize)

imgListCtrl = []
imgListL5 = []

# Image를 6개로 잘라서 imgList에 저장
for i in range(imgCount):
    startPixel = i * singleImgSize[0]
    endPixel = (i+1) * singleImgSize[0]
    extractArea = (startPixel, 0, endPixel, singleImgSize[1])
    # print(extractArea)
    extractImgCtrl = imgCtrlGray.crop(extractArea)
    extractImgL5 = imgL5Gray.crop(extractArea)
    imgListCtrl.append(extractImgCtrl)  # 자른 이미지를 imgListCtrl에 추가
    imgListL5.append(extractImgL5)  # 자른 이미지를 imgListL5에 추가

f, axarr = plt.subplots(2,imgCount,figsize=(6,3))
for i in range(imgCount):
    axarr[0][i].imshow(imgListCtrl[i], cmap="gray")
    axarr[1][i].imshow(imgListL5[i], cmap="gray")
plt.tight_layout()
plt.show()

imgSaveFlag = False  # 저장하고 싶다면 True로 변경
if imgSaveFlag:
    for i, (imgC, imgL) in enumerate(zip(imgListCtrl, imgListL5)):
        fileNameCtrl = "ExprCtrl_" + str(i) + ".jpg"
        fileNameL5 = "ExprL5_" + str(i) + ".jpg"
        imgC.save(fileNameCtrl)
        imgL.save(fileNameL5)

intensityCtrl = []
intensityL5 = []

for imCtrl, imL5 in zip(imgListCtrl, imgListL5):
    arrCtrl = np.array(imCtrl)  # 이미지를 numpy.array로 변환
    arrL5 = np.array(imL5)  # 이미지를 numpy.array로 변환
    arrCtrlSum = np.sum(255 - arrCtrl)  # 255에서 각 행렬의 값을 뺀 후 모든 요소의 값을 더함
    arrL5Sum = np.sum(255 -  arrL5)  # 255에서 각 행렬의 값을 뺀 후 모든 요소의 값을 더함
    intensityCtrl.append(arrCtrlSum)  # 총 합을 sumListCtrl에 추가
    intensityL5.append(arrL5Sum)  # 총 합을 sumListL5에 추가
    
intensityCtrl = np.array(intensityCtrl)
intensityL5 = np.array(intensityL5)
normIntensityCtrl = intensityCtrl/intensityCtrl.max()*100  # 각 이미지마다 총 합을 최대값으로 normalization
normIntensityL5 = intensityL5/intensityL5.max()*100  # 각 이미지마다 총 합을 최대값으로 normalization
print(normIntensityCtrl)
print(normIntensityL5)

time = np.array([0, 10, 20, 30, 40, 60])  # 시간축 생성을 위한 배열
plt.xlabel("CHX(min)")
plt.ylabel("Relative Amount of p53 (%)")
plt.plot(time, normIntensityCtrl, time, normIntensityL5, marker='o')
plt.show()