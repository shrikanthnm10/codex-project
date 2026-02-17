import os
import tempfile

from app.main import create_app
from app.models import db


def test_healthcheck():
    fd, path = tempfile.mkstemp()
    os.close(fd)
    os.environ["DATABASE_URL"] = f"sqlite:///{path}"

    app = create_app()
    app.config["TESTING"] = True

    with app.app_context():
        db.create_all()

    client = app.test_client()
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json["status"] == "ok"
