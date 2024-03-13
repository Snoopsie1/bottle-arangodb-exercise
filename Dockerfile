FROM python:3.11.5
WORKDIR /app
COPY requirements.txt /app
RUN pip install -r requirements.txt
COPY . .
# EXPOSE 80
# CMD [ "python" "-m" "bottle" "--server" "paste" "--bind" "0.0.0.0" "--debug" "--reload" "app"]
CMD python -m bottle --server paste --bind 0.0.0.0:80 --debug --reload app