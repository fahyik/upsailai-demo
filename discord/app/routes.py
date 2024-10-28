from flask import Blueprint, jsonify

# Create a Blueprint instance
main_bp = Blueprint("main", __name__)


# Define a route for this Blueprint
@main_bp.route("/ready", methods=["GET"])
def ready():
    return jsonify({"status": "ready"}), 200
