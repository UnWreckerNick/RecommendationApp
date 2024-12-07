from fastapi import APIRouter, Depends, HTTPException
from app.auth import hash_password, pwd_context, create_access_token, get_current_user
from app.database import get_db, SessionLocal
from app.models import User, UserPreference
from app.schemas import RegisterUser, PreferenceCreate

router = APIRouter()

@router.post("/register/")
def register_user(user: RegisterUser, db: SessionLocal = Depends(get_db)):
    if db.query(User).filter(User.username == user.username).first():
        raise HTTPException(status_code=400, detail="Username already exists")
    hashed_password = hash_password(user.password)
    new_user = User(username=user.username, hashed_password=hashed_password)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return {"message": "User successfully registered", "user_id": new_user.id}

@router.post("/login/")
def login_user(user_login: RegisterUser, db: SessionLocal = Depends(get_db)):
    user = db.query(User).filter(User.username == user_login.username).first()
    if not user or not pwd_context.verify(user_login.password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Invalid username and/or password")
    access_token = create_access_token(data={"sub": user.username})
    return {"access_token": access_token, "token_type": "bearer"}

@router.post("/preferences/")
def add_preference(
        preference: PreferenceCreate,
        db: SessionLocal = Depends(get_db),
        current_user = Depends(get_current_user)
):
    if preference.item_type not in ["movie", "book"]:
        raise HTTPException(status_code=400, detail="Invalid item type")
    preference = UserPreference(
        user_id=current_user.id,
        item_id=preference.item_id,
        item_type=preference.item_type,
        interaction=preference.interaction
    )
    db.add(preference)
    db.commit()
    db.refresh(preference)
    return {"message": "Preference successfully added", "preference_id": preference.id}
