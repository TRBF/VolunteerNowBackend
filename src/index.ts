import { serve } from '@hono/node-server'
import { Hono } from 'hono'
import {serveStatic} from '@hono/node-server/serve-static'
import sqlite3 from 'sqlite3'
import {open} from 'sqlite'
import regep_experiences from './api/experiences'
import regep_auth from './api/login'
import regep_events from './api/events'
import regep_volunteers from './api/volunteers'

import nodemailer from 'nodemailer'

async function main() {
    const database = await open({
        filename: 'database.sqlite3',
        driver: sqlite3.Database
    });
    const mailTransporter = nodemailer.createTransport({
        service: 'gmail',
        auth: {
            'user': 'volunteernowwastaken@gmail.com',
            'pass': 'zrjlwgunaqjsutur'
        }
    });

    const app = new Hono()
    regep_auth(app, database, mailTransporter)
    regep_experiences(app, database)
    regep_events(app, database)
    regep_volunteers(app, database)


    const port = 3000
    console.log(`Server is running on port ${port}`)

    serve({
        fetch: app.fetch,
        port
    })
}
main();


