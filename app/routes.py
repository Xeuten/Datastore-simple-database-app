from flask import Blueprint, request
from google.cloud import datastore

from app.datastore_wrapper import Datastore
from app.manager import DatastoreManager
from app.operation import Set, Unset
from app.schemas import Variable

main = Blueprint('main', __name__)


@main.route("/set", methods=["GET"])
def set():
    variable_name = request.args.get("name")
    variable_value = request.args.get("value")
    if variable_name is None or variable_value is None:
        return "Both 'name' and 'value' query parameters are required.", 400

    manager = DatastoreManager()
    operation = Set(Variable(name=variable_name, value=variable_value))
    return str(manager.execute(operation))


@main.route("/get", methods=["GET"])
def get():
    variable_name = request.args.get("name")
    if variable_name is None:
        return "The 'name' query parameter is required.", 400

    return str(Datastore("Variable").get(variable_name))


@main.route("/unset", methods=["GET"])
def unset():
    variable_name = request.args.get("name")
    if variable_name is None:
        return "The 'name' query parameter is required.", 400

    manager = DatastoreManager()
    operation = Unset(variable_name)
    return str(manager.execute(operation))


@main.route("/numequalto", methods=["GET"])
def numequalto():
    variable_value = request.args.get("value")
    if variable_value is None:
        return "The 'value' query parameter is required.", 400

    query = datastore.Client().query(kind="Variable")
    query.add_filter("value", "=", variable_value)
    return str(len(list(query.fetch())))


@main.route("/undo", methods=["GET"])
def undo():
    manager = DatastoreManager()
    variable = manager.undo()
    if not variable:
        return "NO COMMANDS"
    return str(variable)


@main.route("/redo", methods=["GET"])
def redo():
    manager = DatastoreManager()
    variable = manager.redo()
    if not variable:
        return "NO COMMANDS"
    return str(variable)


@main.route("/end", methods=["GET"])
def end():
    Datastore.clear_all()
    return "CLEANED"
