import openreview
from tqdm import tqdm

# Step 1: Connect to OpenReview API (API v2)
client = openreview.api.OpenReviewClient(
    baseurl='https://api2.openreview.net',
    username='chen.12915@osu.edu',
    password='Alex08180818'
)

# Step 2: Fetch all ICLR 2025 submissions
print("🔍 Fetching all ICLR 2025 submissions...")
submissions = client.get_all_notes(invitation='ICLR.cc/2025/Conference/-/Submission')

# Step 3: Count accepted papers by venue label
accepted_labels = ['ICLR 2025 Oral', 'ICLR 2025 Spotlight', 'ICLR 2025 Poster']
category_counts = {label: 0 for label in accepted_labels}

for submission in tqdm(submissions, desc="Processing submissions"):
    venue_label = submission.content.get('venue', '')
    if isinstance(venue_label, dict):  
        venue_label = venue_label.get('value', '')
    if venue_label in category_counts:
        category_counts[venue_label] += 1

# Step 4: Print results
print("\n📊 ICLR 2025 Accepted Paper Distribution:")
for category, count in category_counts.items():
    print(f"- {category}: {count}")

