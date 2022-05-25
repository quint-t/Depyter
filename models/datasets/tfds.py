# template-name: tensorflow-datasets
# template-type: Библиотека
# <code-block> Load dataset from tensorflow-datasets
import tensorflow_datasets as tfds

# tf.data.Dataset
ds = tfds.load('mnist', split='train', shuffle_files=True)
# datasets: https://www.tensorflow.org/datasets/catalog/overview#all_datasets
