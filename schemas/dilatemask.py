DILATE_MASK_SCHEMA = {
    'input_image': {
        'type': str,
        'required': True,
    },
    'mask': {
        'type': str,
        'required': True,
    },
    'dilate_amount': {
        'type': int,
        'required': False,
        'default': 10,
    },
}
