FROM python:3.9
ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1
WORKDIR /opt/backend
COPY requirements.txt ./
RUN pip install --upgrade pip && pip install -r requirements.txt
COPY . ./
RUN python manage.py migrate
EXPOSE 8000
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]