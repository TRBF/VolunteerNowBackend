import { serve } from '@hono/node-server'
import { Hono } from 'hono'
import {serveStatic} from '@hono/node-server/serve-static'
import sqlite3 from 'sqlite3'
import {open} from 'sqlite'
import register_experiences_endpoints from './api/experiences'

async function main() {
    const database = await open({
        filename: 'db.sqlite3',
        driver: sqlite3.Database
    });

    const app = new Hono()
    register_experiences_endpoints(app, database)

    const port = 3000
    console.log(`Server is running on port ${port}`)

    serve({
        fetch: app.fetch,
        port
    })
}
main();


