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
    #画像の読み込み(fixed...元画像、moving...移動(目標)画像) itk.F...float
    #1次元画像(256)
    #itk.uc 8bit　  itk.f 32bit
    #fixed_image = itk.imread('ori_images/ori_images1/out_7', itk.F)
    #moving_image = itk.imread('ori_images/ori_images1/out_10', itk.F)
    #fixed_image = itk.imread('data/image_1/2022-02-16 13-33-54.345000.tif', itk.F)

    maskname = "mask/mask"+str(pati_num)+"-"+str(direction_num)+".nrrd"
    #maskname = "mask/mask9-"+str(direction_num)+".nrrd"
    if(ex==True):
        maskname = "mask/mask"+str(pati_num)+"-"+str(direction_num)+"-er2.nrrd"
    if((pati_num==2)or(pati_num==37)or(pati_num==38))and(direction_num==2)and(int(dark[counter-1])==1):
        maskname = f'mask/mask{pati_num}-2-undark.nrrd'


    if(pati_num==1):
        if(direction_num==1):
            #fixedname = 'data/image_1/2022-02-16 13-33-54.111000.tif'
            fixedname = 'normalizedimages/image1_1/normalized_1.png'
        elif(direction_num==2):
            #fixedname = 'data/image_1/2022-02-16 13-33-54.345000.tif'
            fixedname = 'normalizedimages/image1_1/normalized_2.png'
        elif(direction_num==3):
            fixedname = 'normalizedimages/image1_1/normalized_3.png'
    elif(pati_num==2):
        if(direction_num==1):
            #fixedname = 'data/image_2/2022-09-27 13-38-08.112000.tif'
            #fixedname = 'data/image_2/2022-09-27 13-42-52.917000.tif'
            fixedname = 'normalizedimages/image2_2/normalized_244.png'
        elif(direction_num==2):
            #fixedname = 'data/image_2/2022-09-27 13-38-08.347000.tif'
            #fixedname = 'data/image_2/2022-09-27 13-42-31.297000.tif'
            if(int(dark[counter-1])==-1):
                fixedname = 'normalizedimages/image2_2/normalized_137.png'
            elif(int(dark[counter-1])==1):
                fixedname = 'normalizedimages/image2_1/normalized_2.png'
            else:
                print("error in dark")
        elif(direction_num==3):
            fixedname = 'normalizedimages/image2_1/normalized_3.png'
    elif(pati_num==3):
        if(direction_num==1):
            #fixedname = 'data/image_3/2022-05-13 14-03-02.876000.tif'
            fixedname = 'normalizedimages/image3_1/normalized_1.png'
            if(ex==True):
                fixedname = 'normalizedimages/image3_2/normalized_2.png'
        elif(direction_num==2):
            #fixedname = 'data/image_3/2022-05-13 14-03-03.110000.tif'
            fixedname = 'normalizedimages/image3_1/normalized_2.png'
            if(ex==True):
                fixedname = 'normalizedimages/image3_2/normalized_3.png'
        elif(direction_num==3):
            fixedname = 'normalizedimages/image3_1/normalized_3.png'
    elif(pati_num==4):
        if(direction_num==1):
            #fixedname = 'data/image_4/2022-03-23 13-29-21.887000.tif'
            fixedname = 'normalizedimages/image4_1/normalized_3.png'
        elif(direction_num==2):
            #fixedname = 'data/image_4/2022-03-23 13-29-22.012000.tif' 
            fixedname = 'normalizedimages/image4_1/normalized_1.png'
        elif(direction_num==3):
            fixedname = 'normalizedimages/image4_1/normalized_59.png'
    elif(pati_num==5):
        if(direction_num==1):
            #fixedname = 'data/image_5/2023-01-26 13-25-48.521000.tif' 
            fixedname = 'normalizedimages/image5_1/normalized_1.png'
            if(ex==True):
                fixedname = 'normalizedimages/image5_2/normalized_1.png'
        elif(direction_num==2):
            #fixedname = 'data/image_5/2023-01-26 13-25-48.740000.tif'
            fixedname = 'normalizedimages/image5_1/normalized_2.png' 
        elif(direction_num==3):
            fixedname = 'normalizedimages/image5_1/normalized_12.png'
    elif(pati_num==6):
        if(direction_num==1):
            #fixedname = 'data/image_6/2022-07-04 13-42-00.427000.tif'
            fixedname = 'normalizedimages/image6_1/normalized_1.png'
        elif(direction_num==2):
            #fixedname = 'data/image_6/2022-07-04 13-42-00.662000.tif'
            fixedname = 'normalizedimages/image6_1/normalized_2.png'
        elif(direction_num==3):
            fixedname = 'normalizedimages/image6_1/normalized_3.png'
    elif(pati_num==7):
        if(direction_num==1):
            #fixedname = 'data/image_7/2022-06-08 13-29-02.293000.tif'
            fixedname = 'normalizedimages/image7_1/normalized_1.png'
        elif(direction_num==2):
            #fixedname = 'data/image_7/2022-06-08 13-29-02.527000.tif'
            fixedname = 'normalizedimages/image7_1/normalized_2.png'
        elif(direction_num==3):
            fixedname = 'normalizedimages/image7_1/normalized_3.png'
    elif(pati_num==8):
        if(direction_num==1):
            #fixedname = 'data/image_8/2022-08-24 13-24-46.083000.tif'
            fixedname = 'normalizedimages/image8_1/normalized_1.png'
        elif(direction_num==2):
            #fixedname = 'data/image_8/2022-08-24 13-24-46.333000.tif'
            fixedname = 'normalizedimages/image8_1/normalized_2.png'
        elif(direction_num==3):
            fixedname = 'normalizedimages/image8_1/normalized_3.png'
    elif(pati_num==9):
        if(direction_num==1):
            #fixedname = 'data/image_8/2022-08-24 13-24-46.083000.tif'
            fixedname = 'normalizedimages/image9_1/normalized_1.png'
        elif(direction_num==2):
            #fixedname = 'data/image_8/2022-08-24 13-24-46.333000.tif'
            fixedname = 'normalizedimages/image9_1/normalized_41.png'
        elif(direction_num==3):
            fixedname = 'normalizedimages/image9_1/normalized_3.png'
    elif(pati_num==10):
        if(direction_num==1):
            #fixedname = 'data/image_8/2022-08-24 13-24-46.083000.tif'
            fixedname = 'normalizedimages/image10_1/normalized_1.png'
            if(ex==True):
                fixedname = 'normalizedimages/image10_3/normalized_1.png'
        elif(direction_num==2):
            #fixedname = 'data/image_8/2022-08-24 13-24-46.333000.tif'
            fixedname = 'normalizedimages/image10_1/normalized_2.png'
        elif(direction_num==3):
            fixedname = 'normalizedimages/image10_1/normalized_3.png'
    elif(pati_num==11):
        if(direction_num==1):
            #fixedname = 'data/image_8/2022-08-24 13-24-46.083000.tif'
            fixedname = 'normalizedimages/image11_1/normalized_1.png'
            if(ex==True):
                fixedname = 'normalizedimages/image11_3/normalized_3.png'
        elif(direction_num==2):
            #fixedname = 'data/image_8/2022-08-24 13-24-46.333000.tif'
            fixedname = 'normalizedimages/image11_1/normalized_2.png'
        elif(direction_num==3):
            fixedname = 'normalizedimages/image11_1/normalized_3.png'
    elif(pati_num==12):
        if(direction_num==1):
            #fixedname = 'data/image_8/2022-08-24 13-24-46.083000.tif'
            fixedname = 'normalizedimages/image12_1/normalized_1.png'
        elif(direction_num==2):
            #fixedname = 'data/image_8/2022-08-24 13-24-46.333000.tif'
            fixedname = 'normalizedimages/image12_1/normalized_2.png'
        elif(direction_num==3):
            fixedname = 'normalizedimages/image12_1/normalized_3.png'
    elif(pati_num==13):
        if(direction_num==1):
            #fixedname = 'data/image_8/2022-08-24 13-24-46.083000.tif'
            fixedname = 'normalizedimages/image13_1/normalized_1.png'
        elif(direction_num==2):
            #fixedname = 'data/image_8/2022-08-24 13-24-46.333000.tif'
            fixedname = 'normalizedimages/image13_1/normalized_2.png'
        elif(direction_num==3):
            fixedname = 'normalizedimages/image13_1/normalized_3.png'
    elif(pati_num==14):
        if(direction_num==1):
            #fixedname = 'data/image_8/2022-08-24 13-24-46.083000.tif'
            fixedname = 'normalizedimages/image14_1/normalized_1.png'
        elif(direction_num==2):
            #fixedname = 'data/image_8/2022-08-24 13-24-46.333000.tif'
            fixedname = 'normalizedimages/image14_1/normalized_2.png'
        elif(direction_num==3):
            fixedname = None
            #fixedname = 'normalizedimages/image9_1/normalized_3.png'
    elif(pati_num==15):
        if(direction_num==1):
            #fixedname = 'data/image_8/2022-08-24 13-24-46.083000.tif'
            fixedname = 'normalizedimages/image15_1/normalized_1.png'
        elif(direction_num==2):
            #fixedname = 'data/image_8/2022-08-24 13-24-46.333000.tif'
            fixedname = 'normalizedimages/image15_1/normalized_2.png'
        elif(direction_num==3):
            fixedname = None
            #fixedname = 'normalizedimages/image9_1/normalized_3.png'
    elif(pati_num==16):
        if(direction_num==1):
            #fixedname = 'data/image_8/2022-08-24 13-24-46.083000.tif'
            fixedname = 'normalizedimages/image16_1/normalized_1.png'
        elif(direction_num==2):
            #fixedname = 'data/image_8/2022-08-24 13-24-46.333000.tif'
            fixedname = 'normalizedimages/image16_1/normalized_2.png'
        elif(direction_num==3):
            fixedname = None
            #fixedname = 'normalizedimages/image9_1/normalized_3.png'
    elif(pati_num==17):
        if(direction_num==1):
            #fixedname = 'data/image_8/2022-08-24 13-24-46.083000.tif'
            fixedname = 'normalizedimages/image17_1/normalized_1.png'
        elif(direction_num==2):
            #fixedname = 'data/image_8/2022-08-24 13-24-46.333000.tif'
            fixedname = 'normalizedimages/image17_1/normalized_2.png'
        elif(direction_num==3):
            fixedname = None
            #fixedname = 'normalizedimages/image9_1/normalized_3.png'
    elif(pati_num==18):
        if(direction_num==1):
            #fixedname = 'data/image_8/2022-08-24 13-24-46.083000.tif'
            fixedname = 'normalizedimages/image18_1/normalized_1.png'
        elif(direction_num==2):
            #fixedname = 'data/image_8/2022-08-24 13-24-46.333000.tif'
            fixedname = 'normalizedimages/image18_1/normalized_2.png'
        elif(direction_num==3):
            fixedname = 'normalizedimages/image18_1/normalized_9.png'
    elif(pati_num==19):
        if(direction_num==1):
            #fixedname = 'data/image_8/2022-08-24 13-24-46.083000.tif'
            fixedname = 'normalizedimages/image19_1/normalized_1.png'
        elif(direction_num==2):
            #fixedname = 'data/image_8/2022-08-24 13-24-46.333000.tif'
            fixedname = 'normalizedimages/image19_1/normalized_2.png'
        elif(direction_num==3):
            fixedname = 'normalizedimages/image19_1/normalized_3.png'
    elif(pati_num==23):
        if(direction_num==1):
            #fixedname = 'data/image_8/2022-08-24 13-24-46.083000.tif'
            fixedname = 'normalizedimages/image23_1/normalized_1.png'
        elif(direction_num==2):
            #fixedname = 'data/image_8/2022-08-24 13-24-46.333000.tif'
            fixedname = 'normalizedimages/image23_1/normalized_2.png'
        elif(direction_num==3):
            fixedname = 'normalizedimages/image23_1/normalized_15.png'
    elif(pati_num==24):
        if(direction_num==1):
            #fixedname = 'data/image_8/2022-08-24 13-24-46.083000.tif'
            fixedname = 'normalizedimages/image24_1/normalized_1.png'
        elif(direction_num==2):
            #fixedname = 'data/image_8/2022-08-24 13-24-46.333000.tif'
            fixedname = 'normalizedimages/image24_1/normalized_2.png'
        elif(direction_num==3):
            fixedname = 'normalizedimages/image24_1/normalized_3.png'
    elif(pati_num==25):
        if(direction_num==1):
            #fixedname = 'data/image_8/2022-08-24 13-24-46.083000.tif'
            fixedname = 'normalizedimages/image25_1/normalized_1.png'
        elif(direction_num==2):
            #fixedname = 'data/image_8/2022-08-24 13-24-46.333000.tif'
            fixedname = 'normalizedimages/image25_1/normalized_2.png'
        elif(direction_num==3):
            #fixedname = 'normalizedimages/image25_1/normalized_12.png'
            fixedname = 'normalizedimages/image25_1/normalized_6.png'
    elif(pati_num==26):
        if(direction_num==1):
            #fixedname = 'data/image_8/2022-08-24 13-24-46.083000.tif'
            fixedname = 'normalizedimages/image26_1/normalized_1.png'
        elif(direction_num==2):
            #fixedname = 'data/image_8/2022-08-24 13-24-46.333000.tif'
            fixedname = 'normalizedimages/image26_1/normalized_2.png'
        elif(direction_num==3):
            fixedname = 'normalizedimages/image26_1/normalized_9.png'
    elif(pati_num==27):
        if(direction_num==1):
            #fixedname = 'data/image_8/2022-08-24 13-24-46.083000.tif'
            fixedname = 'normalizedimages/image27_1/normalized_1.png'
        elif(direction_num==2):
            #fixedname = 'data/image_8/2022-08-24 13-24-46.333000.tif'
            fixedname = 'normalizedimages/image27_1/normalized_2.png'
        elif(direction_num==3):
            fixedname = 'normalizedimages/image27_1/normalized_3.png'
    elif(pati_num==28):
        if(direction_num==1):
            #fixedname = 'data/image_8/2022-08-24 13-24-46.083000.tif'
            fixedname = 'normalizedimages/image28_1/normalized_1.png'
        elif(direction_num==2):
            #fixedname = 'data/image_8/2022-08-24 13-24-46.333000.tif'
            fixedname = 'normalizedimages/image28_1/normalized_2.png'
        elif(direction_num==3):
            fixedname = 'normalizedimages/image28_1/normalized_3.png'
    elif(pati_num==29):
        if(direction_num==1):
            #fixedname = 'data/image_8/2022-08-24 13-24-46.083000.tif'
            fixedname = 'normalizedimages/image29_1/normalized_1.png'
        elif(direction_num==2):
            #fixedname = 'data/image_8/2022-08-24 13-24-46.333000.tif'
            fixedname = 'normalizedimages/image29_1/normalized_2.png'
        elif(direction_num==3):
            fixedname = 'normalizedimages/image29_1/normalized_3.png'
    elif(pati_num==30):
        if(direction_num==1):
            #fixedname = 'data/image_8/2022-08-24 13-24-46.083000.tif'
            fixedname = 'normalizedimages/image30_1/normalized_1.png'
        elif(direction_num==2):
            #fixedname = 'data/image_8/2022-08-24 13-24-46.333000.tif'
            fixedname = 'normalizedimages/image30_1/normalized_2.png'
        elif(direction_num==3):
            fixedname = 'normalizedimages/image30_1/normalized_3.png'
    elif(pati_num==31):
        if(direction_num==1):
            #fixedname = 'data/image_8/2022-08-24 13-24-46.083000.tif'
            fixedname = 'normalizedimages/image31_1/normalized_1.png'
        elif(direction_num==2):
            #fixedname = 'data/image_8/2022-08-24 13-24-46.333000.tif'
            fixedname = 'normalizedimages/image31_1/normalized_2.png'
        elif(direction_num==3):
            fixedname = 'normalizedimages/image31_1/normalized_3.png'
    elif(pati_num==32):
        if(direction_num==1):
            #fixedname = 'data/image_8/2022-08-24 13-24-46.083000.tif'
            fixedname = 'normalizedimages/image32_1/normalized_1.png'
        elif(direction_num==2):
            #fixedname = 'data/image_8/2022-08-24 13-24-46.333000.tif'
            fixedname = 'normalizedimages/image32_1/normalized_2.png'
        elif(direction_num==3):
            fixedname = 'normalizedimages/image32_1/normalized_3.png'
    elif(pati_num==33):
        if(direction_num==1):
            #fixedname = 'data/image_8/2022-08-24 13-24-46.083000.tif'
            fixedname = 'normalizedimages/image33_1/normalized_1.png'
        elif(direction_num==2):
            #fixedname = 'data/image_8/2022-08-24 13-24-46.333000.tif'
            fixedname = 'normalizedimages/image33_1/normalized_2.png'
        elif(direction_num==3):
            fixedname = 'normalizedimages/image33_1/normalized_3.png'
    elif(pati_num==34):
        if(direction_num==1):
            #fixedname = 'data/image_8/2022-08-24 13-24-46.083000.tif'
            fixedname = 'normalizedimages/image34_1/normalized_1.png'
        elif(direction_num==2):
            #fixedname = 'data/image_8/2022-08-24 13-24-46.333000.tif'
            fixedname = 'normalizedimages/image34_1/normalized_2.png'
        elif(direction_num==3):
            fixedname = 'normalizedimages/image34_1/normalized_3.png'
            if(ex==True):
                fixedname = "normalizedimages/image34_2/normalized_3.png"
    elif(pati_num==36):
        if(direction_num==1):
            #fixedname = 'data/image_8/2022-08-24 13-24-46.083000.tif'
            fixedname = 'normalizedimages/image36_1/normalized_1.png'
        elif(direction_num==2):
            #fixedname = 'data/image_8/2022-08-24 13-24-46.333000.tif'
            fixedname = 'normalizedimages/image36_1/normalized_2.png'
        elif(direction_num==3):
            fixedname = 'normalizedimages/image36_1/normalized_3.png'
    elif(pati_num==37):
        if(direction_num==1):
            #fixedname = 'data/image_8/2022-08-24 13-24-46.083000.tif'
            fixedname = 'normalizedimages/image37_1/normalized_1.png'
        elif(direction_num==2):
            #fixedname = 'data/image_8/2022-08-24 13-24-46.333000.tif'
            if(int(dark[counter-1])==-1):
                fixedname = 'normalizedimages/image37_1/normalized_38.png'
            elif(int(dark[counter-1])==1):
                fixedname = 'normalizedimages/image37_1/normalized_2.png'
            else:
                print("error in dark")
        elif(direction_num==3):
            #fixedname = 'normalizedimages/image37_1/normalized_3.png'
            fixedname = 'normalizedimages/image37_1/normalized_9.png'
    elif(pati_num==38):
        if(direction_num==1):
            #fixedname = 'data/image_8/2022-08-24 13-24-46.083000.tif'
            fixedname = 'normalizedimages/image38_1/normalized_1.png'
        elif(direction_num==2):
            if(int(dark[counter-1])==-1):
                fixedname = 'normalizedimages/image38_1/normalized_2.png'
            elif(int(dark[counter-1])==1):
                fixedname = 'normalizedimages/image38_1/normalized_8.png'
            else:
                print("error in dark")
        elif(direction_num==3):
            fixedname = 'normalizedimages/image38_1/normalized_3.png'
    elif(pati_num==39):
        if(direction_num==1):
            fixedname = 'normalizedimages/image39_1/normalized_1.png'
        elif(direction_num==2):
            fixedname = 'normalizedimages/image39_1/normalized_2.png'
        elif(direction_num==3):
            fixedname = 'normalizedimages/image39_1/normalized_3.png'
    elif(pati_num==40):
        if(direction_num==1):
            fixedname = 'normalizedimages/image40_1/normalized_1.png'
        elif(direction_num==2):
            fixedname = 'normalizedimages/image40_1/normalized_2.png'
        elif(direction_num==3):
            fixedname = 'normalizedimages/image40_1/normalized_3.png'
    elif(pati_num==41):
        if(direction_num==1):
            fixedname = 'normalizedimages/image41_1/normalized_1.png'
        elif(direction_num==2):
            fixedname = 'normalizedimages/image41_1/normalized_2.png'
        elif(direction_num==3):
            fixedname = 'normalizedimages/image41_1/normalized_3.png'
    elif(pati_num==42):
        if(direction_num==1):
            fixedname = 'normalizedimages/image42_1/normalized_1.png'
        elif(direction_num==2):
            fixedname = 'normalizedimages/image42_1/normalized_2.png'
        elif(direction_num==3):
            fixedname = 'normalizedimages/image42_1/normalized_3.png'



    fixed_image = itk.imread(fixedname, itk.F)
    moving_image = itk.imread(filename, itk.F)
    mask_image = itk.imread(maskname, itk.UC)
    ndimage, header = nrrd.read(maskname, index_order='F')#ndarrayを取得
    

    threshold_filter = itk.ThresholdImageFilter.New(fixed_image)
    threshold_filter.SetLower(0)  # 例えば100以上のピクセルを変換する
    threshold_filter.SetUpper(3000)
    threshold_filter.SetOutsideValue(3000)
    #threshold_filter.SetInsideValue(200) # 例えば200に変換する
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


    #parameter_map_rigid = parameter_object.GetDefaultParameterMap('rigid')
    #parameter_object.AddParameterMap(parameter_map_rigid)
    parameter_object.AddParameterFile('data/Rigid_te.txt')

    #parameter_map_affine= parameter_object.GetDefaultParameterMap('affine')
    #parameter_object.AddParameterMap(parameter_map_affine)
    parameter_object.AddParameterFile('data/Affine.txt')

    #parameter_map_bspline = parameter_object.GetDefaultParameterMap('bspline')
    #parameter_object.AddParameterMap(parameter_map_bspline)
    parameter_object.AddParameterFile('data/Bspline.txt')


    #groupwise_parameter_map = parameter_object.GetDefaultParameterMap('groupwise')
    #parameter_object.AddParameterMap(groupwise_parameter_map)


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


    #error
    #itk.imwrite(result_image, "outimages/result1-2.png")
    #mask_image = itk.imread('mask/test2-1.nrrd', itk.UC)
    img = itk.GetArrayFromImage(mask_image)
    thresh, img = cv2.threshold(img, 0, 255, cv2.THRESH_BINARY)
    #imshow(img)
    img = img.astype(np.uint8)[0]
    #img = img[0]


    #maskまるごと
    #contours = np.column_stack(np.where(img == 255))[:,::-1]

    #輪郭のみ
    contours, hierarchy = cv2.findContours(img, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    contours = contours[0].reshape(len(contours[0]), 2)

    num_points = len(contours)
    np.savetxt("fixed_points.txt", contours, fmt = "%.5f")


    # Modify the file
    with open("fixed_points.txt", 'r') as f:
        l = f.readlines()

    l.insert(0, 'point\n')
    #l.insert(1, '15000\n')
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
    #result_points = np.loadtxt('point_transformed/outputpoints.txt', dtype='str')[:,27:29].astype('int')
    #result_points = np.array(result_points).reshape(1,-1,2)
    #result_points = np.reshape(result_points,(len(result_points), 1, len(result_points[0])))

    #print(result_points)
    #x>268を268に矯正
    for num in range(len(result_points)):
        for dim in range(2):
            if(result_points[num][dim] < 0):
                result_points[num][dim] = 0
            """
            if(result_points[num][dim] > 267):
                result_points[num][dim] = 267
            """

    #(312,312)は画像サイズ，真っ黒画像に抽出した輪郭をはりつける
    black_img=np.zeros((268,268),np.uint8)
    #points = np.array([[100, 50], [120, 180], [50, 250], [270, 120], [220, 50]]).reshape(1, -1, 2)
    #print(points)
    points = np.array(result_points).reshape(1, -1, 2).astype(np.int32)
    #print(points)

    cv2.fillPoly(black_img, points, color=[255,255,255])
    #cv2.drawContours(black_img, [result_points], 0, 255, -1)

    thresh, img = cv2.threshold(black_img, 0, 1, cv2.THRESH_BINARY)

    img = np.array(list(img)).T
    
    #img = img.reshape(1, 268, 268)
    img = img.reshape(268, 268, 1)

    nrrd.write(dirname+"/movemask/movemask"+str(counter)+".nrrd", img, header)

    """
    plt.gray()
    plt.imshow(black_img)
    plt.savefig(dirname+"/movemask/movemask"+str(counter)+".png")
    #plt.show()
    plt.close()
    """

    #重心を抽出
    M = cv2.moments(black_img, False)

    if(float(M["m00"])==0):
        #print("None extract")
        x,y,x2,y2 = 0,0,0,0
        #x,y= float(M["m10"]/(M["m00"] + pow(10,-8))) , float(M["m01"]/(M["m00"] + pow(10,-8)))
        #x2,y2=int(M["m10"]/(M["m00"] + pow(10,-8))) , int(M["m01"]/(M["m00"] + pow(10,-8)))
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


"""
datalist = ["1_1", "1_2", "1_3", "1_4", "1_5", "1_6", "2_1", "2_2", "3_1", "3_2", "3_3", 
            "4_1", "4_2", "4_3", "5_1", "5_2", "5_3", "5_4", "6_1", "6_2", "6_3", "7_1", 
            "8_1", "8_2", "8_3"]  
datalist = ["9_1", "9_2", "9_3", "10_1", "10_2", "10_3", "11_1", "11_2", 
            "12_1", "12_2", "12_3", "13_1", "13_2", "14_1", "15_1", 
            "16_1", "16_2", "17_1", "18_1", "18_2", "18_3", "18_4", "19_1", "19_2"]
datalist = ["27_1", "28_1", "29_1", "30_1"] ["31_1", "31_2", "32_1", "32_2", "32_3", "33_1", "34_1"]
"24_1", "24_2", "24_3", "24_4", "25_1", "25_2", "26_1", "26_2", "26_3", "26_4"
"""

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
