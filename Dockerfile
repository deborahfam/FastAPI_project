FROM python:3.10-slim-bullseye

COPY . .

RUN pip install -r ./requirements.txt

EXPOSE 10000

CMD ['uvicorn','app.main:app','--host','0.0.0.0','--port','10000']