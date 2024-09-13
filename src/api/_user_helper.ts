import {Database} from 'sqlite'

export default async function(db : Database, token : string) : Promise<any|undefined> {
    const db_result = await db.all("SELECT ID,AccountType FROM users WHERE Token = ?", [token]);
    if(db_result.length == 0) return null;
    return db_result[0];
}