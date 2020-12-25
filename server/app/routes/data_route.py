from app import app


@app.route('/')
def index():
    return 'ok'


@app.route('/api/data/get', methods=['GET', 'POST'])
def get_all():
    pass
