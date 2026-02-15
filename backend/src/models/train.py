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

def main():
    
    # Download Data
    dataset_path = download_and_extract_data()
    
    # If standard path doesn't exist, use the downloaded one
    train_dir = os.path.join(dataset_path, "train")
    val_dir = os.path.join(dataset_path, "validation")
    
    # Verify directories exist
    if not os.path.exists(train_dir):
        print(f"Error: Train directory not found at {train_dir}")
        return

    train_gen = ImageDataGenerator(
        rescale=1./255,
        rotation_range=20,
        zoom_range=0.2,
        horizontal_flip=True
    )

    test_gen = ImageDataGenerator(rescale=1./255)

    train_data = train_gen.flow_from_directory(
        train_dir,
        target_size=(224, 224),
        batch_size=BATCH_SIZE,
        class_mode="binary"
    )

    val_data = test_gen.flow_from_directory(
        val_dir,
        target_size=(224, 224),
        batch_size=BATCH_SIZE,
        class_mode="binary",
        shuffle=False
    )
    
    # For test, we reuse validation set for simplicity in this pipeline context
    test_data = val_data

    model = build_baseline_cnn()

    with mlflow.start_run():
        mlflow.log_param("epochs", EPOCHS)
        mlflow.log_param("batch_size", BATCH_SIZE)

        history = model.fit(
            train_data,
            validation_data=val_data,
            epochs=EPOCHS
        )

        # ---------- Evaluate on test ----------
        y_true = test_data.classes
        y_prob = model.predict(test_data)
        y_pred = (y_prob > 0.5).astype(int).flatten()

        # ---------- Confusion Matrix ----------
        os.makedirs("artifacts", exist_ok=True)
        cm_path = "artifacts/confusion_matrix.png"

        plot_confusion_matrix(
            y_true=y_true,
            y_pred=y_pred,
            class_names=["Cat", "Dog"],
            save_path=cm_path
        )

        mlflow.log_artifact(cm_path)

        # ---------- Save model ----------
        model.save("model.h5")
        mlflow.log_artifact("model.h5")

        # ---------- Log metrics ----------
        test_loss, test_acc = model.evaluate(test_data)
        mlflow.log_metric("test_accuracy", test_acc)
        mlflow.log_metric("test_loss", test_loss)

        for epoch in range(EPOCHS):
            mlflow.log_metric("train_accuracy", history.history["accuracy"][epoch], step=epoch)
            mlflow.log_metric("val_accuracy", history.history["val_accuracy"][epoch], step=epoch)
            mlflow.log_metric("train_loss", history.history["loss"][epoch], step=epoch)
            mlflow.log_metric("val_loss", history.history["val_loss"][epoch], step=epoch)

if __name__ == "__main__":
    main()
