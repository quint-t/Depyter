# template-name: Dropout-Dense-ReLU model
# template-type: MNIST Classification Models
# <code-block> Dropout-Dense-ReLU model for MNIST Classification
import tensorflow as tf

model = tf.keras.models.Sequential([
    tf.keras.layers.Dropout(0.4, input_shape=(784,)),
    tf.keras.layers.Dense(250, activation='linear'),
    tf.keras.layers.ReLU(),
    tf.keras.layers.Dense(250, activation='linear'),
    tf.keras.layers.ReLU(),
    tf.keras.layers.Dense(10, activation='linear')
])
model.compile(optimizer=tf.keras.optimizers.Adadelta(lr=5),
              loss=tf.nn.softmax_cross_entropy_with_logits,
              metrics=['accuracy'])
model.summary()
