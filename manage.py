def deploy():
    from flask_migrate import init, migrate, stamp, upgrade

    from app import create_app, db
    from models import Posts, Role, User

    app = create_app()
    app.app_context().push()
    db.create_all()

    init()
    stamp()
    migrate()
    upgrade()


deploy()
