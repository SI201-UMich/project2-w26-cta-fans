# SI 201 HW4 (Library Checkout System)
# Your name: Cass Dietz and Jayden Lee
# Your student id: cassd and jdenlee
# Your email: cassd@umich.edu and jdenlee@umich.edu
# Who or what you worked with on this homework (including generative AI like ChatGPT):
# If you worked with generative AI also add a statement for how you used it.
# e.g.:
# Asked ChatGPT for hints on debugging and for suggestions on overall code structure
#
# Did your use of GenAI on this assignment align with your goals and guidelines in your Gen AI contract? If not, why?
#
# --- ARGUMENTS & EXPECTED RETURN VALUES PROVIDED --- #
# --- SEE INSTRUCTIONS FOR FULL DETAILS ON METHOD IMPLEMENTATION --- #

from fileinput import filename
from importlib.resources import path

from bs4 import BeautifulSoup
import re
import os
import csv
import unittest
import requests  # kept for extra credit parity


# IMPORTANT NOTE:
"""
If you are getting "encoding errors" while trying to open, read, or write from a file, add the following argument to any of your open() functions:
    encoding="utf-8-sig"
"""


def load_listing_results(html_path) -> list[tuple]:
    """
    Load file data from html_path and parse through it to find listing titles and listing ids.

    Args:
        html_path (str): The path to the HTML file containing the search results

    Returns:
        list[tuple]: A list of tuples containing (listing_title, listing_id)
    """
    # TODO: Implement checkout logic following the instructions
    # ==============================
    # YOUR CODE STARTS HERE
    # ==============================
    base_path = os.path.abspath(os.path.dirname(__file__))
    full_path = os.path.join(base_path, html_path)

    lst = []
    with open(full_path, "r", encoding="utf-8-sig") as f:
        file = f.read()
        soup = BeautifulSoup(file, 'html.parser')
        listings = soup.find_all('div', class_="c1l1h97y")
        for listing in listings:
            title = listing.find('div', class_="t1jojoys").text
            id = re.findall(r"\/(\d+)\?", listing.find('a').get('href'))[0]
            lst.append((title, id))
        # print(lst)
        return lst

    # ==============================
    # YOUR CODE ENDS HERE
    # ==============================


def get_listing_details(listing_id) -> dict:
    """
    Parse through listing_<id>.html to extract listing details.

    Args:
        listing_id (str): The listing id of the Airbnb listing

    Returns:
        dict: Nested dictionary in the format:
        {
            "<listing_id>": {
                "policy_number": str,
                "host_type": str,
                "host_name": str,
                "room_type": str,
                "location_rating": float
            }
        }
    """
    # TODO: Implement checkout logic following the instructions
    # ==============================
    # YOUR CODE STARTS HERE
    # ==============================
    base_path = os.path.abspath(os.path.dirname(__file__))
    new_path = os.path.join(base_path, "html_files")
    full_path = os.path.join(new_path, f"listing_{listing_id}.html")

    try:
        with open(full_path, 'r', encoding="utf-8-sig") as f:
            file = f.read()
            soup = BeautifulSoup(file, 'html.parser')

            # POLICY_NUMBER
            policy_number = "Pending"
            li = soup.find_all('li', class_='f19phm7j')
            for l in li:
                if "Policy" in l.get_text():
                    policy_number = l.find("span").text
                    if "pending" in policy_number.lower():
                        policy_number = "Pending"
                    elif "exempt" in policy_number.lower():
                        policy_number = "Exempt"
                # print(policy_number)
            
            # HOST_TYPE
            host_type = "regular"
            sp = soup.find_all('span', class_="l1dfad8f")
            for s in sp:
                if "Superhost" in s.get_text():
                    host_type = "Superhost"

            host_name = ""
            di = soup.find_all('div', class_="tehcqxo")
            for d in di:
                matches = re.findall(r"Hosted by (.+)Joined in .+", d.get_text())
                if matches:
                    host_name = matches[0]

            # ROOM TYPE
            room_type = ""
            di2 = soup.find_all('div', class_="_cv5qq4")
            for d2 in di2:
                if re.search(r"Entire.+", d2.get_text()):
                    room_type = "Entire Room"
                elif re.search(r"Shared.+", d2.get_text()):
                    room_type = "Shared Room"
                elif re.search(r"Private.+", d2.get_text()):
                    room_type = "Private Room"

            # LOCATION RATING
            location_rating = 0.0
            di3 = soup.find('div', class_="_y1ba89", string="Location")
            if di3:
                rating = di3.find_next_sibling('div', class_="_bgq2leu")
                if rating:
                    location_rating = float(rating.text.strip())
            # for d3 in di3:
            #     if re.search("Location", d3.get_text()):
            #         matches = re.findall(r"(\d\.\d) out of 5.0", d3.get_text())
            #         if matches:
            #             location_rating = float(matches[0])

        
        out = {listing_id: {"policy_number": policy_number, "host_type": host_type, "host_name": host_name, "room_type": room_type, "location_rating": location_rating}}
        # print(out)
        return out
    except Exception as e:
        print(e)
    # ==============================
    # YOUR CODE ENDS HERE
    # ==============================


def create_listing_database(html_path) -> list[tuple]:
    """
    Use prior functions to gather all necessary information and create a database of listings.

    Args:
        html_path (str): The path to the HTML file containing the search results

    Returns:
        list[tuple]: A list of tuples. Each tuple contains:
        (listing_title, listing_id, policy_number, host_type, host_name, room_type, location_rating)
    """
    # TODO: Implement checkout logic following the instructions
    # ==============================
    # YOUR CODE STARTS HERE
    # ==============================
    listings = load_listing_results(html_path)
    database = []
    for listing_title, listing_id in listings:
        details = get_listing_details(listing_id)
        info = details[listing_id]
        row = (
            listing_title,
            listing_id,
            info["policy_number"],
            info["host_type"],
            info["host_name"],
            info["room_type"],
            info["location_rating"]
        )
        database.append(row)
    return database
    # ==============================
    # YOUR CODE ENDS HERE
    # ==============================


def output_csv(data, filename) -> None:
    """
    Write data to a CSV file with the provided filename.

    Sort by Location Rating (descending).

    Args:
        data (list[tuple]): A list of tuples containing listing information
        filename (str): The name of the CSV file to be created and saved to

    Returns:
        None
    """
    # TODO: Implement checkout logic following the instructions
    # ==============================
    # YOUR CODE STARTS HERE
    # ==============================
    data.sort(key=lambda x: x[6], reverse=True)
    with open(filename, 'w', encoding="utf-8-sig", newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["title", "listing_id", "policy_number", "host_type", "host_name", "room_type", "location_rating"])
        for listing in data:
            writer.writerow(listing)
    # YOUR CODE ENDS HERE
    # ==============================


def avg_location_rating_by_room_type(data) -> dict:
    """
    Calculate the average location_rating for each room_type.

    Excludes rows where location_rating == 0.0 (meaning the rating
    could not be found in the HTML).

    Args:
        data (list[tuple]): The list returned by create_listing_database()

    Returns:
        dict: {room_type: average_location_rating}
    """
    # TODO: Implement checkout logic following the instructions
    # ==============================
    # YOUR CODE STARTS HERE
    # ==============================
    ratings = {}
    counts = {}
    for listing in data:
        room_type = listing[5]
        location_rating = listing[6]
        if location_rating != 0.0:
            if room_type in ratings:
                ratings[room_type] += location_rating
                counts[room_type] += 1
            else:
                ratings[room_type] = location_rating
                counts[room_type] = 1
    avg_ratings = {room_type: ratings[room_type] / counts[room_type] for room_type in ratings}
    return avg_ratings
    # ==============================
    # YOUR CODE ENDS HERE
    # ==============================


def validate_policy_numbers(data) -> list[str]:
    """
    Validate policy_number format for each listing in data.
    Ignore "Pending" and "Exempt" listings.

    Args:
        data (list[tuple]): A list of tuples returned by create_listing_database()

    Returns:
        list[str]: A list of listing_id values whose policy numbers do NOT match the valid format
    """
    # TODO: Implement checkout logic following the instructions
    # ==============================
    # YOUR CODE STARTS HERE
    # ==============================
    invalid_listings = []
    for _, listing_id, policy_number, _, _, _, _ in data:
        if policy_number in ["Pending", "Exempt"]:
            continue
        if not re.match(r"^STR-000\d{4}$", policy_number) and not re.match(r"^20\d{2}\-00\d{4}STR$", policy_number):
            invalid_listings.append(listing_id)
    return invalid_listings
    # ==============================
    # YOUR CODE ENDS HERE
    # ==============================


# EXTRA CREDIT
def google_scholar_searcher(query):
    """
    EXTRA CREDIT

    Args:
        query (str): The search query to be used on Google Scholar
    Returns:
        List of titles on the first page (list)
    """
    # TODO: Implement checkout logic following the instructions
    # ==============================
    # YOUR CODE STARTS HERE
    # ==============================
    url = f"https://scholar.google.com/scholar?q={query}"
    response = requests.get(url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        titles = [h3.text for h3 in soup.find_all('h3', class_='gs_rt')]
        return titles
    # ==============================
    # YOUR CODE ENDS HERE
    # ==============================


class TestCases(unittest.TestCase):
    def setUp(self):
        self.base_dir = os.path.abspath(os.path.dirname(__file__))
        self.search_results_path = os.path.join(self.base_dir, "html_files", "search_results.html")

        self.listings = load_listing_results(self.search_results_path)
        self.detailed_data = create_listing_database(self.search_results_path)

    def test_load_listing_results(self):
        # TODO: Check that the number of listings extracted is 18.
        # TODO: Check that the FIRST (title, id) tuple is  ("Loft in Mission District", "1944564").
        self.assertEqual(len(self.listings), 18)
        self.assertEqual(self.listings[0], ("Loft in Mission District", "1944564"))

    def test_get_listing_details(self):
        html_list = ["467507", "1550913", "1944564", "4614763", "6092596"]

        # TODO: Call get_listing_details() on each listing id above and save results in a list.
        id_list = []
        for id in html_list:
            id_list.append(get_listing_details(id))

        # TODO: Spot-check a few known values by opening the corresponding listing_<id>.html files.
        # 1) Check that listing 467507 has the correct policy number "STR-0005349".
        # 2) Check that listing 1944564 has the correct host type "Superhost" and room type "Entire Room".
        # 3) Check that listing 1944564 has the correct location rating 4.9.
        self.assertEqual(id_list[0]["467507"]["policy_number"], "STR-0005349")
        self.assertEqual(id_list[2]["1944564"]["host_type"], "Superhost")
        self.assertEqual(id_list[2]["1944564"]["room_type"], "Entire Room")
        self.assertAlmostEqual(id_list[2]["1944564"]["location_rating"], 4.9)

    def test_create_listing_database(self):
        # TODO: Check that each tuple in detailed_data has exactly 7 elements:
        # (listing_title, listing_id, policy_number, host_type, host_name, room_type, location_rating)
        for tup in self.detailed_data:
            self.assertEqual(len(tup), 7)

        # TODO: Spot-check the LAST tuple is ("Guest suite in Mission District", "467507", "STR-0005349", "Superhost", "Jennifer", "Entire Room", 4.8).
        self.assertEqual(self.detailed_data[-1], ("Guest suite in Mission District", "467507", "STR-0005349", "Superhost", "Jennifer", "Entire Room", 4.8))

    def test_output_csv(self):
        out_path = os.path.join(self.base_dir, "test.csv")

        # TODO: Call output_csv() to write the detailed_data to a CSV file.
        # TODO: Read the CSV back in and store rows in a list.
        # TODO: Check that the first data row matches ["Guesthouse in San Francisco", "49591060", "STR-0000253", "Superhost", "Ingrid", "Entire Room", "5.0"].
        output_csv(self.detailed_data, out_path)
        with open(out_path, 'r', encoding="utf-8-sig") as file:
            reader = csv.reader(file)
            rows = list(reader)
        self.assertEqual(rows[1], ["Guesthouse in San Francisco", "49591060", "STR-0000253", "Superhost", "Ingrid", "Entire Room", "5.0"]) 
        os.remove(out_path)

    def test_avg_location_rating_by_room_type(self):
        # TODO: Call avg_location_rating_by_room_type() and save the output.
        # TODO: Check that the average for "Private Room" is 4.9.
        avg_ratings = avg_location_rating_by_room_type(self.detailed_data)
        self.assertAlmostEqual(avg_ratings["Private Room"], 4.9)

    def test_validate_policy_numbers(self):
        # TODO: Call validate_policy_numbers() on detailed_data and save the result into a variable invalid_listings.
        # TODO: Check that the list contains exactly "16204265" for this dataset.
        invalid_listings = validate_policy_numbers(self.detailed_data)
        self.assertEqual(invalid_listings, ["16204265"])



def main():
    detailed_data = create_listing_database(os.path.join("html_files", "search_results.html"))


if __name__ == "__main__":
    main()
    unittest.main(verbosity=2)