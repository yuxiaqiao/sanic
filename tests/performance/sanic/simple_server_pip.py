import sys
from sanic import Sanic
from sanic.response import json

app = Sanic("test")

@app.route("/")
async def test(req):
    return json({"test": True})

app.run(host="0.0.0.0", port=sys.argv[1])
