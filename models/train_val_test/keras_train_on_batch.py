# template-name: Train on batch
# template-type: Keras-Model methods
# <code-block> Train on batch
loss = model.train_on_batch(
    x,
    y=None,
    sample_weight=None,
    class_weight=None,
    reset_metrics=True,
    return_dict=False
)
