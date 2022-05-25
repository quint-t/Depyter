# template-name: SaveBestWeights and EarlyStopping
# template-type: Tensorflow-Callbacks
# <code-block> SaveBestWeights and EarlyStopping
import numpy as np
import tensorflow as tf


class SaveBestWeightsAndEarlyStopping(tf.keras.callbacks.Callback):
    def __init__(self,
                 monitor='val_accuracy',
                 baseline=0.9,
                 baseline_epochs=1,
                 restore_best_weights=True):
        super(SaveBestWeightsAndEarlyStopping, self).__init__()

        self.monitor = monitor
        self.baseline = baseline
        self.baseline_epochs = baseline_epochs
        self.wait = 0
        self.stopped_epoch = 0
        self.restore_best_weights = restore_best_weights
        self.best_weights = None
        if 'acc' in self.monitor:
            self.monitor_op = np.greater
        else:
            self.monitor_op = np.less

    def on_train_begin(self, logs=None):
        self.wait = 0
        self.stopped_epoch = 0
        self.best = np.Inf if self.monitor_op == np.less else -np.Inf
        self.best_weights = None

    def on_epoch_end(self, epoch, logs=None):
        current = self.get_monitor_value(logs)
        if current is None:
            return
        if self.restore_best_weights and self.best_weights is None:
            self.best_weights = self.model.get_weights()
        if self._is_improvement(current, self.best):
            self.best = current
            self.wait = 0
            if self.restore_best_weights:
                self.best_weights = self.model.get_weights()
        if self._is_improvement(current, self.baseline):
            self.wait = 0
        else:
            self.wait += 1
        if self.wait >= self.baseline_epochs:
            self.stopped_epoch = epoch
            self.model.stop_training = True
            if self.restore_best_weights and self.best_weights is not None:
                self.model.set_weights(self.best_weights)

    def on_train_end(self, logs=None):
        if self.restore_best_weights and self.best_weights is not None:
            self.model.set_weights(self.best_weights)

    def get_monitor_value(self, logs):
        logs = logs or {}
        monitor_value = logs.get(self.monitor)
        if monitor_value is None:
            logging.warning('Early stopping conditioned on metric `%s` '
                            'which is not available. Available metrics are: %s',
                            self.monitor, ','.join(list(logs.keys())))
        return monitor_value

    def _is_improvement(self, monitor_value, reference_value):
        return self.monitor_op(monitor_value, reference_value)
