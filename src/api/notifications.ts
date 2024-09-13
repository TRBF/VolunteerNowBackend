import {Database} from 'sqlite'
import {open} from 'sqlite'
import {Hono} from 'hono'
import {success, fail} from './_success_wrapper'
import authorizeUser from './_user_helper'

export default function(app : Hono, db : Database) {
    app.get("/api/get_notifications", async (c) => {
        const {authorization} = c.req.header();
        if(authorization == null) return c.json(fail("invalid request"));
        const userdata = await authorizeUser(db, authorization);
        if(userdata == null) return c.json(fail("invalid token"));
        return c.json(success(await db.all("SELECT notif.ID as ID, notif.Title as Title, notif.Message as Message, user.DisplayName as AuthorName, user.LinkToPFP as AuthorPicture FROM users user INNER JOIN notifications notif on user.ID = notif.EmmiterID WHERE notif.TargetID = ?", [userdata.ID])));
    });

    app.get("/api/get_notification_by_id/:id", async (c) => {
        const {id} = c.req.param();
        const parse_id = parseInt(id);
        if(isNaN(parse_id)) return c.json(fail("invalid id"));
        const {authorization} = c.req.header();
        if(authorization == null) return c.json(fail("invalid request"));
        const userdata = await authorizeUser(db, authorization);
        if(userdata == null) return c.json(fail("invalid token"));
        const db_result = await db.all("SELECT * FROM notifications WHERE ID = ? AND TargetID = ?", [id, userdata.ID]);
        if(db_result.length == 0) return c.json(fail("invalid notification id"));
        return c.json(success(db_result[0]));
    });

    app.post("/api/add_notification", async (c) => {
        const {authorization} = c.req.header();
        if(authorization == null) return c.json(fail("invalid request"));
        const userdata = await authorizeUser(db, authorization);
        if(userdata == null) return c.json(fail("invalid token"));
        if(userdata.AccountType == 0) return c.json(fail("invalid account type"));
        const {target, title, message} = await c.req.json();
        if(target == null || title == null || message == null) return c.json(fail("invalid json parameters"));
        const parse_target = parseInt(target);
        if(isNaN(parse_target) || (await db.all("SELECT * FROM users WHERE ID = ?", [parse_target])).length == 0) return c.json(fail("invalid target id"));
        await db.run("INSERT INTO notifications (EmmiterID,TargetID,Title,Message) VALUES (?,?,?,?)", [userdata.ID, parse_target, title, message]);
        return c.json(success(true));
    });
}