_base_ = [
    '../../_base_/models/faster_rcnn_r50_dc5.py',
    # '../../_base_/models/faster_rcnn_r50_fpn.py',
    '../../_base_/datasets/imagenet_vid_fgfa_style_sm.py',     ##
    '../../_base_/default_runtime.py'
]
model = dict(
    type='SELSA',
    detector=dict(
        backbone=dict(
            _delete_=True,
            type='SwinTransformer',
            embed_dims=96,
            depths=[2, 2, 6, 2],
            num_heads=[3, 6, 12, 24],
            window_size=7,
            mlp_ratio=4,
            qkv_bias=True,
            qk_scale=None,
            drop_rate=0.,
            attn_drop_rate=0.,
            drop_path_rate=0.2,
            patch_norm=True,
            # out_indices=(0, 1, 2, 3),
            out_indices=(3, ),
            with_cp=False,
            convert_weights=True,
            init_cfg=dict(type='Pretrained', checkpoint='checkpoints/swin_tiny_patch4_window7_224.pth')),
        neck=dict(in_channels=[768]),
        rpn_head=dict(
            type='RPNHead',
            in_channels=512,
            feat_channels=512,
            anchor_generator=dict(
                type='AnchorGenerator',
                # scales=[4, 8, 16, 32],
                scales=[2, 4, 8, 16],
                ratios=[0.5, 1.0, 2.0],
                strides=[32]),  ##16
            bbox_coder=dict(
                type='DeltaXYWHBBoxCoder',
                target_means=[.0, .0, .0, .0],
                target_stds=[1.0, 1.0, 1.0, 1.0]),
            loss_cls=dict(
                type='CrossEntropyLoss', use_sigmoid=True, loss_weight=1.0),
            loss_bbox=dict(
                type='SmoothL1Loss', beta=1.0 / 9.0, loss_weight=1.0)),
        roi_head=dict(
            type='SelsaRoIHead',
            bbox_roi_extractor=dict(
                type='TemporalRoIAlign',
                num_most_similar_points=2,
                num_temporal_attention_blocks=4,
                roi_layer=dict(
                    type='RoIAlign', output_size=7, sampling_ratio=2),
                out_channels=512,
                featmap_strides=[32]),  ##16
            bbox_head=dict(
                type='SelsaBBoxHead',
                num_shared_fcs=3,
                aggregator=dict(
                    type='SelsaAggregator',
                    in_channels=1024,
                    num_attention_blocks=16)))))

# dataset settings
data = dict(
    val=dict(
        ref_img_sampler=dict(
            _delete_=True,
            num_ref_imgs=14,
            frame_range=[-7, 7],
            method='test_with_adaptive_stride')),
    test=dict(
        ref_img_sampler=dict(
            _delete_=True,
            num_ref_imgs=14,
            frame_range=[-7, 7],
            method='test_with_adaptive_stride')))

# optimizer
optimizer = dict(type='SGD', lr=0.005, momentum=0.9, weight_decay=0.0001)
optimizer_config = dict(
    _delete_=True, grad_clip=dict(max_norm=35, norm_type=2))
# learning policy
lr_config = dict(
    policy='step',
    warmup='linear',
    warmup_iters=500,
    warmup_ratio=1.0 / 3,
    step=[2, 5])
# runtime settings
total_epochs = 21
evaluation = dict(metric=['bbox'], interval=1)
load_from = 'checkpoints/selsa_troialign_faster_rcnn_r50_dc5_7e_imagenetvid_20210820_162714-939fd657.pth'
