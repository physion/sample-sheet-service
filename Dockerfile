FROM python:3

RUN mkdir -p /var/secrets

# Set the WORKDIR to /app so all following commands run in /app
WORKDIR /app

# Install requirements
RUN pip install --upgrade pip
COPY requirements.txt dev-requirements.txt ./
RUN pip install -r requirements.txt -r dev-requirements.txt

# Copy app
COPY . ./

