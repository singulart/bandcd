## Useful queries


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