import bcrypt from "bcrypt";
import { pool } from "../db.js";
// import { db } from "../db.js";          // your pg pool or query helper
// import { users } from "../schema.js";   // if using an ORM

const SALT_ROUNDS = 10;

export async function getUserByEmail(email) {
  const result = await pool.query(
    "SELECT id, email, hashed_password, full_name FROM users WHERE email = $1 LIMIT 1",
    [email]
  );
  return result.rows[0] || null;
}

export async function createUser({ email, password, full_name }) {
  const existing = await getUserByEmail(email);
  if (existing) {
    const err = new Error("Email already registered");
    err.status = 400;
    throw err;
  }

  const hashedPassword = await bcrypt.hash(password, SALT_ROUNDS);

  // Example insert
  // const result = await db.query(
  //   `INSERT INTO users (email, hashed_password, full_name)
  //    VALUES ($1, $2, $3)
  //    RETURNING *`,
  //   [email, hashedPassword, full_name]
  // );
  // return result.rows[0];

  // Placeholder — replace with your actual insert
  return { id: 1, email, hashed_password: hashedPassword, full_name };
}

export async function userExists({ email, username, userId } = {}) {
  if (!email && !username && !userId) return false;

  // Build a simple existence check
  // const conditions = [];
  // const values = [];
  // let i = 1;
  // if (email) { conditions.push(`email = $${i++}`); values.push(email); }
  // if (username) { conditions.push(`username = $${i++}`); values.push(username); }
  // if (userId) { conditions.push(`id = $${i++}`); values.push(userId); }
  //
  // const result = await db.query(
  //   `SELECT 1 FROM users WHERE ${conditions.join(" AND ")} LIMIT 1`,
  //   values
  // );
  // return result.rows.length > 0;

  return false;
}

export async function authenticateUser(email, password) {
  const user = await getUserByEmail(email);
  if (!user) return null;

  const ok = await bcrypt.compare(password, user.hashed_password);
  return ok ? user : null;
}