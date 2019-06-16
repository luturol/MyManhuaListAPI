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
        public async void ConnectMongoDb()
        {
            const string connectionString = "mongodb://localhost:27017";

            // Create a MongoClient object by using the connection string
            var client = new MongoClient(connectionString);

            //Use the MongoClient to access the server
            var database = client.GetDatabase("test");

            //get mongodb collection
            var collection = database.GetCollection<Manhua>("Teste");
            await collection.InsertOneAsync(new Manhua { Name = "Teste", Chapter = 1 });
        }
    }
}
