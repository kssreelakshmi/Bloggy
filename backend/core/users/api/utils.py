from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.exceptions import AuthenticationFailed
import requests
from datetime import datetime, timedelta, timezone

GOOGLE_USERINFO_URL = "https://www.googleapis.com/oauth2/v3/userinfo"
GITHUB_USER_URL = "https://api.github.com/user"
GITHUB_EMAILS_URL = "https://api.github.com/user/emails"

def get_tokens_for_user(user):
    if not user.is_active:
        raise AuthenticationFailed("User account is inactive or banned.")
    
    refresh = RefreshToken.for_user(user)
    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }


def get_google_profile(access_token):
    """
    Validate Google token and return profile dict or raise requests.HTTPError.
    """
    headers = {"Authorization": f"Bearer {access_token}"}
    resp = requests.get(GOOGLE_USERINFO_URL, headers=headers, timeout=10)
    resp.raise_for_status()
    data = resp.json()
    # Google returns fields like: sub (id), email, email_verified, given_name, family_name, picture
    return {
        "provider": "google",
        "id": data.get("sub"),
        "email": data.get("email"),
        "email_verified": data.get("email_verified", False),
        "first_name": data.get("given_name"),
        "last_name": data.get("family_name"),
        "avatar": data.get("picture"),
        "profile_url": None,
        "access_token": access_token,
        # Google token expiration is not returned here; frontend can pass 'expires_in' if available
    }

def get_github_profile(access_token):
    """
    Get GitHub user profile and primary email. Returns profile dict.
    """
    headers = {"Authorization": f"Bearer {access_token}", "Accept": "application/vnd.github+json"}
    user_resp = requests.get(GITHUB_USER_URL, headers=headers, timeout=10)
    user_resp.raise_for_status()
    user = user_resp.json()

    email = user.get("email")
    email_verified = True if email else False

    # If email is not public, fetch emails
    if not email:
        emails_resp = requests.get(GITHUB_EMAILS_URL, headers=headers, timeout=10)
        emails_resp.raise_for_status()
        # emails_resp.json() -> list of {email, primary, verified, visibility}
        emails = emails_resp.json()
        primary = next((e for e in emails if e.get("primary") and e.get("verified")), None)
        if primary:
            email = primary.get("email")
            email_verified = primary.get("verified", False)
        else:
            # fallback to first verified
            verified = next((e for e in emails if e.get("verified")), None)
            if verified:
                email = verified.get("email")
                email_verified = verified.get("verified", False)

    return {
        "provider": "github",
        "id": str(user.get("id")),
        "email": email,
        "email_verified": email_verified,
        "first_name": user.get("name") or "",
        "last_name": "",
        "avatar": user.get("avatar_url"),
        "profile_url": user.get("html_url"),
        "access_token": access_token,
    }
