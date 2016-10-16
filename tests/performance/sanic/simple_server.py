import sys
import os
import inspect

currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
sys.path.insert(0, currentdir + '/../../../')

from sanic import Sanic

app = Sanic("test")


@app.route("/")
async def test(req, res):
    return res.json({"test": True})


app.run(host="0.0.0.0", port=sys.argv[1])
