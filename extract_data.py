import json
import statistics



from time import time

likes_per_post = []
users = {}

start = time()
# Open file in context to avoid leaving it open when debugging.
with open("posts.jsonl", 'r') as fp:
    while True:
        # Read one line at the time from the file
        line = fp.readline()
        if not line:  # EOF
            break
        blog_post = json.loads(line)

        likes_per_post.append(blog_post['like_count'])

        if users.get(blog_post['author_id']):  # If the author already exists among users, add 1 to his posts count
            users[blog_post['author_id']]['posts'] += 1
        else:  # Create a new user, which is an author since they posted at least a blog
            users[blog_post['author_id']] = {'posts': 1, 'given_likes': 0}
        if blog_post['like_count'] > 0:  # Find the likers only for posts with likes
            for user_id in blog_post['liker_ids']:
                if users.get(user_id):  # If the user already exists among users, add 1 to his likes count
                    users[user_id]['given_likes'] += 1
                else:  # Create a new user, which is a liker since they gave at least one like
                    users[user_id] = {'posts': 0, 'given_likes': 1}

print(f"data extracted from json in {time() - start} seconds")
# What are the median and the mean numbers of likes per post in this data sample?
print(f"mean likes per post: {statistics.mean(likes_per_post)}")
print(f"median likes per post: {statistics.median(likes_per_post)}")
# What is the mean number of posts per author in this data sample?
posts_per_author = []
# How many of the authors in this sample have not liked any of the posts in this sample?
authors_not_liking = 0
for user_data in users.values():
    if user_data['posts'] > 0:  # determines authors
        posts_per_author.append(user_data['posts'])
        if user_data['given_likes'] < 1:  # determines non-likers
            authors_not_liking += 1

print(f"mean posts per author: {statistics.mean(posts_per_author)}")
print(f"authors not liking: {authors_not_liking}, over {len(posts_per_author)} authors and {len(users)} users.")

print(f"script completed in {time() - start} seconds")