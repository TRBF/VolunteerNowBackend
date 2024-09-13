import {Database} from 'sqlite'
import {open} from 'sqlite'
import {Hono} from 'hono'
import { success, fail } from './_success_wrapper';
import {createHash} from 'crypto';


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
        return c.json(success({token: token}));
    });
    app.post('/api/register', async (c) => {
        try {
            const {username, password, gender, first_name, last_name, email} = await c.req.json();
            if(username == null || password == null || gender == null || first_name == null || last_name == null || email == null) return c.json(fail("invalid json parameters"));
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
            await db.run("INSERT INTO users (Username,PassHash,PassSalt,VerifyToken,Email,Gender,FirstName,LastName,CreationDate) VALUES (?,?,?,?,?,?,?,?,?)", [username, pass_hash, pass_salt, verifyToken, email, gender, first_name, last_name, new Date().getTime() / 1000]);
            // send email
            mailTransporter.sendMail({
                from: 'volunteernowwastaken@gmail.com',
                to: email,
                subject: 'Verify your email address',
                text: 'Please verify your account by visiting the following link: <link>/api/verify/' + verifyToken
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
        return c.json(success(true));
    });
}