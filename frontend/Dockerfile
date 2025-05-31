
FROM python:3.12-bookworm


WORKDIR /frontend

RUN pip install --upgrade pip && \
    pip install streamlit


COPY ./frontend /frontend/


EXPOSE 8501


CMD ["streamlit", "run", "app.py"]
