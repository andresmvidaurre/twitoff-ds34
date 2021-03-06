from flask import Flask, render_template, request
from .models import DB, User, Tweet
from os import getenv
from .twitter import add_or_update_user
from .predict import predict_user




#factory
def create_app():


    app = Flask(__name__)

    # configuration variable to our app
    app.config['SQLALCHEMY_DATABASE_URI'] = getenv('DATABASE_URI')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # Connect our database to the app object
    DB.init_app(app)

    @app.route("/")
    def home_page():
        # query for all users in the database
        return render_template('base.html', title='Home', users=User.query.all())

   # @app.route('/populate')
    # Test my database functionality
    # by inserting some fake data into the DB
    #def populate():

      #  add_or_update_user('nasa')
     #   add_or_update_user('euphoriaHBO')
       # add_or_update_user('ryanallred')

        
        #return render_template('base.html', title='Populate')

    @app.route('/update')
    # Test my database functionality
    # by inserting some fake data into the DB
    def update():

        usernames = get_usernames()
        for username in usernames:
            add_or_update_user(username)

        
        return render_template('base.html', title='All Users have been updated')


    @app.route('/reset')
    def reset():
 
        DB.drop_all()
        DB.create_all()
        return render_template('base.html', title='Reset Database')
    
    # user route is a more traditional API endpoint
    # This endpoint can only accept certain kinds of http requests.
    @app.route('/user', methods=['POST'])
    @app.route('/user/<username>', methods=['GET'])
    def user(username=None, message=''):
        username = username or request.values['user_name']
        try:
            if request.method=='POST':
                add_or_update_user(username)
                message = f'User {username} has been successfully added!'
            tweets = User.query.filter(User.username == username).one().tweets
        except Exception as error:
            message = f'Error adding {username}: {error}'
            tweets = []
        return render_template('user.html', titel=username, tweets=tweets, message=message)

    @app.route('/compare', methods=['POST'])
    def compare():
        user0, user1 = sorted([request.values['user0'], request.values['user1']])

        if user0 == user1:
            message = 'Cannot compare user to themselves'
        else:
            prediction = predict_user(user0, user1, request.values['tweet_text'])
            message = "'{}' is more likely to be said by {} than {}".format(request.values['tweet_text'],
                                                                            user1 if prediction else user0,
                                                                            user0 if prediction else user1)
        return render_template('prediction.html', title='Prediction', message=message)

    return app


def get_usernames():
    # get all of the usernames of existing users
    Users = User.query.all()
    usernames = []
    for user in Users:
        usernames.append(user.username)
    return usernames