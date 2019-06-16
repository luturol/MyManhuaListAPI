using MongoDB.Bson;
using MongoDB.Bson.Serialization.Attributes;
using System;
using System.Collections.Generic;
using System.Linq;
using System.Threading.Tasks;

namespace MyManhuaList.Model
{
    [BsonIgnoreExtraElements]
    public class Manhua
    {
        public ObjectId Id { get; set; }
        public string Name { get; set; }
        public int Chapter { get; set; }
    }
}
