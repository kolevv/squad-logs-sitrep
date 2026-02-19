# Squad HAB & Radio Damage Analytics

This project processes event data produced by **SquadJS** and visualizes which players deal the most damage to **HABs** and **FOB radios** in _Squad_.

The analysis:

- Treats **SteamID as the unique player identity**
- Uses the most recently seen player name for display
- Separates HAB damage, radio damage, and combined totals
- Allows filtering by player and damage type
- Presents results as tables and interactive charts

The UI is built with **Streamlit** and intended to be simple, readable, and easy to extend.

## Data

Users are expected to provide their own SquadJS-exported JSON file

The expected format of the log is an array of objects with the following shape:

```json
 {
    "messageId": "1234567890123456789",
    "timestamp": "2025-02-13T20:08:07.267Z",
    "playerName": "Bishop",
    "steamID": "01234567890123456",
    "eosID": "0001a2b345c678d90e1fg23456789012",
    "deployable": "US_Hab_Forest",
    "weapon": "BP_PLA_Deployable_TNT_Explosive_Timed"
  },
```

## Requirements

- Python 3.10+
- pip

Python dependencies are listed in `requirements.txt`.

## Setup & Run

Create a virtual environment (recommended):

```bash
python -m venv .venv
source .venv/bin/activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Run the app:

```bash
streamlit run app.py
```

Then open the URL Streamlit prints (usually [http://localhost:8501](http://localhost:8501)).

## Notes

- All grouping and statistics are done by **SteamID**
- Player names are for display only and may change over time
