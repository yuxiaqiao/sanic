from sanic import Sanic
from sanic.log import log
from sanic.exceptions import ServerError

app = Sanic(__name__)


@app.route("/")
async def test_async(req, res):
    return res.json({"test": True})


@app.route("/sync", methods=['GET', 'POST'])
def test_sync(req, res):
    return res.json({"test": True})


@app.route("/dynamic/<name>/<id:int>")
def test_params(req, res, name, id):
    return res.text("yeehaww {} {}".format(name, id))


@app.route("/exception")
def exception(req, res):
    raise ServerError("It's dead jim")


# ----------------------------------------------- #
# Exceptions
# ----------------------------------------------- #

@app.exception(ServerError)
async def test(req, res, exception):
    return res.json({"exception": "{}".format(exception), "status": exception.status_code}, status=exception.status_code)


# ----------------------------------------------- #
# Read from request
# ----------------------------------------------- #

@app.route("/json")
def post_json(req, res):
    return res.json({"received": True, "message": req.json})


@app.route("/form")
def post_json(req, res):
    return res.json({"received": True, "form_data": req.form, "test": req.form.get('test')})


@app.route("/query_string")
def query_string(req, res):
    return res.json({"parsed": True, "args": req.args, "url": req.url, "query_string": req.query_string})


# ----------------------------------------------- #
# Run Server
# ----------------------------------------------- #

def after_start(loop):
    log.info("OH OH OH OH OHHHHHHHH")


def before_stop(loop):
    log.info("TRIED EVERYTHING")


app.run(host="0.0.0.0", port=8000, debug=True, after_start=after_start, before_stop=before_stop)
