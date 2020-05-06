# PF2-API
Final project for Harvardx CS50. Attempting an API for the Pathfinder 2 RPG.

Application built in python on Flask.
Database built with SQLite3.

Content use protected by Open Game Licence.
All Pathfinder content is owned by Paizo Publishing, LLC, which are used under Paizo's Community Use Policy. I am expressly prohibited from charging you to use or access this content. This applicaton is not published, endorsed, or specifically approved by Paizo Publishing. For more information about Paizo's Community Use Policy, please visit paizo.com/communityuse. For more information about Paizo Publishing and Paizo products, please visit paizo.com.

Documentation

All text is UTF-8 encoded

GET /traits

Returns JSON data for all traits.

example:
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

count: Number of traits in the results list
results: list of Traits

trait data
id: integer id number
name: text full name of the trait
description: text full description (empty for those without description)
source: text book title and page number of original source
