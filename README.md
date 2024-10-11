# Dogy Web Backend

This is the backend service for the Dogy application, which provides AI-powered product suggestions and location information for dog owners.

## Project Structure

- `main.py`: The main FastAPI application entry point.
- `o1_preview.py`: Contains the logic for interacting with the O1 Preview AI model.
- `gpt4o.py`: Contains the logic for interacting with the GPT-4O AI model (currently using O1 as a placeholder).
- `config.py`: Configuration settings for the application.
- `product_data.json`: JSON file containing product information.
- `requirements.txt`: List of Python dependencies.
- `.gitignore`: Specifies intentionally untracked files to ignore.
- `.env`: (Not in repository) Contains environment variables, e.g. OPENAI_API_KEY
- `test_api.py`: Contains tests for the API endpoints.

## Setup

1. **Clone the repository:**
   ```bash
   git clone https://github.com/MFaiqKhan/dogy.webbackend.git
   cd dogy.webbackend
   ```

2. **Create a virtual environment:**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Create a `.env` file in the root directory with the following content:**
   ```env
   OPENAI_API_KEY=your_openai_api_key_here
   PORT=8000  # Optional: specify a custom port
   ```

## Configuration

The `config.py` file uses `pydantic_settings` to manage configuration. It includes:

- `ALLOWED_ORIGINS`: List of allowed origins for CORS.
- `openai_api_key`: OpenAI API key (loaded from `.env` file).

## Main Application (`main.py`)

The main FastAPI application includes:

- **CORS Middleware Setup:**
  Configures Cross-Origin Resource Sharing to allow requests from specified origins.

- **Rate Limiting:**
  Utilizes `slowapi` to limit requests to 20 per minute per IP address.

- **API Endpoints:**
  - `POST /process-chat`: Processes chat messages and returns product suggestions and locations.
  - `GET /health`: Health check endpoint to verify if the service is running.

## O1 Preview Integration (`o1_preview.py`)

This module handles interaction with the O1 Preview AI model:

- **Functionality:**
  - Extracts product suggestions and locations from user messages.
  - Matches extracted keywords with product data from `product_data.json`.
  - Returns structured product suggestions and location information.

- **Error Handling:**
  Logs errors and ensures the application remains stable in case of failures.

## GPT-4O Integration (`gpt4o.py`)

This module is set up for future integration with the GPT-4O model:

- **Current State:**
  - Uses the O1 model as a placeholder.
  - Provides similar functionality to the O1 Preview integration.

- **Future Enhancements:**
  - Replace the placeholder model with GPT-4O once available.
  - Optimize response handling based on GPT-4O capabilities.

## Product Data (`product_data.json`)

Product information is stored in `product_data.json`. The structure includes:

- `name`: Product name.
- `categories`: List of categories the product belongs to.
- `price`: Price of the product.
- `description`: Detailed description of the product.
- `productUrl`: URL to the product page.
- `graphicUrl`: URL to the product image.

## Running the Application

To run the application:

```bash
python main.py
```

The server will start on `http://0.0.0.0:8000` by default. You can specify a different port by setting the `PORT` variable in the `.env` file.

## API Endpoints

- **POST `/process-chat`:**
  - **Description:** Processes a chat message and returns product suggestions and locations.
  - **Request Body:**
    ```json
    {
      "message": "I'm looking for a good dog bed and some durable toys for my energetic Labrador."
    }
    ```
  - **Response:**
    ```json
    {
      "chat_response": "Sure! Here are some product suggestions and nearby stores:",
      "products": [
        {
          "name": "Orthopedic Dog Bed",
          "category": "Beds",
          "price": "$59.99",
          "description": "A comfortable orthopedic bed for your dog.",
          "productUrl": "http://example.com/product/bed",
          "graphicUrl": "http://example.com/images/bed.jpg"
        }
        // More products...
      ],
      "locations": [
        {
          "name": "PetStore A",
          "address": "123 Bark Street"
        }
        // More locations...
      ]
    }
    ```

- **GET `/health`:**
  - **Description:** Health check endpoint.
  - **Response:**
    ```json
    {
      "status": "healthy"
    }
    ```

## Error Handling and Logging

The application uses Python's `logging` module for error tracking and information logging. Errors are logged and returned as HTTP exceptions when appropriate.

## Rate Limiting

The application uses `slowapi` for rate limiting, currently set to 20 requests per minute per IP address. Exceeding this limit will result in a `429 Too Many Requests` error.

## Testing (`test_api.py`)

To run tests:

1. **Ensure the virtual environment is activated and dependencies are installed.**

2. **Run the tests using pytest:**
   ```bash
   pytest test_api.py
   ```

   This will execute the test cases defined in `test_api.py` to verify the functionality of the API endpoints.

## Contributing

1. **Fork the repository.**

2. **Create your feature branch:**
   ```bash
   git checkout -b feature/AmazingFeature
   ```

3. **Commit your changes:**
   ```bash
   git commit -m 'Add some AmazingFeature'
   ```

4. **Push to the branch:**
   ```bash
   git push origin feature/AmazingFeature
   ```

5. **Open a Pull Request.**
