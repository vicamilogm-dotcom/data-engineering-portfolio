# 2️⃣ MongoDB Basics

❓ Switch the database
```bash
use food
```

❓ Create a collection 📁
```bash
db.createCollection("fruits")
```

✅ Verify in `Mongo-express` that the database has been created.

❓ Insert multiple documents 📄
```bash
db.fruits.insertMany([ {name: "apple", origin: "usa", price: 5}, {name: "orange", origin: "italy", price: 3}, {name: "mango", origin: "malaysia", price: 3} ])
```

❓ Query the documents using the find command
```bash
db.fruits.find() #.pretty()
db.fruits.find({name: "orange"})
db.fruits.find({_id: ObjectId("63af03444c0b9ec718b6c79f")})
```

❓ Insert another record, but now also containing the color, 💡 this is no problem for Mongodb due to it being **schemaless**
```bash
db.fruits.insertOne( { name: "apple", origin: "usa", price: 3, color: "red" } )
```

❓ Update the record you just inserted in the previous step by increasing its price to 4 ☝️.
```bash
db.fruits.updateOne( { name: "apple", origin: "usa", color: "red" }, { $set: { price: 4 } } )
```

❓ Use the `countDocuments` command to count the number of documents in the collection
```bash
db.fruits.countDocuments()
```

❓ Use the `deleteMany` command to delete all the fruits that are from Italy:
```bash
db.fruits.deleteMany( { origin: "italy" } )
```

❓ Use the `drop` command to drop the entire collection 💥
```bash
db.fruits.drop()
```
