import json

from utilities.file_searcher import PathFinder


def add_model(new_model_data):
    try:
        file_path = PathFinder.get_complet_path("ressources/json_files/models.json")
        # Load the existing data
        with open(file_path, 'r') as file:
            data = json.load(file)
        models = data.get('models', [])

        # Check if the model already exists
        found = False
        for model in models:
            if model['name'] == new_model_data["name"]:
                # Update existing model
                model['parameters'] = new_model_data['parameters']
                model['status'] = new_model_data['status']
                found = True
                break

        if not found:
            # Add new model if not found
            models.append({
                "name": new_model_data["name"],
                "parameters": new_model_data['parameters'],
                "status": new_model_data['status']
            })

        # Write the updated models list back to the file
        with open(file_path, 'w') as file:
            json.dump(data, file, indent=4)
        print(f"Model '{new_model_data["name"]}' updated/added successfully.")
    except Exception as e:
        print(f"Error updating/adding model '{new_model_data["name"]}': {str(e)}")
