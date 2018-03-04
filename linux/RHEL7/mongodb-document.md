# MongoDb - Document

## Create/Add

### [insertOne](https://docs.mongodb.com/manual/reference/method/db.collection.insertOne/)

```sql
> db.collection.insertOne(
   <document>,
   {
      writeConcern: <document>
   }
)
```

`example`

```sql
> db.fruit.insertOne({_id: "apples", qty: 5})
```

### [insertMany](https://docs.mongodb.com/manual/reference/method/db.collection.insertMany/)

```sql
> db.collection.insertMany(
   [ <document 1> , <document 2>, ... ],
   {
      writeConcern: <document>,
      ordered: <boolean>
   }
)
```

`example`

```sql
> db.fruit.insertMany([
  {_id: "bananas", qty: 7},
  {_id: "oranges", qty: {"in stock": 8, "ordered": 12}},
  {_id: "avocados", qty: "fourteen"}
])
```

### [insert](https://docs.mongodb.com/manual/reference/method/db.collection.insert)

```sql
> db.collection.insert(
   <document or array of documents>,
   {
     writeConcern: <document>,
     ordered: <boolean>
   }
)
```

`example`

```sql
> db.fruit.insert({_id: "grape", qty: 10})
> db.fruit.insert([
  {_id: "berry", qty: 20},
  {_id: "lemon", qty: 9}
])
```

---

## Read/Query

### [find](https://docs.mongodb.com/manual/reference/method/db.collection.find/)

```sql
                                                                      not show field
                                                                      v
> db.<collection>.find({<field>: <value>, ...}, {<field>: 1, <field>: 0,...}).limit(1).pretty()
                        ^                        ^
                        query                   projection: show field
> db.<collection>.find({<field>: <value>, ...}, {<field>: {$slice: [i, j]}, ...}).sort(<field>: 1).pretty()
```

`example`

```
{_id: "apples", "qty": 5},
{_id: "bananas", "qty": 7},
{_id: "oranges", "qty": {"in stock": 8, "ordered": 12}},
{_id: "avocados", "qty": "fourteen"},
{_id: "grape", qty: 10}
```

```sql
// basic
> db.fruit.findOne()
> db.fruit.find()
> db.fruit.find({qty: 5})
> db.fruit.find({}, {_id: 1})                      // show field
> db.fruit.find({qty: {$gte: 5}})                  // comparsion operator: $eq, $gt, $gte, $lt, $lte
> db.fruit.find({qty: {$gte: 5}}, {_id: 1})
> db.fruit.find({_id: "apples"})                   // search string
> db.fruit.find({_id: {$in: ["apples", "grape"]})  // comparsion operator: $in, $ne, $nin
> db.fruit.find({_id: /an/})                       // regex
> db.fruit.find({$or: [                            // logical operator: $and, $not, $or, $nor
                       {qty: {$gt: 5}},
                       {_id: "apples"}
]})
> db.fruit.find({"qty.ordered": {$exists: true}})  // check field exists or not

// chain
> db.fruit.find().pretty()
> db.fruit.find().count()
> db.fruit.find().limit(1)
> db.fruit.find().sort({qty: 1})
> db.fruit.find().skip(2)
> db.fruit.find({_id: "APPLES"}).collation({ locale: "en_US", strength: 1 })

// advance
> var myCursor = db.fruit.find()
> myCursor
> db.fruit.find().forEach(function(myDoc) {
  print("fruite: " + myDoc._id);
});

// $size
// $elemMatch
// $where
// $regex
```

### [aggregate](https://docs.mongodb.com/manual/reference/method/db.collection.aggregate/)

```sql
> db.<collection>.aggregate(<pipeline>, <options>)
```

### [aggregation-pipeline](https://docs.mongodb.com/manual/reference/operator/aggregation-pipeline/)

```sql
> db.<collection>.aggregate( [ { <stage> }, ... ] )
```

常用的 stage 如下

[$match](https://docs.mongodb.com/manual/reference/operator/aggregation/match/)

```sql
> db.articles.aggregate([{$match: {<query>} }])
```

```
{author: "dave", score: 80, views: 100, otherAuthor: ["john", "mary"]},
{author: "dave", score: 85, views: 521},
{author: "ahn",  score: 60, views: 1000},
{author: "li",   score: 55, views: 5000},
{author: "annT", score: 60, views: 50},
{author: "li",   score: 94, views: 999},
{author: "ty",   score: 95, views: 1000}
```

```sql
// 設定搜尋條件
> db.articles.aggregate({$match: {views: {$gt: 500}}})

// 配合 group 做分群
> db.articles.aggregate([
                         {$match: {author: "dave"}},
                         {$group: {_id: "$author",
                                   count: {$sum: 1},
                                   totalViews: {$sum: "$views"}
                                  }
                         }
])

// 配合 project 指定處理 field
> db.articles.aggregate([{
                          $match: {views: {$gt: 500}}},
                          $project: {_id: 1}
])
```

[$group](https://docs.mongodb.com/manual/reference/operator/aggregation/group/)

```sql
> db.articles.aggregate([
                         {$group: {_id: null,
                                   totalViews: {$sum: "$views"},
                                   averageSore: {$avg: "$score"}
                                  }
                         }
])
```

[$project](https://docs.mongodb.com/manual/reference/operator/aggregation/project/)

```sql
> db.articles.aggregate({$project: {_id: 1, author: 1}})
```

[$unwind](https://docs.mongodb.com/manual/reference/operator/aggregation/unwind/)

[$out](https://docs.mongodb.com/manual/reference/operator/aggregation/out/)


[$lookup](https://docs.mongodb.com/manual/reference/operator/aggregation/lookup/)

[$sort](https://docs.mongodb.com/manual/reference/operator/aggregation/sort/)



---

## Update/Modify


---

## Delete/Remove
