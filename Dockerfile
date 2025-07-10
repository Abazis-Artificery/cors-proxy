FROM python:latest

ENV HTTP_PORT=8080

EXPOSE $HTTP_PORT

#Copy over files
COPY ./ /code/
WORKDIR "/code/"
# Get dependencies
RUN pip install -r requirements.txt
# Run server
CMD ["python", "main.py"]