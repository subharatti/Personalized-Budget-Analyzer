CATEGORY_MAP = {
    "Starbucks": "Food",
    "McDonalds": "Food",
    "Uber": "Transportation",
    "Lyft": "Transportation",
    "Netflix": "Entertainment",
    "Spotify": "Entertainment",
    "Rent": "Housing"
}

def categorize(name):
    return CATEGORY_MAP.get(name, "Other")
