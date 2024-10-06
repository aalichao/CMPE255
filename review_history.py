import csv
import time
import json
import requests
from http import HTTPStatus

def get_steam_api_url() -> str:
    return "https://store.steampowered.com/appreviews/"

def get_steam_api_rate_limits():
    return {
        "max_num_queries": 150,
        "cooldown": (5 * 60) + 10,  # 5 minutes plus a cushion
        "cooldown_bad_gateway": 10,
    }

def get_default_request_parameters():
    return {
        "json": "1",
        "language": "all",
        "filter": "recent",
        "review_type": "all",
        "purchase_type": "all",
        "num_per_page": "100",  # Maximum number of reviews per request
    }

def write_reviews_to_csv(app_id, reviews):
    csv_filename = f"reviews_{app_id}.csv"

    with open(csv_filename, 'a', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)

        # print(reviews)

        for review in reviews:
            # print(review)
            writer.writerow([
                review['recommendationid'],
                app_id,
                review['author']['steamid'],
                review['author']['num_games_owned'],
                review['author']['num_reviews'],
                review['author']['playtime_forever'],
                review['author']['playtime_last_two_weeks'],
                review['author']['playtime_at_review'],
                review['author']['last_played'],
                review['language'],
                len(review['review']),
                review['timestamp_created'],
                review['timestamp_updated'],
                review['voted_up'],
                review['votes_up'],
                review['votes_funny'],
                review['weighted_vote_score'],
                review['comment_count'],
                review['steam_purchase'],
                review['received_for_free'],
                review['written_during_early_access'],
                review['hidden_in_steam_china'],
                review['steam_china_location'],
                review['primarily_steam_deck'],
            ])

def get_reviews_for_app_id(app_id, cursor="*"):

    rate_limits = get_steam_api_rate_limits()

    url = get_steam_api_url() + str(app_id)
    params = get_default_request_parameters()
    params["cursor"] = cursor

    response = requests.get(url, params=params)
    status_code = response.status_code

    while (status_code == HTTPStatus.BAD_GATEWAY) and (
        query_count < rate_limits["max_num_queries"]
    ):
        cooldown_duration_for_bad_gateway = rate_limits["cooldown_bad_gateway"]
        print(
            f"{status_code} Bad Gateway for appID = {app_id} and cursor = {cursor}. Cooldown: {cooldown_duration_for_bad_gateway} seconds",
        )
        time.sleep(cooldown_duration_for_bad_gateway)

        resp_data = requests.get(
            url,
            params=params,
        )
        status_code = resp_data.status_code
        query_count += 1

    # Good result
    if status_code == HTTPStatus.OK:
        result = response.json()
        # print(result)
        reviews = result.get("reviews", [])
        next_cursor = result.get("cursor", None)
        return reviews, next_cursor
    # Handle rate limiting
    elif status_code == HTTPStatus.TOO_MANY_REQUESTS:
        print("429 Too Many Requests: Sleeping for 1 hour before retrying...")
        time.sleep(3600 + 10)  # 1 hour sleep with buffer
        get_reviews_for_app_id(app_id, cursor=cursor) # Retry
    else:
        print(f"Failed to fetch reviews for app_id {app_id}, status code: {status_code}")
        return None, None

def download_reviews_for_app_id(app_id):
    print(f"Processing app_id {app_id}")
    cursor = "*"
    query_count = 0
    rate_limits = get_steam_api_rate_limits()

    csv_headers = ['recommendationid', 'gameid',
                    'steamid', 'num_games_owned', 'num_reviews', 'playtime_forever', 'playtime_last_two_weeks', 'playtime_at_review', 'last_played', # Author features
                    'language', 'review_length', 'timestamp_created', 'timestamp_updated',
                    'voted_up', 'votes_up', 'votes_funny', 'weighted_vote_score', 'comment_count', 'steam_purchase',
                    'received_for_free', 'written_during_early_access', 'hidden_in_steam_china', 'steam_china_location',
                    'primarily_steam_deck']

    # Create a new file and write the header before fetching reviews
    csv_filename = f"reviews_{app_id}.csv"
    with open(csv_filename, 'w', newline='', encoding='utf-8') as csv_file:
        header = csv.writer(csv_file)
        header.writerow(csv_headers)

    while cursor:
        reviews, cursor = get_reviews_for_app_id(app_id, cursor)
        
        if reviews:
            write_reviews_to_csv(app_id, reviews)
            query_count += 1

            # Check if we've reached the maximum allowed queries, then cooldown
            if query_count >= rate_limits["max_num_queries"]:
                print(f"Max queries reached. Cooling down for {rate_limits['cooldown']} seconds.")
                time.sleep(rate_limits["cooldown"])
                query_count = 0  # Reset query count after cooldown
        else:
            print(f"No more reviews to process for app_id {app_id}.")
            break

# Example usage:
if __name__ == "__main__":
    app_id = 774861  # Example app_id for CS:GO
    download_reviews_for_app_id(app_id)
