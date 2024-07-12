import pytest
from sqlalchemy.exc import IntegrityError
from app import app
from models import db, Recipe, User

class TestRecipe:
    '''Tests for the Recipe model in models.py'''

    def _create_user(self, username):
        '''Helper method to create a user with a unique username'''
        user = User(username=username)
        user.password = "testpassword"  # Ensure password is set
        db.session.add(user)
        db.session.commit()
        return user

    def test_has_attributes(self):
        '''has attributes title, instructions, and minutes_to_complete.'''
        
        with app.app_context():

            Recipe.query.delete()
            User.query.delete()  # Clean up users to avoid UNIQUE constraint errors
            db.session.commit()

            user = self._create_user("UniqueUserForTest1")

            recipe = Recipe(
                title="Delicious Shed Ham",
                instructions="""Or kind rest bred with am shed then. In raptures building an bringing be. Elderly is detract tedious assured private so to visited. Do travelling companions contrasted it. Mistress strongly remember up to. Ham him compass you proceed calling detract. Better of always missed we person mr. September smallness northward situation few her certainty something.""",
                minutes_to_complete=60,
                user_id=user.id  # Ensure user_id is set
            )

            db.session.add(recipe)
            db.session.commit()

            new_recipe = Recipe.query.filter(Recipe.title == "Delicious Shed Ham").first()

            assert new_recipe.title == "Delicious Shed Ham"
            assert new_recipe.instructions == """Or kind rest bred with am shed then. In raptures building an bringing be. Elderly is detract tedious assured private so to visited. Do travelling companions contrasted it. Mistress strongly remember up to. Ham him compass you proceed calling detract. Better of always missed we person mr. September smallness northward situation few her certainty something."""
            assert new_recipe.minutes_to_complete == 60

    def test_requires_title(self):
        '''requires each record to have a title.'''

        with app.app_context():

            Recipe.query.delete()
            User.query.delete()  # Clean up users to avoid UNIQUE constraint errors
            db.session.commit()

            user = self._create_user("UniqueUserForTest2")

            recipe = Recipe(user_id=user.id)  # Set user_id to avoid IntegrityError
            
            with pytest.raises(IntegrityError):
                db.session.add(recipe)
                db.session.commit()

    def test_requires_50_plus_char_instructions(self):
        '''requires instructions to be at least 50 characters long.'''

        with app.app_context():

            Recipe.query.delete()
            User.query.delete()  # Clean up users to avoid UNIQUE constraint errors
            db.session.commit()

            user = self._create_user("UniqueUserForTest3")

            # Ensure instructions are less than 50 characters to trigger the validation
            with pytest.raises((IntegrityError, ValueError)):
                recipe = Recipe(
                    title="Generic Ham",
                    instructions="idk lol",
                    user_id=user.id  # Set user_id to avoid IntegrityError
                )
                db.session.add(recipe)
                db.session.commit()
