import {Database} from 'sqlite'
import {open} from 'sqlite'
import {Hono} from 'hono'
import {success, fail} from './_success_wrapper'
import authorizeUser from './_user_helper'

export default function(app : Hono, db : Database) {
    app.get("/api/get_events", async (c) => {
        return c.json(success(await db.all("SELECT * FROM events")));
    });
    app.get("/api/get_event_by_id/:id", async (c) => {
        const {id} = c.req.param();
        const parsed_id = parseInt(id);
        if(isNaN(parsed_id)) return c.json(fail("invalid id"));
        const db_result = await db.all("SELECT * FROM events WHERE ID = ?", [parsed_id]);
        if(db_result.length == 0) return c.json(fail("no event with that id"));
        return c.json(success(db_result[0]));
    });
    app.post("/api/add_event", async (c) => {
        const {authorization} = c.req.header();
        if(authorization == null) return c.json(fail("invalid request"));
        const userdata = await authorizeUser(db, authorization);
        if(userdata == null) return c.json(fail("invalid token"));
        if(userdata.AccountType != 1) return c.json(fail("operation not supported for your account type"));
        try {
            const {name, description, link_to_pfp, link_to_cover_image, edition, location, time} = await c.req.json();
            if(name == null || description == null || link_to_pfp == null || link_to_cover_image == null
                || edition == null || location == null || time == null)
                return c.json(fail("invalid json parameters"));
            const event_id = (await db.run("INSERT INTO events (Name,Description,LinkToPFP,LinkToCoverImage,Edition,Location,Time) VALUES (?,?,?,?,?,?,?)", [name, description, link_to_pfp, link_to_cover_image, edition, location, time])).lastID;
            // register organiser of event
            await db.run("INSERT INTO event_organisers (EventID,OrganiserID) VALUES (?,?)", [event_id, userdata.ID]);
            return c.json(success(true));
        } catch {
            return c.json(fail("invalid json"));
        }
    });
}