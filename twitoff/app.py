from flask import Flask, render_template
from .models import DB, User, Tweet



#factory
def create_app():


    app = Flask(__name__)

    # configuration variable to our app
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite3'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # Connect our database to the app object
    DB.init_app(app)

    @app.route("/")
    def home_page():
        # query for all users in the database
        users = User.query.all()
        print(users)
        return render_template('base.html', title='Home', users=users)

    @app.route('/populate')
    # Test my database functionality
    # by inserting some fake data into the DB
    def populate():

        #Reset the database first
        # remove everything from the DB
        DB.drop_all()
        # recreate the User and Tweet tables
        # so that they're ready to be used (inserted into)
        DB.create_all()
        

        # Make two new users
        andres = User(id=1, username='andres')
        caleb = User(id=2, username='caleb')
        satan = User(id=3, username='satan')
        satansdog = User(id=4, username='satans dog')
        andresinhell = User(id=5, username='andres in hell')
        calebinhell = User(id=6, username='caleb in hell')

        # Make two tweets
        tweet1 = Tweet(id=1, text='Hi I am andres', user=andres)
        tweet2 = Tweet(id=2, text='Hi I am caleb', user=caleb)
        tweet3 = Tweet(id=3, text='welcome, to hell', user=satan)
        tweet4 = Tweet(id=4, text='be careful with that chalice, its poison', user=satansdog)
        tweet5 = Tweet(id=5, text='whats in this chalice. It looks delicious.', user=andresinhell)
        tweet6 = Tweet(id=6, text='omg, youre here too?!', user=calebinhell)

        # Inserting into the DB when working with SQLite directly
        DB.session.add(andres)
        DB.session.add(caleb)
        DB.session.add(satan)
        DB.session.add(satansdog)
        DB.session.add(andresinhell)
        DB.session.add(calebinhell)
        DB.session.add(tweet1)
        DB.session.add(tweet2)
        DB.session.add(tweet3)
        DB.session.add(tweet4)
        DB.session.add(tweet5)
        DB.session.add(tweet6)

        # Commit the DB changes
        DB.session.commit()

        
        return render_template('base.html', title='Populate')
        # Make two tweets and attach the tweets to those users






    @app.route('/reset')
    def reset():
        #Do some database stuff
        #Drop old DB Tables
        # Remake new DB Tables
        # remove everything from the DB
        DB.drop_all()
        # recreate the User and Tweet tables
        # so that they're ready to be used (inserted into)
        DB.create_all()
        return render_template('base.html', title='Reset Database')



    return app