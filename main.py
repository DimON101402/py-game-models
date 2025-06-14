import init_django_orm  # noqa: F401

from db.models import Race, Skill, Player, Guild
import json


def main() -> None:
    with open("players.json", "r", encoding="utf-8") as f:
        players_data = json.load(f)

    for player_data in players_data:
        race_name = player_data["race"]["name"]
        race_description = player_data["race"].get("description", "")
        race, _ = Race.objects.get_or_create(
            name=race_name,
            defaults={"description": race_description}
        )

        for skill_data in player_data["race"].get("skills", []):
            Skill.objects.get_or_create(
                name=skill_data["name"],
                race=race,
                defaults={"bonus": skill_data["bonus"]}
            )

        guild = None
        if "guild" in player_data and player_data["guild"]:
            guild_name = player_data["guild"]["name"]
            guild_description = player_data["guild"].get("description", None)
            guild, _ = Guild.objects.get_or_create(
                name=guild_name,
                defaults={"description": guild_description}
            )

        Player.objects.update_or_create(
            nickname=player_data["nickname"],
            defaults={
                "email": player_data["email"],
                "bio": player_data["bio"],
                "race": race,
                "guild": guild,
            }
        )


if __name__ == "__main__":
    main()
