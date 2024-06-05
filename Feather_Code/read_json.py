import ujson
import numpy as np

def load_config(filename):
    with open(filename, 'r') as f:
        config = ujson.load(f)
    return config

def similarity_score(vector1, vector2):

    array1 = np.array(vector1)
    array2 = np.array(vector2)
    
    # Compute dot product
    dot_product = np.dot(array1, array2)
    
    # Compute magnitudes
    magnitude1 = np.linalg.norm(array1)
    magnitude2 = np.linalg.norm(array2)
    
    # Handle division by zero
    if magnitude1 == 0 or magnitude2 == 0:
        return 0.0
    
    # Compute similarity score with magnitude adjustment
    similarity = dot_product / (magnitude1 * magnitude2)
    
    # Normalize between 0 and 1
    normalized_similarity = (similarity + 1) / 2
    
    return normalized_similarity

config = load_config('diagnostic_results_varying.json')
user_data = config.get('user', {}).get('data', [])
blend_data = config.get('blend', {}).get('data', [])
alpha_data = config.get('alpha', {}).get('data', [])
# Open the serial port


# # Send data in a loop
# while True:
#     for i in range(len(user_data)-1):
#         data = str(similarity_score(user_data[i][0], blend_data[i][0]))

