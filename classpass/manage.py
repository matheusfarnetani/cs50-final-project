def deploy():
    """Run deployment tasks."""
    from . import create_app
    from .extensions import db
    from flask_migrate import upgrade, migrate, init, stamp
    import database.models as models

    app = create_app()
    app.app_context().push()
    db.create_all()

    # migrate database to latest revision
    init()
    stamp()
    migrate()
    upgrade()


deploy()
