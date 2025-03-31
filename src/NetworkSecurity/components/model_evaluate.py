import pandas as pd
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score
import mlflow
from src.NetworkSecurity.utils.common import save_json
import pickle
from src.NetworkSecurity.entity.config_entity import ModelEvaluationConfig

class ModelEvaluate:
    def __init__(self, config: ModelEvaluationConfig):
        self.config = config
    
    def eval_metrics(self, actual, pred):
        accuracy = accuracy_score(actual, pred)
        precision = precision_score(actual, pred, average='weighted')
        recall = recall_score(actual, pred, average='weighted')
        f1 = f1_score(actual, pred, average='weighted')
        return accuracy, precision, recall, f1 

    def validate_model(self, model_uri, sample_input):
        """Validates the model before using it for evaluation."""
        try:
            mlflow.models.predict(
                model_uri=model_uri,
                input_data=sample_input,
                env_manager="uv",
            )
            print(" Model validation successful!")
        except Exception as e:
            print(f"Model validation failed: {e}")
            raise e
    
    def evaluate(self):
        test_data = pd.read_csv(self.config.test_data_path)
        x_test = test_data.drop([self.config.target_column], axis=1)
        y_test = test_data[self.config.target_column]

        with open(self.config.ss_file_path, "rb") as file:
            scaler = pickle.load(file)
        x_test = scaler.transform(x_test)

        mlflow.set_tracking_uri(self.config.mlflow_uri)
        mlflow.set_registry_uri(self.config.mlflow_uri)
        
        model_uri = f"runs:/{self.config.model_run}/model"
        loaded_model = mlflow.pyfunc.load_model(model_uri)

        # Validate model
        sample_input = x_test[:1]  # Taking a single row for validation
        self.validate_model(model_uri, sample_input)

        # Predict
        y_pred = loaded_model.predict(pd.DataFrame(x_test))
        # Evaluate
        accuracy, precision, recall, f1 = self.eval_metrics(y_test, y_pred)

        scores = {
            "accuracy": accuracy,
            "precision": precision,
            "recall": recall,
            "f1_score": f1,
        }

        save_json(self.config.metric_file_name,scores)
        print(f"Evaluation Metrics - Accuracy: {accuracy}, Precision: {precision}, Recall: {recall}, F1 Score: {f1}")
