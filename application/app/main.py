from fastapi import FastAPI
import logging
import json
import sys
import time
import uuid


class JSONFormatter(logging.Formatter):
    def format(self, record):
        log_entry = {
            "timestamp": time.strftime(
                "%Y-%m-%dT%H:%M:%SZ",
                time.gmtime(record.created)
            ),
            "level": record.levelname,
            "service": "k8s-observability-demo",
            "message": record.getMessage(),
        }

        return json.dumps(log_entry)


handler = logging.StreamHandler(sys.stdout)
handler.setFormatter(JSONFormatter())

logger = logging.getLogger("app")
logger.setLevel(logging.INFO)
logger.handlers.clear()
logger.addHandler(handler)
logger.propagate = False


app = FastAPI(
    title="Kubernetes Observability Demo",
    version="1.0.0"
)


@app.get("/")
def root():
    request_id = str(uuid.uuid4())

    logger.info(
        f"Root endpoint called request_id={request_id}"
    )

    return {
        "message": "Hello from Kubernetes!",
        "application": "k8s-observability-demo",
        "request_id": request_id
    }


@app.get("/health")
def health():
    return {
        "status": "healthy"
    }


@app.get("/api")
def api():
    request_id = str(uuid.uuid4())

    logger.info(
        f"API endpoint called request_id={request_id}"
    )

    return {
        "status": "success",
        "request_id": request_id,
        "timestamp": time.time()
    }


@app.get("/error")
def error():
    request_id = str(uuid.uuid4())

    logger.error(
        f"Test error generated request_id={request_id}"
    )

    return {
        "status": "error",
        "request_id": request_id
    }
