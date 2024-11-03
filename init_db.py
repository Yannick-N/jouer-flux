from app import create_app, db
from app.models.user import Role, User
from flask_security import SQLAlchemyUserDatastore
from werkzeug.security import generate_password_hash

app = create_app()

with app.app_context():
    user_datastore = SQLAlchemyUserDatastore(db, User, Role)
    
    db.create_all()

    if not user_datastore.find_role("admin"):
        user_datastore.create_role(name="admin", description="Admin Role")
    if not user_datastore.find_role("user"):
        user_datastore.create_role(name="user", description="User Role")
    
    if not user_datastore.find_user(email="admin@example.com"):
        user_datastore.create_user(
            email="admin@example.com",
            password=generate_password_hash("password", method='pbkdf2:sha256'),
            roles=["admin"],
            fs_uniquifier="admin@example.com"
        )
    
    db.session.commit()
    print("Database initialized and default user created.")