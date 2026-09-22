from flask import Flask, render_template_string

app = Flask(__name__)

# HTML template as a string
html_template = """
<!DOCTYPE html>
<html lang="en">
<head>
	<meta charset="UTF-8">
	<meta name="viewport" content="width=device-width, initial-scale=1.0">
	<title>Greeting Page</title>
</head>
<body>
	<h1>Hello, {{ name }}!</h1>
	<p>Welcome to your simple Flask web app.</p>
</body>
</html>
"""

# Define a route for the homepage
@app.route('/')
def home():
	return render_template_string(html_template, name="Alice")


# Define a dynamic route that takes a name parameter
@app.route('/greet/<name>')
def greet(name):
	return render_template_string(html_template, name=name)


if __name__ == '__main__':
	app.run(debug=True)
