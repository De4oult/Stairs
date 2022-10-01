from ion import Ion

app = Ion()

@app.pathway("/index")
def handler(req, res):
    res.body = app.template(
        "index.html", 

        context = {
            "title" : "Ion", 
            "text"  : "Ion is best framework"
        }
    ).encode()
