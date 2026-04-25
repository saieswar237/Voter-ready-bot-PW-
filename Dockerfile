# Use an official lightweight Python image
FROM python:3.11-slim

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file into the container
COPY requirements.txt .

# Install the Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of your app's code into the container
COPY . .

# Ensure the container has permissions to write the frontend directory
RUN chmod -R 777 /app

# Expose port 8080
EXPOSE 8080

# Command to run Streamlit in strict Headless/Production mode
# This forces Streamlit to use Google's 8080 port and bind to 0.0.0.0
CMD streamlit run app.py --server.port=${PORT} --server.address=0.0.0.0 --server.headless=true