import logging
from random import choice
from faker import Faker
from app import app, db
from models import Soldier, Machine

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

fake = Faker()
machine_types = ['Abrams Tank', 'Bulldozer', 'Crane', 'Bradley Vehicle', 'Humvee']
ranks = ['Sergeant', 'Staff Sergeant', 'Lieutenant', 'Captain']

with app.app_context():
    try:
        logging.info("Clearing tables...")
        Machine.query.delete()
        Soldier.query.delete()
        db.session.commit()

        logging.info("Seeding 100 soldiers...")
        soldiers = [Soldier(name=fake.name(), rank=choice(ranks)) for _ in range(100)]
        db.session.add_all(soldiers)
        db.session.commit()

        logging.info("Seeding 50 machines...")
        machines = [
            Machine(
                type=choice(machine_types),
                serial_number=f'SN-{i:04d}',
                status='Operational',
                assigned_soldier_id=choice(soldiers).id
            ) for i in range(50)
        ]
        db.session.add_all(machines)
        db.session.commit()

        logging.info("Seeding completed successfully.")

    except Exception as e:
        logging.error(f"Seeding failed: {str(e)}")
        db.session.rollback()
        raise
