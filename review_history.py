import steamreviews
import csv
from datetime import datetime

# List of AppIDs for the games you're interested in
app_ids = [1959580]  # Example: Team Fortress 2, Dota 2, Counter-Strike: Global Offensive

# Specify the CSV file name
csv_file = 'steam_reviews_multiple_games.csv'

# Open the CSV file for writing
with open(csv_file, mode='w', newline='', encoding='utf-8') as file:
    # Create a CSV writer
    writer = csv.writer(file)

    # Write the header row (adjust fields as needed)
    writer.writerow(['Game AppID', 'Review ID', 'Date', 'Voted Up', 'Votes Up', 'Votes Funny', 'Weighted Vote Score', 'Comment Count', 'Steam Purchase', 'Receieved For Free', 'Written During Early Access'])

    # Loop through each game AppID
    for app_id in app_ids:
        print(f"Downloading reviews for game with AppID {app_id}...")

        # Download all reviews for the current game
        reviews_dict, query_count = steamreviews.download_reviews_for_app_id(app_id)

        # Check if there are reviews
        if query_count > 0:
            # Process each review and write to the CSV
            for review_id, review_data in reviews_dict['reviews'].items():
                # Convert the timestamp to a readable date format
                review_date = datetime.utcfromtimestamp(review_data['timestamp_created']).strftime('%Y-%m-%d %H:%M:%S')

                # Determine the sentiment (positive/negative) based on 'voted_up'
                sentiment = "Positive" if review_data['voted_up'] else "Negative"

                # Write the review data to a row in the CSV
                writer.writerow([
                    review_id,
                    app_id,  # Save the AppID of the game
                    review_date,
                    review_data['voted_up'],  # Whether the review is positive
                    review_data['votes_up'],  # Votes up count
                    review_data['votes_funny'],  # Votes funny count
                    sentiment,
                ])

                print(review_data)
            
            # print(f"Saved {len(reviews_dict['reviews'])} reviews for game with AppID {app_id}.")
            # print(reviews_dict.keys())
            # print(reviews_dict['query_summary'])
        else:
            print(f"No reviews found for game with AppID {app_id}.")

print(f"All reviews saved to '{csv_file}'.")