import logging
from flask import Flask, jsonify, request
import os
import uuid
from ultralytics import YOLO
from PIL import Image

app = Flask(__name__)

# Configure logging
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

# Load your YOLOv8 model directly
MODEL_PATH = '640_300_model_v2.pt'  # Update this to your model path
try:
    model = YOLO(MODEL_PATH)
    logging.info("YOLOv8 model loaded successfully")
except Exception as e:
    logging.error(f"Error loading YOLOv8 model: {e}")
    raise

# Path to store uploaded images
UPLOAD_FOLDER = "images/"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Middleware for API key verification
API_KEY = 'ccf036fe-0697-4781-9ead-c0149408b4d3'  # Replace with your actual API key

@app.before_request
def require_api_key():
    api_key = request.headers.get('x-api-key')
    if api_key != API_KEY:
        logging.warning("Unauthorized access attempt")
        return jsonify({'error': 'Unauthorized'}), 401
    logging.info("API key verified successfully")

# Endpoint for uploading a user picture
@app.route('/upload', methods=['POST'])
def upload_image():
    if 'file' not in request.files:
        logging.error("No file part in the request")
        return jsonify({'error': 'No file part'}), 400
    
    file = request.files['file']
    
    if file.filename == '':
        logging.error("No selected file")
        return jsonify({'error': 'No selected file'}), 400
    
    if file:
        try:
            # Generate a unique UUID for the image
            image_uuid = str(uuid.uuid4())
            filename = f"{image_uuid}.jpg"
            file_path = os.path.join(UPLOAD_FOLDER, filename)
            
            # Save the uploaded image
            file.save(file_path)
            logging.info(f"File {file.filename} uploaded successfully as {filename}")

            return jsonify({'message': 'File uploaded successfully', 'image_uuid': image_uuid}), 200
        except Exception as e:
            logging.error(f"Error saving file: {e}")
            return jsonify({'error': str(e)}), 500

# Endpoint for predicting the image class based on UUID
@app.route('/predict/<image_uuid>', methods=['GET'])
@app.route('/predict/<image_uuid>', methods=['GET'])
def run_prediction(image_uuid):
    image_path = os.path.join(UPLOAD_FOLDER, f"{image_uuid}.jpg")
    
    if not os.path.exists(image_path):
        logging.error(f"Image with UUID {image_uuid} not found")
        return jsonify({'error': 'Image not found'}), 404

    try:
        # Load and preprocess the image
        image = Image.open(image_path)
        
        # Run inference
        results = model(image)
        
        # Extract predictions
        predictions = []
        for result in results:
            if hasattr(result, 'boxes'):
                for box in result.boxes.data.tolist():  # Extract box data
                    predictions.append({
                        'xmin': box[0],
                        'ymin': box[1],
                        'xmax': box[2],
                        'ymax': box[3],
                        'confidence': box[4],
                        'class': int(box[5])  # Adjust based on your class mapping
                    })

        logging.info(f"Prediction successful for image {image_path}")
        return jsonify(predictions), 200
    except Exception as e:
        logging.error(f"Error processing prediction: {e}")
        return jsonify({'error': str(e)}), 500


# Run the app
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
