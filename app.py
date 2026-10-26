
from flask import Flask, render_template, request, jsonify

from core.trie import Trie
from core.autocomplete import Autocomplete
from core.dictionary_loader import load_dictionary
from core.spell_corrector import SpellCorrector

app = Flask(__name__)

# Load the dictionary once when Flask starts
print("Loading dictionary...")

dictionary = load_dictionary()

# Build the Trie for autocomplete
trie = Trie()

for word, frequency in dictionary:
    trie.insert(word, frequency)

autocomplete = Autocomplete(trie)

# Initialize the spell corrector using the same dictionary
spell_corrector = SpellCorrector(dictionary)

print(f"Loaded {len(dictionary)} words into the Trie.")
print("Autocomplete and spell correction are ready.")


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/health")
def health():
    return jsonify({
        "status": "ok"
    })


@app.route("/api/autocomplete")
def autocomplete_api():
    prefix = request.args.get("q", "").strip()

    try:
        limit = int(request.args.get("limit", 5))
    except ValueError:
        return jsonify({
            "error": "Limit must be an integer."
        }), 400

    if limit < 1 or limit > 10:
        return jsonify({
            "error": "Limit must be between 1 and 10."
        }), 400

    suggestions = autocomplete.get_suggestions(
        prefix,
        limit=limit
    )

    return jsonify({
        "query": prefix,
        "suggestions": suggestions
    })


@app.route("/api/correct")
def spell_correction_api():
    word = request.args.get("q", "").strip()

    try:
        limit = int(request.args.get("limit", 5))
    except ValueError:
        return jsonify({
            "error": "Limit must be an integer."
        }), 400

    if limit < 1 or limit > 10:
        return jsonify({
            "error": "Limit must be between 1 and 10."
        }), 400

    if not word:
        return jsonify({
            "error": "Please provide a word."
        }), 400

    suggestions = spell_corrector.correct(
        word,
        limit=limit
    )

    return jsonify({
        "query": word,
        "suggestions": suggestions
    })


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=False)
