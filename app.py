from flask import Flask, render_template_string, request, jsonify
# you can simply know what to import by using the official Flask documentation at flask.palletsprojects.com
#we want to import the search function
from sec_lookup import search

app = Flask(__name__)

HTML = """
<!DOCTYPE html>
<html lang = "en">
<head> 
    <meta charset = "UTF-8">
    <title> SEC CIK Lookup </title>
</head>
<body>
    <header>
        <h1> Welcome to Prev's SEC CIK Lookup! </h1>
        <p> Search the SEC EDGAR database by company name, ticker, or CIK...you ready? </p>
    </header>
        <main>
            <div class = "search-box">
               <input id="query" type="text" placeholder="e.g. Apple, AAPL, or 320193" />
                <select id="field">
                    <option value="name">Company Name</option>
                    <option value="ticker">Ticker</option>
                    <option value="cik">CIK</option>
                </select>
                <button on click="search()">Search</button>
            </div>
            <div id = "results" ></div>
        </main>
            <script>
            async function search(){
                const query = document.getElementById('query').value.trim();
                const field = document.getElementById('field').value;
                if (!query) return;

                const res = await fetch(`/search?q=${encodeURIComponent(query)}&field=${field}`);
                const data = await res.json();

                document.getElementById('results').innerHTML = data.results.map(r =>
                    `<p>${r.name} | ${r.ticker} | CIK: ${r.cik} | ${r.exchange}</p>`
                ).join(''); }
            </script>
</body>
</html>
"""

@app.route("/")
def index():
    return render_template_string(HTML)

@app.route("/search")
def search_route():
    query = request.args.get("q", "")
    field = request.args.get("field", "name")
    results = search(query, field)
    return jsonify({"results": results})


if __name__ == "__main__":
    app.run(debug=True)next


"""
