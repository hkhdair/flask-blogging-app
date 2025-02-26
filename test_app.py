from flask import Flask, render_template, url_for, redirect

app = Flask(__name__)

@app.route('/')
def index():
    return f"Index page. Try <a href='{url_for('search')}'>search</a> or <a href='{url_for('search_results')}?query=test'>search results</a>"

@app.route('/search')
def search():
    return "Search page"

@app.route('/search_results')
def search_results():
    return "Search results page"

if __name__ == "__main__":
    app.run(debug=True)
