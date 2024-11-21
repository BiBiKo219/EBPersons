# pip install mmcv-full -f https://download.openmmlab.com/mmcv/dist/cu102/torch1.7.0/index.html
# export CUDA_VISIBLE_DEVICES=1,2

# train
# Scale Match VID
bash ./tools/dist_train.sh configs/vid/temporal_roi_align/selsa_troialign_faster_rcnn_r50_dc5_7e_imagenetvid_sm.py 4 \
  --work-dir ./work_dirs/selsa_troialign_faster_rcnn_r50_dc5_7e_imagenetvid_sm
bash ./tools/dist_train.sh configs/vid/temporal_roi_align/selsa_troialign_faster_rcnn_r50_dc5_7e_imagenetvid_our.py 4 \
  --work-dir ./work_dirs/selsa_troialign_faster_rcnn_r50_dc5_7e_imagenetvid_our_sm

## Scale Match swin VID
bash ./tools/dist_train.sh configs/vid/temporal_roi_align/selsa_troialign_faster_rcnn_swin_dc5_7e_imagenetvid_sm.py 4 \
  --work-dir ./work_dirs/selsa_troialign_faster_rcnn_swin_dc5_7e_imagenetvid_sm
bash ./tools/dist_train.sh configs/vid/temporal_roi_align/selsa_troialign_faster_rcnn_swin_dc5_7e_imagenetvid_our.py 4 \
  --work-dir ./work_dirs/selsa_troialign_faster_rcnn_swin_dc5_7e_imagenetvid_our_sm

# test
./tools/dist_test.sh configs/vid/selsa/selsa_faster_rcnn_swin_dc5_1x_imagenetvid_our.py 4 \
 --checkpoint work_dirs/selsa_faster_rcnn_swin_dc5_1x_imagenetvid_our/epoch_7.pth \
 --out results.pkl \
 --eval bbox

# inference
python 'demo/demo_vid.py'  \
 'configs/vid/temporal_roi_align/selsa_troialign_faster_rcnn_r50_dc5_7e_imagenetvid_our.py'  \
  --input 'xxx.mp4'  \
  --output 'xxx_output.mp4' \
  --checkpoint 'checkpoints/epoch_7_s.pth'