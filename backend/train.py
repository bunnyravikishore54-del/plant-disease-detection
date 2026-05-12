import tensorflow as tf
from tensorflow.keras import layers, models
from tensorflow.keras.applications import EfficientNetB3
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras.callbacks import (
    ModelCheckpoint,
    EarlyStopping,
    ReduceLROnPlateau,
)
import os
import json
import matplotlib.pyplot as plt

# ── Configuration ──────────────────────────────────────────────────────────────
DATASET_DIR = "PlantVillage"
MODEL_SAVE_PATH = "saved_model/plant_model.h5"
IMG_SIZE = (224, 224)
BATCH_SIZE = 32
EPOCHS = 20

# Create output folder
os.makedirs("saved_model", exist_ok=True)

# ── Data Generators ────────────────────────────────────────────────────────────
train_datagen = ImageDataGenerator(
    rescale=1.0 / 255,
    rotation_range=30,
    width_shift_range=0.2,
    height_shift_range=0.2,
    shear_range=0.2,
    zoom_range=0.2,
    horizontal_flip=True,
    fill_mode="nearest",
    validation_split=0.2,
)

train_generator = train_datagen.flow_from_directory(
    DATASET_DIR,
    target_size=IMG_SIZE,
    batch_size=BATCH_SIZE,
    class_mode="categorical",
    subset="training",
    shuffle=True,
)

val_generator = train_datagen.flow_from_directory(
    DATASET_DIR,
    target_size=IMG_SIZE,
    batch_size=BATCH_SIZE,
    class_mode="categorical",
    subset="validation",
    shuffle=False,
)

# ── Automatically Detect Number of Classes ────────────────────────────────────
NUM_CLASSES = train_generator.num_classes

# Save class indices mapping
class_indices = train_generator.class_indices
idx_to_class = {str(v): k for k, v in class_indices.items()}

with open("saved_model/class_indices.json", "w") as f:
    json.dump(idx_to_class, f, indent=2)

print(f"✅ Classes found: {NUM_CLASSES}")
print(f"✅ Training samples: {train_generator.samples}")
print(f"✅ Validation samples: {val_generator.samples}")

# ── Build Model ────────────────────────────────────────────────────────────────
base_model = EfficientNetB3(
    weights="imagenet",
    include_top=False,
    input_shape=(*IMG_SIZE, 3),
)

# Freeze base model initially
base_model.trainable = False

model = models.Sequential([
    base_model,
    layers.GlobalAveragePooling2D(),
    layers.BatchNormalization(),

    layers.Dense(512, activation="relu"),
    layers.Dropout(0.4),

    layers.Dense(256, activation="relu"),
    layers.Dropout(0.3),

    # Dynamic output layer
    layers.Dense(NUM_CLASSES, activation="softmax"),
])

# ── Compile Model ──────────────────────────────────────────────────────────────
model.compile(
    optimizer=tf.keras.optimizers.Adam(learning_rate=1e-3),
    loss="categorical_crossentropy",
    metrics=["accuracy"],
)

model.summary()

# ── Callbacks ──────────────────────────────────────────────────────────────────
callbacks = [
    ModelCheckpoint(
        MODEL_SAVE_PATH,
        monitor="val_accuracy",
        save_best_only=True,
        verbose=1,
    ),
    EarlyStopping(
        monitor="val_accuracy",
        patience=5,
        restore_best_weights=True,
        verbose=1,
    ),
    ReduceLROnPlateau(
        monitor="val_loss",
        factor=0.2,
        patience=3,
        min_lr=1e-6,
        verbose=1,
    ),
]

# ── Phase 1: Train Top Layers ─────────────────────────────────────────────────
print("\n🔥 Phase 1: Training top layers...")

history1 = model.fit(
    train_generator,
    validation_data=val_generator,
    epochs=10,
    callbacks=callbacks,
    verbose=1,
)

# ── Phase 2: Fine-Tuning ──────────────────────────────────────────────────────
print("\n🔥 Phase 2: Fine-tuning...")

base_model.trainable = True

# Freeze all except last 30 layers
for layer in base_model.layers[:-30]:
    layer.trainable = False

# Recompile with lower learning rate
model.compile(
    optimizer=tf.keras.optimizers.Adam(learning_rate=1e-5),
    loss="categorical_crossentropy",
    metrics=["accuracy"],
)

history2 = model.fit(
    train_generator,
    validation_data=val_generator,
    epochs=EPOCHS,
    callbacks=callbacks,
    verbose=1,
)

# ── Combine Histories ─────────────────────────────────────────────────────────
all_acc = history1.history["accuracy"] + history2.history["accuracy"]
all_val_acc = history1.history["val_accuracy"] + history2.history["val_accuracy"]

all_loss = history1.history["loss"] + history2.history["loss"]
all_val_loss = history1.history["val_loss"] + history2.history["val_loss"]

# ── Plot Results ───────────────────────────────────────────────────────────────
plt.figure(figsize=(12, 5))

# Accuracy Plot
plt.subplot(1, 2, 1)
plt.plot(all_acc, label="Train Accuracy")
plt.plot(all_val_acc, label="Validation Accuracy")
plt.title("Model Accuracy")
plt.xlabel("Epoch")
plt.ylabel("Accuracy")
plt.legend()

# Loss Plot
plt.subplot(1, 2, 2)
plt.plot(all_loss, label="Train Loss")
plt.plot(all_val_loss, label="Validation Loss")
plt.title("Model Loss")
plt.xlabel("Epoch")
plt.ylabel("Loss")
plt.legend()

plt.tight_layout()
plt.savefig("saved_model/training_history.png")
plt.show()

# ── Final Messages ─────────────────────────────────────────────────────────────
print(f"\n✅ Model saved to: {MODEL_SAVE_PATH}")
print("✅ Class mapping saved to: saved_model/class_indices.json")
print("✅ Training graph saved to: saved_model/training_history.png")
print("🎉 Training complete!")