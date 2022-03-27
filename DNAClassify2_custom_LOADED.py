import matplotlib.pyplot as plt
import os
import tensorflow as tf
import time

from tensorflow.keras import layers
from tensorflow.keras import losses
from tensorflow.keras import preprocessing
from tensorflow.keras.layers.experimental.preprocessing import TextVectorization
from tensorflow.keras.optimizers import SGD
from tensorflow.keras.layers import Dense
from tensorflow.python.keras.layers.core import Activation
from tensorflow.python.keras.layers.embeddings import Embedding
from tensorflow.python.ops.gen_math_ops import mod

batch_size = 32

seed = 42

raw_train_ds = tf.keras.preprocessing.text_dataset_from_directory(
    'K-MersRandomMutOld/Train', 
    batch_size=batch_size)

raw_val_ds = tf.keras.preprocessing.text_dataset_from_directory(
    'K-MersRandomMutOld/Validation', 
    batch_size=batch_size)

raw_test_ds = tf.keras.preprocessing.text_dataset_from_directory(
    'K-MersRandomMutOld/Test', 
    batch_size=batch_size)

def custom_standardization(input_data):
  lowercase = tf.strings.lower(input_data)   
  return tf.strings.regex_replace(lowercase, '', '')
                            
max_features = 5000
sequence_length = 30000

vectorize_layer = TextVectorization(
    standardize=custom_standardization,
    max_tokens= max_features,
    output_mode='int',
    output_sequence_length=sequence_length)

# Make a text-only dataset (without labels), then call adapt
train_text = raw_train_ds.map(lambda text, labels: text)
vectorize_layer.adapt(train_text)

def vectorize_text(text, label):
  text = tf.expand_dims(text, -1)
  return vectorize_layer(text), label

# retrieve a batch (of 32 reviews and labels) from the dataset
text_batch, label_batch = next(iter(raw_train_ds))
first_DNA, first_label = text_batch[0], label_batch[0]
print("DNA: ", first_DNA)
print("DNA spaced: ", custom_standardization(first_DNA))
print("Label: ", raw_train_ds.class_names[first_label])
print("Vectorized DNA: ", vectorize_text(first_DNA, first_label))

# print("1 ---> ",vectorize_layer.get_vocabulary()[1])
# print("4 ---> ",vectorize_layer.get_vocabulary()[4])
print('Vocabulary size: {}'.format(len(vectorize_layer.get_vocabulary())))
for k in range(0,len(vectorize_layer.get_vocabulary())):
  print("{0} ---> {1}".format(k, vectorize_layer.get_vocabulary()[k]))

train_ds = raw_train_ds.map(vectorize_text)
val_ds = raw_val_ds.map(vectorize_text)
test_ds = raw_test_ds.map(vectorize_text)

AUTOTUNE = tf.data.AUTOTUNE

train_ds = train_ds.cache().prefetch(buffer_size=AUTOTUNE)
val_ds = val_ds.cache().prefetch(buffer_size=AUTOTUNE)
test_ds = test_ds.cache().prefetch(buffer_size=AUTOTUNE)

vocab_size=max_features + 1
num_labels=4

# Create a basic model instance
model = tf.keras.Sequential([])
model.add(layers.Embedding(vocab_size, 64, mask_zero=True))
for layer in model.layers:
    print(layer.name)
    print(layer.output_shape)
model.add(layers.Conv1D(64, 5, padding="valid", activation="relu", strides=2))
for layer in model.layers:
    print(layer.name)
    print(layer.output_shape)
model.add(layers.Dropout(0.5))
for layer in model.layers:
    print(layer.name)
    print(layer.output_shape)
# model.add(layers.GlobalMaxPooling1D())
# for layer in model.layers:
#     print(layer.name)
#     print(layer.output_shape)
# model.add(layers.LSTM(64))
# for layer in model.layers:
#     print(layer.name)
#     print(layer.output_shape)
model.add(layers.GlobalMaxPooling1D())
for layer in model.layers:
    print(layer.name)
    print(layer.output_shape)
model.add(layers.Dropout(0.5))
for layer in model.layers:
    print(layer.name)
    print(layer.output_shape)
model.add(layers.Dense(num_labels))

model.compile(
    loss=losses.SparseCategoricalCrossentropy(from_logits=True),
    optimizer='adam',
    metrics=['accuracy'])

# Evaluate the model
loss, acc = model.evaluate(test_ds, verbose=2)
print("Untrained model, accuracy: {:5.2f}%".format(100 * acc))

# Loads the weights
model.load_weights('Images/cp.ckpt')

# Re-evaluate the model
loss, acc = model.evaluate(test_ds, verbose=2)
print("Restored model, accuracy: {:5.2f}%".format(100 * acc))
