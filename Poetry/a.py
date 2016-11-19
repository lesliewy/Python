db.poem.insert_one(
            {
                "category": {
                    "name": category.name,
                    "url": category.url,
                    "numofauthors": category.numofauthors
                },
                "author": {
                    "name": author.name,
                    "url": author.url,
                    "numofpoems": author.numofpoems,
                    "brief": author.brief
                },
                "poems": [
                    {
                        "name": poem.name,
                        "url": poem.url,
                        "content": poem.content,
                        "tags": poem.tags,
                        "appreciation": poem.appreciation
                    }
                ]
            }
        )