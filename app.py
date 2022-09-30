from api import API

app = API()

#app()

@app.pathway("/main/{text}")
def home(req, res, text):
    res.text = f'Home Page - {text}'