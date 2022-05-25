# template-name: Predict
# template-type: Keras-Model methods
# <code-block> Predict
predictions = model.predict(
    x,
    batch_size=None,
    verbose='auto',
    steps=None,
    callbacks=None,
    max_queue_size=10,
    workers=1,
    use_multiprocessing=False
)
