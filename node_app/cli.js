import fs from "node:fs/promises";
import path from "node:path";
import pg from "pg";
import bcrypt from "bcryptjs";
import readline from "readline";

const { Client } = pg;

async function withDb(fn) {
  const client = new Client({ connectionString: process.env.DATABASE_URL });
  await client.connect();
  try {
    await fn(client);
  } finally {
    await client.end();
  }
}

function confirm(question) {
  const rl = readline.createInterface({
    input: process.stdin,
    output: process.stdout,
  });
  return new Promise((resolve) => {
    rl.question(`${question} (y/N) `, (answer) => {
      rl.close();
      resolve(/^y(es)?$/i.test(answer.trim()));
    });
  });
}

async function resetDb() {
  const ok = await confirm("Are you sure you want to drop all data?");
  if (!ok) {
    console.log("Aborted.");
    process.exit(1);
  }


  await withDb(async (client) => {
    const info = await client.query(`
    SELECT current_database() AS db,
            current_user AS usr,
            inet_server_addr() AS addr,
            inet_server_port() AS port
    `);
    console.log("CLI connection:", info.rows[0]);
    await client.query("DROP SCHEMA public CASCADE");
    await client.query("CREATE SCHEMA public");

    const tables = await client.query(`
      SELECT tablename FROM pg_tables WHERE schemaname = 'public'
    `);
    console.log("Tables after DROP:", tables.rows);

    const sql = await fs.readFile(
      path.join(process.cwd(), "sql", "init.sql"),
      "utf8"
    );
    await client.query(sql);

    console.log("♻️ Database has been reset.");
  });
}

async function seedData() {
  await withDb(async (client) => {
    const { rows } = await client.query(
      "SELECT id FROM users WHERE email = $1",
      ["admin@example.com"]
    );

    if (rows.length === 0) {
      const hashedPassword = await bcrypt.hash("adminUser", 10);
      await client.query(
        `INSERT INTO users (email, hashed_password, user_role)
         VALUES ($1, $2, $3)`,
        ["admin@example.com", hashedPassword, "admin"]
      );
      console.log("👤 Admin user created: admin@example.com / adminUser");
    } else {
      console.log("ℹ️ Admin user already exists.");
    }
  });
}

async function dumpUsers() {
  await withDb(async (client) => {
    const { rows } = await client.query(
      "SELECT id, email, user_role, is_active FROM users ORDER BY id"
    );
    console.table(rows);
  });
}

async function countUsers() {
  await withDb(async (client) => {
    const { rows } = await client.query("SELECT count(*)::int AS n FROM users");
    console.log(rows[0].n);
  });
}

const commands = {
  "reset-db": resetDb,
  "seed-data": seedData,
  "dump-users": dumpUsers,
  "count-users": countUsers,
};

function printHelp() {
  console.log("usage: node cli.js <command>");
  console.log("commands:");
  for (const name of Object.keys(commands)) {
    console.log("  " + name);
  }
}

const [,, name] = process.argv;
if (!name || name === "help") {
  printHelp();
  process.exit(0);
}

const command = commands[name];
if (!command) {
  console.log("usage: node cli.js <command>");
  console.log("commands:");
  for (const name of Object.keys(commands)) {
    console.log(`  ${name}`);
  }
  process.exit(1);
}
await command();