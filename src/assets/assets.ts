import {Database} from 'sqlite'
import {open} from 'sqlite'
import {Hono} from 'hono'
import {success, fail} from '../api/_success_wrapper'
import authorizeUser from '../api/_user_helper'
import sqlstring from 'sqlstring'
import fs from 'fs'
import crypto from 'crypto'
import { stream } from 'hono/streaming'

export default function (app : Hono, db : Database)
{
    app.post("/api/upload", async (c) => {
        const {authorization} = c.req.header();
        if(authorization == null) return c.json(fail("invalid request"));
        const userdata = await authorizeUser(db, authorization);
        if(userdata == null) return c.json(fail("invalid token"));
        const body = await c.req.formData();
        console.log(body);
        // if(body.file == null) return c.json(fail("no file is present"));
        // console.log("new file: " + body.file);
        // if(!(body.file instanceof File)) return c.json(fail("file is not File type"));
        // const buffer = Buffer.from(await (body.file as File).arrayBuffer());
        
        // // compute asset hash
        // const hash = crypto.createHash('sha256').update(buffer).digest('hex');
        // if(fs.existsSync(`${process.cwd()}/_stored_assets/${hash}`))
        //     return c.json(success(hash)); // the file already exists, return the hash
        // // write file
        // var extension = (body.file as File).name.split('.').findLast(_ => true);
        // if(!fs.existsSync(`${process.cwd()}/_stored_assets`))
        //     fs.mkdirSync(`${process.cwd()}/_stored_assets`);
        // fs.writeFileSync(`${process.cwd()}/_stored_assets/${hash}`, buffer);
        
        // return c.json(success(hash));
    });

    app.get("/assets/:asset_id", async (c) => {
        const {asset_id} = c.req.param();
        if(!fs.existsSync(`${process.cwd()}/_stored_assets/${asset_id}`))
            return c.text("File not found", 404);
        return stream(c, async (stream) => {
            await stream.write(fs.readFileSync(`${process.cwd()}/_stored_assets/${asset_id}`))
        });
    });
}