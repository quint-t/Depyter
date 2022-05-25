# template-name: Test on batch
# template-type: Keras-Model methods
# <code-block> Test on batch
loss = model.test_on_batch(
    x, y=None, sample_weight=None, reset_metrics=True, return_dict=False
)
