from flask import Flask, render_template

app = Flask(__name__)
# Load config file.
app.config.from_pyfile('config.py')


@app.route('/')
def main():
    return render_template('index.html')


if __name__ == "__main__":
    app.run(port=40001, debug=True)
