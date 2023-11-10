import matplotlib
matplotlib.use('Agg')
from matplotlib import pyplot as plt
import itk
import numpy as np
import cv2
import glob
import os
import nrrd
from natsort import natsorted 
import re



def registration1(filename, counter="NULL", dirname="test", pati_num=0, direction_num=0, ex = False, dark = []):
    #画像の読み込み(fixed...元画像、moving...移動(目標)画像) 
    #itk.F...float
    #itk.uc 8bit　  itk.f 32bit

    
    maskname = "mask/mask"+str(pati_num)+"-"+str(direction_num)+".nrrd"
    if(ex==True):
        maskname = "mask/mask"+str(pati_num)+"-"+str(direction_num)+"-er2.nrrd"
    if((pati_num==2)or(pati_num==37)or(pati_num==38))and(direction_num==2)and(int(dark[counter-1])==1):
        maskname = f'mask/mask{pati_num}-2-undark.nrrd'

    # 省略
    fixed_image = ...
    
      
    fixed_image = itk.imread(fixedname, itk.F)
    moving_image = itk.imread(filename, itk.F)
    mask_image = itk.imread(maskname, itk.UC)
    ndimage, header = nrrd.read(maskname, index_order='F')#ndarrayを取得

    
    #画素値を3000上限に設定
    threshold_filter = itk.ThresholdImageFilter.New(fixed_image)
    threshold_filter.SetLower(0) 
    threshold_filter.SetUpper(3000)
    threshold_filter.SetOutsideValue(3000)
    fixed_image = threshold_filter.GetOutput()
    fixed_image.Update()

    threshold_filter = itk.ThresholdImageFilter.New(moving_image)
    threshold_filter.SetLower(0)  # 例えば100以上のピクセルを変換する
    threshold_filter.SetUpper(3000)
    threshold_filter.SetOutsideValue(3000)
    #threshold_filter.SetInsideValue(200) # 例えば200に変換する
    moving_image = threshold_filter.GetOutput()
    moving_image.Update()

    # Forward Parameter Map
    # レジストレーションの手法の指定
    #groupwise_parameter_map = parameter_object.GetDefaultParameterMap('groupwise') グループワイズ

    parameter_object = itk.ParameterObject.New()

    parameter_object.AddParameterFile('data/Rigid_te.txt')
    parameter_object.AddParameterFile('data/Affine.txt')
    parameter_object.AddParameterFile('data/Bspline.txt')


    # Registration 以下引数
    """
        fixed_image: 固定画像のITK Imageオブジェクト
        moving_image: 移動画像のITK Imageオブジェクト
        parameter_file_path: elastixパラメータファイルへのパス
        output_directory: 出力ディレクトリへのパス
        output_file_prefix: 出力ファイル名のプレフィックス
        log_to_console: コンソールにログを表示するかどうかのフラグ（デフォルトはFalse）
        log_to_file: ファイルにログを保存するかどうかのフラグ（デフォルトはFalse）
        output_transform_param_file: 変換パラメータをファイルに保存する場合のファイル名（デフォルトは""）
        initial_transform_parameter_file_name : 事前に計算された変換パラメータを保存しているファイルのパスを指定
    """

    result_image, result_transform_parameters = itk.elastix_registration_method(
        fixed_image, moving_image,
        parameter_object=parameter_object,
        output_directory='exampleoutput/fwd',
        log_to_console=False
    )


    img = itk.GetArrayFromImage(mask_image)
    thresh, img = cv2.threshold(img, 0, 255, cv2.THRESH_BINARY)
    img = img.astype(np.uint8)[0]



    #maskまるごと
    #contours = np.column_stack(np.where(img == 255))[:,::-1]

    
    #maskの輪郭情報のみ取得
    contours, hierarchy = cv2.findContours(img, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    contours = contours[0].reshape(len(contours[0]), 2)

    
    num_points = len(contours)
    np.savetxt("fixed_points.txt", contours, fmt = "%.5f")


    # Modify the file
    with open("fixed_points.txt", 'r') as f:
        l = f.readlines()

    l.insert(0, 'point\n')
    l.insert(1, str(num_points)+'\n')

    with open("fixed_points.txt", 'w') as f:
        f.writelines(l)



    """
    変換パラメータを使用して、画像の変換やデフォルメーションフィールドの計算を行う
    moving_imageを変換して、output_directoryに保存
    変換された画像に対して、空間的ヤコビアン、ヤコビアンの行列式、およびデフォルメーションフィールドを計算

    moving_image: 変換対象の画像を指定します。
    transform_parameter_object: elastix_registration_methodで得られた変換パラメータを指定します。
    output_directory: 変換された画像が保存されるディレクトリを指定します。
    log_to_console: ログをコンソールに出力するかどうかを指定します。デフォルトはTrueです。
    log_file_name: ログファイルの名前を指定します。デフォルトは"transformix.log"です。
    number_of_threads: スレッド数を指定します。デフォルトは自動です。
    compute_deformation_field: デフォルメーションフィールドを計算するかどうかを指定します。デフォルトはFalseです。
    compute_spatial_jacobian: 空間的ヤコビアンを計算するかどうかを指定します。デフォルトはFalseです。
    compute_determinant_of_spatial_jacobian: 空間的ヤコビアンの行列式を計算するかどうかを指定します。デフォルトはFalseです。
    compute_deformation_field_jacobian: デフォルメーションフィールドのヤコビアンを計算するかどうかを指定します。デフォルトはFalseです。
    fixed_point_set_file_name: 固定点セットファイルの名前を指定します。デフォルトは空です。
    """


    result_image = itk.transformix_filter(
        moving_image, result_transform_parameters,
        fixed_point_set_file_name='fixed_points.txt',
        output_directory = './point_transformed')



    # for 2D 
    #[27:29]でoutputのみを出力
    result_points = np.loadtxt('point_transformed/outputpoints.txt', dtype='str')[:,27:29].astype('float64')
    
    #x<0を0に矯正
    for num in range(len(result_points)):
        for dim in range(2):
            if(result_points[num][dim] < 0):
                result_points[num][dim] = 0
            """
            if(result_points[num][dim] > 267):
                result_points[num][dim] = 267
            """

    #(268,268)は画像サイズ，真っ黒画像に抽出した輪郭をはりつける
    black_img=np.zeros((268,268),np.uint8)

    points = np.array(result_points).reshape(1, -1, 2).astype(np.int32)


    cv2.fillPoly(black_img, points, color=[255,255,255])


    thresh, img = cv2.threshold(black_img, 0, 1, cv2.THRESH_BINARY)

    img = np.array(list(img)).T
    
    img = img.reshape(268, 268, 1)

    nrrd.write(dirname+"/movemask/movemask"+str(counter)+".nrrd", img, header)

    #重心を抽出
    M = cv2.moments(black_img, False)

    if(float(M["m00"])==0):
        #print("None extract")
        x,y,x2,y2 = 0,0,0,0
    else:
        #グラフ用のx,yと画像用のx2,y2
        x,y= float(M["m10"]/M["m00"]) , float(M["m01"]/M["m00"])
        x2,y2=int(M["m10"]/M["m00"]) , int(M["m01"]/M["m00"])

    plt.gray()
    plt.imshow(moving_image)
    plt.plot(result_points[:,0], result_points[:, 1], marker="o", markersize=1, linewidth=0)
    plt.plot(x, y, marker='.', markersize=10, color='r')
    plt.savefig(dirname+"/move/move"+str(counter)+".png")
    #plt.show()
    plt.close()

    return [x, y]


def interface(dataname="0_1", savedirname = "NULL", first = True, direction_num=0, patinumber=0, diffnum=0, plane_num=3):
    #files = sorted(glob.glob("data_separate/image"+dataname+"/*"))
    files = glob.glob("normalizedimages/image"+dataname+"/*")
    counter=1
    counter2 =1

    ex = False
    dark = []
    if(dataname=="3_2"):
        ex=True
        print("a")
    if((dataname=="5_2")or(dataname=="5_3")or(dataname=="5_4")or(dataname=="10_3")or(dataname=="11_3"))and(direction_num==1):
        ex=True
        print("a")
    if((dataname=="34_2")and(direction_num==3)):
        ex=True
        print("a")
    if(dataname=="2_1")or(dataname=="2_2")or(dataname=="37_1")or(dataname=="38_1"):
        dark = np.loadtxt(f'dark_checker/darkchecker_{dataname}.txt',
                        dtype="float", skiprows=0)

    dirname = "outimage_list2/" + savedirname
    extract_list = np.array([])

    if(first):
        os.mkdir(dirname)
        os.mkdir(dirname+"/movemask")
        os.mkdir(dirname+"/move")
        os.mkdir(dirname+"/moveonly")
        os.mkdir(dirname+"/result")

    #for f in files:
    for f in natsorted(files):
        if((counter + diffnum + (plane_num-direction_num)) % plane_num == 0):
            print(f)
            #registration1(f, counter, dirname)
            #counter → f(filename)
            extract = registration1(f, counter2, dirname, pati_num=patinumber, direction_num=direction_num, ex=ex, dark = dark)
            if(counter2==1):
                extract_list = np.array([extract])
            else:
                extract_list = np.vstack([extract_list, extract])
            counter2+=1
        counter+=1
    
    listname = dirname + "/extract_list" + dataname + "_" + str(direction_num) + ".txt"
    np.savetxt(listname, extract_list, fmt = "%.8f")

    # Modify the file
    with open(listname, 'r') as f:
        l = f.readlines()

    l.insert(0, '[x, y]\n')

    with open(listname, 'w') as f:
        f.writelines(l)

    return 0



# ここに取得したい患者データを入力
datalist = ["39_1", "39_2", "39_3", "40_1", "40_2", "41_1", "41_2", "42_1", "42_2"]


for i, dataname in enumerate(datalist):
    for j in range(3):
        pati_num = int(re.findall(r"\d+", dataname)[0])
        #正面:1  側面:2
        direction_num = j+1
        #direction_num = 3
        firstFlag = True

        diff_num=0
        if(dataname=="1_2") or (dataname=="4_1") or (dataname=="11_3") or (dataname=="13_2") or(dataname=="14_1") or (dataname=="24_4") or (dataname=="25_2") or (dataname=="39_2"):
            diff_num=1
        if(dataname=="1_5") or (dataname=="3_2") or (dataname=="3_3") or (dataname=="5_3") or (dataname=="6_2") or (dataname=="8_2") or (dataname=="9_2") or (dataname=="9_3") or (dataname=="19_2"):
            diff_num=2
        
        plane_num = 3
        if(pati_num>=15)and(pati_num<=17):
            plane_num = 2

        savedirname = "normalized_out_images"+str(dataname)+"_"+str(direction_num)

        interface(dataname=dataname, first=firstFlag, savedirname=savedirname, 
                direction_num=direction_num, patinumber=pati_num, diffnum=diff_num, plane_num=plane_num)
