import {Database} from 'sqlite'
import {open} from 'sqlite'
import {Hono} from 'hono'

export default function(app : Hono, db : Database) {
    app.get('/api/get_experiences', async (c) => {
        return c.json(await getExperiences(db));
    });
}

async function getExperiences(db : Database) {
    return await db.all("SELECT * FROM volunteering_experience");
}