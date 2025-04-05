import tkinter as tk
import re

def score_candidate(item, tokens):
    """
    Scores a candidate string based on:
      1. Whether it matches the last token (flag: 1 if yes, 0 if no)
      2. Number of tokens matched.
      3. Total score (token length + bonus for whole-word or substring-at-word-start).
      4. Earliest match position (lower index is better).
    
    Returns a tuple: (matches_last, matched_count, total_score, -earliest)
    """
    lower_item = item.lower()
    matched_count = 0
    total_score = 0
    earliest = float('inf')
    matches_last = False
    last_token = tokens[-1].lower()

    for token in tokens:
        token_lower = token.lower()
        # Check for whole-word match.
        whole_pattern = r'\b' + re.escape(token_lower) + r'\b'
        whole_match = re.search(whole_pattern, lower_item)
        if whole_match:
            matched_count += 1
            score = len(token_lower) + 15  # bonus for whole-word match
            pos = whole_match.start()
            if token_lower == last_token:
                matches_last = True
            total_score += score
            earliest = min(earliest, pos)
        else:
            # Fallback: substring match.
            substring_match = re.search(re.escape(token_lower), lower_item)
            if substring_match:
                matched_count += 1
                score = len(token_lower)
                pos = substring_match.start()
                # Bonus if substring match is at the beginning of a word.
                if pos == 0 or (pos > 0 and lower_item[pos - 1] == ' '):
                    score += 10
                if token_lower == last_token:
                    matches_last = True
                total_score += score
                earliest = min(earliest, pos)
    # If no match at all, set earliest to a high value.
    if earliest == float('inf'):
        earliest = 1e9
    # Convert matches_last to an integer flag.
    return (int(matches_last), matched_count, total_score, -earliest)

def highlight_text(item, tokens):
    """
    Highlights all occurrences (case-insensitive) of any token from tokens
    by enclosing them in square brackets.
    """
    intervals = []
    for token in tokens:
        for match in re.finditer(re.escape(token), item, re.IGNORECASE):
            intervals.append((match.start(), match.end()))
    intervals.sort(key=lambda x: x[0])
    # Merge overlapping intervals.
    merged = []
    for start, end in intervals:
        if not merged or start > merged[-1][1]:
            merged.append([start, end])
        else:
            merged[-1][1] = max(merged[-1][1], end)
    highlighted = ""
    last_index = 0
    for start, end in merged:
        highlighted += item[last_index:start]
        highlighted += "[" + item[start:end] + "]"
        last_index = end
    highlighted += item[last_index:]
    return highlighted

def update_search(event=None):
    query = search_entry.get().strip().lower()
    if query == "":
        result_box.delete(1.0, tk.END)
        return

    # Split the query into tokens (preserving order).
    tokens = query.split()
    
    scored_results = []
    for item in data:
        score = score_candidate(item, tokens)
        scored_results.append((score, item))
    
    # Sort candidates by the score tuple in descending order.
    scored_results.sort(reverse=True, key=lambda x: x[0])
    
    result_box.delete(1.0, tk.END)
    for score, item in scored_results:
        highlighted_item = highlight_text(item, tokens)
        result_box.insert(tk.END, highlighted_item + "\n")

# Example data.
data = [
    "desktop computer",
    "laptop",
    "computing device",
    "electric car",
    "comp",
    "computing resources",
    "computer"
]

root = tk.Tk()
root.title("Search Highlight Example")

search_entry = tk.Entry(root, width=50)
search_entry.pack(pady=10)

result_box = tk.Text(root, width=50, height=10, wrap=tk.WORD)
result_box.pack(pady=10)

search_entry.bind("<KeyRelease>", update_search)
root.mainloop()
