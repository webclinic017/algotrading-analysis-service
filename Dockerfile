# 
FROM python:3.9

# 
WORKDIR /code

# 
COPY ./requirements.txt /code/requirements.txt

# 
RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

# 
COPY ./App /code/App
COPY ./main.py /code/main.py
# COPY ./credentials.json /code/credentials.json

# 
CMD ["uvicorn", "main:app","--proxy-headers", "--host", "0.0.0.0", "--port", "5000"]
