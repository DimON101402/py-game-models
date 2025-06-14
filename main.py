import json
from db.models import Race, Skill, Player, Guild
import init_django_orm  # noqa: F401

def main() -> None:
    with open("players.json", "r", encoding="utf-8") as f:
        players_data = json.load(f)

    for player_data in players_data:
        race_data = player_data.get("race")
        if isinstance(race_data, dict):
            race_name = race_data.get("name")
            race_description = race_data.get("description", "")
            skills_data = race_data.get("skills", [])
        else:
            race_name = race_data
            race_description = ""
            skills_data = []

        race, _ = Race.objects.get_or_create(
            name=race_name,
            defaults={"description": race_description}
        )

        for skill_data in skills_data:
            Skill.objects.get_or_create(
                name=skill_data["name"],
                race=race,
                defaults={"bonus": skill_data["bonus"]}
            )

        guild_data = player_data.get("guild")
        if isinstance(guild_data, dict):
            guild_name = guild_data.get("name")
            guild_description = guild_data.get("description")
            guild, _ = Guild.objects.get_or_create(
                name=guild_name,
                defaults={"description": guild_description}
            )
        elif isinstance(guild_data, str):
            guild, _ = Guild.objects.get_or_create(name=guild_data)
        else:
            guild = None

        Player.objects.update_or_create(
            name=player_data["name"],
            defaults={
                "email": player_data.get("email"),
                "bio": player_data.get("bio"),
                "race": race,
                "guild": guild,
            }
        )

if __name__ == "__main__":
    main()