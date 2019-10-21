# crane_plus_src
  
## crane操作メモ
  
### 起動準備(おまじない)
`ubuntu% roslaunch crane_plus_src controller_manager.launch`  
`ubuntu% roslaunch crane_plus_src start_tilt_controller.launch`  
  
  
### コマンド操作の場合
`ubuntu% rostopic pub -1 /tilt1_controller/command std_msgs/Float64 -- 1.0`  
  
  
### テンキー操作の場合　
`ubuntu% rosrun crane_plus_src test_arm_tenkey.py`  
  q: プログラム終了  
  8,2: 前後移動(tilt2,3,4制御)  
  6,4: 左右移動(tilt1制御)  
  5,0: 全体上下(tilt2制御)  
  9,3: 手首上下(tilt4制御)  
  7,1: グリップ開閉(tilt5制御)  
  
※プログラムが反応なくなった場合は、Ctrl+zで中断してから、  
  `ubuntu% kill -9 %%`  
  で強制終了させる。  
  

### テンキー操作の場合　(x,y,z)座標制御バージョン
`ubuntu% rosrun crane_plus_src test_arm_tenkey2.py`  
  q: プログラム終了  
  8,2: y軸移動（縦）  
  6,4: x軸移動（横）  
  5,0: z軸移動（上下）  
  9,3: 手首の角度   
  7,1: グリップ開閉   
  
  
### バッチ処理の場合
`ubuntu% rosrun test_moveit test_arm_asakusa.py`  
"アサクサ"の文字を書くプログラム。  
※ほかの動きをさせる場合は、プログラム中の座標データを変更すればいい。  
  
  
## 補足
### 事前にインストール必要なもの
`ubuntu% git clone git://github.com/arebgun/dynamixel_motor.git`  
