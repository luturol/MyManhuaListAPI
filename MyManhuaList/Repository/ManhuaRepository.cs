using MongoDB.Driver;
using MyManhuaList.Model;
using System;
using System.Collections.Generic;
using System.Linq;
using System.Threading.Tasks;

namespace MyManhuaLIst.Repository
{
    public class ManhuaRepository
    {
        private IMongoCollection<Manhua> ConnectMongoDb()
        {
            const string connectionString = "mongodb://localhost:27017";

            // Create a MongoClient object by using the connection string
            var client = new MongoClient(connectionString);

            //Use the MongoClient to access the server
            var database = client.GetDatabase("test");

            //get mongodb collection
            var collection = database.GetCollection<Manhua>("Teste");
            return collection;
        }

        public IEnumerable<Manhua> GetAll()
        {
            //get mongodb collection
            var collection = ConnectMongoDb().AsQueryable().Where(e => true).ToList();

            return collection;//.Find(x => true).ToEnumerable();
        }

        public async void Add(Manhua manhua)
        {
            var collection = ConnectMongoDb();
            if(collection.FindOneAndUpdate(x => x.Name == manhua.Name, Builders<Manhua>.Update.Set(e => e.Chapter, manhua.Chapter)) == null)
                await collection.InsertOneAsync(manhua);
        }
         
        public Manhua Get(string name)
        {
            var collection = ConnectMongoDb();
            return collection.Find(x => x.Name == name).FirstOrDefault();
        }
    }
}
