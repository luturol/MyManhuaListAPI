using Microsoft.AspNetCore.Mvc;
using MyManhuaLIst.Repository;
using System;
using System.Collections.Generic;
using System.Linq;
using System.Threading.Tasks;

namespace MyManhuaList.Controllers
{
    [Route("api/[controller]")]
    [ApiController]
    public class ManhuaController : ControllerBase
    {
        [HttpGet]
        public ActionResult<IEnumerable<string>> Get()
        {
            return new string[] { "value1", "value2" };
        }

        // GET api/values/5
        [HttpGet("{id}")]
        public ActionResult<string> Get(int id)
        {
            return "value";
        }

        // POST api/values
        [HttpPost]
        public void Post([FromBody] string value)
        {
            var repository = new ManhuaRepository();
            repository.ConnectMongoDb();
        }
    }
}
