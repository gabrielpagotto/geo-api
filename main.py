import json
from fastapi import FastAPI


def get_data(name):
    with open(f"dataset/{name}.json", "r") as f:
        data = json.load(f)
    return data


all_cities = get_data("cities")
all_countries = get_data("countries")
all_states = get_data("states")

app = FastAPI(docs_url="/swagger", swagger_ui_parameters={"syntaxHighlight.theme": "obsidian"})


@app.get("/cities")
def get_cities(country_code, state_code):
    return [
        city
        for city in all_cities
        if city["country_code"] == country_code.upper() and city["state_code"] == state_code.upper()
    ]


@app.get("/states")
def get_states(country_code):
    return [state for state in all_states if state["country_code"] == country_code.upper()]


@app.get("/cities-by-name")
def get_cities_by_name(city_name):
    cities = [city for city in all_cities if city["name"].lower().__contains__(city_name.lower())]
    for city in cities:
        for state in all_states:
            if city["state_id"] == state["id"]:
                city["state"] = state
        for country in all_countries:
            if city["country_id"] == country["id"]:
                city["country"] = country
    return cities
