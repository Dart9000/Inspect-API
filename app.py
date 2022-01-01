from flask import Flask, request
import api

app = Flask(__name__)

# To run python file without re-running the flask command
def before_request():
    app.jinja_env.cache = {}
app.before_request(before_request)


# analysis-routes
@app.route('/analysis')
def home():
    url=request.args.get('url')
    return api.Analysis(url)

# compare-routes
@app.route('/compare')
def compare():
    url1=request.args.get('url1')
    url2=request.args.get('url2')
    return api.Compare(url1,url2)

# compare-routes
@app.route('/rate')
def rate():
    return api.Rate()


# init
if __name__ == '__main__':
    app.run(debug=True)

