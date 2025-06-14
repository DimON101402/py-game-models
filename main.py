import json
from db.models import Race, Skill, Player, Guild
import init_django_orm  # noqa: F401


def main() -> None:
    with open("players.json", "r", encoding="utf-8") as f:
        players_data = json.load(f)

    for player in players_data:
        race = None
        skills_data = []
        if isinstance(player.get("race"), dict):
            race_info = player["race"]
            race, _ = Race.objects.get_or_create(
                name=race_info.get("name"),
                defaults={"description": race_info.get("description", "")}
            )
            skills_data = race_info.get("skills", [])
        elif isinstance(player.get("race"), str):
            race, _ = Race.objects.get_or_create(
                name=player["race"],
                defaults={"description": ""}
            )

        for skill in skills_data:
            Skill.objects.get_or_create(
                name=skill["name"],
                race=race,
                defaults={"bonus": skill.get("bonus", 0)}
            )

        guild = None
        if isinstance(player.get("guild"), dict):
            guild_info = player["guild"]
            guild, _ = Guild.objects.get_or_create(
                name=guild_info.get("name"),
                defaults={"description": guild_info.get("description", "")}
            )
        elif isinstance(player.get("guild"), str):
            guild, _ = Guild.objects.get_or_create(
                name=player["guild"]
            )

        Player.objects.update_or_create(
            name=player["name"],
            defaults={
                "email": player.get("email", ""),
                "bio": player.get("bio", ""),
                "race": race,
                "guild": guild,
            }
        )


if __name__ == "__main__":
    main()