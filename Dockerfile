# ---- Builder Stage ----
FROM python:3.9-alpine as builder
WORKDIR /usr/src/app

# Install GCC and other dependencies for building
RUN apk add --no-cache gcc musl-dev

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the source code (you might need to adjust paths depending on your structure)
COPY . .

# Run any build scripts you have here

# ---- Production Stage ----
FROM python:3.9-alpine as production

WORKDIR /usr/src/app

# Copy the built dependencies
COPY --from=builder /usr/local/lib/python3.9/site-packages /usr/local/lib/python3.9/site-packages
COPY --from=builder /usr/src/app .

# Expose the port your app runs on
EXPOSE 8000

# Run your application
CMD ["python", "./main.py"]
