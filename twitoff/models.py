from flask_sqlalchemy import SQLAlchemy

# Create a DB Object
DB = SQLAlchemy()

# Make a User table by creating a User class


class User(DB.Model):
    '''Creates a User Table with SQLAlchemy'''
    # id column
    id = DB.Column(DB.BigInteger, primary_key=True,nullable=False)
    # username column
    username = DB.Column(DB.String(15),unique= True, nullable=False)
    # keeps track of id for the newest tweet said by user
    newest_tweet_id = DB.Column(DB.BigInteger)

    def __repr__(self):
        return f'[User: {self.username}]'


# Make a Tweet table by creating a Tweet class
class Tweet(DB.Model):
    '''Creates a Tweet Table with SQLAlchemy'''
    # id column
    id = DB.Column(DB.BigInteger, primary_key=True,nullable=False)
    # text column
    # Unicode allows for both text and links and emojis, etc.
    text = DB.Column(DB.Unicode(300),nullable=False)

    # Create a relationship between a tweet and a user
    user_id = DB.Column(DB.BigInteger, DB.ForeignKey(
    'user.id'), nullable=False)
    embeddings = DB.Column(DB.PickleType, nullable=False)

    # Finalizing the relationship making sure it goes both ways.
    user = DB.relationship('User', backref=DB.backref('tweets', lazy=True))

    def __repr__(self):
        return f'[Tweet: {self.text}]'