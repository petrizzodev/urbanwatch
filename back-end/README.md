## Available Scripts

In the project directory, you can run:

### `uvicorn main:app --reload`

Runs the app in the development mode.\
Open [http://localhost:8000](http://localhost:8000) to view it in your browser.

The page will reload when you make changes.\
You may also see any lint errors in the console.


### `Create a .env file with the next variables`

SECRET_KEY = 'ec051cd48850ed3768e731b8a6c5be789bcc57cebfb3a27df2b30438a694fa28'
ALGORITHM = 'HS256'
ACCESS_TOKEN_EXPIRE_MINUTES = 30
SQLALCHEMY_DATABASE_URL='sqlite:///./database/sql_app.db'