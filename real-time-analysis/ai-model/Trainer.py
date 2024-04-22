import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Conv1D, BatchNormalization, MaxPooling1D, Dropout, Flatten, Dense
from tensorflow.keras.regularizers import l2

# TAKEN FROM THE THESIS


def build_1d_cnn(input_shape):
    model = Sequential()

    # First convolutional block
    model.add(Conv1D(filters=64, kernel_size=3, activation='relu',
              input_shape=input_shape, kernel_regularizer=l2(0.01), bias_regularizer=l2(0.01)))
    model.add(BatchNormalization())
    model.add(MaxPooling1D(pool_size=2))
    model.add(Dropout(0.2))

    # Second convolutional block
    model.add(Conv1D(filters=128, kernel_size=3, activation='relu',
              kernel_regularizer=l2(0.01), bias_regularizer=l2(0.01)))
    model.add(BatchNormalization())
    model.add(MaxPooling1D(pool_size=2))
    model.add(Dropout(0.1))

    # Flattening the layers to feed into a fully connected layer
    model.add(Flatten())

    # Fully connected layers
    model.add(Dense(units=128, activation='relu'))
    model.add(Dense(units=64, activation='relu'))

    # Output layer
    # Assuming 2D coordinates as output
    model.add(Dense(units=2, activation='linear'))

    return model


# Assuming input_shape is (36000, 4) for raw audio data or (spectrogram_height, spectrogram_width, 4) for spectrogram input
input_shape = (36000, 4)  # or (128, 128, 4) for spectrogram input
model = build_1d_cnn(input_shape)

# Compile the model
model.compile(optimizer='adam', loss='mean_squared_error')

# Assuming you have prepared your training data as per the thesis
# X_train, y_train = your_data_loader_function()

# Train the model
# model.fit(X_train, y_train, batch_size=32, epochs=100, validation_split=0.1)
