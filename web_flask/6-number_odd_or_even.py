#!/usr/bin/python3
""" Starts a Flask web application """

from flask import Flask, render_template

app = Flask(__name__)


@app.route('/', strict_slashes=False)
def hello_hbnb():
    """ Display 'Hello HBNB!' """
    return 'Hello HBNB!'


@app.route('/hbnb', strict_slashes=False)
def display_hbnb():
    """ Display 'HBNB' """
    return 'HBNB'


@app.route('/c/<text>', strict_slashes=False)
def display_c_text(text):
    """ Display 'C' followed by the value of the text variable """
    return 'C {}'.format(text.replace('_', ' '))


@app.route('/python/', defaults={'text': 'is cool'}, strict_slashes=False)
@app.route('/python/<text>', strict_slashes=False)
def display_python_text(text):
    """ Display 'Python' followed by the value of the text variable """
    return 'Python {}'.format(text.replace('_', ' '))


@app.route('/number/<int:n>', strict_slashes=False)
def is_number(n):
    """ Display 'n is a number' only if n is an integer """
    return '{} is a number'.format(n)


@app.route('/number_template/<int:n>', strict_slashes=False)
def number_template(n):
    """ Display a HTML page only if n is an integer """
    return render_template('6-number.html', number=n)


@app.route('/number_odd_or_even/<int:n>', strict_slashes=False)
def number_odd_or_even(n):
    """ Display a HTML page only if n is an integer
        Also, determine if the number is odd or even """
    if n % 2 == 0:
        even_or_odd = 'even'
    else:
        even_or_odd = 'odd'
    return render_template('6-number_odd_or_even.html', number=n, even_or_odd=even_or_odd)


if __name__ == "__main__":
    app.run(host='0.0.0.0', port='5000')
