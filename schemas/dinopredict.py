DINO_PREDICT_SCHEMA = {
    'input_image': {
        'type': str,
        'required': True
    },
    'dino_model_name': {
        'type': str,
        'required': False,
        'default': "GroundingDINO_SwinT_OGC (694MB)"
    },
    'text_prompt': {
        'type': str,
        'required': True
    },
    'box_threshold': {
        'type': float,
        'required': False,
        'default': 0.3
    },
}
