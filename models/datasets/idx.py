# template-name: IDX
# template-type: Файл
# <code-block> Load dataset from IDX file
import numpy as np


def load_ubyte(train_images_filename, train_labels_filename,
               test_images_filename, test_labels_filename,
               n_train_images=60000, n_test_images=10000,
               image_size=784):
    with open(train_images_filename) as f:
        loaded = np.fromfile(file=f, dtype=np.uint8)[16:]
        training_images = loaded.reshape((n_train_images, image_size, 1)).astype(np.float)
        training_images = training_images

    with open(train_labels_filename) as f:
        loaded = np.fromfile(file=f, dtype=np.uint8)
        training_labels = loaded[8:].reshape((n_train_images,)).astype(np.int)

    with open(test_images_filename, 'rb') as f:
        loaded = np.fromfile(file=f, dtype=np.uint8)[16:]
        test_images = loaded.reshape((n_test_images, image_size, 1)).astype(np.float)
        test_images = test_images

    with open(test_labels_filename, 'rb') as f:
        loaded = np.fromfile(file=f, dtype=np.uint8)
        test_labels = loaded[8:].reshape((n_test_images,)).astype(np.int)

    return training_images, training_labels, test_images, test_labels, len(set(training_labels))
