# YOLOv8 Image Classification API

This project is a Flask-based API for image classification using a YOLOv8 model. The API allows users to upload images and receive predictions based on the uploaded images.

## Installation

1. **Clone the Repository**:
   ```bash
   git clone <repository-url>
   cd <repository-name>
   
2. **Create a Virtual Environment**:
    ```bash
    python -m venv .venv
    
3. **Activate the Virtual Environment**:
    ```bash
    .venv\Scripts\activate

4. **Install Required Packages**:
    ```bash
    pip install -r requirements.txt

## Running the Application

5. **Start the Flask Application**:
    ```bash
    python app.py

## API Documentation

### 1. Upload an Image
- **Endpoint**: `/upload`
- **Method**: `POST`
- **Description**: Uploads an image to the server for prediction.
- **Request Headers**:
  - `x-api-key`: Your API key (string)
- **Request Body**:
  - `file`: The image file to be uploaded (multipart/form-data)
- **Response**:
  - **200 OK**: Successfully uploaded.
    ```json
    {
      "message": "File uploaded successfully",
      "image_uuid": "unique-uuid-value"
    }
    ```
  - **400 Bad Request**: If no file is provided or if the file is invalid.
    ```json
    {
      "error": "No file part"
    }
    ```

### 2. Predict Image Class
- **Endpoint**: `/predict/<image_uuid>`
- **Method**: `GET`
- **Description**: Retrieves predictions for the uploaded image using its UUID.
- **Request Headers**:
  - `x-api-key`: Your API key (string)
- **URL Parameters**:
  - `image_uuid`: The UUID of the uploaded image.
- **Response**:
  - **200 OK**: Returns predictions for the image.
    ```json
    [
      {
        "xmin": 0,
        "ymin": 0,
        "xmax": 100,
        "ymax": 100,
        "confidence": 0.99,
        "class": 1,
        "name": "class_name"
      },
      ...
    ]
    ```
  - **404 Not Found**: If the image is not found.
    ```json
    {
      "error": "Image not found"
    }
    ```
  - **401 Unauthorized**: If the API key is invalid.
    ```json
    {
      "error": "Unauthorized"
    }
    ```

### UUID Generation
For generating UUIDs, you can use the following link: [UUID Generator](https://www.uuidgenerator.net/version4).
