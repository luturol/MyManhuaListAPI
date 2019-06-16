using Microsoft.AspNetCore.Mvc;
using MyManhuaList.Model;
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
        public ActionResult<IEnumerable<Manhua>> Get()
        {
            var repository = new ManhuaRepository();
            List<Manhua> list = repository.GetAll().ToList();
            return Ok(list);
        }
        
        [HttpGet("{name}")]
        public ActionResult<string> Get(string name)
        {
            var repository = new ManhuaRepository();
            return Ok(repository.Get(name));
        }

        [HttpPost]
        public void Post(Manhua manhua)
        {
            var repository = new ManhuaRepository();
            repository.Add(manhua);
        }
    }
}
