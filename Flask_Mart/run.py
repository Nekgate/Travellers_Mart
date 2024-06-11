from flask_station import create_app, db
from flask_migrate import Migrate
from flask import request

app = create_app()
migrate = Migrate(app, db)

@app.context_processor
def inject_request_path():
    return dict(request_path=request.path)

if __name__ == '__main__':
    app.run(debug=True)
    db.create_all()
