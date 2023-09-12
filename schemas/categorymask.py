CATEGORY_MASK_REQUEST_SCHEMA = {
    'sam_model_name': {
        'type': str,
        'required': False,
        'default': "sam_vit_h_4b8939.pth",
    },
    'processor': {
        'type': str,
        'required': False,
        'default': "seg_ofade20k",
    },
    'processor_res': {
        'type': int,
        'required': False,
        'default': 512,
    },
    'pixel_perfect': {
        'type': bool,
        'required': False,
        'default': False,
    },
    'resize_mode': {
        'type': int,
        'required': False,
        'default': 1,
    },
    'target_W': {
        'type': int,
        'required': False,
    },
    'target_H': {
        'type': int,
        'required': False,
    },
    'category': {
        'type': str,
        'required': True,
    },
    'input_image': {
        'type': str,
        'required': True,
    },
}
