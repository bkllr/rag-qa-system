# MongoDB 基础

```javascript
db.users.insertOne({name: '张三', age: 25})
db.users.find({age: {$gt: 18}})
db.users.updateOne({_id: id}, {$set: {age: 26}})
db.users.deleteOne({_id: id})
```

## 聚合管道
```javascript
db.orders.aggregate([
  {$match: {status: 'done'}},
  {$group: {_id: '$product', total: {$sum: '$amount'}}},
])
```