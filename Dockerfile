FROM python:3.9

LABEL maintainer="Sezer Bozkir <admin@sezerbozkir.com>"

WORKDIR /code

COPY . /code

COPY ./requirements.txt /code/requirements.txt

RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

CMD ["uvicorn", "api:app", "--host", "0.0.0.0", "--port", "80"]