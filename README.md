# Autocomplete and Spell Corrector
### DSA Project | Trie Data Structure and Dynamic Programming

**Project Repository:** [AutoComplete_and_SpellCorrector](https://github.com/Drashti2308/AutoComplete_and_SpellCorrector)  
**Live Application:** [Open the deployed application](https://autocomplete-and-spellcorrector-2.onrender.com/)  
**Project Type:** Data Structures and Algorithms (DSA)  
**Programming Language:** Python | **Web Framework:** Flask

---

## 1. Team Members

| Student ID | Student Name |
|---|---|
| 202618001 | Kaushal Trada |
| 202618006 | Avdhi Shah |
| 202618015 | Rachit Zaveri |
| 202618022 | Diya Shah |
| 202618023 | Drashti Akbari |
| 202618043 | Priyanshu Madi |

---

## 2. Project Overview

Autocomplete and Spell Corrector is a web-based application that helps users type words more efficiently and identify possible spelling mistakes.

The project implements two main features:

1. **Autocomplete:** Suggests complete words when a user enters the beginning characters of a word.
2. **Spell Correction:** Finds and ranks possible correct spellings when a user enters a misspelled word.

The project demonstrates how data structures and algorithms can solve practical text-search problems. A **Trie (prefix tree)** organizes dictionary words and supports prefix searching. **Dynamic programming** calculates edit distance for spelling correction.

The application is developed using Python and Flask, with HTML, CSS, and JavaScript for the user interface.

---

## 3. Problem Statement

When users type into search boxes, text editors, or other applications, they often need help completing words or correcting typing mistakes.

A basic approach may compare the input against many dictionary words individually. This can become inefficient as the dictionary grows.

This project addresses the problem by:

- Organizing dictionary words using a Trie.
- Searching the Trie for words that match a given prefix.
- Measuring spelling differences using Levenshtein edit distance.
- Improving approximate spelling search using dynamic programming during Trie traversal and branch pruning.

The objective is to provide useful suggestions while reducing unnecessary searching and calculations.

---

## 4. Project Objectives

- Implement a Trie data structure from scratch.
- Build an autocomplete feature based on prefix searching.
- Implement spelling correction using Levenshtein edit distance.
- Rank spelling suggestions using the implemented scoring logic.
- Improve the performance of spelling correction.
- Develop a simple web interface using Flask, HTML, CSS, and JavaScript.
- Test the core functionality and deploy the application.

---

## 5. Main Features

### 5.1 Autocomplete

Autocomplete suggests words that begin with the characters entered by the user.

| Input prefix | Example suggestions |
|---|---|
| `app` | `apple`, `application`, `applied` |
| `comp` | `computer`, `complete`, `company` |
| `pyth` | `python` |

**How it works:**

1. The user enters a prefix.
2. The application searches for that prefix in the Trie.
3. Once the matching Trie node is found, the application explores the relevant subtree.
4. Matching words are collected and returned as suggestions.

### 5.2 Spell Correction

Spell correction suggests possible dictionary words for a misspelled input.

| Input | Possible correction |
|---|---|
| `helo` | `hello` |
| `aple` | `apple` |
| `bananna` | `banana` |
| `computr` | `computer` |

**How it works:**

1. The user enters a word.
2. The application checks whether the word already exists in the dictionary.
3. If it is not found, approximate search explores the Trie.
4. Dynamic programming calculates edit-distance values during Trie traversal.
5. Branches that cannot produce a word within the allowed edit distance are pruned.
6. Matching candidates are scored, ranked, and returned.

The spell corrector uses a maximum edit distance of **2** in the application configuration.

---

## 6. Algorithms and Data Structures Used

### 6.1 Trie (Prefix Tree)

A Trie is a tree-like data structure used to store words character by character. Words with common prefixes share the same initial nodes.

For example, `apple`, `apply`, and `application` share the prefix `appl`.

**Why Trie is used:**

- Efficient prefix searching.
- Shared storage of common prefixes.
- Supports autocomplete.
- Can also be reused for approximate spell searching.

### 6.2 Levenshtein Edit Distance

Levenshtein distance measures the minimum number of single-character operations needed to transform one word into another.

The three allowed operations are:

- **Insertion:** Add a character.
- **Deletion:** Remove a character.
- **Substitution:** Replace one character with another.

For example, converting `computr` into `computer` requires one insertion, so the edit distance is 1.

### 6.3 Dynamic Programming

Dynamic programming solves a problem by breaking it into smaller subproblems and reusing their results. In this project, it is used to calculate edit distance efficiently.

### 6.4 Banded Levenshtein Distance

The initial implementation calculated the complete DP matrix for each candidate word.

The optimized implementation calculates only the cells within a permitted band around the main diagonal because the application accepts candidates only up to a maximum edit distance.

Additional improvements include:

- Rejecting candidates immediately when their word-length difference exceeds the allowed edit distance.
- Using rolling DP rows instead of storing the complete matrix.
- Stopping a calculation early when the current row shows that the candidate cannot meet the allowed distance.

### 6.5 Trie-Based Approximate Search and Branch Pruning

The next optimization performs dynamic programming while traversing the Trie.

Instead of independently calculating a complete edit-distance matrix for every dictionary word:

- A DP row is updated as each Trie character is visited.
- Trie branches that cannot produce a valid candidate are stopped early.
- The existing Trie is reused for both autocomplete and spell correction.

This reduces unnecessary candidate exploration. The actual amount of pruning depends on the input word and dictionary.

### 6.6 Candidate Ranking

Candidates that satisfy the maximum edit-distance condition are ranked using the spell-correction scoring logic.

The implementation considers factors including:

- Edit distance.
- Character similarity.
- Common prefix.
- Length difference.
- Word frequency.
- Alphabetical order as a final tie-breaker.

The application returns the requested number of top suggestions.

---

## 7. Performance Optimization Journey

Performance improvement was carried out in stages.

| Stage | Original issue | Improvement |
|---|---|---|
| Original implementation | Many dictionary candidates were checked individually using full DP matrices. | Established the initial implementation and measured its performance. |
| Optimization 1 | Full DP calculations performed unnecessary work and stored many values. | Added banded edit distance, rolling rows, length filtering, and early termination. |
| Optimization 2 | Even with faster distance calculations, many dictionary candidates were still examined. | Reused the Trie for approximate search and added incremental DP with branch pruning. |
| Alternative investigated | A deletion-index approach could require substantial additional memory. | A SymSpell-style deletion-index experiment was evaluated and not selected for production. |

### Local Benchmark

For the input word `computr`, the recorded local measurements were:

| Implementation | Approximate execution time |
|---|---:|
| Original spell-correction implementation | 1.2906 seconds |
| Trie-based optimized implementation | 0.074 seconds |

This particular local comparison represents approximately **17 times faster execution** after the Trie-based optimization.

Execution times can vary depending on the machine, input word, dictionary, and runtime conditions. These are local algorithm measurements, not guaranteed response times for every request.

### Live API Verification

The deployed application was tested through its API endpoints. The recorded browser measurements were:

| API request | Recorded response time |
|---|---:|
| Spell correction for `computr` | 509 ms |
| Autocomplete for `comput` | 559 ms |

These live response times include browser, network, and server overhead. They should not be directly compared with local algorithm-only timings.

---

## 8. Time and Space Complexity

The following notation is used:

- `C` = Number of dictionary candidates considered by the original search.
- `L` = Length of the input word (assuming candidate words have comparable length).
- `k` = Maximum allowed edit distance.
- `V` = Number of Trie nodes visited during approximate search.
- `D` = Maximum Trie depth.
- `A` = Number of matching candidates.

| Approach | Approximate search time | Additional search space |
|---|---|---|
| Original dictionary scanning with full DP | `O(C × L²)` | `O(L²)` per distance calculation |
| Dictionary scanning with banded DP | `O(C × k × L)` | `O(L)` |
| Trie-based approximate search | `O(V × L)` | `O(L × D + A)` |

**Important notes:**

- These are simplified bounds for the search stage, assuming words have comparable lengths.
- Trie-based search time depends on how many nodes are visited and how effectively branches are pruned. It is not guaranteed to be faster for every possible input.
- The final similarity-scoring and sorting stages also require work. If `A` candidates are ranked, sorting takes approximately `O(A log A)`.
- The Trie itself requires storage proportional to the number of character nodes in the dictionary. It is reused by autocomplete and spell correction.
- Rolling-row and banded-DP improvements reduce temporary memory used for edit-distance calculations.

---

## 9. Project Structure

```text
AutoComplete_and_SpellCorrector/
│
├── app.py
│
├── core/
│   ├── __init__.py
│   ├── autocomplete.py
│   ├── dictionary_loader.py
│   ├── edit_distance.py
│   ├── spell_corrector.py
│   ├── trie.py
│   └── trie_node.py
│
├── data/
│   └── valid_words_sorted_by_frequency.csv
│
├── static/
│   ├── script.js
│   └── style.css
│
├── templates/
│   └── index.html
│
├── tests/
│   ├── __pycache__/
│   ├── .gitkeep
│   ├── test_autocomplete.py
│   ├── test_correction_ranking.py
│   ├── test_dictionary_autocomplete.py
│   ├── test_dictionary_spell_corrector.py
│   ├── test_dictionary_trie.py
│   ├── test_edit_distance.py
│   ├── test_spell_correction_quality.py
│   ├── test_spell_corrector.py
│   └── test_trie.py
│
├── benchmarks/
│
├── requirements.txt
├── .gitignore
└── README.md
```

### File-by-File Explanation

| File / Folder | Responsibility |
|---|---|
| `app.py` | Main Flask application. Loads the dictionary, builds the Trie, initializes autocomplete and spell correction, and defines API routes. |
| `core/trie_node.py` | Defines an individual Trie node, including its children, end-of-word marker, and frequency. |
| `core/trie.py` | Implements the Trie data structure, including word insertion and searching operations. |
| `core/dictionary_loader.py` | Loads dictionary words and their frequency information from the data file. |
| `core/autocomplete.py` | Implements prefix-based word suggestion using the Trie. |
| `core/edit_distance.py` | Implements Levenshtein edit distance using dynamic programming, including the optimized banded calculation. |
| `core/spell_corrector.py` | Implements spell correction, candidate searching, Trie-based approximate search, branch pruning, similarity scoring, and ranking. |
| `data/` | Contains the dictionary dataset used by the application. |
| `templates/index.html` | Defines the web application's HTML structure. |
| `static/style.css` | Contains the visual styling of the web interface. |
| `static/script.js` | Handles browser-side interactions and communicates with the Flask API. |
| `tests/` | Contains the project's test files for autocomplete, correction ranking, dictionary-based autocomplete and spell correction, Trie operations, edit distance, and spell-correction quality. The `__pycache__/` folder contains Python-generated cache files, while `.gitkeep` keeps the tests folder present in version control. |
| `benchmarks/` | Reserved for performance measurement and benchmark-related work. |
| `requirements.txt` | Lists the Python dependencies required to run the application. |
| `.gitignore` | Specifies files and folders that Git should ignore. |
| `README.md` | Provides project documentation, setup instructions, architecture, and usage information. |

---

## 10. Application Architecture and Workflow

```text
                  USER
                    |
                    v
             WEB INTERFACE
          (HTML, CSS, JavaScript)
                    |
                    v
              FLASK APP
                app.py
                    |
          +---------+---------+
          |                   |
          v                   v
     AUTOCOMPLETE        SPELL CORRECTION
          |                   |
          v                   v
         TRIE          TRIE-BASED DP SEARCH
          |                   |
          v                   v
    PREFIX MATCHING      BRANCH PRUNING
          |                   |
          |                   v
          |             CANDIDATE SCORING
          |                   |
          +---------+---------+
                    |
                    v
              API RESPONSE
                    |
                    v
             WEB INTERFACE
                    |
                    v
             USER SEES RESULTS
```

### Application Startup

When the Flask application starts:

1. The dictionary is loaded from the data file.
2. A Trie is created.
3. Dictionary words and their frequencies are inserted into the Trie.
4. The autocomplete component is initialized.
5. The spell corrector is initialized with the dictionary and the existing Trie.
6. The application becomes ready to receive requests.

---

## 11. API Endpoints

The Flask application provides the following endpoints.

### 11.1 Health Check

**Endpoint:** `/health`  
**Method:** `GET`

Checks whether the application is running.

```text
GET /health
```

Expected response:

```json
{
  "status": "ok"
}
```

### 11.2 Autocomplete API

**Endpoint:** `/api/autocomplete`  
**Method:** `GET`

| Parameter | Description | Default |
|---|---|---:|
| `q` | Prefix entered by the user | Required |
| `limit` | Maximum number of suggestions (1–10) | 5 |

Example:

```text
/api/autocomplete?q=comp&limit=5
```

### 11.3 Spell Correction API

**Endpoint:** `/api/correct`  
**Method:** `GET`

| Parameter | Description | Default |
|---|---|---:|
| `q` | Word to check or correct | Required |
| `limit` | Maximum number of suggestions (1–10) | 5 |

Example:

```text
/api/correct?q=computr&limit=5
```

An empty input or invalid limit returns an error response.

---

## 12. Installation and Local Setup

### Step 1: Clone the Repository

```bash
git clone https://github.com/Drashti2308/AutoComplete_and_SpellCorrector.git
```

### Step 2: Open the Project Directory

```bash
cd AutoComplete_and_SpellCorrector
```

### Step 3: Create a Virtual Environment

```bash
python -m venv venv
```

### Step 4: Activate the Virtual Environment

**Windows:**

```bash
venv\Scripts\activate
```

**Linux / macOS:**

```bash
source venv/bin/activate
```

### Step 5: Install Dependencies

```bash
python -m pip install -r requirements.txt
```

### Step 6: Run the Application

```bash
python app.py
```

### Step 7: Open the Application

Open the local address printed by Flask in your browser. With the default application configuration, this is:

```text
http://127.0.0.1:5000/
```

---

## 13. Testing

Run the tests from the project root:

```bash
python -m tests.test_autocomplete
```

```bash
python -m tests.test_dictionary_autocomplete
```

```bash
python -m tests.test_spell_correction_quality
```

```bash
python -m tests.test_correction_ranking
```

Run only commands corresponding to test files present in the repository.

The spell-correction quality tests include examples such as:

- `aple` → `apple`
- `bananna` → `banana`
- `computr` → `computer`
- `helo` → `hello`

The ranking tests check the ordering of suggestions returned by the spell corrector.

---

## 14. Deployment

The application is deployed using **Render**.

**Live Application:**  
https://autocomplete-and-spellcorrector-2.onrender.com/

Example live API requests:

```text
https://autocomplete-and-spellcorrector-2.onrender.com/health
```

```text
https://autocomplete-and-spellcorrector-2.onrender.com/api/autocomplete?q=comp&limit=5
```

```text
https://autocomplete-and-spellcorrector-2.onrender.com/api/correct?q=computr&limit=5
```

The live endpoints were tested and returned successful HTTP responses during project verification.

**Note:** On free hosting plans, an application may take additional time to respond after a period of inactivity.

---

## 15. Technologies Used

| Technology | Purpose |
|---|---|
| Python | Core programming language and algorithm implementation |
| Flask | Backend web framework and API |
| Trie | Prefix searching and shared dictionary representation |
| Dynamic Programming | Edit-distance calculation |
| Levenshtein Distance | Measuring spelling differences |
| HTML | Web page structure |
| CSS | Web page styling |
| JavaScript | User interaction and API communication |
| Git and GitHub | Version control and team collaboration |
| Render | Application deployment |

---

## 16. Challenges and Solutions

| Challenge | Solution |
|---|---|
| Searching through many dictionary words | Organized words using a Trie. |
| High cost of repeated edit-distance calculations | Implemented banded Levenshtein distance and rolling DP rows. |
| Unnecessary DP calculations | Added length filtering and early termination. |
| Too many candidate branches during spell correction | Implemented Trie-based dynamic programming and branch pruning. |
| Additional memory required by alternative indexing | Evaluated a deletion-index approach and chose to reuse the existing Trie instead. |
| Integrating algorithms with a usable application | Connected the backend algorithms to Flask APIs and a browser-based interface. |
| Verifying correctness after optimization | Ran autocomplete, spell-correction quality, and ranking tests. |

---

## 17. Learning Outcomes

Through this project, the team gained practical experience in:

- Understanding and implementing the Trie data structure.
- Applying tree traversal to prefix searching.
- Understanding dynamic programming.
- Implementing Levenshtein edit distance.
- Applying optimization techniques such as banding, rolling rows, and early termination.
- Using branch pruning to reduce unnecessary search.
- Understanding time and space complexity.
- Connecting algorithm implementations to a Flask web application.
- Testing, debugging, version control, and deployment.
- Working collaboratively on a modular software project.

---

## 18. Future Enhancements

Possible future improvements include:

- Improving suggestion ranking so the most likely correction appears first.
- Supporting sentence-level spelling correction.
- Adding context-aware suggestions.
- Supporting multiple languages.
- Adding caching for frequently requested prefixes and words.
- Evaluating performance on larger dictionaries.
- Improving automated test coverage.
- Adding more detailed performance reports.

---

## 19. Conclusion

The Autocomplete and Spell Corrector project demonstrates how fundamental data structures and algorithms can be applied to a practical text-processing problem.

The project combines Trie-based prefix searching with dynamic programming-based spelling correction. During optimization, the original full-matrix edit-distance approach was improved using banded calculation and rolling rows. The spell-correction search was then improved further by reusing the existing Trie, calculating DP values during Trie traversal, and pruning branches that could not produce valid suggestions.

The result is a working web application with autocomplete and spell-correction functionality, tested core components, and a live deployment.

---

## 20. Project Links

- **GitHub Repository:** https://github.com/Drashti2308/AutoComplete_and_SpellCorrector
- **Live Application:** https://autocomplete-and-spellcorrector-2.onrender.com/

---

*Developed as a collaborative academic project on Data Structures and Algorithms.*
