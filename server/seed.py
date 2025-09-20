from app import app, db, User

with app.app_context():
    db.drop_all()
    db.create_all()

    users = [
        User(username="alex"),
        User(username="stacey"),
        User(username="guest")
    ]

    db.session.add_all(users)
    db.session.commit()

    print("✅ Database seeded with users!")
