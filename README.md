# PyFrameKit

![Image](https://github.com/user-attachments/assets/4f346d16-b4a2-468b-83c4-2a7326c0b91e)

![purpose](https://img.shields.io/badge/purpose-learning-green)
![PyPI - Version](https://img.shields.io/pypi/v/pyframekit)

PyFrameKit is a lightweight Python web framework built for learning. It's WSGI-compliant and can be used with servers like Gunicorn.

## Installation

To install PyFrameKit, use pip:

```
pip install pyframekit
```

## Hot to Use

### Quick Start Example

Here's how you can createa a basic PyFrameKit application:

```
from pyframekit.app import PyFrameKitApp

app = PyFrameKitApp()

@app.route("/home")
def home(request, response):
    response.text = "Hello! This is the Home Page"

@app.route("/hello/{name}")
def greeting(request, response, name):
    response.text = f"Hello {name}"

@app.route("/books")
class Books:
    def get(self, request, response):
        response.text = "Book Page"

    def post(self, request, response):
        response.text = "Endpoint to create a book"
```

### Advanced Features

#### Template Rendering
PyFrameKit supports template rendering for dynamic HTML content:
```
@app.route("/template")
def template_handler(req, resp):
    resp.html = app.template(
        "home.html",
        context={"new_title": "New Title", "new_body": "New Body"}
    )
```


#### JSON Response
Easily handle JSON data:
```
@app.route("/json")
def json_handler(req, resp):
    response_data = {"name": "some name", "type": "json"}
    resp.body = json.dumps(response_data).encode()
    resp.content_type = "application/json"

```


### Unit Tests

The recommended way of writing unit tests is with [pytest](https://docs.pytest.org/en/latest/). There are two built in fixtures that you may want to use when writing unit tests with PyFrameKit.
```
def test_duplicate_routes_throws_exception(app):
    @app.route("/home")
    def home(req, resp):
        resp.text = "Hello from Home"

    with pytest.raises(AssertionError):
        @app.route("/home")
        def home2(req, resp):
            resp.text = "Hello from Home2"
```

The other one is client that you can use to send HTTP requests to your handlers. It is based on the famous [request](https://requests.readthedocs.io/en/latest/) and it should feel very familiar:
```
def test_parameterized_routing(app, test_client):
    @app.route("/hello/{name}")
    def greeting(request, response, name):
        response.text = f"Hello {name}"
```

## Templates
The default folder for templates is templates. You can customize this location:
```
app = PyFrameKitApp(templates_dir="path/to/your/templates")
```
Then you can use HTML files in that folder like so in a handler:
```
@app.route("/template")
def template_handler(req, resp):
    resp.html = app.template(
        "home.html",
        context={"new_title": "New Title", "new_body": "New Body"}
    )
```

## Static Files
Static files are served from the static directory by default. This location is also configurable:
```
app = PyFrameKitApp(static_dir="path/to/your/static")
```
Then you can use the files inside this folder in HTML files:
```
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>{{title}}</title>
    <link rel="stylesheet" href="/static/home.css">
</head>
<body>
    <h1>{{body}}</h1>
    <p>This is a paragraph</p>
</body>
</html>
```

## Middleware
Add custom middleware to process requests and responses. Middleware classes inherit from `pyframekit.middleware.Middleware` and override the `process_request` and `process_response` methods:
```
from pyframekit.app import PyFrameKitApp
from pyframekit.middleware import Middleware

app = PyFrameKitApp()

class Middleware:
    def process_request(self, req):
        print("Before dispatch", req.url)

    def process_response(self, req, resp):
        print("After dispatch", req.url)

app.add_middleware(Middleware)

```