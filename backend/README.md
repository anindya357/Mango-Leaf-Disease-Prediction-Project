# Mango Leaf Disease Prediction Backend

This backend is a **Streamlit-based web app** for predicting mango leaf diseases using a trained MobileNetV2 deep learning model.

## 🌟 Running the App

Start the interactive Streamlit app:

```bash
streamlit run app.py
```

The app will open automatically at `http://localhost:8501`

**Features:**
- Beautiful UI with gradient design
- Drag & drop image upload
- Real-time disease prediction
- Confidence visualization with progress bars
- Treatment recommendations
- Sidebar with disease information

## Features

### Streamlit App
- **Interactive UI**: Modern, responsive web interface
- **Real-time Analysis**: Instant disease detection
- **Confidence Visualization**: Bar charts showing prediction probabilities
- **Treatment Guidance**: Step-by-step recommendations
- **Professional Design**: Custom CSS styling with gradient theme
- **Disease Information**: Emojis and descriptions for each condition

## Supported Diseases

1. 🦠 Anthracnose
2. ⚫ Bacterial Canker
3. 🐛 Cutting Weevil
4. 🤎 Die Back
5. 🪰 Gall Midge
6. ✅ Healthy
7. ☁️ Powdery Mildew
8. 🖤 Sooty Mould

## Setup

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Verify Model Location

The model file should be at:
```
../notebooks/mango_leaf_disease_MobileNetV2_model.h5
```

If using a different path, update line 53-54 in `app.py`:
```python
model_path = os.path.join(os.path.dirname(__file__), "path/to/model.h5")
```

Run the training notebook (`notebooks/train_model.ipynb`) to generate this file if it doesn't exist.

### 3. Run Streamlit App

```bash
streamlit run app.py
```



## Project Structure

```
backend/
├── app.py                             # Streamlit application entry point
├── main.py                            # FastAPI application (not used)
├── requirements.txt                   # Python dependencies
└── utils/
    ├── model_loader.py               # Model management
    └── preprocess.py                 # Image preprocessing utilities
```

## Notes

- Images are automatically resized to 224x224 pixels (MobileNetV2 input size)
- Pixel values are normalized to 0-1 range
- The model uses batch normalization and dropout for regularization
- All predictions are returned with probabilities for all 8 disease classes
- Model is loaded once at startup for performance
- Images are processed in-memory (not stored on disk)
