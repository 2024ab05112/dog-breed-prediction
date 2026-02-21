import os
import mlflow
import tensorflow as tf
import numpy as np

from tensorflow.keras.preprocessing.image import ImageDataGenerator
from src.models.model import build_baseline_cnn
from src.utils.metrics import plot_confusion_matrix


DATA_DIR = "data/processed"
BATCH_SIZE = 32
EPOCHS = 1

# Trigger model training pipeline with MLflow for real this time
# Now that OOM is fixed, this should inject data correctly
MLFLOW_URL = "https://dog-breed-prediction.centralindia.cloudapp.azure.com/mlflow"
mlflow.set_tracking_uri(MLFLOW_URL)

mlflow.set_experiment("cats_vs_dogs_baseline")

# Function to download small subset dataset
def download_and_extract_data():
    
    # Check if data already exists
    if os.path.exists(os.path.join(DATA_DIR, "train/cats")):
        print(f"Data found at {DATA_DIR}, skipping download.")
        return

    print("Downloading dataset...")
    
    # Using a small subset of Cats vs Dogs hosted publicly for easy CI/CD usage
    # Original Source: Kaggle / Microsoft (Dogs vs Cats)
    # This URL points to a curated small zip (~20MB) perfect for quick training
    url = "https://storage.googleapis.com/mledu-datasets/cats_and_dogs_filtered.zip"
    
    zip_path = tf.keras.utils.get_file("cats_and_dogs.zip", origin=url, extract=True)
    base_dir = os.path.dirname(zip_path) # ~/.keras/datasets/
    dataset_dir = os.path.join(base_dir, "cats_and_dogs_filtered")
    
    # Create symlink or copy to expected location
    os.makedirs(DATA_DIR, exist_ok=True)
    
    # We will point the generators to the downloaded location directly to keep it simple
    return dataset_dir

mlflow.set_experiment("cats_vs_dogs_transfer_learning")

import tensorflow_datasets as tfds

def preprocess(image, label):
    image = tf.image.resize(image, (224, 224))
    image = tf.cast(image, tf.float32) / 255.0
    return image, label

def main():
    print("Downloading dataset using TensorFlow Datasets...")
    
    # Load Cats vs Dogs dataset using TFDS
    # We use 'train[:20%]' to keep data small for quick CI training
    # For real training, remove [:20%] or increase percentage
    dataset, info = tfds.load(
        'cats_vs_dogs', 
        split='train[:20%]', 
        as_supervised=True, 
        with_info=True
    )
    
    # Create validation split from the remaining data if needed, or just split train
    # Here we split the 20% into 80% train / 20% val
    train_size = int(0.8 * len(dataset))
    train_ds = dataset.take(train_size)
    val_ds = dataset.skip(train_size)
    
    # Apply preprocessing pipeline
    train_ds = train_ds.map(preprocess, num_parallel_calls=tf.data.AUTOTUNE).shuffle(1000).batch(BATCH_SIZE).prefetch(tf.data.AUTOTUNE)
    val_ds = val_ds.map(preprocess, num_parallel_calls=tf.data.AUTOTUNE).batch(BATCH_SIZE).prefetch(tf.data.AUTOTUNE)

    model = build_baseline_cnn()

    with mlflow.start_run():
        mlflow.log_param("epochs", EPOCHS)
        mlflow.log_param("batch_size", BATCH_SIZE)

        history = model.fit(
            train_ds,
            validation_data=val_ds,
            epochs=EPOCHS
        )

        # ---------- Confusion Matrix & Evaluation ----------
        # Evaluate on validation set
        y_true = []
        y_pred = []
        
        # Iterate over validation dataset to get predictions
        for images, labels in val_ds:
            preds = model.predict(images)
            y_true.extend(labels.numpy())
            y_pred.extend((preds > 0.5).astype(int).flatten())
        
        y_true = np.array(y_true)
        y_pred = np.array(y_pred)

        os.makedirs("artifacts", exist_ok=True)
        cm_path = "artifacts/confusion_matrix.png"

        try:
            plot_confusion_matrix(
                y_true=y_true,
                y_pred=y_pred,
                class_names=["Cat", "Dog"],
                save_path=cm_path
            )
            mlflow.log_artifact(cm_path)
        except Exception as e:
            print(f"Warning: Could not plot CM: {e}")

        # ---------- Save model ----------
        model.save("model.h5")
        mlflow.log_artifact("model.h5")

        # ---------- Log metrics ----------
        test_loss, test_acc = model.evaluate(val_ds)
        mlflow.log_metric("test_accuracy", test_acc)
        mlflow.log_metric("test_loss", test_loss)

        for epoch in range(EPOCHS):
            mlflow.log_metric("train_accuracy", history.history["accuracy"][epoch], step=epoch)
            mlflow.log_metric("val_accuracy", history.history["val_accuracy"][epoch], step=epoch)
            mlflow.log_metric("train_loss", history.history["loss"][epoch], step=epoch)
            mlflow.log_metric("val_loss", history.history["val_loss"][epoch], step=epoch)

if __name__ == "__main__":
    main()
