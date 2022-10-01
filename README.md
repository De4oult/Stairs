# Ion
Progressive Python web-framework by _de4oult_ (_Soda_ main developer)

---
## Installaion

```sh
pipenv shell
pipenv install
waitress-server main:app # Windows
```

## Development

### Initialization

```python
from ion import Ion

app = Ion()
```

### Pathways

__Pathways__ register a page along a specific route

It is enough to specify a decorator before the function:
```python
@app.pathway('/index')
def index_page(req, res):
    res.text = "Hallo, Welt!"
```

or add a __pathway__ after the function:

```python
def index_page(req, res):
    res.text = "Hallo, Welt!"

add_pathway('/index', index_page())
```

### Templates

With the help of __templates__, you can transfer variables from the backend to an HTML file.

___Python file___
```python
@app.pathway("/index")
def index_page(req, res):
    res.body = app.template(
        "index.html", # ./index/index.html 

        context = {
            "title" : "Ion", 
            "text"  : "Ion is best framework"
        }
    ).encode()
```
<br>

___HTML file___
```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>{{ title }}</title>
</head>
<body>
    {{ text }}
</body>
</html>
```

---
## ___Thank you!___ - _de4oult_