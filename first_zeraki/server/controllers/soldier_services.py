from flask import jsonify
from models.soldier import db, Soldier

def fetch_a_soldier(id):
    soldier = Soldier.query.get(id)
    if soldier:
        return soldier.to_dict(), 200
    return {
        "error": f'Soldier {id} not found'
    }, 404

def fetch_all_soldiers():
    try:
        soldiers = Soldier.query.all()
        return {
            "count" : len(soldiers),
            "soldiers" : [soldier.to_dict() for soldier in soldiers]
        }, 200
    except Exception as e:
        return {
            "error" : "Error fetching soldiers"
        }, 500
    