
# from decouple import config

from flask import Flask, render_template, request

from .models import DB, User,Tweet
from .predict import predict_user
from .twitter import get_user_and_tweets


def create_app():
    app = Flask(__name__)

    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite3'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    DB.init_app(app)

    @app.route('/')
    def base():
        if not User.query.all():
            return render_template('base.html', users=[])
        return render_template('base.html', users=User.query.all())
    @app.route('/')
    def root():
        # query the DB for all users
        users = User.query.all()
        tweets = Tweet.query.all()
        # what I want to happen when somebody goes to home page
        return render_template('base.html', title="Home", users=User.query.all(), tweets=tweets)

    @app.route('/add_user', methods=['POST'])
    def add_user():
        user = request.form.get('user_name')

        try:
            response = get_user_and_tweets(user)
            if not response:
                return 'Nothing was added.' \
                       '<br><br><a href="/" class="button warning">Go Back!</a>'
            else:
                return f'User: {user} successfully added!' \
                       '<br><br><a href="/" class="button warning">Go Back!</a>'
        except Exception as e:
            return str(e)

    @app.route('/user/<name>', methods=['GET'])
    def user(username=None, message=''):
        try:
            tweets = User.query.filter(User.username == username).one().tweets
            # return str(tweets)
        except Exception as e:
            message = f'Error adding @{username}: {e}'
            tweets = []
        return render_template('user.html', title=username, tweets=tweets, message=message)

    @app.route('/compare', methods=['POST'])
    def predict():
        user0 = request.form.get('user0')
        user1 = request.form.get('user1')
        tweet_text = request.form.get('tweet_text')

        prediction = predict_user(user0, user1, tweet_text)
        message = '"{}" is more likely to be said by @{} than @{}'.format(
            tweet_text, user0 if prediction else user1,
            user1 if prediction else user0
        )

        return message + '<br><br><a href="/" class="button warning">Go Back!</a>'

    @app.route('/refresh')
    def refresh():
        DB.drop_all()
        DB.create_all()
        return 'Database Refreshed!'

    @app.route('/reset')
    def reset():
        # remove everything from the database
        DB.drop_all()
        # Creates the database file initially.
        DB.create_all()
        return '''The database has been reset. 
        <a href='/'>Go to Home</a>
        <a href='/reset'>Go to reset</a>
        <a href='/populate'>Go to populate</a>'''    

    return app


if __name__ == '__main__':
    create_app().run()
