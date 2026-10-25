import pg from "pg";
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
  console.log("commands:", Object.keys(commands).join(", "));
  process.exit(1);
}

await command();