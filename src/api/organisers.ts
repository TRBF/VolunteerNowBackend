import {Database} from 'sqlite'
import {open} from 'sqlite'
import {Hono} from 'hono'
import {success, fail} from './_success_wrapper'

export default function(app : Hono, db : Database) {
    app.get("/api/get_organiser_by_id/:id", async (c) => {
        const {id} = c.req.param();
        const parse_id = parseInt(id);
        if(isNaN(parse_id)) return c.json(fail("invalid id"));
        const db_result = await db.all("SELECT * FROM users WHERE ID = ?", [parse_id]);
        if(db_result.length == 0) return c.json(fail("no user with that id"));
        if(db_result[0].AccountType != 1) return c.json(fail("that user is not an organiser"));
        return c.json(success(db_result[0]));
    });
}