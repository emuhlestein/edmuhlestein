import bcrypt from "bcryptjs";
import { pool } from "../db.js";

const SALT_ROUNDS = 10;

export async function getUserByEmail(email) {
  const result = await pool.query(
    "SELECT id, email, hashed_password, full_name, user_role FROM users WHERE email = $1 LIMIT 1",
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

  const result = await pool.query(
    `INSERT INTO users (email, hashed_password, full_name, user_role)
     VALUES ($1, $2, $3, 'user')
     RETURNING id, email, full_name`,
    [email, hashedPassword, full_name]
  );

  return result.rows[0];
}

export async function userExists({ email, username, userId } = {}) {
  if (!email && !username && !userId) return false;

  const conditions = [];
  const params = [];

  if (email) {
    params.push(email);
    conditions.push(`email = $${params.length}`);
  }
  if (username) {
    params.push(username);
    conditions.push(`username = $${params.length}`);
  }
  if (userId) {
    params.push(userId);
    conditions.push(`id = $${params.length}`);
  }

  const result = await pool.query(
    `SELECT 1 FROM users WHERE ${conditions.join(" OR ")} LIMIT 1`,
    params
  );

  return result.rows.length > 0;
}

export async function authenticateUser(email, password) {
  const user = await getUserByEmail(email);
  if (!user) return null;

  const ok = await bcrypt.compare(password, user.hashed_password);
  return ok ? user : null;
}