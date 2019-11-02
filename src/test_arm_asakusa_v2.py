#! /usr/bin/env python
# -*- coding: utf-8 -*-

import rospy
import numpy as np
import write_char_v1 as write_char


class write_text:
    ########################################
    #INIT
    def __init__(self):
        self.wc=write_char.write_char(True,True)
        #self.setup_param()
        self.main_loop()

    ########################################
    #パラメータ初期設定
    def setup_param(self):
        self.wc.HeightDown=0.090
        self.wc.FontSize=0.05
        self.wc.Rotate=0

    ########################################
    #メイン処理
    def main_loop(self):
        self.wc.FontSize=0.03

        #富士山(文字)
        #x=self.wc.x_Right-self.wc.FontSize
        #y=self.wc.y_Top-0.04
        #self.wc.HeightDown=0.105
        #data = np.load("/home/ubuntu/font/fu.npy")
        ##self.wc.write_char(data,x,y)
        #
        #data = np.load("/home/ubuntu/font/ji.npy")
        #y=y-self.wc.FontSize
        #self.wc.HeightDown=0.095
        ##self.wc.write_char(data,x,y)

        #data = np.load("/home/ubuntu/font/san.npy")
        #y=y-self.wc.FontSize
        #self.wc.HeightDown=0.085
        ##self.wc.write_char(data,x,y)

        ##富士山(絵)
        #self.wc.FontSize=0.10
        #x=x-self.wc.FontSize
        #y=self.wc.y_Top-0.04
        #self.wc.HeightDown=0.095
        #data = np.load("/home/ubuntu/font/fujisan.npy")
        #self.wc.write_char(data,x,y)

        ##チーム浅草
        #self.wc.FontSize=0.04
        #x=x-self.wc.FontSize
        #y=self.wc.y_Top-0.01
        #data = np.load("/home/ubuntu/font/team.npy")
        ##self.wc.write_char(data,x,y)
        #
        #y=y-self.wc.FontSize
        #data = np.load("/home/ubuntu/font/asa.npy")
        ##self.wc.write_char(data,x,y)

        #data = np.load("/home/ubuntu/font/kusa.npy")
        #y=y-self.wc.FontSize
        ##self.wc.write_char(data,x,y)

        #チーム浅草
        self.wc.HeightDown=0.090
        self.wc.FontSize=0.04
        x=self.wc.x_Left
        y=self.wc.y_Bottom+0.05
        #data = np.load("/home/ubuntu/font/team.npy")
        #self.wc.write_char(data,x,y)
        
        #x=x+self.wc.FontSize
        data = np.load("/home/ubuntu/font/asa.npy")
        #self.wc.write_char(data,x,y)

        x=x+self.wc.FontSize
        data = np.load("/home/ubuntu/font/kusa.npy")
        self.wc.write_char(data,x,y)
        
        key = raw_input('Please enter to finish.')
        exit()

       
if __name__ == '__main__':
 
    try:
        ts = write_text()
        rospy.spin()
    except rospy.ROSInterruptException: pass
