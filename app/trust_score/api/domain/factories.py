from transformers import AutoTokenizer, AutoModelForSequenceClassification, Trainer, TrainingArguments
import numpy as np
from sklearn.metrics import mean_squared_error
from datasets import Dataset


class ModelFactory:
    def __init__(self, model_name: str, num_labels: int):
        self.model_name = model_name
        self.num_labels = num_labels

    def create_tokenizer(self):
        return AutoTokenizer.from_pretrained(self.model_name)

    def create__model(self):
        return AutoModelForSequenceClassification.from_pretrained(self.model_name, num_labels=self.num_labels)


class TrainerFactory:
    def __init__(self, source_model_name: str, dest_model_name: str, num_labels: int):
        self.source_model_name = source_model_name
        self.dest_model_name = dest_model_name
        self.source_model_factory = ModelFactory(source_model_name, num_labels=num_labels)
        self.dest_model_factory = ModelFactory(dest_model_name, num_labels=num_labels)

    def create_trainer(self, dataset: Dataset):
        training_args = TrainingArguments(
            output_dir=self.dest_model_name,
            eval_strategy="epoch",
            learning_rate=2e-5,
            per_device_train_batch_size=4,
            per_device_eval_batch_size=4,
            num_train_epochs=3,
            weight_decay=0.01,
            logging_dir="./logs_multi",
            logging_steps=10,
        )

        # -------------------------------
        # 5. Metric: RMSE für jede Dimension
        # -------------------------------

        def compute_metrics(eval_pred):
            logits, labels = eval_pred
            preds = logits  # shape: (batch, num_labels)
            rmse = np.sqrt(mean_squared_error(y_pred=preds, y_true=labels, multioutput="uniform_average"))
            return {"rmse": rmse}

        tokenizer = self.source_model_factory.create_tokenizer()


        # -------------------------------
        # 6. Trainer konfigurieren
        # -------------------------------
        trainer = Trainer(
            model=self.create_source_model(),
            args=training_args,
            train_dataset=dataset,
            eval_dataset=dataset,
            tokenizer=tokenizer,
            compute_metrics=compute_metrics,
        )
        return trainer

    def create_source_model(self):
        return self.source_model_factory.create__model()

    def create_dest_model(self):
        return self.dest_model_factory.create__model()
