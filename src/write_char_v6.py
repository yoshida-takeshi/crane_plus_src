#! /usr/bin/env python
# -*- coding: utf-8 -*-
        
import rospy
import numpy as np
from time import sleep
import cv2

import move_arm_v4 as move_arm


class write_char:
    ########################################
    #INIT
    def __init__(self,ARM_ON,GRAPH_ON):
        #ARM制御ONモード[True/False]
        self.ARM_ON=ARM_ON
        #画面描画ONモード[True/False]
        self.GRAPH_ON=GRAPH_ON

        #ARM制御準備
        if self.ARM_ON==True:
            self.arm=move_arm.move_arm()
            self.arm.Step=100
            self.arm.WaitMove=False

        #パラメータ初期設定
        self.setup_param()

        if self.ARM_ON==True:
            self.arm.Step=100
            self.arm.x=(self.x_Left+self.x_Right)/2-0.04
            self.arm.y=(self.y_Top+self.y_Bottom)/2+0.04
            self.HeightUp  = self.HeightDown + self.HeightDelta
            z=self.HeightUp
            self.arm.z=self.HeightUp
            self.arm.move_xyz()
            self.arm.x=(self.x_Left+self.x_Right)/2
            self.arm.y=(self.y_Top+self.y_Bottom)/2
            self.arm.z=self.HeightDown+0.1
            self.arm.grip(0)
            self.arm.move_xyz()

        
    ########################################
    #パラメータ初期設定
    def setup_param(self):
        #描画サイズの定義
        self.CampusSizeX=0.22
        self.CampusSizeY=0.22
        self.CampusOffsetX=-0.11
        self.CampusOffsetY=+0.13
        self.x_Left   = self.CampusOffsetX
        self.x_Right  = self.CampusOffsetX + self.CampusSizeX
        self.y_Top    = self.CampusOffsetY + self.CampusSizeY
        self.y_Bottom = self.CampusOffsetY

        #文字制御関連
        self.FontSize=0.22
        self.Rotate=0 #文字回転(0-3)
        self.DeltaTh=0.0013 #移動処理スキップの閾値

        #ペン高さ設定
        self.HeightDown=0.01
        self.HeightDelta=0.1

        #画面描画用の設定
        self.Ratio=1000  #[dot/m]
        self.ImageSizeX=int(self.CampusSizeX * self.Ratio)
        self.ImageSizeY=int(self.CampusSizeY * self.Ratio)
        self.Img = np.zeros((self.ImageSizeY, self.ImageSizeX, 3), np.uint8)
        self.Img[:,:,:]=(255,255,255)
        self.Color = (0, 0, 0)
        self.Thickness = 2
        if self.GRAPH_ON==True:
            cv2.namedWindow("img")
            cv2.imshow("img", self.Img)
            cv2.waitKey(10)
        
    ########################################
    #1文字分の文字書き関数
    def write_char(self,VectData,OffsetX,OffsetY):

        ########################################
        #初期設定
        self.HeightUp  = self.HeightDown + self.HeightDelta
        z=self.HeightUp
        x0=0
        y0=0

        #Step数制御
        Step_atFirst=100 #初期移動
        Step_atJump=100 #一筆間の移動
        Step_atWrite=1 #筆記
        Step_atPenUp=50 #PEN上げ動作
        #Step_atPenDown=50 #PEN下げ動作
        Step_atPenDown=1 #PEN下げ動作
        if self.ARM_ON==True:
            self.arm.Step=Step_atFirst

        ####################
        #一筆分ずつデータ取得
        for VectData0 in VectData:
            #NULLデータの場合は処理スキップ
            if VectData0[0][0]==-100: continue
            print VectData0
                        
            ####################
            #サンプリング単位のデータ取得
            for VectData1 in VectData0: 
                #NULLデータの場合は処理スキップ
                if VectData1[0]==-100: continue
                print VectData1
                #座標算出
                #rotate 0
                x= (VectData1[0]/100.0) * self.FontSize + OffsetX
                y=-(VectData1[1]/100.0) * self.FontSize + OffsetY
                #rotate 90
                if self.Rotate==1:
                    x= (VectData1[1]/100.0) * self.FontSize + OffsetX
                    y= (VectData1[0]/100.0) * self.FontSize + OffsetY
                #rotate 180
                if self.Rotate==2:
                    x=-(VectData1[0]/100.0) * self.FontSize + OffsetX
                    y= (VectData1[1]/100.0) * self.FontSize + OffsetY
                #rotate 270
                if self.Rotate==3:
                    x=-(VectData1[1]/100.0) * self.FontSize + OffsetX
                    y=-(VectData1[0]/100.0) * self.FontSize + OffsetY

                FontFlg=VectData1[2]

                #移動量が小さい場合はスキップ
                if abs(x-x0)+abs(y-y0)<self.DeltaTh: continue

                #アームを動かす
                if self.ARM_ON == True and 0 <= FontFlg < 10:
                    self.arm.x=x
                    self.arm.y=y
                    self.arm.z=z
                    self.arm.move_xyz()
                    sleep(0.05)
                #永字八法
                #はらい
                if self.ARM_ON == True and 20 <= FontFlg < 22:
                    self.arm.x = x
                    self.arm.y = y
                    self.arm.z += 0.0001
                    self.arm.move_xyz()
                    sleep(0.01)
                #Migiharai
                if self.ARM_ON == True and 22 <= FontFlg < 30:
                    self.arm.x += 0.001
                    self.arm.y = y
                    self.arm.z += 0.0003
                    self.arm.move_xyz()
                    sleep(0.01)
                #止め
                if self.ARM_ON == True and 30 <= FontFlg < 40:
                    self.arm.x = x
                    self.arm.y = y
                    self.arm.z -= 0.001
                    self.arm.move_xyz()
                    sleep(0.3)
                #hidariはね
                if self.ARM_ON == True and 40 <= FontFlg < 41:
                    self.arm.x -= 0.002
                    self.arm.y += 0.0025
                    self.arm.z += 0.001
                    self.arm.move_xyz()
                    sleep(0.001)
                #hane
                if self.ARM_ON == True and 41 <= FontFlg < 50:
                    self.arm.x -= 0.0015
                    self.arm.y += 0.0015
                    self.arm.z += 0.0003
                    self.arm.move_xyz()
                    sleep(0.001)

                #点
                if self.ARM_ON == True and 50 <= FontFlg < 60:
                    self.arm.x = x
                    self.arm.y = y
                    self.arm.z -= 0.001
                    self.arm.move_xyz()
                    sleep(0.1)
                #折れ
                if self.ARM_ON == True and FontFlg == 60:
                    self.arm.x = x
                    self.arm.y = y
                    self.arm.z -= 0.001
                    self.arm.move_xyz()
                    sleep(0.5)

                if self.ARM_ON == True and FontFlg == 61:
                    self.arm.WaitMove=True
                    self.arm.x = x
                    self.arm.y = y
                    self.arm.z += 0.02
                    self.arm.move_xyz()
                    sleep(0.3)
                    self.arm.z -= 0.02
                    self.arm.move_xyz()
                    sleep(0.1)
                    self.arm.WaitMove=False

                #高さがdownモードの時は、画面にもライン描画
                if z!=self.HeightUp:
                    #描画用座標算出してラインを引く
                    lx0=int((x0-self.CampusOffsetX)*self.Ratio)
                    lx =int((x -self.CampusOffsetX)*self.Ratio)
                    ly0=self.ImageSizeY-int((y0-self.CampusOffsetY)*self.Ratio)
                    ly =self.ImageSizeY-int((y -self.CampusOffsetY)*self.Ratio)
                    print(ly,self.ImageSizeY,y,self.CampusOffsetY,self.Ratio)
                    if self.GRAPH_ON==True:
                        cv2.line(self.Img, (lx0,ly0), (lx,ly), self.Color, self.Thickness)
                        cv2.imshow("img", self.Img)
                        cv2.waitKey(1)

                #高さがupモードの時は、x,y移動後にペンを下げる
                if z==self.HeightUp :
                    sleep(1.0)
                    z=self.HeightDown
                    if self.ARM_ON==True:
                        self.arm.Step=Step_atPenDown
                        self.arm.WaitMove=False

                        #筆を斜めに下ろす場合、いったん左上に少しずらす
                        if True: #FontFlg==1:
                            Offset=0.04
                            self.arm.x=x-Offset 
                            self.arm.y=y+Offset 
                            self.arm.Step=Step_atJump
                            self.arm.move_xyz()
                            self.arm.Step=Step_atPenDown
#                        key = raw_input('Please enter to resume.') #forDebug

                        #SERVO負荷を見ながらz軸を少しずつ下ろす処理
                        z_unit=0.001
                        for z in np.arange(self.HeightUp,self.HeightDown-0.01,-1*z_unit):
                            self.arm.z=z
                            #斜めに下ろす場合はx,y座標もずらしていく
                            if True: #FontFlg==1:
                                self.arm.x+=Offset/(self.HeightUp-self.HeightDown)*z_unit
                                self.arm.y-=Offset/(self.HeightUp-self.HeightDown)*z_unit
                                if self.arm.x > x : self.arm.x=x
                                if self.arm.y < y : self.arm.y=y
                            self.arm.move_xyz()
                            sleep(0.01)
                            #SERVO負荷で接地検出できたら終了
                            if self.check_load(2):
                                self.HightDown = z +0.005
                                break

                        #self.HightDownも実測値に合わせて更新しておく
                        #self.HightDown=z+0.001

#                        key = raw_input('Please enter to resume.') #forDebug
                        sleep(1.0)

                #次回参照用のx,y座標を退避
                x0=x
                y0=y

            #一筆分が終了したら、ペンを上げる
            sleep(0.01)
            z=self.HeightUp
            if self.ARM_ON==True:
                self.arm.WaitMove=False
                self.arm.z=z
                self.arm.Step=Step_atPenUp
                self.arm.move_xyz()
                self.arm.Step=Step_atJump
                self.arm.WaitMove=False
                sleep(1.5)
            #self.HeightDown =0.01

        #一文字書き終わり
        if self.ARM_ON==True:
            self.arm.Step=Step_atFirst


    ########################################
    #墨を付ける動作
    def refill(self,x,y):
        Step_atJump=100 #一筆間の移動
        Step_atPenUp=50 #PEN上げ動作
        Step_atPenDown=1 #PEN下げ動作

        self.arm.WaitMove=False
        self.arm.Step=Step_atJump
        self.arm.x = x
        self.arm.y = y
        self.arm.move_xyz()

        #SERVO負荷を見ながらz軸を少しずつ下ろす処理
        z_unit=0.001
        self.arm.Step=Step_atPenDown
        self.arm.WaitMove=False
        for z in np.arange(self.HeightUp,self.HeightDown-0.01,-1*z_unit):
            self.arm.z=z
            self.arm.move_xyz()
            sleep(0.01)
            #SERVO負荷で接地検出できたら終了
            if self.check_load(2):
                break

        #すずりの中で筆を移動させる
        self.arm.WaitMove=False
        self.arm.Step=100
        self.arm.x += 0
        self.arm.y += -0.05
        self.arm.z += +0.03
        self.arm.move_xyz()
        sleep(0.5)

        #筆を上げる
        self.arm.WaitMove=False
        self.arm.Step=Step_atPenUp
        self.arm.z = self.HeightUp
        self.arm.move_xyz()
        sleep(1.0)



    ########################################
    #SERVO負荷チェック
    def check_load(self,ch):
        ret=False
        LoadTh=-0.002
        l=[0,0,0,0,0,0]
        l[1]=self.arm.Tilt_State[1].load
        l[2]=self.arm.Tilt_State[2].load
        l[3]=self.arm.Tilt_State[3].load
        l[4]=self.arm.Tilt_State[4].load
        l[5]=self.arm.Tilt_State[5].load
        rospy.loginfo("Load:[%6.3f,%6.3f,%6.3f,%6.3f,%6.3f]", l[1],l[2],l[3],l[4],l[5])
        if(l[ch]<=LoadTh):
            self.arm.WaitMove=True
            self.arm.move_xyz()
            self.arm.WaitMove=False
            l[1]=self.arm.Tilt_State[1].load
            l[2]=self.arm.Tilt_State[2].load
            l[3]=self.arm.Tilt_State[3].load
            l[4]=self.arm.Tilt_State[4].load
            l[5]=self.arm.Tilt_State[5].load
            rospy.loginfo("Load(verify):[%6.3f,%6.3f,%6.3f,%6.3f,%6.3f]", l[1],l[2],l[3],l[4],l[5])
            if(l[ch]<=LoadTh):
                ret=True
        return ret 

    ########################################
    #GRAPH CLEAR
    def graph_clear(self):
        self.Img[:,:,:]=(255,255,255)

if __name__ == '__main__':
 
    try:
        ts = write_char()
        rospy.spin()
    except rospy.ROSInterruptException: pass

