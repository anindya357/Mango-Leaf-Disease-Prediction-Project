import os
import streamlit as st
from PIL import Image
import numpy as np
import tensorflow as tf
import json
import tempfile
import h5py
import shutil

def load_model_with_config_fix(model_path):
    """Load model and fix quantization_config compatibility issue"""
    try:
        # Try standard loading first
        return tf.keras.models.load_model(model_path, compile=False)
    except TypeError as e:
        if "quantization_config" in str(e):
            # Copy model to temp file for modification
            temp_dir = tempfile.mkdtemp()
            temp_model_path = os.path.join(temp_dir, "temp_model.h5")
            shutil.copy(model_path, temp_model_path)
            
            try:
                # Open and modify the HDF5 file
                with h5py.File(temp_model_path, 'r+') as f:
                    if 'model_config' in f.attrs:
                        config_str = f.attrs['model_config']
                        if isinstance(config_str, bytes):
                            config_str = config_str.decode('utf-8')
                        
                        config = json.loads(config_str)
                        
                        # Remove quantization_config from all layers
                        if 'config' in config and 'layers' in config['config']:
                            for layer in config['config']['layers']:
                                if 'config' in layer and 'quantization_config' in layer['config']:
                                    del layer['config']['quantization_config']
                        
                        # Save modified config back
                        modified_config_str = json.dumps(config)
                        f.attrs['model_config'] = modified_config_str.encode('utf-8')
                
                # Load the modified model
                model = tf.keras.models.load_model(temp_model_path, compile=False)
                shutil.rmtree(temp_dir)
                return model
            except Exception as fix_error:
                shutil.rmtree(temp_dir, ignore_errors=True)
                raise fix_error
        else:
            raise

# Load the trained model
model_path = os.path.join(os.path.dirname(__file__), "models", "mango_leaf_disease_MobileNetV2_model.h5")
model_loaded = load_model_with_config_fix(model_path)

# Define class labels
class_labels = {
    0: "Anthracnose",
    1: "Bacterial Canker",
    2: "Cutting Weevil",
    3: "Die Back",
    4: "Gall Midge",
    5: "Healthy",
    6: "Powdery Mildew",
    7: "Sooty Mould"
}

DISEASE_DESCRIPTIONS = {
    'Anthracnose': 'A fungal disease that causes dark, sunken spots on leaves with concentric rings. Control requires fungicide application and removal of infected leaves.',
    'Bacterial Canker': 'A bacterial infection that causes lesions and cankers on stems and leaves. Good sanitation practices are essential for management.',
    'Cutting Weevil': 'An insect pest that cuts leaves and shoots, causing physical damage. Management requires integrated pest control strategies.',
    'Die Back': 'This condition causes shoots and branches to die gradually from the tip backward. Often caused by stress or fungal pathogens.',
    'Gall Midge': 'An insect pest that causes abnormal leaf growth and galls. Affects leaf development and plant vigor.',
    'Healthy': 'The leaf shows no signs of disease or pest damage. Proper management maintains this healthy condition.',
    'Powdery Mildew': 'A fungal disease that creates a white powder-like coating on leaves. Reduces photosynthesis and plant vigor.',
    'Sooty Mould': 'A fungal disease that appears as black, sooty coating on leaves. Often follows pest infestations.',
}

DISEASE_EMOJIS = {
    'Anthracnose': '🦠',
    'Bacterial Canker': '⚫',
    'Cutting Weevil': '🐛',
    'Die Back': '🤎',
    'Gall Midge': '🪰',
    'Healthy': '✅',
    'Powdery Mildew': '☁️',
    'Sooty Mould': '🖤',
}

# Page Configuration
st.set_page_config(
    page_title="Mango Leaf Disease Detector",
    page_icon="🥭",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for modern, professional styling
st.markdown("""
    <style>
    * {
        margin: 0;
        padding: 0;
    }
    
    .main {
        background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
        padding: 20px;
    }
    
    .stApp {
        background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
    }
    
    /* Header Styling */
    .header-title {
        text-align: center;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 40px 20px;
        border-radius: 15px;
        margin-bottom: 30px;
        box-shadow: 0 8px 32px rgba(0,0,0,0.1);
    }
    
    .header-title h1 {
        font-size: 3em;
        font-weight: bold;
        margin-bottom: 10px;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.2);
        color: #ffffff;
    }
    
    .header-title p {
        font-size: 1.2em;
        opacity: 1;
        margin-top: 10px;
        color: #ffffff;
    }
    
    /* Card Styling */
    .result-card {
        background: white;
        padding: 30px;
        border-radius: 15px;
        box-shadow: 0 10px 30px rgba(0,0,0,0.1);
        margin: 20px 0;
        border-top: 5px solid #667eea;
    }
    
    .result-card h3, .result-card h2, .result-card p, .result-card div {
        color: #222222 !important;
    }
    
    .disease-card {
        background: linear-gradient(135deg, #fff5e6 0%, #fff9f0 100%);
        padding: 25px;
        border-radius: 12px;
        margin: 15px 0;
        border-left: 6px solid #ff6b6b;
        box-shadow: 0 4px 15px rgba(255, 107, 107, 0.15);
    }
    
    .disease-card h3, .disease-card p {
        color: #333333 !important;
    }
    
    .healthy-card {
        background: linear-gradient(135deg, #d4edda 0%, #e8f5e9 100%);
        border-left-color: #28a745;
        box-shadow: 0 4px 15px rgba(40, 167, 69, 0.15);
    }
    
    .healthy-card h3, .healthy-card p, .healthy-card div {
        color: #1e4620 !important;
    }
    
    .disease-info-box {
        background: linear-gradient(135deg, #f8d7da 0%, #f5c2c7 100%);
        border-left-color: #dc3545;
        box-shadow: 0 4px 15px rgba(220, 53, 69, 0.15);
    }
    
    .disease-info-box h2, .disease-info-box p, .disease-info-box div {
        color: #721c24 !important;
    }
    
    /* Prediction Confidence */
    .confidence-box {
        background: white;
        padding: 20px;
        border-radius: 10px;
        margin: 15px 0;
        border: 2px solid #667eea;
    }
    
    .confidence-label {
        font-weight: bold;
        color: #222222 !important;
        margin-bottom: 8px;
    }
    
    /* Recommendations */
    .recommendations-header {
        color: #667eea;
        font-size: 1.5em;
        font-weight: bold;
        margin: 20px 0 15px 0;
        display: flex;
        align-items: center;
        gap: 10px;
    }
    
    .recommendation-item {
        background: #f8f9fa;
        padding: 15px;
        margin: 10px 0;
        border-radius: 8px;
        border-left: 4px solid #667eea;
        line-height: 1.6;
        color: #333333 !important;
    }
    
    .recommendation-item strong {
        color: #667eea !important;
    }
    
    /* Metrics */
    .metric-card {
        background: white;
        padding: 15px;
        border-radius: 10px;
        text-align: center;
        box-shadow: 0 4px 12px rgba(0,0,0,0.08);
    }
    
    .metric-value {
        color: #667eea;
        font-size: 2em;
        font-weight: bold;
    }
    
    .metric-label {
        color: #666;
        font-size: 0.9em;
        margin-top: 5px;
    }
    
    /* Progress Bar */
    .progress-container {
        margin: 12px 0;
    }
    
    .progress-label {
        display: flex;
        justify-content: space-between;
        margin-bottom: 5px;
        font-size: 0.9em;
        color: #333333 !important;
    }
    
    .progress-bar-bg {
        background: #e0e0e0;
        height: 8px;
        border-radius: 10px;
        overflow: hidden;
    }
    
    .progress-bar {
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        height: 100%;
        border-radius: 10px;
        transition: width 0.3s ease;
    }
    
    /* Sidebar */
    .sidebar-header {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 15px;
        border-radius: 10px;
        margin-bottom: 20px;
    }
    
    .sidebar-header h3 {
        color: #ffffff !important;
        margin: 0 !important;
    }
    
    .info-section {
        background: white;
        padding: 15px;
        border-radius: 10px;
        margin-bottom: 15px;
        box-shadow: 0 2px 8px rgba(0,0,0,0.08);
    }
    
    .info-section h4 {
        color: #667eea !important;
        margin-bottom: 10px !important;
    }
    
    .info-section ul li {
        color: #333333 !important;
    }
    
    .info-section p {
        color: #333333 !important;
    }
    
    /* Upload Area */
    .upload-container {
        background: white;
        padding: 30px;
        border-radius: 15px;
        border: 2px dashed #667eea;
        text-align: center;
        margin-bottom: 20px;
        box-shadow: 0 4px 15px rgba(0,0,0,0.08);
    }
    
    /* Text Styling */
    .stMarkdown h2 {
        color: #667eea !important;
        margin-top: 20px;
        margin-bottom: 15px;
    }
    
    .stMarkdown h3 {
        color: #764ba2 !important;
        margin-top: 15px;
        margin-bottom: 10px;
    }
    
    .stMarkdown p {
        color: #333333 !important;
    }
    
    /* Button Styling */
    .stButton > button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        padding: 12px 30px;
        border-radius: 8px;
        font-weight: bold;
        cursor: pointer;
        box-shadow: 0 4px 15px rgba(102, 126, 234, 0.4);
        transition: transform 0.2s;
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(102, 126, 234, 0.6);
    }
    
    </style>
""", unsafe_allow_html=True)

def classify_image(img):
    try:
        # Resize and preprocess the image
        img = img.resize((224, 224))
        img = np.array(img) / 255.0
        img = np.expand_dims(img, axis=0)

        # Make predictions
        predictions = model_loaded.predict(img)

        # Get the predicted class and corresponding label
        predicted_class_idx = np.argmax(predictions)
        predicted_class = class_labels[predicted_class_idx]

        return predicted_class, predictions[0]
    except Exception as e:
        return None, None

def main():
    # Header
    st.markdown("""
        <div class="header-title">
            <h1>🥭 Mango Leaf Disease Detector</h1>
            <p>AI-Powered Disease Classification & Analysis</p>
        </div>
    """, unsafe_allow_html=True)
    
    # Sidebar Information
    with st.sidebar:
        st.markdown('<div class="sidebar-header"><h3>📋 About This App</h3></div>', unsafe_allow_html=True)
        st.markdown("""
        This application uses a **MobileNetV2** deep learning model trained on 
        mango leaf disease images to automatically detect and classify:
        
        - 🦠 Anthracnose
        - ⚫ Bacterial Canker
        - 🐛 Cutting Weevil
        - 🤎 Die Back
        - 🪰 Gall Midge
        - ✅ Healthy Leaves
        - ☁️ Powdery Mildew
        - 🖤 Sooty Mould
        """)
        
        st.markdown('<div class="info-section"><h4>📸 How to Use:</h4></div>', unsafe_allow_html=True)
        st.markdown("""
        1. Upload a clear photo of a mango leaf
        2. Wait for the model to analyze the image
        3. View the diagnosis and confidence scores
        4. Get treatment recommendations
        """)
        
        st.markdown('<div class="info-section"><h4>⚙️ Model Information:</h4></div>', unsafe_allow_html=True)
        st.markdown("""
        - **Architecture:** MobileNetV2
        - **Classes:** 8 disease types
        - **Input Size:** 224×224 pixels
        - **Framework:** TensorFlow/Keras
        """)
    
    # Main content
    col1, col2 = st.columns([1.5, 1], gap="medium")
    
    with col1:
        st.markdown('<div class="upload-container">', unsafe_allow_html=True)
        st.markdown('<h3 style="color: #667eea; margin-top: 0;">📤 Upload Mango Leaf Image</h3>', unsafe_allow_html=True)
        uploaded_file = st.file_uploader(
            "Choose an image file",
            type=["jpg", "jpeg", "png"],
            label_visibility="collapsed"
        )
        st.markdown('</div>', unsafe_allow_html=True)
        
        if uploaded_file is not None:
            st.markdown('<div class="result-card">', unsafe_allow_html=True)
            st.markdown('<h3 style="margin-top: 0; color: #667eea;">📷 Uploaded Image</h3>', unsafe_allow_html=True)
            image = Image.open(uploaded_file)
            st.image(image, use_column_width=True, caption='Your uploaded leaf image')
            st.markdown('</div>', unsafe_allow_html=True)
    
    with col2:
        if uploaded_file is not None:
            with st.spinner('🔍 Analyzing image...'):
                predicted_class, prediction_probabilities = classify_image(image)
            
            if predicted_class is not None:
                # Determine card styling
                is_healthy = predicted_class == 'Healthy'
                card_class = 'healthy-card' if is_healthy else 'disease-info-box'
                emoji = DISEASE_EMOJIS.get(predicted_class, '🔍')
                
                st.markdown(f'<div class="{card_class}">', unsafe_allow_html=True)
                st.markdown(f'<h2 style="margin-top: 0; margin-bottom: 10px;">{emoji} {predicted_class}</h2>', unsafe_allow_html=True)
                
                # Confidence
                confidence = prediction_probabilities[np.argmax(prediction_probabilities)] * 100
                st.markdown(f'<div class="confidence-box"><div class="confidence-label">Confidence: {confidence:.1f}%</div></div>', unsafe_allow_html=True)
                
                st.markdown('</div>', unsafe_allow_html=True)
    
    # Full width results
    if uploaded_file is not None and predicted_class is not None:
        st.markdown('---')
        
        # All predictions
        st.markdown('<div class="result-card">', unsafe_allow_html=True)
        st.markdown('<h3 style="margin-top: 0; color: #667eea;">📊 Prediction Confidence Scores</h3>', unsafe_allow_html=True)
        
        # Sort predictions
        sorted_indices = np.argsort(prediction_probabilities)[::-1]
        
        for idx in sorted_indices:
            class_name = class_labels[idx]
            confidence = prediction_probabilities[idx] * 100
            emoji = DISEASE_EMOJIS.get(class_name, '🔍')
            
            # Create progress bar
            bar_width = int(confidence / 100 * 50)
            st.markdown(f"""
            <div class="progress-container">
                <div class="progress-label">
                    <span>{emoji} <strong>{class_name}</strong></span>
                    <span style="color: #667eea; font-weight: bold;">{confidence:.1f}%</span>
                </div>
                <div class="progress-bar-bg">
                    <div class="progress-bar" style="width: {confidence}%"></div>
                </div>
            </div>
            """, unsafe_allow_html=True)
        
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Recommendations
        if predicted_class != 'Healthy':
            st.markdown('<div class="result-card">', unsafe_allow_html=True)
            st.markdown(f'<div class="recommendations-header">💡 Treatment Recommendations</div>', unsafe_allow_html=True)
            
            recommendations_text = DISEASE_DESCRIPTIONS[predicted_class]
            recommendations_list = [r.strip() for r in recommendations_text.split('.') if r.strip()]
            
            for i, recommendation in enumerate(recommendations_list, 1):
                st.markdown(f'<div class="recommendation-item"><strong>Step {i}:</strong> {recommendation}</div>', unsafe_allow_html=True)
            
            st.markdown('</div>', unsafe_allow_html=True)
        else:
            st.markdown('<div class="healthy-card">', unsafe_allow_html=True)
            st.markdown("""
            <div class="recommendations-header">✅ Leaf Status: Healthy</div>
            <div class="recommendation-item">
            Your mango leaf appears to be in excellent condition! Continue with routine maintenance:
            <ul style="margin-top: 10px;">
                <li>Regular watering and proper irrigation</li>
                <li>Adequate sunlight exposure</li>
                <li>Periodic pest monitoring</li>
                <li>Balanced fertilization</li>
            </ul>
            </div>
            """, unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)
    
    elif uploaded_file is None:
        st.markdown("""
        <div style="text-align: center; padding: 40px; color: #999;">
            <h3>👈 Upload an image to get started</h3>
            <p>Select a clear photo of a mango leaf to analyze</p>
        </div>
        """, unsafe_allow_html=True)

if __name__ == '__main__':
    main()