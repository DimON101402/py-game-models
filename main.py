import json
import init_django_orm  # noqa: F401
from db.models import Race, Skill, Player, Guild


def main() -> None:
    with open("players.json", "r", encoding="utf-8") as f:
        players_data = json.load(f)
    for nickname, data in players_data.items():
        race = None
        race_data = data.get("race")
        if isinstance(race_data, dict):
            race_name = race_data.get("name", "")
            race_description = race_data.get("description", "")
            race, _ = Race.objects.get_or_create(
                name=race_name,
                defaults={"description": race_description}
            )
            for skill in race_data.get("skills", []):
                Skill.objects.get_or_create(
                    name=skill.get("name", ""),
                    race=race,
                    defaults={"bonus": skill.get("bonus", "")}
                )
        guild = None
        guild_data = data.get("guild")
        if isinstance(guild_data, dict):
            guild_name = guild_data.get("name", "")
            guild_description = guild_data.get("description")
            if guild_description is None:
                guild_description = ""
            guild, _ = Guild.objects.get_or_create(
                name=guild_name,
                defaults={"description": guild_description}
            )
            guild.description = guild_description
            guild.save()
        Player.objects.update_or_create(
            nickname=nickname,
            defaults={
                "email": data.get("email", ""),
                "bio": data.get("bio", ""),
                "race": race,
                "guild": guild,
            }
        )


if __name__ == "__main__":
    main()
