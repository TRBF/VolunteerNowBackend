import {Database} from 'sqlite'
import {open} from 'sqlite'
import {Hono} from 'hono'
import {success, fail} from './_success_wrapper'
import authorizeUser from './_user_helper'
import sqlstring from 'sqlstring'

export default function(app : Hono, db : Database) {
    const application_valid_parameters = ["Question1", "Question2", "Question3", "Question4", "Question5", "Question6", "Question7", "Question8", "Question9", "Question10", "Question11", "Question12", "Question13", "Question14", "Question15", "Open"];
    const application_valid_fields = ["Question1", "Question2", "Question3", "Question4", "Question5", "Question6", "Question7", "Question8", "Question9", "Question10", "Question11", "Question12", "Question13", "Question14", "Question15"];
    app.post("/api/modify_application_form/:id", async (c) => {
        const {authorization} = c.req.header();
        if(authorization == null) return c.json(fail("invalid request"));
        const userdata = await authorizeUser(db, authorization);
        if(userdata == null) return c.json(fail("invalid token"));
        if(userdata.AccountType != 1) return c.json(fail("operation not supported for your account type"));
        const {id} = c.req.param();
        const parse_id = parseInt(id);
        if(isNaN(parse_id)) return c.json(fail("invalid id"));
        // check if event exists
        if((await db.all("SELECT ID FROM events WHERE ID = ?", [id])).length == 0) return c.json(fail("event doesn't exist"));
        // check if account is organiser of event
        if((await db.all("SELECT * FROM event_organisers WHERE EventID = ? AND OrganiserID = ?", [id, userdata.ID])).length == 0) return c.json(fail("unauthorized to edit application form"));
        // check if we should 'INSERT INTO' OR 'UPDATE' application form
        const db_result = await db.all("SELECT ID FROM event_applications WHERE EventID = ? LIMIT 1", [id]);
        var app_id : any = 0;
        if(db_result.length == 0) {
            // insert new row
            app_id = (await db.run("INSERT INTO event_applications (EventID,Open) VALUES (?,0)", [id])).lastID;
        } else {
            app_id = db_result[0].ID;
        }
        const params_to_change = await c.req.json();
        var query = "UPDATE event_applications SET ";
        
        var first_param = true;
        for (const parameter of application_valid_parameters) {
            if(params_to_change[parameter] != null) {
                if(!first_param)
                    query += ", ";
                query += parameter + " = " + sqlstring.escape(params_to_change[parameter]) + " ";
                first_param = false;
            }
        }
        query += "WHERE EventID = " + parse_id;
        await db.exec(query);
        return c.json(success(true));
    });
    app.get("/api/get_application_form/:id", async (c) => {
        const {id} = c.req.param();
        const parse_id = parseInt(id);
        if(isNaN(parse_id)) return c.json(fail("invalid id"));
        const db_result = await db.all("SELECT * FROM event_applications WHERE EventID = ? LIMIT 1", [id]);
        if(db_result.length == 0) return c.json(fail("no application form for that event"));
        return c.json(success(db_result[0]));
    });
    app.post("/api/apply/:id", async (c) => {
        const {authorization} = c.req.header();
        if(authorization == null) return c.json(fail("invalid request"));
        const userdata = await authorizeUser(db, authorization);
        if(userdata == null) return c.json(fail("invalid token"));
        if(userdata.AccountType != 0) return c.json(fail("operation not supported for your account type"));
        const {id} = c.req.param();
        const parse_id = parseInt(id);
        if(isNaN(parse_id)) return c.json(fail("invalid id"));
        // check if user didn't already apply
        if((await db.all("SELECT ID FROM applications WHERE ApplicantID = ? AND EventID = ? LIMIT 1", [userdata.ID, parse_id])).length > 0)
            return c.json(fail("you already applied for that event"));
        try {
            const push_params = await c.req.json();
            var parameters = [];
            parameters.push(userdata.ID);
            parameters.push(parse_id);
            for (const param of application_valid_fields) {
                if(push_params[param] != null)
                    parameters.push(push_params[param]);
                else
                    parameters.push("");
            }
            await db.run("INSERT INTO applications (ApplicantID,EventID,Question1,Question2,Question3,Question4,Question5,Question6,Question7,Question8,Question9,Question10,Question11,Question12,Question13,Question14,Question15) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)", parameters);
            return c.json(success(true));
        } catch {
            return c.json(fail("invalid json"));
        }
    });
    app.get("/api/get_applications/:id", async (c) => {
        const {authorization} = c.req.header();
        if(authorization == null) return c.json(fail("invalid request"));
        const userdata = await authorizeUser(db, authorization);
        if(userdata == null) return c.json(fail("invalid token"));
        if(userdata.AccountType != 1) return c.json(fail("operation not supported for your account type"));
        const {id} = c.req.param();
        const parse_id = parseInt(id);
        if(isNaN(parse_id)) return c.json(fail("invalid id"));
        return c.json(success(await db.all("SELECT app.Status as Status, user.ID as UserID, user.FirstName as FirstName, user.LastName as LastName, user.LinkToPFP as LinkToPFP FROM applications app INNER JOIN users user ON user.ID = app.ApplicantID WHERE app.EventID = ?", [parse_id])));
    });
    app.get("/api/get_application/:id", async (c) => {
        const {id} = c.req.param();
        const parse_id = parseInt(id);
        if(isNaN(parse_id)) return c.json(fail("invalid id"));
        const db_result = await db.all("SELECT * FROM applications WHERE ID = ?", [id]);
        if(db_result.length == 0) return c.json(fail("application doesn't exist"));
        return c.json(success(db_result[0]));
    });
    app.get("/api/accept_application/:id", async (c) => {
        const {authorization} = c.req.header();
        if(authorization == null) return c.json(fail("invalid request"));
        const userdata = await authorizeUser(db, authorization);
        if(userdata == null) return c.json(fail("invalid token"));
        if(userdata.AccountType != 1) return c.json(fail("operation not supported for your account type"));
        const {id} = c.req.param();
        const parse_id = parseInt(id);
        // check if user owns event and application is in pending status
        const db_result = await db.all("SELECT event.Name as eventName, app.ApplicantID as applicantID, event.ID as eventID FROM event_organisers org INNER JOIN applications app ON app.EventID = org.EventID INNER JOIN events event ON event.ID = app.EventID WHERE org.OrganiserID = ? AND app.ID = ? AND app.Status = 0", [userdata.ID, parse_id]);
        if(db_result.length == 0)
            return c.json(fail("application doesn't exist or you don't partake the event organisers of the application or the application is not in pending state"));
        // mark application as accepted
        await db.run("UPDATE applications SET Status = 1 WHERE ID = ?", id);
        // add user to volunteering team for that event
        await db.run("INSERT INTO event_volunteers (EventID,VolunteerID) VALUES (?,?)", [db_result[0].eventID, db_result[0].applicantID]);
        // notify user that their application has been accepted
        await db.run("INSERT INTO notifications (EmmiterID,TargetID,Title,Message) VALUES (?,?,?,?)",[userdata.ID, db_result[0].applicantID, "Application accepted", `Your application for ${db_result[0].eventName} has been accepted. You are now a part of the volunteering team.`]);
        return c.json(success(true));
    });
    app.post("/api/reject_application/:id", async (c) => {
        const {authorization} = c.req.header();
        if(authorization == null) return c.json(fail("invalid request"));
        const userdata = await authorizeUser(db, authorization);
        if(userdata == null) return c.json(fail("invalid token"));
        if(userdata.AccountType != 1) return c.json(fail("operation not supported for your account type"));
        const {id} = c.req.param();
        const parse_id = parseInt(id);
        const {reason} = await c.req.json();
        if(reason == null) return c.json(fail("invalid json parameters"));
        // check if user owns event and application is in pending status
        const db_result = await db.all("SELECT event.Name as eventName, app.ApplicantID as applicantID, event.ID as eventID FROM event_organisers org INNER JOIN applications app ON app.EventID = org.EventID INNER JOIN events event ON event.ID = app.EventID WHERE org.OrganiserID = ? AND app.ID = ? AND app.Status = 0", [userdata.ID, parse_id]);
        if(db_result.length == 0)
            return c.json(fail("application doesn't exist or you don't partake the event organisers of the application or the application is not in pending state"));
        // mark application as rejected
        await db.run("UPDATE applications SET Status = 2 WHERE ID = ?", id);
        // notify user that their application has been rejected and the reason for it
        await db.run("INSERT INTO notifications (EmmiterID,TargetID,Title,Message) VALUES (?,?,?,?)",[userdata.ID, db_result[0].applicantID, "Application rejected", `Your application for ${db_result[0].eventName} has been rejected. Reason: ${reason}`]);
        return c.json(success(true));
    });
    app.get("/api/reopen_application/:id", async (c) => {
        const {authorization} = c.req.header();
        if(authorization == null) return c.json(fail("invalid request"));
        const userdata = await authorizeUser(db, authorization);
        if(userdata == null) return c.json(fail("invalid token"));
        if(userdata.AccountType != 1) return c.json(fail("operation not supported for your account type"));
        const {id} = c.req.param();
        const parse_id = parseInt(id);
        // check if user owns event and application is in reject state. other applications can not be re-open
        const db_result = await db.all("SELECT event.Name as eventName, app.ApplicantID as applicantID, event.ID as eventID FROM event_organisers org INNER JOIN applications app ON app.EventID = org.EventID INNER JOIN events event ON event.ID = app.EventID WHERE org.OrganiserID = ? AND app.ID = ? AND NOT app.Status = 2", [userdata.ID, parse_id]);
        if(db_result.length == 0)
            return c.json(fail("application doesn't exist or you don't partake the event organisers of the application or the application is not in pending state"));
        // mark application as accepted
        await db.run("UPDATE applications SET Status = 0 WHERE ID = ?", id);
        // notify user that their application has been accepted
        await db.run("INSERT INTO notifications (EmmiterID,TargetID,Title,Message) VALUES (?,?,?,?)",[userdata.ID, db_result[0].applicantID, "Application re-opened", `Your application for ${db_result[0].eventName} has been re-opened. It is now in pending state again and is awaiting review.`]);
        return c.json(success(true));
    });

}