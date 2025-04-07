from aiogram.fsm.state import State, StatesGroup


# Create instances of StatesGroup for each form
class QueryFormer(StatesGroup):
    name = State()
    genre = State()
    years = State()
    countries = State()
    ratings = State()
    age_ratings = State()
    limit = State()
    select_date = State()
