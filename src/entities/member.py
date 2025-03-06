from dataclasses import dataclass


@dataclass
class Member:
    """
        Class representing members (users) that use the app.
    """
    id: int         # Identifiant
    username: str   # Login
    password: str   # Mot de passe
    role: str       # Rôle pouvant être soit "admin" soit "user"
    uuid: str       # UUID NOTE: Revoir cette notion
