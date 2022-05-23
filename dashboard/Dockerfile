FROM python:3.9.5-slim-buster

WORKDIR /usr/app/

RUN pip install --upgrade pip

COPY requirements.txt requirements.txt

RUN pip install -r requirements.txt

COPY app ./

RUN adduser --disabled-password wordle_pulse_user
USER wordle_pulse_user

EXPOSE ${PORT}

CMD ["sh", "-c", "streamlit run --server.port $PORT /usr/app/main.py"]
