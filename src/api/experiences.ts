import {Database} from 'sqlite'
import {open} from 'sqlite'
import {Hono} from 'hono'
import {success, fail} from './_success_wrapper'
import authorizeUser from './_user_helper'

export default function(app : Hono, db : Database) {
    app.get('/api/get_experiences', async (c) => {
        const {userid} = c.req.query();
        if(userid == null) return c.json(fail("invalid query parameters"));
        var userid_parsed = parseInt(userid);
        if(isNaN(userid_parsed)) return c.json(fail("invalid userid"));
        const db_result = await db.all("SELECT * FROM experiences WHERE VolunteerID = ?", [userid_parsed]);
        return c.json(success(db_result));
    });
    app.get('/api/get_experience_by_id/:id', async (c) => {
        const {id} = c.req.param();
        var id_parsed = parseInt(id);
        if(isNaN(id_parsed)) return c.json(fail("invalid id"));
        const db_result = await db.all("SELECT * FROM experiences WHERE ID = ?", [id_parsed]);
        if(db_result.length == 0) return c.json(fail("no experience with that id"));
        return c.json(success(db_result[0]));
    });
    app.post('/api/add_experience', async (c) => {
        const {authorization} = c.req.header();
        if(authorization == null) return c.json(fail("invalid request"));
        const userdata = await authorizeUser(db, authorization);
        if(userdata == null) return c.json(fail("invalid token"));
        if(userdata.AccountType != 0) return c.json(fail("operation not supported for your account type"));
        try {
            const {name, description, location, time} = await c.req.json();
            if(name == null || description == null || location == null || time == null)
                return c.json(fail("invalid json parameters"));
            await db.run("INSERT INTO experiences (Name,Description,Location,Time,VolunteerID) VALUES (?,?,?,?,?)", [name, description, location, time, userdata.ID]);
            return c.json(success(true));
        } catch {
            return c.json(fail("invalid json"));
        }
    });
}