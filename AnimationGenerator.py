import yaml
import copy
import Tool

class AnimationGenerator:
    data_dir = Tool.data_menu+'animation/'
    # 骨骼点编号对应关系
    bone5 = "bone_1/bone_5"
    # 由骨骼捕捉输入数据
    model_output = {"bone5": {"time": [0.5], "zRot": [100]}}
    # 基于输入数据更新输出数据
    bones_keyValue = {"bone5": {"time": [0.5], "zRot": [100]}}


    def generate_anim(self):
        with open(self.data_dir+'test.yaml', encoding='utf-8') as file:
            animation_file = yaml.safe_load(file)  # 为列表类型
        animation_clip = animation_file.get('AnimationClip')
        euler_curves = animation_clip.get('m_EulerCurves')
        bone5_curve = euler_curves[0].get('curve').get('m_Curve')  # 参考骨骼编号对照表，得到对应骨骼的帧序列
        key_format = copy.deepcopy(bone5_curve[0])  # 传值不传址
        euler_curves[0].get('curve')

        # 新建关键帧数据 bone5_keys
        bone5_keyValue = self.bones_keyValue.get("bone5")
        bone5_keys = [key_format for i in range(len(bone5_keyValue.get("time")))]
        for index, key in enumerate(bone5_keys):
            key = key_format
            key.update({"time": bone5_keyValue.get("time")[index]})
            key.update({"value": {'x': 0, 'y': 0, 'z': bone5_keyValue.get("zRot")[index]}})
            bone5_keys[index] = key# 完成更新


        # 将新的关键帧数据插入到帧序列之中（只需要插入中间位置即可）
        start_key = copy.deepcopy([bone5_curve[0]])
        end_key = copy.deepcopy([bone5_curve[1]])
        start_key.extend(bone5_keys)
        start_key.extend(end_key)
        bone5_curve = start_key

        # 还原animation文档
        old_animation_file = copy.deepcopy(animation_file)
        old_animation_clip = copy.deepcopy(animation_clip)
        old_euler_curves = copy.deepcopy(euler_curves)
        old_curve = copy.deepcopy(old_euler_curves[0].get('curve'))  # 0为骨头对应的关节点

        new_curve = Tool.update_dict(old_curve, {'m_Curve': bone5_curve})
        new_euler_curves = [Tool.update_dict(old_euler_curves[0], {'curve': new_curve})]  # 0对应bone5的编号
        new_animation_clip = Tool.update_dict(old_animation_clip, {'m_EulerCurves': new_euler_curves})
        new_animation_file = Tool.update_dict(old_animation_file, {'AnimationClip': new_animation_clip})

        # 导出新的animation文件
        with open(self.data_dir+'newTest.yaml', mode='w', encoding='utf-8') as file:
            yaml.safe_dump(new_animation_file, file, default_flow_style=False, sort_keys=False)

anim_generator = AnimationGenerator()
anim_generator.generate_anim()
