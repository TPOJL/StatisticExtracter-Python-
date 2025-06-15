# Football Match Report Parser

**Language**: Python 2.7  
**Submission Format**: ZIP archive containing exactly two files: `parser.py` and `stats.py` (no directories)

## Problem Statement

You are tasked with implementing two classes to process football match reports coming from different sources.

### Files and Class Responsibilities

1. **`stats.py`** — Must contain only the following:
   - The class `TeamStats`
   - Any required imports
   - The first line must be a comment with the author's full name (e.g. `# John Doe`)
   - No other code (no testing, no `main`, no print statements outside class methods)

2. **`parser.py`** — Must contain only:
   - The class `GameParser`
   - Any required imports
   - The first line must be a comment with the author's full name
   - No other code

## Class: TeamStats (in `stats.py`)

Represents basic statistics for a single football team.

**Responsibilities**:
- Store data such as: matches played, wins, losses, draws, goals scored, goals conceded, etc.
- Provide a way to update statistics after a match
- Provide a method to print or export the statistics in a standard format

## Class: GameParser (in `parser.py`)

Parses raw text match reports and extracts data needed to update team statistics.

**Responsibilities**:
- Accept match report text (string input)
- Parse the result and extract team names, scores, outcomes, etc.
- Update the appropriate `TeamStats` instances

## Example Usage (in external script)

```python
from parser import GameParser
from stats import TeamStats

stats = {}
parser = GameParser()

with open('matches.txt') as f:
    for line in f:
        team1, team2, score1, score2 = parser.parse(line)
        
        if team1 not in stats:
            stats[team1] = TeamStats(team1)
        if team2 not in stats:
            stats[team2] = TeamStats(team2)

        stats[team1].update(score1, score2)
        stats[team2].update(score2, score1)

for team in sorted(stats.keys()):
    print stats[team]
