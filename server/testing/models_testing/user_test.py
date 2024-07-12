import pytest
from sqlalchemy.exc import IntegrityError
from app import app
from models import db, User, Recipe

class TestUser:
    '''User in models.py'''

    def test_has_attributes(self):
        '''has attributes username, _password_hash, image_url, and bio.'''
        
        with app.app_context():

            # Clear existing users
            User.query.delete()
            db.session.commit()

            # Create a new user
            user = User(
                username="Liz",
                image_url="https://prod-images.tcm.com/Master-Profile-Images/ElizabethTaylor.jpg",
                bio="""Dame Elizabeth Rosemond Taylor DBE (February 27, 1932 - March 23, 2011) was a British-American actress..."""
            )
            user.password = "whosafraidofvirginiawoolf"  # Set the password

            db.session.add(user)
            db.session.commit()

            # Fetch the created user
            created_user = User.query.filter(User.username == "Liz").first()

            # Assertions
            assert created_user.username == "Liz"
            assert created_user.image_url == "https://prod-images.tcm.com/Master-Profile-Images/ElizabethTaylor.jpg"
            assert created_user.bio == """Dame Elizabeth Rosemond Taylor DBE (February 27, 1932 - March 23, 2011) was a British-American actress..."""
            
            # Check that password raises AttributeError if accessed
            with pytest.raises(AttributeError):
                created_user.password

    def test_requires_username(self):
        '''requires each record to have a username.'''

        with app.app_context():

            User.query.delete()
            db.session.commit()

            user = User()
            user.password = "validpassword"  # Ensure password is set

            with pytest.raises(IntegrityError):
                db.session.add(user)
                db.session.commit()

    def test_requires_unique_username(self):
        '''requires each record to have a unique username.'''

        with app.app_context():

            User.query.delete()
            db.session.commit()

            user_1 = User(username="Ben")
            user_1.password = "password1"  # Ensure password is set

            user_2 = User(username="Ben")
            user_2.password = "password2"  # Ensure password is set

            db.session.add(user_1)
            db.session.commit()

            with pytest.raises(IntegrityError):
                db.session.add(user_2)
                db.session.commit()

    def test_has_list_of_recipes(self):
        '''has records with lists of recipes records attached.'''

        with app.app_context():

            User.query.delete()
            db.session.commit()

            # Create and save a user
            user = User(username="Prabhdip")
            user.password = "securepassword"  # Set the password
            db.session.add(user)
            db.session.commit()

            # Create recipes with valid instructions
            recipe_1 = Recipe(
                title="Delicious Shed Ham",
                instructions="""Or kind rest bred with am shed then. In raptures building an bringing be. Elderly is detract tedious assured private so to visited. Do travelling companions contrasted it. Mistress strongly remember up to. Ham him compass you proceed calling detract. Better of always missed we person mr. September smallness northward situation few her certainty something.""",
                minutes_to_complete=60,
                user_id=user.id  # Set the user_id
            )
            recipe_2 = Recipe(
                title="Hasty Party Ham",
                instructions="""As am hastily invited settled at limited civilly fortune me. Really spring in extent an by. Judge but built gay party world. Of so am he remember although required. Bachelor unpacked be advanced at. Confined in declared marianne is vicinity.""",
                minutes_to_complete=30,
                user_id=user.id  # Set the user_id
            )

            db.session.add_all([recipe_1, recipe_2])
            db.session.commit()

            # Check that all were created in db
            assert user.id
            assert recipe_1.id
            assert recipe_2.id

            # Check that recipes were saved to user
            assert recipe_1 in user.recipes
            assert recipe_2 in user.recipes
