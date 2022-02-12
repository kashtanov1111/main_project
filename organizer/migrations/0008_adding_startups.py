
from datetime import date

from django.db import migrations, models

STARTUPS = [
    {
        "name": "Boundless Software",
        "slug": "boundless-software",
        "contact": "hello@boundless.com",
        "description": "The sky was the limit.",
        "founded_date": date(2013, 5, 15),
        "tags": ["big-data"],
        "website": "http://boundless.com/",
    },
    {
        "name": "Game Congress",
        "slug": "game-congress",
        "contact": "vote@gamecongress.com",
        "description":
            "By gamers, for gamers, of gamers.",
        "founded_date": date(2012, 7, 4),
        "tags": ["video-games"],
        "website": "http://gamecongress.com/",
    },
    {
        "name": "Lightning Rod Consulting",
        "slug": "lightning-rod-consulting",
        "contact": "help@lightningrod.com",
        "description":
            "Channel the storm. "
            "Trouble shoot the cloud.",
        "founded_date": date(2014, 4, 1),
        "tags":
            ["ipython", "jupyter", "big-data"],
        "website": "http://lightningrod.com/",
    },
    {
        "name": "Monkey Software",
        "slug": "monkey-software",
        "contact": "shakespeare@monkeysw.com",
        "description":
            "1000 code monkeys making software.",
        "founded_date": date(2014, 12, 10),
        "tags": ["video-games"],
        "website": "http://monkeysw.com/",
    },
    {
        "name": "Simple Robots",
        "slug": "simple-robots",
        "contact": "yoshimi@simplerobots.com",
        "description":
            "Your resource to understanding "
            "computer, robots, and technology.",
        "founded_date": date(2010, 1, 2),
        "tags": ["python", "augmented-reality"],
        "website": "http://simplerobots.com/",
    },
    {
        "name": "Thingies",
        "slug": "thingies",
        "contact": "help@lightningrod.com",
        "description":
            "A marketplace for arduino, "
            "raspberry pi, and other "
            "homemade stuff.",
        "founded_date": date(2015, 4, 7),
        "tags": ["python"],
        "website": "http://buythingies.com/",
    },
]


def add_startup_data(apps, schema_editor):
    Startup = apps.get_model(
        'organizer', 'Startup')
    Tag = apps.get_model('organizer', 'Tag')
    for startup in STARTUPS:
        startup_object = Startup.objects.create(
            name=startup['name'],
            slug=startup['slug'],
            contact=startup['contact'],
            description=startup['description'],
            founded_date=startup['founded_date'],
            website=startup['website'])
        for tag_slug in startup['tags']:
            startup_object.tags.add(
                Tag.objects.get(
                    slug=tag_slug))

class Migration(migrations.Migration):

    dependencies = [
        ('organizer', '0007_adding_tags'),
    ]

    operations = [
        migrations.RunPython(
            add_startup_data,
        )
    ]
