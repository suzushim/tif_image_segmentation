import matplotlib
matplotlib.use('Agg')
from matplotlib import pyplot as plt
import itk
import numpy as np
import cv2
import glob
import os
import nrrd

def image_95(filename="NULL", dataname="0_0", count=0):
    # 画像の読み込み
    img = cv2.imread(filename, -1)

    # 画像の最小値と最大値を取得
    min_val, max_val, _, _ = cv2.minMaxLoc(img)

    # 画像の95%の範囲を計算
    a = np.percentile(img, 2.5)
    b = np.percentile(img, 97.5)

    # 95%の範囲を0~255にスケーリング
    normalized_img = ((img - a) / (b - a)) * 255

    # 0以下の値を0に、255以上の値を255にクリップ
    normalized_img = np.clip(normalized_img, 0, 255)

    # uint8に変換
    normalized_img = normalized_img.astype(np.uint8)

    #print(normalized_img)

    # 画像の保存
    cv2.imwrite("normalizedimages/image"+dataname+"/normalized_"+str(count)+".png", normalized_img)



def image_hist(filename="NULL", dataname="0_0", count=0):

    # 画像の読み込み
    img = cv2.imread(filename, -1)

    # 画像の最小値と最大値を取得
    min_val, max_val, _, _ = cv2.minMaxLoc(img)

    # 画像のピクセル値のヒストグラムを計算
    hist = cv2.calcHist([img], [0], None, histSize=[int(max_val-min_val-30)], ranges=[min_val+30, max_val])

    # ヒストグラムのプロット
    plt.plot(hist)

    # グラフのタイトルと軸ラベルを設定
    plt.title('Pixel Values Histogram')
    plt.xlabel('Pixel Value')
    plt.ylabel('Frequency')

    # グラフを表示
    #plt.savefig("test"+str(count)+".png")
    plt.savefig("hist/image"+dataname+"/test_norm"+str(count)+".png")
    #plt.show()
    plt.close()




datalist=["39_1", "39_2", "39_3", "40_1", "40_2", "41_1", "41_2", "42_1", "42_2"]
first = True


for dataname in datalist:
    files = sorted(glob.glob("data_separate/image"+dataname+"/*"))
    dirname1 = "normalizedimages/image"+dataname

    if(first):
        os.mkdir(dirname1)
    counter=0
    for f in files:
        counter+=1
        #image_hist(f, dataname, counter)
        image_95(f, dataname, counter)
