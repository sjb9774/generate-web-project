from {$name} import app

@app.route('/', methods=['GET'])
def home():
    return 'Hello world!'
