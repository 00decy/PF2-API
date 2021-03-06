# PF2-API
Final project for Harvardx CS50. Attempting an API for the Pathfinder 2 RPG.

Application built in python on Flask.
Database built with SQLite3.

This project is not live, to run it yourself you need the python application `app.py` and the database `pathfinder2.db`.

## Licence

This project is published under the MIT licence.

Content use protected by the [Open Game Licence](https://en.wikipedia.org/wiki/Open_Game_License).

All Pathfinder content is owned by Paizo Publishing, LLC, which are used under Paizo's Community Use Policy. I am expressly prohibited from charging you to use or access this content. This applicaton is not published, endorsed, or specifically approved by Paizo Publishing. For more information about Paizo's Community Use Policy, please visit [paizo.com/communityuse](https://paizo.com/community/communityuse). For more information about Paizo Publishing and Paizo products, please visit [paizo.com](https://paizo.com/).

All content sourced from [The Archives of Nethys](https://aonprd.com/).

## API Documentation

All text is UTF-8 encoded

### GET `/traits`

Returns JSON data for traits.

Accepts following query parameters:
1. id - integer
 - trait id number, eg
 `/traits?id=69`
2. source - text
 - book title eg
 `/traits?source=Core+Rulebook`
 - optional page number eg
 `/traits?source=Core+Rulebook+pg.+628`
3. name - text
 - trait name, eg
 `/traits?name=Aberration`

All other query parameters ignored. Queries return empty `results` list if no matches are found.
If none of the listed query parameters are given, returns all traits.

example: `/traits`
```
{
    "count": 284,
    "reults": [
        {
            "id": 1,
            "name": "Aberration",
            "description": "Aberrations are creatures from beyond the planes or corruptions of the natural order.",
            "source": "Core Rulebook pg. 628"
        },
        ...
    ]
}
```
- count: integer length of results list
- results: list of traits

  - id: integer id number
  - name: text full name of the trait
  - description: text full description (`null` for those without description)
  - source: text book title and page number of original source

### GET '/feats'

Returns JSON data for feats.

Accepts following query parameters:
1. id - integer
 - feat id number, eg
 `/feats?id=69`
2. source - text
 - book title, eg
 `/feats?source=Core+Rulebook`
 - optional page number, eg
 `/feats?source=Core+Rulebook+pg.+101`
3. name - text
 - feat name, eg
 `/feats?name=Harmonize`
4. action - text
 - action type, eg
 `/feats?action=Single+Action`
5. level - integer
 - feat level, eg
 `/feats?level=6`
6. archetype - text
 - archetype name, g
 `/feats?archetype=Fighter`
7. trait - text
 - single trait name, eg
 `/feats?trait=Additive`
 - multiple trait names or any additional trait values like 'Additive 1' will return empty results list

All other query parameters ignored. Queries return empty `results` list if no matches are found.
If none of the listed query parameters are given, returns all feats.

example: `/feats`
```
{
  "count": 1182,
  "reults": [
    ...
    {
        "id": 193,
        "name": "Harmonize",
        "action": "Single Action",
        "level": 6,
        "prerequisites": "maestro muse",
        "archetype": null,
        "frequencey": null,
        "requirements": null,
        "trigger": null,
        "description": "You can perform multiple compositions simultaneously. If your next action is to cast a composition, it becomes a harmonized composition. Unlike a normal composition, a harmonized composition doesn\u2019t end if you cast another composition, and you can cast another composition on the same turn as a harmonized one. Casting another harmonized composition ends any harmonized composition you have in effect.",
        "source": "Core Rulebook pg. 101",
        "traits": [
          "Bard",
          "Concentrate",
          "Manipulate",
          "Metamagic"
        ]
    },
    ...
  ]
}
```
- count: integer length of results list
- results: list of feats

  - id: integer id number
  - name: text full name of the feat
  - action: text type of action provided by the feat
  - level: integer feat level
  - prerequisites: text any additional prerequisites
  - archetype: text name of the associated archetype
  - frequencey: text any restriction on how often the feat can be used
  - requirements: text any requirements need to use the feat
  - trigger: text the trigger for a reaction feat
  - description: text full description
  - source: text book title and page number of original source
  - traits: list of text trait names (with any additional trait values) of the feat


- For feats without the relevent info those fields are left `null`
