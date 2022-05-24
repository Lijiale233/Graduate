import os
import cv2
import Tool
import numpy as np
import pandas as pd
import csv

from skelton_detect.openpose.demo import detectSkelton
"""
    INPUT: movement.MP4
    OUTPUT: 时序关节转动数据
"""
class KeyGenerator:
    video_dir = Tool.data_menu+"skelton/"

    def mp4_to_frame(self,video_name):
        """视频转图片 参数需指定此视频所属的任务，以及视频路径"""
        video_path = self.video_dir + "mp4/" + video_name +".mp4"
        frame_path = self.video_dir + "frame/" + video_name

        os.makedirs(frame_path, exist_ok=True)  # 创建存放frame的目录
        vc = cv2.VideoCapture(video_path)
        fps = vc.get(cv2.CAP_PROP_FPS)
        rval = vc.isOpened()
        c = 1
        while rval:
            rval, frame = vc.read()
            pic_path = frame_path + '/'
            if rval:
                if (c % 6 == 0):
                    cv2.imwrite(pic_path + video_name + '_' + str(c) + '.jpg',
                                frame)
                cv2.waitKey(1)
                c = c + 1
            else:
                break
        vc.release()
        print("frame save to" + frame_path)

    """时序骨骼点的生成"""
    def frame_skelton_pos(self,video_name):
        frame_path = self.video_dir + "frame/" + video_name
        frames = os.listdir(frame_path)
        results=[]
        for i in frames:
            frame = frame_path+"/" + i
            results.append(detectSkelton(frame,str(i)))
        results.sort()

        #本地文件数据备份
        with open("data/skelton/keys/"+video_name+".csv",'w') as f:
            writer = csv.writer(f)
            for result in results:
                for pose in result:
                    if len(pose)>0:
                        print(pose)
                        writer.writerow(pose)
        f.close()

        # with open("data/skelton/keys/"+video_name+".txt",'w+') as f:
        #     for i in results:
        #         f.write(str(i)+"\n")
        #     f.close()

    # 把二维列表存入excel中


keyGenerator = KeyGenerator()
keyGenerator.frame_skelton_pos("hello_a")