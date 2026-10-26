import pytest
from script import cleanup, finder, json_parser, url_input

TEST_URLS = {
    "1": "https://mykoreankitchen.com/korean-beef-bone-broth/",
    "2": "https://mykoreankitchen.com/korean-fried-chicken/",
    "3": "https://boldbeanco.com/blogs/beanspo-recipes/homemade-baked-beans?srsltid=AfmBOopkr11KNW1BU6rqKyp_RTdpiDcQQwREQuEX-g_a3bMmMPpiq8lB",
}


TEST_RECIPE_OUTPUTS = {
    "Korean Fried Chicken": [
        "1.4 kg whole chicken",
        "2 Tbsp rice wine",
        "2 tsp minced ginger",
        "1 tsp fine sea salt",
        "1/2 tsp ground black pepper",
        "1 cup potato starch (or corn starch)",
        "Some cooking oil (for deep frying (I used rice bran oil))",
        "3 Tbsp tomato sauce ( / ketchup)",
        "2 Tbsp gochujang ((Korean chilli paste), add 1/2 Tbsp more to make it spicier)",
        "1/4 cup honey",
        "1/4 cup brown sugar",
        "2 Tbsp soy sauce",
        "2 Tbsp minced garlic",
        "1 Tbsp sesame oil",
        "toasted sesame seeds",
        "green onion (finely chopped or thinly shredded)",
    ],
    "Homemade baked beans": [
        "3 tbsp olive oil",
        "1 onion, finely chopped",
        "2 fat garlic cloves, finely chopped",
        "1 tbsp tomato puree",
        "250ml passata",
        "2 tsp smoked paprika",
        "2 tsp tamarind paste (optional)",
        "1 tsp brown sugar",
        "1x 570g jar Organic White Beans - with their bean stock (or 2 x 400g tins of Cannellini or Haricot beans, with 150ml veg stock)",
        "1 tsp dried oregano",
        "1 tsp dried parsley",
        "½ tsp dried thyme",
        "1 tsp ground coriander",
        "½ tsp cayenne pepper",
        "1 tsp smoked paprika (additional to what’s in the base recipe)",
        "1 tsp ground cumin",
        "1 tsp chipotle paste or powder (optional)",
        "Pinch of chilli flakes",
    ],
}


def test_url_input(URL: str) -> list:
    # try:
    #     URL = input("Input your recipe URL: ")
    # except Exception as e:
    #     print(f"No valid url, error {e}")

    if URL:
        trial_db = cleanup(finder(json_parser(url_input(URL))))
    return trial_db
