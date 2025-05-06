# server/app.py
import logging
from flask import Flask, jsonify, request
from flask_migrate import Migrate
from models import db, Soldier, Machine

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

app = Flask(__name__)
import os
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{os.path.join(basedir, "app.db")}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

db.init_app(app)
migrate = Migrate(app, db)
logging.info("Flask app and database initialized.")

# Soldier endpoints
@app.route('/soldiers', methods=['GET'])
def get_soldiers():
    soldiers = Soldier.query.all()
    return jsonify({'count': len(soldiers), 'soldiers': [s.to_dict() for s in soldiers]}), 200

@app.route('/soldiers/<int:id>', methods=['GET'])
def get_soldier(id):
    soldier = Soldier.query.get(id)
    if soldier:
        return jsonify(soldier.to_dict()), 200
    return jsonify({'message': f'Soldier {id} not found.'}), 404

@app.route('/soldiers', methods=['POST'])
def add_soldier():
    data = request.get_json()
    required_fields = ['name', 'rank']
    if not data or not all(field in data for field in required_fields):
        return jsonify({'message': 'Missing required fields.'}), 400

    try:
        soldier = Soldier(
            name=data['name'],
            rank=data['rank']
        )
        db.session.add(soldier)
        db.session.commit()
        return jsonify(soldier.to_dict()), 201
    except Exception as e:
        db.session.rollback()
        logging.error(f"Error adding soldier: {str(e)}")
        return jsonify({'message': 'Invalid data.'}), 400

# Machine endpoints
@app.route('/machines', methods=['GET'])
def get_machines():
    machines = Machine.query.all()
    return jsonify({'count': len(machines), 'machines': [m.to_dict() for m in machines]}), 200

@app.route('/machines', methods=['POST'])
def add_machine():
    data = request.get_json()
    required_fields = ['type', 'serial_number', 'soldier_id']
    if not data or not all(field in data for field in required_fields):
        return jsonify({'message': 'Missing required fields.'}), 400

    try:
        machine = Machine(
            type=data['type'],
            serial_number=data['serial_number'],
            status=data.get('status', 'Operational'),
            assigned_soldier_id=data['soldier_id']
        )
        db.session.add(machine)
        db.session.commit()
        return jsonify(machine.to_dict()), 201
    except Exception as e:
        db.session.rollback()
        logging.error(f"Error adding machine: {str(e)}")
        return jsonify({'message': 'Invalid data or duplicate serial number.'}), 400

@app.route('/machines/<int:id>', methods=['GET'])
def get_machine(id):
    machine = Machine.query.get(id)
    if machine:
        return jsonify(machine.to_dict()), 200
    return jsonify({'message': f'Machine {id} not found.'}), 404

@app.route('/machines/<int:id>', methods=['PUT'])
def update_machine(id):
    data = request.get_json()
    if not data:
        return jsonify({'message': 'No data provided.'}), 400

    machine = Machine.query.get(id)
    if not machine:
        return jsonify({'message': f'Machine {id} not found.'}), 404

    try:
        for key in ['type', 'serial_number', 'status', 'soldier_id']:
            if key in data:
                setattr(machine, key, data[key])
        db.session.commit()
        return jsonify(machine.to_dict()), 200
    except Exception as e:
        db.session.rollback()
        logging.error(f"Error updating machine: {str(e)}")
        return jsonify({'message': 'Invalid data or duplicate serial number.'}), 400

@app.route('/machines/<int:id>', methods=['DELETE'])
def delete_machine(id):
    machine = Machine.query.get(id)
    if not machine:
        return jsonify({'message': f'Machine {id} not found.'}), 404
    try:
        db.session.delete(machine)
        db.session.commit()
        return jsonify({'message': f'Machine {id} deleted.'}), 204
    except Exception as e:
        db.session.rollback()
        logging.error(f"Error deleting machine: {str(e)}")
        return jsonify({'message': 'Error deleting machine.'}), 400

if __name__ == '__main__':
    app.run(port=5555, debug=True)

