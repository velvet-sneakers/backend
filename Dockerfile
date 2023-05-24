FROM python:3.9
ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1
WORKDIR /opt/backend
RUN python -m venv venv
RUN . venv/bin/activate
COPY requirements.txt /opt/backend/
RUN . venv/bin/activate && pip install --upgrade pip && pip install -r requirements.txt
COPY . /opt/backend/
EXPOSE 8000
CMD ["venv/bin/python", "manage.py", "runserver"]