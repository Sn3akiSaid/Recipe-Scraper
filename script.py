import requests
import time
import random
import json
import re
from requests.exceptions import HTTPError, Timeout, RequestException
from bs4 import BeautifulSoup

USER_AGENT = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
    "AppleWebKit/537.36 (KHTML, like Gecko)"
    "Chrome/155.0.0.0 Safari/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Accept-Language": "en-US,en;q=0.5",
    "Accept-Encoding": "gzip, deflate",
    "Connection": "keep-alive",
}


# from databaser import data_entry
def url_input(
    url: str, max_retries: int = 3, initial_delay: int = 1
) -> requests.Response:
    """Soupify data"""
    delay = initial_delay
    # response = requests.get(url, headers=USER_AGENT, timeout=5)
    # response.raise_for_status()
    # return response

    # Error guards, need to fix
    for attempt in range(max_retries):
        try:
            response = requests.get(url, headers=USER_AGENT, timeout=(5, 30))

            if response.status_code == 429:
                print(
                    f"Rate limited. Attempt {attempt + 1}/{max_retries}. Waiting {delay} seconds..."
                )
                # retry_after = response.headers.get("Retry-After")
                # delay = float(retry_after) if retry_after else min(2**attempt, 60)
                time.sleep(delay)
                delay *= 2
                # print(retry_after)
                # raise RuntimeError(f"Still rate limited after {max_retries} retries")
                # except Exception as exc:
                #     print(f"There was a problem: {exc}")
            else:
                response.raise_for_status()
                return response
        except HTTPError as http_err:
            print(f"HTTP Error occured: {http_err}")

        except Timeout as timeout_err:  # Some error at requests.get()
            print(f"TIMEOUT Error occured: {timeout_err}")

        except RequestException as request_err:
            print(f"REQUEST Error occured: {request_err}")

            # except Exception as err:
            #     print(f"HTTP Error occured: {err}")
            if attempt == max_retries - 1:
                raise  # Raise final error if max retries reached
    raise Exception("Max retries reached")


# Dated Parsing
def helper_method(data, title_element, ingredient_list):
    """
    Filters and formats data
    """
    data[title_element] = ()
    for ingredient in ingredient_list:
        label = ingredient_list.find("label", class_="wprm-checkbox-label").text
        data[title_element] = data[title_element] + (
            re.sub(label, "", ingredient.text),
        )
    return data


def html_parser(soup):
    """
    Parses HTML and finds ingredient group, works for specific websites only.
    """
    ingredients_lists = soup.find_all("div", class_="wprm-recipe-ingredient-group")
    list_dict = {}

    for recipes in ingredients_lists:
        ingredients = recipes.find("ul", class_="wprm-recipe-ingredients")

        try:
            sub_recipe = recipes.find("h4", class_="wprm-recipe-group-name").text

            helper_method(list_dict, sub_recipe, ingredients)

        except AttributeError:
            helper_method(list_dict, "Ingredients", ingredients)

    return list_dict


# Dated Parsing


def json_parser(validresponse: requests.Response) -> dict | list:
    """
    Updated json parser, takes in a valid JSON string and returns a Python object - dict or list
    """
    soup = BeautifulSoup(validresponse.content, "lxml")
    try:
        script = soup.find("script", type="application/ld+json")
        if script is None:
            raise ValueError("No JSON-LD found.")
        script_text = script.string
        if script_text is None:
            raise ValueError("No text content in JSON-LD")
        data = json.loads(script_text)
    except ValueError:
        print("No valid json")

    return data


def finder(data: dict | list, target: str = "recipeIngredient") -> list[str] | None:
    """
    Targets the specific ingredient convention of sites,
    checks if the data is a list or dict based on the site's specification.
    """

    if isinstance(data, dict):
        if target in data:
            return data[target]
        # Go through the dict values and call the function recursively to locate the target
        for value in data.values():
            # Checks if
            result = finder(value, target)
            if result is not None:
                return result
    elif isinstance(data, list):
        for item in data:
            # Matches @type to Recipe
            if item.get("@type") == "Recipe":
                # Takes out ingredients only
                return item[target]


def cleanup(unformatted_list: list | None) -> list[str]:
    """
    Filters out whitespaces and unnecessary words.
    """
    if unformatted_list is not None:
        # Removes trailing whitespace, newlines, etc.
        stripped_list = [j.strip() for j in unformatted_list]
        # Filters out specific instances from a list - "blank" for one of the websites
        formatted_list = list(filter(lambda a: a != "blank", stripped_list))

    return formatted_list


if __name__ == "__main__":
    try:
        URL = input("Input your recipe URL: ")
    except Exception as e:
        print(f"No valid url, error {e}")

    if URL:
        trial_db = cleanup(finder(json_parser(url_input(URL))))
    print(trial_db)
