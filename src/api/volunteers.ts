import {Database} from 'sqlite'
import {open} from 'sqlite'
import {Hono} from 'hono'
import {success, fail} from './_success_wrapper'

export default function(app : Hono, db : Database) {
    app.get("/api/get_volunteer_by_id/:id", async (c) => {
        const {id} = c.req.param();
        const parse_id = parseInt(id);
        if(isNaN(parse_id)) return c.json(fail("invalid id"));
        const db_result = await db.all("SELECT user.*, SUM(exp.Days) as DaysOfVolunteering FROM users user INNER JOIN experiences exp ON exp.VolunteerID = user.ID WHERE user.ID = ?", [parse_id]);
        if(db_result.length == 0) return c.json(fail("no user with that id"));
        console.log(db_result[0]);
        if(db_result[0].AccountType != 0) return c.json(fail("that user is not a volunteer"));
        delete db_result[0].PassHash;
        delete db_result[0].PassSalt;
        delete db_result[0].Token;
        delete db_result[0].VerifyToken;
        delete db_result[0].Birthday;
        delete db_result[0].DisplayName;
        delete db_result[0].AccountType;
        delete db_result[0].Email;
        return c.json(success(db_result[0]));
    });
}