FROM python:3.9-slim

# Create app directory
WORKDIR /app

# Install app dependencies
COPY requirements.txt /app/

RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Bundle app source
COPY . /app/

EXPOSE 8080
CMD [ "python3", "-m" , "flask", "run", "--host=0.0.0.0" , "--port=8080"]
