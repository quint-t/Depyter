# template-name: Отдельный каталог для класса
# template-type: Директория
# <code-block> Load image dataset from directory
import tensorflow as tf

filename_dataset = tf.data.Dataset.list_files("path/to/*.png")

image_dataset = filename_dataset.map(lambda x: tf.decode_png(tf.read_file(x)))
