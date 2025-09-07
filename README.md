# Professional Portfolio Website

This project contains the files for a professional portfolio website with a frontend built with HTML and Tailwind CSS, and a backend powered by FastAPI.

## How to Run the Website

You need to run both the frontend and the backend separately.

### Running the Frontend

1.  **Open the HTML File:** Simply open the `index.html` file in your web browser (like Chrome, Firefox, or Edge).
2.  **Live Server (Recommended):** For a better development experience, use a live server. If you use Visual Studio Code, you can install the "Live Server" extension. Right-click on `index.html` and choose "Open with Live Server".

### Running the Backend

1.  **Prerequisites:**
    * Make sure you have Python 3.7+ installed on your system.
    * Open your terminal or command prompt.

2.  **Navigate to the `backend` directory:**
    ```bash
    cd backend
    ```

3.  **Set up a Virtual Environment (Recommended):**
    ```bash
    # Create a virtual environment
    python -m venv venv

    # Activate the virtual environment
    # On Windows:
    venv\Scripts\activate
    # On macOS/Linux:
    source venv/bin/activate
    ```

4.  **Install Dependencies:**
    * With your virtual environment activated, install the required packages:
        ```bash
        pip install -r requirements.txt
        ```

5.  **Start the Server:**
    * Run the following command in your terminal from inside the `backend` directory:
        ```bash
        uvicorn main:app --reload
        ```
    * The backend will now be running at `http://127.0.0.1:8000`.

## Using the Contact Form

Once both the frontend and backend are running, you can fill out the "Get In Touch" form on the website. The form data will be sent to your local FastAPI backend, and you will see the message printed in the terminal where the backend is running.