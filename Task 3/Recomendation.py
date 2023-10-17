# Install Surprise library if you haven't already
# pip install scikit-surprise

from surprise import Dataset, Reader, KNNBasic
from surprise.model_selection import train_test_split

# Load the MovieLens dataset (you can replace this with your own dataset)
reader = Reader(line_format='user item rating timestamp', sep='\t')
data = Dataset.load_from_file('path_to_dataset/ml-100k/u.data', reader=reader)

# Split the data into a training set and a test set
trainset, testset = train_test_split(data, test_size=0.25)

# Create a collaborative filtering model
sim_options = {
    'name': 'cosine',
    'user_based': False  # Item-based collaborative filtering
}

model = KNNBasic(sim_options=sim_options)

# Train the model on the training set
model.fit(trainset)

# Make recommendations for a user
user_id = str(1)  # Replace with the user for whom you want to make recommendations
user_items = set([item for (item, _) in trainset.ur[int(user_id)]])

# Get recommendations for the user
predictions = model.test(testset)

recommendations = []
for uid, iid, true_r, est, _ in predictions:
    if uid == user_id and iid not in user_items:
        recommendations.append((iid, est))

# Sort the recommendations by estimated rating in descending order
recommendations.sort(key=lambda x: x[1], reverse=True)

# Print the top N recommendations
top_N = 10  # Number of recommendations to display
print(f"Top {top_N} Recommendations for User {user_id}:")

for i, (item, rating) in enumerate(recommendations[:top_N]):
    print(f"{i + 1}: Item {item} (Estimated Rating: {rating:.2f})")
