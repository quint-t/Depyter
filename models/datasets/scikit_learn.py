# template-name: scikit-learn
# template-type: Библиотека
# <code-block> Load dataset from scikit-learn
from sklearn.datasets import load_boston, load_iris, load_diabetes, load_digits, \
    load_linnerud, load_wine, load_breast_cancer

boston = load_boston(return_X_y=False)
iris = load_iris(return_X_y=False)
diabetes = load_diabetes(return_X_y=False)
digits = load_digits(n_class=10, return_X_y=False)
linnerud = load_linnerud(return_X_y=False)
wine = load_wine(return_X_y=False)
breast_cancer = load_breast_cancer(return_X_y=False)

from sklearn.datasets import load_sample_image

china = load_sample_image('china.jpg')  # np.array
