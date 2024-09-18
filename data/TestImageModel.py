from skimage import io, transform
import numpy as np
import pickle

# Load the model from the file
with open('./data/model.p', 'rb') as file:
    loaded_model = pickle.load(file)

# Load and preprocess the image (e.g., resize to 28x28 pixels and convert to grayscale if necessary)
image = io.imread('./data/CatPics/bento_orig/2024-09-16_12-45-56.jpg')
image_resized =  transform.rescale(image, (.25/.7))

# Flatten the image to match the input shape expected by the SVC model
image_flattened = image_resized.flatten()

# Convert to a 2D array as the model expects an array of samples
image_for_model = np.array([image_flattened])

# Use the loaded model to predict the class
prediction = loaded_model.predict(image_for_model)

print(f"Predicted class: {prediction}")
