# template-name: hugging-face
# template-type: Библиотека
# <code-block> Load dataset from hugging-face-datasets
from datasets import load_dataset

data_files = {'train': 'train.csv', 'validation': 'validation.csv', 'test': 'test.csv'}
dataset = load_dataset('allenai/c4', data_files=data_files)
# datasets: https://huggingface.co/datasets
# load datasets tutorial: https://huggingface.co/docs/datasets/loading
