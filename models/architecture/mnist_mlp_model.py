# template-name: MLP model
# template-type: MNIST Classification Models
# <code-block> MLP model for MNIST Classification
import tensorflow as tf

model = tf.keras.models.Sequential([
    tf.keras.layers.Dense(250, activation='sigmoid', input_shape=(784,)),
    tf.keras.layers.Dense(250, activation='sigmoid'),
    tf.keras.layers.Dense(10, activation='sigmoid')
])
model.compile(optimizer=tf.keras.optimizers.Adadelta(lr=2),
              loss='categorical_crossentropy',
              metrics=['accuracy'])
model.summary()
