import os
import shutil
import ipdb

data_root = 'data/cocovid_50/Data/train'
vid_names = os.listdir(data_root)
video_dir = 'data/cocovid_50/Data/snippets/video_crop_50/'
dst_dir = 'data/cocovid_50/Data/snippets/train'
for vid_name in os.listdir(video_dir):
    vid_name_prev = vid_name[:-4]
    if vid_name_prev in vid_names:
        shutil.copy(os.path.join(video_dir, vid_name), os.path.join(dst_dir, vid_name))