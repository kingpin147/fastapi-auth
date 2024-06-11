from fastapi import FastAPI, Depends, HTTPException
from jose import jwt, JWTError
from datetime import datetime, timedelta
from fastapi.security import OAuth2, OAuth2PasswordBearer, OAuth2PasswordRequestForm
from typing import Annotated

app = FastAPI()

fake_users_db = {"admin": {"username": "admin", "hashed_password": "admin", "email": "admin@admin.com", "full_name": "admin"},
    "user": {"username": "nouman", "hashed_password": "attique", "email": "nouman@nouman.com", "full_name": "nouman"}
    }
    








ALGORITHM:str = "HS256"

"""HS256 stands for HMAC with SHA-256.
It is a cryptographic algorithm used to create a JSON Web Token (JWT). 
This algorithm combines the Hash-based Message Authentication Code (HMAC) 
with the Secure Hash Algorithm (SHA-256)."""


SECRET_KEY:str = "A very secure secret key"




@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.post("/login")
def login(form_data: Annotated[OAuth2PasswordRequestForm, Depends(OAuth2PasswordRequestForm)]):
    """
    Understanding the login system
    -> Takes form_data that have username and password
    """
    #Check username exist
    user_in_fake_db = fake_users_db.get(form_data.username)
    if user_in_fake_db is None:
        raise HTTPException(status_code=400, detail="Incorrect username")
    
    if user_in_fake_db["hashed_password"] != form_data.password:
        raise HTTPException(status_code=400, detail="Incorrect password")
    # We will add Logic here to check the username/email and password
    # If they are valid we will return the access token
    # If they are invalid we will return the error message

    access_token_expires = timedelta(minutes=1)
    generated_access_token = create_access_token(
        subject=form_data.username, expires_delta=access_token_expires
    )



    return {"username": form_data.username, "generated_access_token": generated_access_token}  

@app.get("/all-users")
def get_all_users():
    return fake_users_db






   
def create_access_token(subject: str , expires_delta: timedelta) -> str:
    """
    Creates an access token for a given subject with a specified expiration time.

    Args:
    - subject (str): The subject of the token (e.g., user ID).
    - expires_delta (timedelta): The duration after which the token should expire.

    Returns:
    - str: The encoded JSON Web Token (JWT) as a string.
    """
    # Calculate the expiration time by adding the given duration to the current UTC time
    expire = datetime.utcnow() + expires_delta
    # Prepare the payload with expiration time and subject
    to_encode = {"exp": expire, "sub": str(subject)}
    # Encode the payload into a JWT using the secret key and the specified algorithm
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    # Return the encoded JWT
    return encoded_jwt


@app.get("/new_route")
def get_access_token(user_name: str):
    """
    Endpoint to get an access token for a given user.

    Args:
    - user_name (str): The username for which the access token is to be generated.

    Returns:
    - dict: A dictionary containing the generated access token.
    """
    # Step 1: Define the expiration time for the access token
    access_token_expires = timedelta(minutes=15)
    
    print("access_token_expires", access_token_expires)
    # Step 2: Create the access token by calling the create_access_token function
    # The function takes the subject (user_name) and the expiration delta (access_token_expires)
    access_token = create_access_token(subject=user_name, expires_delta=access_token_expires)
    
    # Step 3: Return the access token in a dictionary
    return {"access_token": access_token}
