import steamreviews
import csv

# AppID for the games you're interested in
app_id = 1959580 

# Specify the CSV file name
csv_file = f'steam_reviews_{app_id}.csv'

# Open the CSV file for writing
with open(csv_file, mode='w', newline='', encoding='utf-8') as file:
    # Create a CSV writer
    writer = csv.writer(file)

    # Write the header row (adjust fields as needed)
    writer.writerow(['recommendationid', 'gameid',
                     'steamid', 'num_games_owned', 'num_reviews', 'playtime_forever', 'playtime_last_two_weeks', 'playtime_at_review', 'last_played', # Author features
                     'language', 'review_length', 'timestamp_created', 'timestamp_updated',
                     'voted_up', 'votes_up', 'votes_funny', 'weighted_vote_score', 'comment_count', 'steam_purchase',
                     'received_for_free', 'written_during_early_access', 'hidden_in_steam_china', 'steam_china_location',
                     'primarily_steam_deck'])


    # BEGIN DOWNLOADING >:(
    print(f'Downloading reviews for game with AppID {app_id}...')

    # Download all reviews for the current game
    reviews_dict, query_count = steamreviews.download_reviews_for_app_id(app_id)

    # Check if there are reviews
    if query_count > 0:
        # Process each review and write to the CSV
        for review_id, review_data in reviews_dict['reviews'].items():

            # Write the review data to a row in the CSV
            writer.writerow([
                review_id,
                app_id,
                review_data['author']['steamid'],
                review_data['author']['num_games_owned'],
                review_data['author']['num_reviews'],
                review_data['author']['playtime_forever'],
                review_data['author']['playtime_last_two_weeks'],
                review_data['author']['playtime_at_review'],
                review_data['author']['last_played'],
                review_data['language'],
                len(review_data['review']),
                review_data['timestamp_created'],
                review_data['timestamp_updated'],
                review_data['voted_up'],
                review_data['votes_up'],
                review_data['votes_funny'],
                review_data['weighted_vote_score'],
                review_data['comment_count'],
                review_data['steam_purchase'],
                review_data['received_for_free'],
                review_data['written_during_early_access'],
                review_data['hidden_in_steam_china'],
                review_data['steam_china_location'],
                review_data['primarily_steam_deck'],
            ])

            # print(reviews_dict['reviews'])
        
        print(f"Saved {len(reviews_dict['reviews'])} reviews for game with AppID {app_id}.")
        # print(reviews_dict.keys())
        # print(reviews_dict['query_summary'])
    else:
        print(f"No reviews found for game with AppID {app_id}.")

print(f"All reviews saved to '{csv_file}'.")