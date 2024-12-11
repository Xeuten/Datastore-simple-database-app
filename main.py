from flask import Flask, request
from google.cloud import datastore

from utils.datastore_wrapper import Datastore
from utils.manager import DatastoreManager
from utils.operation import Set, Unset
from utils.schemas import Variable

app = Flask(__name__)

datastore_client = datastore.Client()


@app.route("/set", methods=["GET"])
def set():
    variable_name = request.args.get("name")
    variable_value = request.args.get("value")
    if variable_name is None or variable_value is None:
        return "Both 'name' and 'value' query parameters are required.", 400

    manager = DatastoreManager()
    operation = Set(Variable(name=variable_name, value=variable_value))
    return str(manager.execute(operation))


@app.route("/get", methods=["GET"])
def get():
    variable_name = request.args.get("name")
    if variable_name is None:
        return "The 'name' query parameter is required.", 400

    return str(Datastore("Variable").get(variable_name))


@app.route("/unset", methods=["GET"])
def unset():
    variable_name = request.args.get("name")
    if variable_name is None:
        return "The 'name' query parameter is required.", 400

    manager = DatastoreManager()
    operation = Unset(variable_name)
    return str(manager.execute(operation))


@app.route("/numequalto", methods=["GET"])
def numequalto():
    variable_value = request.args.get("value")
    if variable_value is None:
        return "The 'value' query parameter is required.", 400

    query = datastore_client.query(kind="Variable")
    query.add_filter("value", "=", variable_value)
    return str(len(list(query.fetch())))


@app.route("/undo", methods=["GET"])
def undo():
    manager = DatastoreManager()
    variable = manager.undo()
    if not variable:
        return "NO COMMANDS"
    return str(variable)


@app.route("/redo", methods=["GET"])
def redo():
    manager = DatastoreManager()
    variable = manager.redo()
    if not variable:
        return "NO COMMANDS"
    return str(variable)


@app.route("/end", methods=["GET"])
def end():
    Datastore.clear_all()
    return "CLEANED"


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=8080, debug=True)
