import pandas as pd
import numpy as np
import time
import shutil
import os
import tensorflow as tf
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder

# Load and preprocess data
resting_data = pd.read_csv('/home/sensor-hub2/Documents/Pi_codes/ML/Training_set/sensor_data_resting.csv')
walking_data = pd.read_csv('/home/sensor-hub2/Documents/Pi_codes/ML/Training_set/sensor_data_walking.csv')
running_data = pd.read_csv('/home/sensor-hub2/Documents/Pi_codes/ML/Training_set/sensor_data_running.csv')

# Combine all data into a single dataframe
data = pd.concat([resting_data, walking_data, running_data], ignore_index=True)
print(data)

# Drop rows with missing values
data = data.dropna()
print(data)
# Split data into input features (X) and output target (y)
X = data.drop(['label'], axis=1)
y = data['label']
print(X)
# Split data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)

# Fit the scaler only on the training set and transform the validation and test sets separately
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)
print(X_train_scaled)

# Convert categorical labels to numerical values
label_encoder = LabelEncoder()
y_train_encoded = label_encoder.fit_transform(y_train)
y_test_encoded = label_encoder.transform(y_test)

# Perform one-hot encoding on the numerical labels
num_classes = len(label_encoder.classes_)
y_train_onehot = tf.keras.utils.to_categorical(y_train_encoded, num_classes=num_classes)
y_test_onehot = tf.keras.utils.to_categorical(y_test_encoded, num_classes=num_classes)

# Building our model
model = tf.keras.Sequential([
    tf.keras.layers.Dense(64, activation='relu', input_shape=(5,)),
    tf.keras.layers.Dense(32, activation='relu'),
    tf.keras.layers.Dense(num_classes, activation='softmax')
])

model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])

# Add early stopping callback to prevent overfitting
early_stop = tf.keras.callbacks.EarlyStopping(monitor='val_loss', patience=10)

# Training the model
history = model.fit(X_train_scaled, y_train_onehot, batch_size=32, epochs=100, validation_split=0.2,
                    callbacks=[early_stop])

# Evaluating the model on the test set
test_loss, test_acc = model.evaluate(X_test_scaled, y_test_onehot)
print('Test Loss:', test_loss)
print('Test Accuracy:', test_acc)

# Making predictions on the entire dataset
X_scaled = scaler.transform(X)
print(X_scaled.shape)
predictions = model.predict(X_scaled, verbose=0)
predicted_labels = label_encoder.inverse_transform(np.argmax(predictions, axis=1))
print('Predicted Labels:', predicted_labels)

file_number = 2  # Set the initial file number 

while True:
    # Specify the original file path
    original_file_path = f"/home/sensor-hub2/Documents/Pi_codes/Hub2_data/Hub2_sensor_data_{file_number}.csv"
        
    # Specify the new folder path
    new_folder_path = "/home/sensor-hub2/Documents/Pi_codes/ML/ML_data"

    # Create the new folder if it doesn't exist
    if not os.path.exists(new_folder_path):
        os.makedirs(new_folder_path)

    # Specify the new file path
    new_file_path = os.path.join(new_folder_path, f"Hub2_ML_data_{file_number}.csv")

    # Copy the original file to the new file path
    shutil.copyfile(original_file_path, new_file_path)

    # Read real-time data from the copied file
    realtime_data = pd.read_csv(new_file_path)

    realtime_data = realtime_data.drop(['Time', 'Sensor1a', 'Amb_Temp', 'Sensor1b', 'Sensor1c', 'Sensor1d',
                                         'Sensor2a', 'Volume', 'Sensor2b', 'Volume_%', 'Sensor3a', 'Batttery_V', 'Sensor3b', 'Batttery_Level_%', 'Sensor4a',
                                         'Pressure', 'Sensor4b', 'Pressure_%', 'Sensor5a', 'Body_Temp_C', 'Sensor5b', 'Sensor6a',
                                         'BPM', 'IBI'], axis=1)

    if realtime_data.isna().sum().sum() > 0:
        # Fill missing values if necessary
        realtime_data = realtime_data.fillna(X.mean())  # or any other appropriate strategy

    # Preprocess the data using the scaler object used in the previous code
    realtime_data_scaled = scaler.transform(realtime_data)

    # Use the trained model to predict the class probabilities for the new data
    predictions_live = model.predict(realtime_data_scaled)

    # Define thresholds for each sensor and activity
    sensor_thresholds = {
        'resting': {'Accel_X': [-0.1, -0.5, -0.8], 'Accel_Y': [0, 0.3, 0.5], 'Accel_Z': [9.93, 9.96, 10],
                    'Heart_rate': [50, 65, 80], 'Body_Temp_F': [89, 90, 91]},
        'walking': {'Accel_X': [0.9, 1.4, 1.9], 'Accel_Y': [-0.5, 0, 0.5], 'Accel_Z': [9, 9.3, 10],
                    'Heart_rate': [50, 70, 90], 'Body_Temp_F': [85, 86, 87]},
        'running': {'Accel_X': [1, 2, 3], 'Accel_Y': [-3, -1.5, 0], 'Accel_Z': [0.1, 0.3, 0.6],
                    'Heart_rate': [130, 150, 170], 'Body_Temp_F': [75, 76, 77]},
    }

    # Classify the current astronaut’s condition based on the predicted probabilities and thresholds
    predicted_label = label_encoder.inverse_transform(np.argmax(predictions_live, axis=1))[0]

    # Get the predicted probabilities for each activity class
    resting_prob = predictions_live[0][0]
    walking_prob = predictions_live[0][1]
    running_prob = predictions_live[0][2]

    # Get the sensor readings
    accel_x = realtime_data_scaled[0]  # replace with accelerometer x data
    accel_y = realtime_data_scaled[1]  # replace with accelerometer y data
    accel_z = realtime_data_scaled[2]  # replace with accelerometer z data
    body_temp_reading = realtime_data_scaled[3]  # replace with body temperature data
    heart_rate_reading = realtime_data_scaled[4]  # replace with heartbeat data

    # Create boolean masks for NaN values
    mask_accel_x = np.isnan(accel_x)
    mask_accel_y = np.isnan(accel_y)
    mask_accel_z = np.isnan(accel_z)
    mask_body_temp_reading = np.isnan(body_temp_reading)
    mask_heart_rate_reading = np.isnan(heart_rate_reading)

    # Use boolean indexing to filter out rows with NaN values
    Accel_X = accel_x[~(mask_accel_x | mask_accel_y | mask_accel_z | mask_body_temp_reading | mask_heart_rate_reading)]
    accel_Y = accel_y[~(mask_accel_x | mask_accel_y | mask_accel_z | mask_body_temp_reading | mask_heart_rate_reading)]
    Accel_Z = accel_z[~(mask_accel_x | mask_accel_y | mask_accel_z | mask_body_temp_reading | mask_heart_rate_reading)]
    Body_Temp_F = body_temp_reading[
        ~(mask_accel_x | mask_accel_y | mask_accel_z | mask_body_temp_reading | mask_heart_rate_reading)]
    Heart_rate = heart_rate_reading[
        ~(mask_accel_x | mask_accel_y | mask_accel_z | mask_body_temp_reading | mask_heart_rate_reading)]

    # Determine condition label based on predicted activity and sensor-specific thresholds
    if predicted_label == 'resting':
        thresholds = sensor_thresholds[predicted_label]
        # rest threshold logic here
    elif predicted_label == 'walking':
        thresholds = sensor_thresholds[predicted_label]
        # walking threshold logic here
    else:
        thresholds = sensor_thresholds[predicted_label]

        abnormal = False
        count_normal = 0
        count_normal_minus = 0
        count_normal_plus = 0

        if np.all(heart_rate_reading >= thresholds['Heart_rate'][0]):
            count_normal += 1
        elif np.all(heart_rate_reading >= thresholds['Heart_rate'][1]):
            count_normal_minus += 1
        elif np.all(heart_rate_reading >= thresholds['Heart_rate'][2]):
            count_normal_plus += 1
        else:
            abnormal = True

        if np.all(body_temp_reading >= thresholds['Body_Temp_F'][0]):
            if not abnormal:
                count_normal += 1
            elif count_normal == 0:
                abnormal = True
        elif np.all(body_temp_reading >= thresholds['Body_Temp_F'][1]):
            if not abnormal:
                count_normal_minus += 1
            elif count_normal_minus == 0:
                abnormal = True
        elif np.all(body_temp_reading >= thresholds['Body_Temp_F'][2]):
            if not abnormal:
                count_normal_plus += 1
            elif count_normal_plus == 0:
                abnormal = True
        else:
            abnormal = True

        if np.all(accel_x <= thresholds['Accel_X'][0]) and np.all(accel_y <= thresholds['Accel_Y'][0]) and np.all(
                accel_z <= thresholds['Accel_Z'][0]):
            if not abnormal:
                count_normal += 1
            elif count_normal == 0:
                abnormal = True
        elif np.all(accel_x <= thresholds['Accel_X'][1]) and np.all(accel_y <= thresholds['Accel_Y'][1]) and np.all(
                accel_z <= thresholds['Accel_Z'][1]):
            if not abnormal:
                count_normal_minus += 1
            elif count_normal_minus == 0:
                abnormal = True
        elif np.all(accel_x <= thresholds['Accel_X'][2]) and np.all(accel_y <= thresholds['Accel_Y'][2]) and np.all(
                accel_z <= thresholds['Accel_Z'][2]):
            if not abnormal:
                count_normal_plus += 1
            elif count_normal_plus == 0:
                abnormal = True
        else:
            abnormal = True

        if abnormal:
            condition = 'abnormal'
        elif count_normal > count_normal_minus and count_normal > count_normal_plus:
            condition = 'normal'
        elif count_normal_minus > count_normal and count_normal_minus > count_normal_plus:
            condition = 'normal -'
        elif count_normal_plus > count_normal and count_normal_plus > count_normal_minus:
            condition = 'normal +'
        else:
            condition = 'undetermined'

    print('Predicted Activity:', predicted_label)
    print('Condition:', condition)

    # Add the predicted activity and condition as new columns in the DataFrame
    data['Predicted_Activity'] = predicted_labels
    data['Status'] = condition

    # Save the updated DataFrame to the original file, without overwriting existing data
    data.to_csv(f"/home/sensor-hub2/Documents/Pi_codes/ML/ML_data/Hub2_ML_data_{file_number}.csv", index=False) 

    # Create a new DataFrame with the predicted activity and condition columns
    new_data = pd.DataFrame({'Predicted Activity': predicted_labels, 'Status': condition})
    print(new_data.shape)
    # Read the original CSV file into a DataFrame
    original_data = pd.read_csv(original_file_path)
    print(original_data.shape)

    print(new_data)
    # Read the original CSV file into a DataFrame
    original_data = pd.read_csv(original_file_path)

    # Create a new DataFrame with the predicted activity and condition columns
    new_data = pd.DataFrame({'Predicted Activity': predicted_labels, 'Status': condition})

    # Concatenate the original DataFrame with the new DataFrame horizontally and sort by the index
    combined_data = pd.concat([original_data, new_data], axis=1).sort_index(axis=1)

    combined_data = combined_data.drop(['Sensor1a', 'Sensor1b', 'Sensor1c', 'Sensor1d', 'Sensor2a',  'Sensor2b', 
                                        'Sensor3a', 'Sensor3b', 'Sensor4a', 'Sensor4b',  'Sensor5a', 'Sensor5b', 'Sensor6a'], axis=1) 
    # Drop rows with missing values
    combined_data = combined_data.dropna()
    print(combined_data)
    # Save the updated DataFrame to the original file, overwriting existing data
    combined_data.to_csv(original_file_path, index=False)

    file_number += 1
    time.sleep(150)
