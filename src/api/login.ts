import {Database} from 'sqlite'
import {open} from 'sqlite'
import {Hono} from 'hono'
import { success, fail } from './_success_wrapper';
import {createHash} from 'crypto';
import authorizeUser from './_user_helper';
import sqlstring from 'sqlstring';


function makeid(length : number) {
    let result = '';
    const characters = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789';
    const charactersLength = characters.length;
    let counter = 0;
    while (counter < length) {
      result += characters.charAt(Math.floor(Math.random() * charactersLength));
      counter += 1;
    }
    return result;
}

export default function(app : Hono, db : Database, mailTransporter : any) {
    app.get('/api/login', async (c) => {
        const {username, password} = c.req.query();
        if(username == null || password == null) return c.json(fail("invalid query parameters"));
        const db_result = await db.all("SELECT ID,PassHash,PassSalt,Token,VerifyToken FROM users WHERE Username = ?", [username]);
        if(db_result.length == 0) return c.json(fail("invalid username or password"));
        // check passhash
        if(createHash('sha256').update(password + db_result[0].PassSalt).digest('hex') != db_result[0].PassHash)
            return c.json(fail("invalid username or password"));
        // check if account email has been verified
        if(db_result[0].VerifyToken != null) return c.json(fail("account hasn't been verified yet"));
        // create new login token if it doesn't exist
        var token = db_result[0].Token;
        if(token == null) {
            token = makeid(64);
            await db.run("UPDATE users SET Token = ? WHERE ID = ?", [token, db_result[0].ID]);
        }
        return c.json(success({token: token, userid: db_result[0].ID}));
    });
    app.post('/api/register', async (c) => {
        try {
            const {username, password, gender, first_name, last_name, email, birthday} = await c.req.json();
            if(username == null || password == null || gender == null || first_name == null || last_name == null || email == null || birthday == null) return c.json(fail("invalid json parameters"));
            const parse_birthday = parseInt(birthday);
            if(isNaN(parse_birthday)) return c.json(fail("invalid birthday"));
            // check for age
            var birthdate = new Date(birthday * 1000), nowdate = new Date();
            var age = nowdate.getFullYear() - birthdate.getFullYear() - 1;
            if(birthdate.getMonth() > nowdate.getMonth())
                age += 1;
            else if(birthdate.getDay() >= nowdate.getDay())
                age += 1;
            if(age < 13) return c.json(fail("you must be 13 or older to sign up"));
            // check username valid
            if(!(/^[a-z0-9.]+$/.test(username))) return c.json(fail("invalid username"));
            if(!(/^[\w-\.]+@([\w-]+\.)+[\w-]{2,4}$/.test(email))) return c.json(fail("invalid email"));
            // check if username already exists in database
            if((await db.all("SELECT * FROM users WHERE Username = ? LIMIT 1", [username])).length > 0)
                return c.json(fail("an account with that username is already registered"));
            if((await db.all("SELECT * FROM users WHERE Email = ? LIMIT 1", [email])).length > 0)
                return c.json(fail("an account with that email is already registered"));
            // create password salt and hash password with it
            var pass_salt = makeid(12);
            var pass_hash = createHash('sha256').update(password + pass_salt).digest('hex');
            // create account verification token
            var verifyToken = makeid(64);
            await db.run("INSERT INTO users (Username,PassHash,PassSalt,VerifyToken,Email,Gender,FirstName,LastName,Birthday,CreationDate) VALUES (?,?,?,?,?,?,?,?,?,?)", [username, pass_hash, pass_salt, verifyToken, email, gender, first_name, last_name, birthday, Math.floor(new Date().getTime() / 1000)]);
            // send email
            mailTransporter.sendMail({
                from: 'volunteernowwastaken@gmail.com',
                to: email,
                subject: 'Verify your email address',
                text: `Please verify your account by visiting the following link: https://api.volunteernow.ro/api/verify/${verifyToken}`
            });
            return c.json(success(true));
        } catch {
            return c.json(fail("invalid json"));
        }
        
    });
    app.get('/api/verify/:vtoken', async (c) => {
        const {vtoken} = c.req.param();
        const db_result = await db.all("SELECT ID FROM users WHERE VerifyToken = ?", [vtoken]);
        if(db_result.length == 0) return c.json(fail("invalid verification token"));
        await db.all("UPDATE users SET VerifyToken = NULL WHERE ID = ?", [db_result[0].ID]);
        return c.json(success("your account has been verified. you can now log in."));
    });
    const valid_fields = ["Username","DisplayName","Gender","FirstName","LastName","Email","Description","LinkToPFP","LinkToCoverImage","Birthday"];
    app.post("/api/modify_profile", async (c) => {
        const {authorization} = c.req.header();
        if(authorization == null) return c.json(fail("invalid request"));
        const userdata = await authorizeUser(db, authorization);
        if(userdata == null) return c.json(fail("invalid token"));
        const params_to_change = await c.req.json();
        var query = "UPDATE users SET ";
        
        var first_param = true;
        for (const parameter of valid_fields) {
            if(params_to_change[parameter] != null) {
                if(!first_param)
                    query += ", ";
                query += parameter + " = " + sqlstring.escape(params_to_change[parameter]) + " ";
                first_param = false;
            }
        }
        query += "WHERE ID = " + userdata.ID;
        await db.exec(query);
        return c.json(success(true));
    });
    app.post("/api/change_password", async (c) => {
        const {authorization} = c.req.header();
        if(authorization == null) return c.json(fail("invalid request"));
        const userdata = await authorizeUser(db, authorization);
        if(userdata == null) return c.json(fail("invalid token"));
        const {password} = await c.req.json();
        if(password == null) return c.json(fail("invalid json parameters"));
        // create new salt
        var passSalt = makeid(12);
        var passHash = createHash('sha256').update(password + passSalt).digest('hex');
        // generate new token
        var newToken = makeid(64);
        // update in database
        await db.run("UPDATE users SET PassHash = ?, PassSalt = ?, Token = ? WHERE ID = ?", [passHash, passSalt, newToken, userdata.ID]);
        return c.json(success({token: newToken}));
    });
    app.get("/api/my_profile", async (c) => {
        const {authorization} = c.req.header();
        if(authorization == null) return c.json(fail("invalid request"));
        const userdata = await authorizeUser(db, authorization);
        if(userdata == null) return c.json(fail("invalid token"));
        const db_result = await db.all("SELECT * FROM users WHERE ID = ?", [userdata.ID]);
        delete db_result[0].PassHash;
        delete db_result[0].PassSalt;
        delete db_result[0].Token;
        delete db_result[0].VerifyToken;
        return c.json(success(db_result[0]));
    });
}