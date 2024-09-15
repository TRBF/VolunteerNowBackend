import {Database} from 'sqlite'
import {open} from 'sqlite'
import {Hono} from 'hono'
import {success, fail} from './_success_wrapper'
import authorizeUser from './_user_helper'
import sqlstring from 'sqlstring'

export default function(app : Hono, db : Database) {
    app.get('/api/get_experiences/:id', async (c) => {
        const {id} = c.req.param();
        var userid_parsed = parseInt(id);
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
            const {name, description, location, time, days, diploma} = await c.req.json();
            if(name == null || description == null || location == null || time == null || days == null)
                return c.json(fail("invalid json parameters"));
            if(isNaN(parseInt(time)) || isNaN(parseInt(days)))
                return c.json(fail("invalid json parameters"));
            await db.run("INSERT INTO experiences (Name,Description,Location,Time,Days,Diploma,VolunteerID) VALUES (?,?,?,?,?,?,?)", [name, description, location, time, days, diploma, userdata.ID]);
            return c.json(success(true));
        } catch {
            return c.json(fail("invalid json"));
        }
    });
    const valid_fields = ["Name", "Description", "Location", "Time", "Days", "Diploma"];
    app.post("/api/modify_expereince/:id", async (c) => {
        const {authorization} = c.req.header();
        if(authorization == null) return c.json(fail("invalid request"));
        const userdata = await authorizeUser(db, authorization);
        if(userdata == null) return c.json(fail("invalid token"));
        if(userdata.AccountType != 0) return c.json(fail("operation not supported for your account type"));
        const {id} = c.req.param();
        const parse_id = parseInt(id);
        if(isNaN(parse_id)) return c.json(fail("invalid id"));
        // check if user owns experience and is not managed by us
        if((await db.all("SELECT ID FROM expereinces WHERE ID = ? AND VolunteerID = ? AND EventID = NULL", [parse_id, userdata.ID])).length == 0)
            return c.json(fail("operation not available for that experience"));
        const params_to_change = await c.req.json();
        var query = "UPDATE experiences SET ";
        
        var first_param = true;
        for (const parameter of valid_fields) {
            if(params_to_change[parameter] != null) {
                if(!first_param)
                    query += ", ";
                query += parameter + " = " + sqlstring.escape(params_to_change[parameter]) + " ";
                first_param = false;
            }
        }
        query += "WHERE ID = " + parse_id;
        await db.exec(query);
        return c.json(success(true));
    });
    app.get("/api/delete_experience/:id", async (c) => {
        const {authorization} = c.req.header();
        if(authorization == null) return c.json(fail("invalid request"));
        const userdata = await authorizeUser(db, authorization);
        if(userdata == null) return c.json(fail("invalid token"));
        if(userdata.AccountType != 0) return c.json(fail("operation not supported for your account type"));
        const {id} = c.req.param();
        const parse_id = parseInt(id);
        if(isNaN(parse_id)) return c.json(fail("invalid id"));
        // check if user owns experience and is not managed by us
        if((await db.all("SELECT ID FROM expereinces WHERE ID = ? AND VolunteerID = ? AND EventID = NULL", [parse_id, userdata.ID])).length == 0)
            return c.json(fail("operation not available for that experience"));
        await db.run("DELETE FROM expereinces WHERE ID = ?", [parse_id]);
        return c.json(success(true));
    });
}