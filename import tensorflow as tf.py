import tensorflow as tf
from tensorflow.keras import layers, models

# Define a simple Vision Transformer (ViT) model
def create_vit_model(image_size, patch_size, num_classes):
    num_patches = (image_size // patch_size) ** 2
    projection_dim = 64
    num_heads = 4
    transformer_units = [projection_dim * 2, projection_dim]
    transformer_layers = 8
    mlp_head_units = [2048, 1024]  # Size of the dense layers of the final classifier

    inputs = layers.Input(shape=(image_size, image_size, 3))
    
    # Create patches
    patches = layers.Conv2D(projection_dim, kernel_size=patch_size, strides=patch_size)(inputs)
    patches = layers.Reshape((num_patches, -1))(patches)
    
    # Add positional encoding
    positions = tf.range(start=0, limit=num_patches, delta=1)
    positional_encoding = layers.Embedding(input_dim=num_patches, output_dim=projection_dim)(positions)
    encoded_patches = patches + positional_encoding
    
    # Create multiple Transformer blocks
    for _ in range(transformer_layers):
        # Layer Normalization
        x1 = layers.LayerNormalization(epsilon=1e-6)(encoded_patches)
        # Multi-head Self-Attention
        attention_output = layers.MultiHeadAttention(num_heads=num_heads, key_dim=projection_dim)(x1, x1)
        # Skip connection
        x2 = layers.Add()([attention_output, encoded_patches])
        # Layer Normalization
        x3 = layers.LayerNormalization(epsilon=1e-6)(x2)
        # MLP
        x3 = layers.Dense(transformer_units[0], activation=tf.nn.gelu)(x3)
        x3 = layers.Dense(transformer_units[1], activation=tf.nn.gelu)(x3)
        # Skip connection
        encoded_patches = layers.Add()([x3, x2])
    
    # Global average pooling
    representation = layers.LayerNormalization(epsilon=1e-6)(encoded_patches)
    representation = layers.GlobalAveragePooling1D()(representation)
    
    # Final classification head
    features = layers.Flatten()(representation)
    for units in mlp_head_units:
        features = layers.Dense(units, activation=tf.nn.gelu)(features)
    logits = layers.Dense(num_classes)(features)
    
    # Create the Keras model
    model = models.Model(inputs=inputs, outputs=logits)
    
    return model

# Create the model
vit_model = create_vit_model(image_size=img_size, patch_size=16, num_classes=1)

# Compile the model
vit_model.compile(optimizer=tf.keras.optimizers.Adam(learning_rate=3e-4),
                  loss=tf.keras.losses.BinaryCrossentropy(from_logits=True),
                  metrics=['accuracy'])

vit_model.summary()
