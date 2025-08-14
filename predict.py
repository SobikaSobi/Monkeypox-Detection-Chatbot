from tensorflow.keras.preprocessing import image
import numpy as np
import tensorflow as tf

# Load the trained model
classifierLoad = tf.keras.models.load_model('model.h5')

# Load and preprocess the test image
test_image = image.load_img('static/upload/Test.png', target_size=(150, 150))
test_image = image.img_to_array(test_image)  # Convert to array
test_image = test_image / 255.0  # Rescale as done during training
test_image = np.expand_dims(test_image, axis=0)  # Expand dimensions for batch format

# Make prediction
result = classifierLoad.predict(test_image)
print(result)

# Get the index of the highest probability class
ind = np.argmax(result)

# Map the index to the class name
class_labels = ['Chickenpox', 'Measles', 'Monkeypox', 'Normal']  # Update this to match your classes
predicted_class = class_labels[ind]

# Output the result
print(f"Predicted class: {predicted_class} with probability: {result[0][ind]}")
