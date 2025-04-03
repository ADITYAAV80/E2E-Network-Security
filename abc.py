import mlflow


mlflow_tracking_uri = "https://dagshub.com/adityaav80/E2E-Network-Security.mlflow"
model_name = "Best Model"

mlflow.set_tracking_uri(mlflow_tracking_uri)
print(mlflow.search_registered_models())
try:
    # Option 1: Load the latest production model
    model = mlflow.pyfunc.load_model(f"models:/{model_name}/latest")
except Exception as e:
    print("error",str(e))

