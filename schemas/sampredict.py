SAM_PREDICT_SCHEMA = {
    'sam_model_name': {
        'type': str,
        'required': False,
        'default': "sam_vit_h_4b8939.pth"
    },
    'input_image': {
        'type': str,
        'required': True
    },
    'sam_positive_points': {
        'type': list,
        'required': False,
        'default': []
    },
    'sam_negative_points': {
        'type': list,
        'required': False,
        'default': []
    },
    'dino_enabled': {
        'type': bool,
        'required': False,
        'default': False
    },
    'dino_model_name': {
        'type': str,
        'required': False,
        'default': "GroundingDINO_SwinT_OGC (694MB)"
    },
    'dino_text_prompt': {
        'type': str,
        'required': False,
        'default': None
    },
    'dino_box_threshold': {
        'type': float,
        'required': False,
        'default': 0.3
    },
    'dino_preview_checkbox': {
        'type': bool,
        'required': False,
        'default': False
    },
    'dino_preview_boxes_selection': {
        'type': list,
        'required': False,
        'default': None
    },
}
