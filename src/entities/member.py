from dataclasses import dataclass


@dataclass
class Member:
    """
        Classe représentant les membres (utilisateurs) qui utilisent l'application.
        Répond aux contraintes de la table Member.
    """
    id: int         # Identifiant
    username: str   # Login
    password: str   # Mot de passe
    role: str       # Rôle pouvant être soit "admin" soit "user"
    uuid: str       # UUID NOTE: Revoir cette notion
