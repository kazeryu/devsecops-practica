FROM python:3.12-alpine
WORKDIR /app
RUN adduser -D -u 10001 appuser
COPY app/requirements.txt .
RUN apk add --no-cache --virtual .build-deps gcc musl-dev libffi-dev \
 && pip install --no-cache-dir -r requirements.txt \
 && apk del .build-deps \
 && rm -rf /root/.cache/pip
COPY app/app.py .
USER appuser
EXPOSE 8080
CMD ["python", "app.py"]
