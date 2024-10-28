import os
import joblib

output_path = "best_models/best_models.json"

# Print the absolute path
print(os.path.abspath(output_path))

models = {}

# Create the folder if it doesn't exist
if not os.path.exists(os.path.dirname(output_path)):
    print("Path does not exist.")
    os.makedirs(os.path.dirname(output_path))

# Check if the file already exists, if not, create an empty file
if not os.path.exists(output_path):
    open(output_path, 'a').close()

with open(output_path, "wb") as json_file:
    joblib.dump(models, json_file)
