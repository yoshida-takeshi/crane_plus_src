#! /usr/bin/env python
# -*- coding: utf-8 -*-

#move_arm制御プログラム実装例
#  試してみたい項目の "if(0):" を "if(1)" に書き換えてから実行してください
 
import rospy
import move_arm_v4 as move_arm
from time import sleep

####################
#move_arm呼出し
arm=move_arm.move_arm()

####################
#xyz座標で移動例(単位:m)
#- 原点はアーム本体の場所（根元）
arm.x=+0.00
arm.y=+0.20
arm.z=+0.20
arm.WaitMove=True
arm.move_xyz()

arm.WaitMove=False
c=0
LoadTh=-0.001
for z in range(200,-100,-1):
    arm.z=float(z)/1000
    arm.WaitMove=False
    arm.move_xyz()
    l=arm.Tilt_State[2].load
    print(l,arm.WaitMove)
    if(l<=LoadTh):
        arm.WaitMove=True
        arm.move_xyz()
        l=arm.Tilt_State[2].load
        print(l,arm.WaitMove)
        if(l<=LoadTh):
            break

arm.WaitMove=False

exit()

