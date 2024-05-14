from flask import Flask
from datetime import datetime
from flask import request
import github_requests

app = Flask(__name__)


@app.route("/")
@app.route("/test")
def test():
    return f"Working! {datetime.now()}"


@app.route("/get_repositories")
def get_repositories():
    from_date = request.args.get("from_date", default=None)
    to_date = request.args.get("to_date", default=None)

    from_date = datetime.strptime(from_date, "%Y%m%d") if from_date else None
    to_date = datetime.strptime(to_date, "%Y%m%d") if to_date else None

    return github_requests.get_repositories(from_date, to_date)
