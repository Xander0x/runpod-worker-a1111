AUTOSAM_CONFIG_SCHEMA = {
    'points_per_side': {
        'type': int,
        'required': False,
        'default': 32,
    },
    'points_per_batch': {
        'type': int,
        'required': True,
    },
    'pred_iou_thresh': {
        'type': float,
        'required': True,
    },
    'stability_score_thresh': {
        'type': float,
        'required': True,
    },
    'stability_score_offset': {
        'type': float,
        'required': True,
    },
    'box_nms_thresh': {
        'type': float,
        'required': True,
    },
    'crop_n_layers': {
        'type': int,
        'required': True,
    },
    'crop_nms_thresh': {
        'type': float,
        'required': True,
    },
    'crop_overlap_ratio': {
        'type': float,
        'required': True,
        'default': 512 / 1500,
    },
    'crop_n_points_downscale_factor': {
        'type': int,
        'required': True,
    },
    'min_mask_region_area': {
        'type': int,
        'required': True,
    },
}