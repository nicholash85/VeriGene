import matplotlib.pyplot as plt
import os
import re
import shutil
import string
import tensorflow as tf
import random

from tensorflow.keras import layers
from tensorflow.keras import losses
from tensorflow.keras import preprocessing
from tensorflow.keras.layers.experimental.preprocessing import TextVectorization
from tensorflow.keras.optimizers import SGD
from tensorflow.keras.layers import Dense
from tensorflow.python.keras.layers.core import Activation
from tensorflow.python.keras.layers.embeddings import Embedding
from tensorflow.python.ops.gen_math_ops import mod

# os.chdir('./Cello_Hardware_Trojans2')
# dataset_dir = './DNA'
# os.listdir(dataset_dir)
# train_dir = os.path.join(dataset_dir, 'Train')
# os.listdir(train_dir)
batch_size = 32

seed = 42

# raw_train_ds = tf.keras.preprocessing.text_dataset_from_directory(
#     'K-Mers/Train', 
#     batch_size=batch_size, 
#     validation_split=0.3, 
#     subset='training', 
#     shuffle=True,
#     seed=seed)

# raw_val_ds = tf.keras.preprocessing.text_dataset_from_directory(
#     'K-Mers/Train', 
#     batch_size=batch_size, 
#     validation_split=0.3, 
#     subset='validation',
#     shuffle=True,
#     seed=seed)

# raw_test_ds = tf.keras.preprocessing.text_dataset_from_directory(
#     'K-Mers/Test', 
#     batch_size=batch_size)

raw_train_ds = tf.keras.preprocessing.text_dataset_from_directory(
    'K-MersRandomMut_custom_NOR/Train', 
    batch_size=batch_size)

raw_val_ds = tf.keras.preprocessing.text_dataset_from_directory(
    'K-MersRandomMut_custom_NOR/Validation', 
    batch_size=batch_size)

raw_test_ds = tf.keras.preprocessing.text_dataset_from_directory(
    'K-MersRandomMut_custom_NOR/Test', 
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

# def create_model(vocab_size, num_labels):
#   model = tf.keras.Sequential([
#       layers.Embedding(vocab_size, 64, mask_zero=True),
#       layers.Conv1D(64, 5, padding="valid", activation="relu", strides=2),
#       layers.LSTM(32, input_shape=(None,64)),
#       layers.GlobalMaxPooling1D(),
#       layers.Dense(num_labels),
      
#   ])
#   return model

# vocab_size is VOCAB_SIZE + 1 since 0 is used additionally for padding.
# model = create_model(vocab_size=max_features + 1, num_labels=4)
vocab_size=max_features + 1
num_labels=4

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

for layer in model.layers:
    print(layer.name)
    print(layer.output_shape)

model.compile(
    loss=losses.SparseCategoricalCrossentropy(from_logits=True),
    optimizer='adam',
    metrics=['accuracy'])

checkpoint_path = "K-MersRandomMut_custom_NOR/cp.ckpt"
checkpoint_dir = os.path.dirname(checkpoint_path)

# Create a callback that saves the model's weights
cp_callback = tf.keras.callbacks.ModelCheckpoint(filepath=checkpoint_path,
                                                 save_weights_only=True,
                                                 verbose=1)

history = model.fit(train_ds, validation_data=val_ds, epochs=30,callbacks=[cp_callback])
#seems to start going back and forth after 85 epochs?


# print("ConvNet model on int vectorized data:")
# print(model.summary())

# int_loss, int_accuracy = model.evaluate(test_ds)
# print("Int model accuracy: {:2.2%}".format(int_accuracy))

# embedding_dim = 50
# model = tf.keras.Sequential([
#   layers.Embedding(max_features + 1, embedding_dim),
#   layers.Dropout(0.2),
#   layers.GlobalAveragePooling1D(),
#   layers.Dropout(0.2),
#   layers.Dense(1)])

# model.summary()

# # model = tf.keras.Sequential([
# #   tf.keras.layers.Embedding(
# #         input_dim=len(vectorize_layer.get_vocabulary()),
# #         output_dim=64,
# #         # Use masking to handle the variable sequence lengths
# #         mask_zero=True),
# #   tf.keras.layers.Bidirectional(tf.keras.layers.LSTM(64)),
# #   tf.keras.layers.Dense(64, activation='relu'),
# #   tf.keras.layers.Dense(1)])

# # model = tf.keras.Sequential([
# #   layers.Embedding(max_features + 1, embedding_dim),
# #   layers.Dropout(0.2),
# #   layers.GlobalAveragePooling1D(),
# #   layers.Dropout(0.2)])

# # Feed Forward Neural Network, 2 hidden layers (50 neurons, 25 neurons), output has 2 neurons. Input neurons = max_features + 1
# # model = tf.keras.Sequential()
# # model.add(Dense(30, input_dim = 50, activation="relu"))
# # model.add(Dense(15, kernel_initializer = "uniform", activation="relu"))
# # model.add(Dense(1))
# # model.add(Activation("softmax"))

# # sgd = SGD(lr = 0.01) #Stocastic gradient descent

# # model.summary()

# model.compile(loss=losses.BinaryCrossentropy(from_logits=True),
#               optimizer='adam',
#               metrics=tf.metrics.BinaryAccuracy(threshold=0.0))

# # model.compile(loss=losses.BinaryCrossentropy(from_logits=True),
# #               optimizer=sgd,
# #               metrics=tf.metrics.BinaryAccuracy(threshold=0.0))

# epochs = 1000
# # history = model.fit(
# #     train_ds,
# #     validation_data=val_ds,
# #     epochs=epochs,
# #     batch_size = 300)

# history = model.fit(
#     train_ds,
#     validation_data=val_ds,
#     epochs=epochs)

print(model.summary())
loss, accuracy = model.evaluate(test_ds)

print("Loss: ", loss)
print("Accuracy: ", accuracy)

history_dict = history.history
history_dict.keys()

acc = history_dict['accuracy']
val_acc = history_dict['val_accuracy']
loss = history_dict['loss']
val_loss = history_dict['val_loss']

epochs = range(1, len(acc) + 1)

# "bo" is for "blue dot"
plt.plot(epochs, loss, 'bo', label='Training loss')
# b is for "solid blue line"
plt.plot(epochs, val_loss, 'b', label='Validation loss')
plt.title('Training and validation loss')
plt.xlabel('Epochs')
plt.ylabel('Loss')
plt.legend()

plt.show()

plt.plot(epochs, acc, 'bo', label='Training acc')
plt.plot(epochs, val_acc, 'b', label='Validation acc')
plt.title('Training and validation accuracy')
plt.xlabel('Epochs')
plt.ylabel('Accuracy')
plt.legend(loc='lower right')

plt.show()

export_model = tf.keras.Sequential(
    [vectorize_layer, model,
     layers.Activation('sigmoid')])

export_model.compile(
    loss=losses.SparseCategoricalCrossentropy(from_logits=False),
    optimizer='adam',
    metrics=['accuracy'])

# Test it with `raw_test_ds`, which yields raw strings
loss, accuracy = export_model.evaluate(raw_test_ds)
print("Accuracy: {:2.2%}".format(accuracy))


os.listdir(checkpoint_dir)

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

# Evaluate the model
loss, acc = model.evaluate(test_ds, verbose=2)
print("Untrained model, accuracy: {:5.2f}%".format(100 * acc))

# Loads the weights
model.load_weights(checkpoint_path)

# Re-evaluate the model
loss, acc = model.evaluate(test_ds, verbose=2)
print("Restored model, accuracy: {:5.2f}%".format(100 * acc))
