## Useful queries


###### H6 Number of releases by tags (Top 100) 

```
db.releases_initial.aggregate([
  {
    $facet: {
      "categorizedByTags": [
        { $unwind: "$tags" },
        { $sortByCount: "$tags" }, 
        { $limit: 100}
      ]
    }
  }
]); 
```

###### H6 Fetches duplicate release documents (if any)

```
db.releases_initial.aggregate([
    {$group: {
        _id: "$genre",
        count: {$sum: 1}
        }
    },
    {$match: { 
        count: {"$gt": 10000}
        }
    },
    { $sort : { count : -1} }
]);
```

###### H6 Genres having 10k+ releases

```
db.releases_initial.aggregate([
    {$group: {
        _id: "$genre",
        count: {$sum: 1}
        }
    },
    {$match: { 
        count: {"$gt": 10000}
        }
    },
    { $sort : { count : -1} }
]);
```

###### H6 Most productive artists

```
db.releases_initial.aggregate([
    {$group: {
        _id: "$artist",
        count: {$sum: 1}
        }
    },
    {$match: { 
        count: {"$gte": 100}
        }
    },
    { $sort : { count : -1} }
]);
```

###### H6 Schema update: add version

```
db.releases_initial.update(
    {"ver":{$exists:false}}, {"$set": {"ver": 1}}, false, true
)
```