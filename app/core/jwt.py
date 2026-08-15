from datetime import datetime, timedelta, timezone

from jose import jwt

from app.core.config import settings


ALGORITHM = "HS256"


def create_access_token(
    data: dict,
    expires_minutes: int = 60
):

    payload = data.copy()

    expire = datetime.now(
        timezone.utc
    ) + timedelta(
        minutes=expires_minutes
    )

    payload.update({
        "exp": expire
    })


    return jwt.encode(
        payload,
        settings.JWT_SECRET,
        algorithm=ALGORITHM
    )



def decode_access_token(
    token: str
):

    try:

        payload = jwt.decode(
            token,
            settings.JWT_SECRET,
            algorithms=[ALGORITHM]
        )

        return payload

    except Exception:

        return None