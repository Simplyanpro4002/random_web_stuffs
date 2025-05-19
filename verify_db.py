from app import app, db
from models import User
import os

def verify_db():
    with app.app_context():
        # Check if database file exists
        db_path = 'risk_assessment.db'
        if not os.path.exists(db_path):
            print(f"Database file not found at {db_path}")
            print("Creating database...")
            db.create_all()
        else:
            print(f"Database file found at {db_path}")
        
        # Try to query the User table
        try:
            users = User.query.all()
            print(f"Found {len(users)} users in database")
            for user in users:
                print(f"User: {user.email}")
        except Exception as e:
            print(f"Error querying users: {e}")
            print("Trying to recreate tables...")
            db.create_all()
        
        # Create admin user if it doesn't exist
        admin = User.query.filter_by(email='admin@example.com').first()
        if not admin:
            print("Creating admin user...")
            admin = User(email='admin@example.com', name='Admin')
            admin.set_password('Admin123!')
            db.session.add(admin)
            db.session.commit()
            print("Admin user created successfully!")
        else:
            print("Admin user already exists")
            # Verify password hash is correct
            if admin.check_password('Admin123!'):
                print("Admin password is correct")
            else:
                print("Admin password is incorrect, updating password...")
                admin.set_password('Admin123!')
                db.session.commit()
                print("Admin password updated")

if __name__ == '__main__':
    verify_db() 