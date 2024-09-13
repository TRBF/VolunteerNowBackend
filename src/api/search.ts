import {Database} from 'sqlite'
import {open} from 'sqlite'
import {Hono} from 'hono'
import {success, fail} from './_success_wrapper'

export default function(app : Hono, db : Database) {
    app.get("/api/search_events/:search_term", async (c) => {
        const {search_term} = c.req.param();
        if(search_term.length < 2) return c.json(fail("please enter at least two characters"));
        var escaped_term = search_term.replace("!", "!!").replace("%", "!%").replace("_", "!_").replace("[", "![");

        return c.json(success(await db.all("SELECT * FROM events WHERE Name LIKE ? ESCAPE '!'", ['%' + escaped_term + '%'])));
    })
    app.get("/api/serach_organisers/:search_term", async (c) => {
        const {search_term} = c.req.param();
        if(search_term.length < 2) return c.json(fail("please enter at least two characters"));
        var escaped_term = search_term.replace("!", "!!").replace("%", "!%").replace("_", "!_").replace("[", "![");

        return c.json(success(await db.all("SELECT * FROM users WHERE AccountType = 1 AND DisplayName LIKE ? ESCAPE '!'", ['%' + escaped_term + '%'])));
    })
    app.get("/api/serach_volunteers/:search_term", async (c) => {
        const {search_term} = c.req.param();
        if(search_term.length < 2) return c.json(fail("please enter at least two characters"));
        var escaped_term = search_term.replace("!", "!!").replace("%", "!%").replace("_", "!_").replace("[", "![");

        return c.json(success(await db.all("SELECT * FROM users WHERE AccountType = 0 AND (FirstName LIKE ? ESCAPE '!' OR LastName LIKE ? ESCAPE '!')", ['%' + escaped_term + '%', '%' + escaped_term + '%'])));
    })
}