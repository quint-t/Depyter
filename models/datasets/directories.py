# template-name: По шаблону:
# template-name: dataset_name/class_N/object_N.png(jpeg)
# template-type: Директория
# <code-block> Load image dataset from directories
import tensorflow as tf

tf.keras.utils.image_dataset_from_directory(
    'path/to/location',
    labels='inferred',  # 'inferred' -- labels are generated from the directory structure
    label_mode='int',  # 'int', 'categorical', 'binary' or None
    class_names=None,  # explicit list of class names; used to control the order of the classes
    color_mode='rgb',  # 'grayscale', 'rgb' or 'rgba'
    batch_size=32,  # if None, the data will not be batched
    image_size=(256, 256),  # (height, width)
    shuffle=True,  # if set to False, sorts the data in alphanumeric order
    seed=None,  # optional random seed (int) for shuffling and transformations
    validation_split=None,  # optional float between 0 and 1, fraction of data to reserve for validation
    subset=None,  # 'training' or 'validation'
    interpolation='bilinear',
    # interpolation method used when resizing images: bilinear, nearest, bicubic, area, lanczos3, lanczos5, gaussian, mitchellcubic
    follow_links=False,  # whether to visits subdirectories pointed to by symlinks
    crop_to_aspect_ratio=False  # if True, resize the images without aspect ratio distortion
)

# main_directory/
# ...class_a/
# ......a_image_1.jpg
# ......a_image_2.jpg
# ...class_b/
# ......b_image_1.jpg
# ......b_image_2.jpg
# Supported image formats: jpeg, png, bmp, gif
# Animated gifs are truncated to the first frame
