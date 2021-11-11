"""Prediction of Users based on Tweet embeddings."""

# Package imports
import numpy as np
import spacy
from sklearn.linear_model import LogisticRegression

# Local imports
from .models import User


def predict_user(user1_name, user2_name, tweet_text):
    """
    Determine and returns which user is more likely to say a given Tweet.
    :param user1_username: str -> Name of first user (User0)
    :param user2_username: str -> Name of second user (User1)
    :param tweet_text: str -> Arbitrary Tweet text to predict
    :returns int (0 | 1) -> Integer representation of User0 or User1 respectively
    """
    # SELECT name FROM User WHERE name = <user1_name> LIMIT 1;
    user1 = User.query.filter(User.username == user1_name).one()
    user2 = User.query.filter(User.username == user2_name).one()

    # Embed the tweets using Basilica's functionality
    user1_embeddings = np.array([tweet.embeddings for tweet in user1.tweets])
    user2_embeddings = np.array([tweet.embeddings for tweet in user2.tweets])

    # X = embeddings
    # y = labels
    # combine the vector/embeddings into an X matrix
    embeddings = np.vstack([user1_embeddings, user2_embeddings])
    # Generate labels and 1s and 2s for a y vector
    labels = np.concatenate([np.zeros(len(user1.tweets)),
                             np.ones(len(user2.tweets))])

    # Fit a LogisticRegression model on X and y
    log_reg = LogisticRegression().fit(embeddings, labels)

    # Embed the tweet_text using SpaCy vectorizer to use with predictive model
    nlp = spacy.load('my_model/')
    tweet_embedding = nlp(tweet_text).vector

    # Return the predicted label
    # [0.] = user1  //  [1.] = user2
    # reshaping to make a 2d array from a 1d numpy array
    return log_reg.predict(np.array(tweet_embedding).reshape(1, -1))