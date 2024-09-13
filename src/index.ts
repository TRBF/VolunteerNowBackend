import { serve } from '@hono/node-server'
import { Hono } from 'hono'
import {serveStatic} from '@hono/node-server/serve-static'
import sqlite3 from 'sqlite3'
import {open} from 'sqlite'
import register_experiences_endpoints from './api/experiences'
import register_authentication_endpoints from './api/login'
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
    register_experiences_endpoints(app, database)
    register_authentication_endpoints(app, database, mailTransporter)

    const port = 3000
    console.log(`Server is running on port ${port}`)

    serve({
        fetch: app.fetch,
        port
    })
}
main();


