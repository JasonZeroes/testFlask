from apps import create_app

config_str = "apps.settings.DevCMSConfig"
app = create_app(config_str)

if __name__ == '__main__':
    with app.app_context():
        from apps.models import db
        db.create_all()
    app.run()
