#! /usr/bin/env python
# -*- coding: utf-8 -*-

import rospy
import numpy as np
import write_char_v5 as write_char


class write_text:
    ########################################
    #INIT
    def __init__(self):
        ARM_ON=True
        GRAPH_ON=True

        self.wc=write_char.write_char(ARM_ON,GRAPH_ON)
        self.setup_param()
        self.main_loop()

    ########################################
    #パラメータ初期設定
    def setup_param(self):
#        self.wc.HeightDown=0.01
#        self.wc.FontSize=0.23
        self.wc.Rotate=0

    ########################################
    #メイン処理
    def main_loop(self):
        if(1):#横書き
            #浅草
            y=self.wc.y_Bottom+0.21
            x=-self.wc.FontSize/2
            data = np.load("/home/ubuntu/ros_groupE_ws/src/crane_plus_src/src/fontdata/sample3/i_plus_flag.npy")
            self.wc.write_char(data,x,y)
           
#            x=x+self.wc.FontSize
#            data = np.load("a.npy")
#            self.wc.write_char(data,x,y)

        if(0):#縦書き
            #浅草
            self.wc.Rotate=3
            y=self.wc.y_Bottom+0.09
            x=+self.wc.FontSize
            data = np.load("eiji2.npy")
            self.wc.write_char(data,x,y)

#            x=x-self.wc.FontSize
#            data = np.load("a.npy")
#            self.wc.write_char(data,x,y)           
        key = raw_input('Please enter to finish.')
        exit()

       
if __name__ == '__main__':
 
    try:
        ts = write_text()
        rospy.spin()
    except rospy.ROSInterruptException: pass
