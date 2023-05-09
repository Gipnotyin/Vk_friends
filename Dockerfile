FROM python:3.9
WORKDIR ./VK_friends
COPY . .
RUN pip install -r requirements.txt
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]