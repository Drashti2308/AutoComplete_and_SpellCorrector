# Autocomplete and Spell Corrector

**DSA Project using Trie and Dynamic Programming**

## Project Overview

This project provides word autocomplete and spelling correction using data structures and algorithms implemented in Python.

The application uses Flask to expose backend API endpoints and a web interface to display suggestions.

## Technologies Used

* Python
* Flask
* Trie data structure
* Levenshtein edit distance using dynamic programming
* HTML, CSS, and JavaScript

## Main Features

### 1. Autocomplete

Autocomplete suggests words that begin with the prefix entered by the user.

Example:

* Input: `app`
* Output: Words such as `application`, `approach`, and `applied`

### 2. Spell Correction

Spell correction suggests dictionary words that are similar to a misspelled input.

Example:

* Input: `helo`
* Suggestions may include `hello`

Suggestions are ranked using the spell-correction algorithm implemented in the project.

## Backend API Endpoints

### Health Check

**Endpoint:** `/health`

Checks whether the Flask application is running.

Example response:

```json
{
  "status": "ok"
}
```

### Autocomplete

**Endpoint:** `/api/autocomplete`

**Method:** `GET`

Parameters:

* `q`: Prefix to search for
* `limit`: Number of suggestions, from 1 to 10; defaults to 5

Example request:

`/api/autocomplete?q=app&limit=5`

### Spell Correction

**Endpoint:** `/api/correct`

**Method:** `GET`

Parameters:

* `q`: Word to check
* `limit`: Number of suggestions, from 1 to 10; defaults to 5

Example request:

`/api/correct?q=helo&limit=5`

An empty word or invalid limit returns an error response.

## Run Locally

1. Open a terminal in the project directory.

2. Install the required dependencies:

   ```bash
   python -m pip install -r requirements.txt
   ```

3. Start the application:

   ```bash
   python app.py
   ```

4. Open the local address shown by Flask in your browser.

## Project Structure

```text
AutoComplete_and_SpellCorrector/
├── app.py
├── core/
│   ├── autocomplete.py
│   ├── dictionary_loader.py
│   ├── edit_distance.py
│   ├── spell_corrector.py
│   ├── trie.py
│   └── trie_node.py
├── data/
├── static/
│   ├── script.js
│   └── style.css
├── templates/
│   └── index.html
└── tests/
```

## Testing

Run the available tests from the project root using commands such as:

```bash
python -m tests.test_autocomplete
python -m tests.test_dictionary_autocomplete
python -m tests.test_spell_correction_quality
python -m tests.test_correction_ranking
```

Only run test commands for test files that exist in the project.

## Team Development

The project is developed collaboratively, with separate responsibilities for dictionary preparation, Trie implementation, autocomplete, spell correction, backend integration, and testing.
