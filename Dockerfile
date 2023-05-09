FROM python:3.9
ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1
WORKDIR /opt/backend
RUN python -m venv venv
RUN source venv/bin/activate
COPY requirements.txt /opt/backend/
RUN pip install --upgrade pip && pip install -r requirements.txt
COPY . /opt/backend/
EXPOSE 8000
CMD ["python", "manage.py", "runserver"]