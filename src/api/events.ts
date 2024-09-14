import {Database} from 'sqlite'
import {open} from 'sqlite'
import {Hono} from 'hono'
import {success, fail} from './_success_wrapper'
import authorizeUser from './_user_helper'

export default function(app : Hono, db : Database) {
    app.get("/api/get_events", async (c) => {
        const {page} = c.req.query();
        if(page == null || isNaN(parseInt(page)))
            return c.json(success(await db.all("SELECT * FROM events ORDER BY ID DESC LIMIT 10")));
        var offset = parseInt(page) * 10
        return c.json(success(await db.all("SELECT * FROM events ORDER BY ID DESC LIMIT 10 OFFSET ?", [offset])));

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

    app.get("/api/mark_event_done/:id", async (c) => {
        const {authorization} = c.req.header();
        if(authorization == null) return c.json(fail("invalid request"));
        const userdata = await authorizeUser(db, authorization);
        if(userdata == null) return c.json(fail("invalid token"));
        if(userdata.AccountType != 1) return c.json(fail("operation not supported for your account type"));
        const {id} = c.req.param();
        const parse_id = parseInt(id);
        if(isNaN(parse_id)) return c.json(fail("invalid id"));
        // check if event's status is 0 and is owned by current user
        if((await db.all("SELECT ev.ID FROM events ev INNER JOIN event_organisers org ON org.EventID = ev.ID WHERE ev.ID = ? AND ev.Status = 0 AND org.OrganiserID = ?", [parse_id, userdata.ID])).length == 0)
            return c.json(fail("the event doesn't exist or you don't partake the organisers team or it is already marked as finished"));
        await db.run("UPDATE events SET Status = 1 WHERE ID = ?", [parse_id]);
        // add experience for all users
        await db.run("INSERT INTO experiences (EventID,VolunteerID) SELECT v.EventID, v.VolunteerID FROM event_volunteers v WHERE v.EventID = ?", [parse_id]);
        return c.json(success(true));
    });

    app.get("/api/get_organisers_of_event/:id", async (c) => {
        const {id} = c.req.param();
        const parse_id = parseInt(id);
        if(isNaN(parse_id)) return c.json(fail("invalid id"));
        if((await db.all("SELECT * FROM events WHERE ID = ?", [parse_id])).length == 0) return c.json(fail("invalid id"));
        return c.json(success(await db.all("SELECT org.ID as ID, org.DisplayName as DisplayName, org.LinkToPFP as LinkToPFP FROM event_organisers ev INNER JOIN users org ON org.ID = ev.OrganiserID WHERE ev.EventID = ?", [id])));
    });
}