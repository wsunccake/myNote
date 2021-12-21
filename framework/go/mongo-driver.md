# mongo-driver

## crud example

```bash
tree 
.
├── main.go
├── makefile
└── utils
    └── db.go
```

```go
package main

import (
	"math/rand"
	"animal/utils"
	"time"

	"go.mongodb.org/mongo-driver/bson"
	"go.mongodb.org/mongo-driver/bson/primitive"
)

const (
	MONGODB_URI     string = "mongodb://127.0.0.1:27017"
	DATABASE_NAME   string = "zoo"
	COLLECTION_NAME string = "animal"
)

type SpeciesDoc struct {
	ID        string    `bson:"_id,omitempty"`
	CreatedAt time.Time `bson:"created_at"`
	Food      []string  `bson:"food"`
}

func main() {
	utils.ConnectDatabase(MONGODB_URI)
	defer utils.DisconnectDatabase()

	utils.ListDatabase()
	utils.ListCollection(DATABASE_NAME)

	utils.ConnectCollection(DATABASE_NAME, COLLECTION_NAME)

	animal0 := utils.AnimalDoc{"mickey", 1, "Mouse", map[string]string{}}
	utils.InsertOneDocument(animal0)

	animal1 := utils.AnimalDoc{"doogy", 1, "Dog", map[string]string{}}
	animal2 := utils.AnimalDoc{"kitty", 2, "Cat", map[string]string{}}
	animal3 := utils.AnimalDoc{"piggy", 3, "Pig", map[string]string{"h": "1", "w": "a"}}
	animals := []interface{}{animal1, animal2, animal3}
	utils.InsertManyDocument(animals)

	filter0 := bson.M{"age": bson.M{"$gt": 2}}
	utils.FindDocumnet(filter0)

	rand.Seed(time.Now().UnixNano())
	age := rand.Intn(5)
	id, _ := primitive.ObjectIDFromHex("615d5471587ec242bcdca7e5")
	filter1 := bson.M{"_id": id}
	update1 := bson.D{
		{"$set", bson.D{{"age", age}}},
	}
	utils.UpdateOneDucmnet(filter1, update1)

	filter2 := bson.M{"species": "Mouse"}
	utils.DeleteManyDocument(filter2)
}
```

```go
package utils

import (
	"context"
	"fmt"
	"log"
	"time"

	"go.mongodb.org/mongo-driver/bson"
	"go.mongodb.org/mongo-driver/mongo"
	"go.mongodb.org/mongo-driver/mongo/options"
)

type AnimalDoc struct {
	Name    string            `bson:"name,omitempty"`
	Age     int               `bson:"age,omitempty"`
	Species string            `bson:"species"`
	Size    map[string]string `bson:"size"`
}

var (
	err        error
	trash      interface{}
	client     *mongo.Client
	ctx        context.Context
	collection *mongo.Collection
)

func ConnectDatabase(uri string) {
	client, err = mongo.NewClient(options.Client().ApplyURI(uri))
	if err != nil {
		log.Fatal(err)
	}
	ctx, trash = context.WithTimeout(context.Background(), 10*time.Second)
	err = client.Connect(ctx)
	if err != nil {
		log.Fatal(err)
	}

	err = client.Ping(context.TODO(), nil)
	if err != nil {
		log.Fatal(err)
	}
	fmt.Println("connect mongodb")
}

func DisconnectDatabase() {
	client.Disconnect(ctx)
	fmt.Println("disconnect mongodb")
}

func ListDatabase() {
	databases, err := client.ListDatabaseNames(ctx, bson.M{})
	if err != nil {
		log.Fatal(err)
	}
	fmt.Println("list database:", databases)
}

func ListCollection(db string) {
	collections, err := client.Database(db).ListCollectionNames(ctx, bson.M{})
	if err != nil {
		log.Fatal(err)
	}
	fmt.Println("list collection:", collections)
}

func ConnectCollection(database_name string, collection_name string) {
	collection = client.Database(database_name).Collection(collection_name)
}

func InsertOneDocument(doc interface{}) {
	result, err := collection.InsertOne(context.TODO(), doc)
	if err != nil {
		log.Fatal(err)
	}
	fmt.Println("insert one document: ", result.InsertedID)
}

func InsertManyDocument(docs []interface{}) {
	result, err := collection.InsertMany(context.TODO(), docs)
	if err != nil {
		log.Fatal(err)
	}
	fmt.Println("insert multiple document: ", result.InsertedIDs)
}

func FindDocumnet(filter interface{}) {
	cur, currErr := collection.Find(ctx, filter)
	if currErr != nil {
		panic(currErr)
	}
	defer cur.Close(ctx)
	var animals []AnimalDoc
	if err := cur.All(ctx, &animals); err != nil {
		panic(err)
	}
	fmt.Println("find document:", animals)
}

func UpdateOneDucmnet(filter interface{}, update interface{}) {
	result, err := collection.UpdateOne(ctx, filter, update)
	if err != nil {
		log.Fatal(err)
	}
	fmt.Printf("update document: %v\n", result.ModifiedCount)
}

func DeleteManyDocument(filter interface{}) {
	result, err := collection.DeleteMany(ctx, filter)
	if err != nil {
		log.Fatal(err)
	}
	fmt.Printf("delete documents %v\n", result.DeletedCount)
}
```

```makefile
.DEFAULT_GOAL := build

.PHONY: fmt
fmt:
	go fmt ./...

.PHONY: lint
lint:
	$(shell go env GOPATH)/bin/golint ./...

.PHONY: vet
vet:
	go vet ./...

.PHONY: build
build: fmt
	go build ./...
	go build

.PHONY: clean
clean:
	rm animal	

.PHONY: run
run: build
	./animal
```
