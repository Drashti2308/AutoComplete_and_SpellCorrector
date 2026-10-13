from flask import Flask, render_template, request, jsonify

from core.trie import Trie
from core.autocomplete import Autocomplete
from core.dictionary_loader import load_dictionary

app = Flask(__name__)

# Load the dictionary and build the Trie once when Flask starts
print("Loading dictionary...")

dictionary = load_dictionary()
trie = Trie()

for word, frequency in dictionary:
    trie.insert(word, frequency)

autocomplete = Autocomplete(trie)

print(f"Loaded {len(dictionary)} words into the Trie.")


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/health")
def health():
    return jsonify({"status": "ok"})


@app.route("/api/autocomplete")
def autocomplete_api():
    prefix = request.args.get("q", "").strip()

    try:
        limit = int(request.args.get("limit", 5))
    except ValueError:
        return jsonify({"error": "Limit must be an integer."}), 400

    if limit < 1 or limit > 10:
        return jsonify({"error": "Limit must be between 1 and 10."}), 400

    suggestions = autocomplete.get_suggestions(prefix, limit=limit)

    return jsonify({
        "query": prefix,
        "suggestions": suggestions
    })


if __name__ == "__main__":
    app.run(debug=True)