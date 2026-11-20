import bcrypt from "bcryptjs";
import { pool } from "../db.js";

export async function showSettings(req, res) {
  res.render("settings", {
    message: req.query.message || null,
    error: req.query.error || null
  });
}

export async function showPasswordForm(req, res) {
  res.render("settings-password", {
    message: req.query.message || null,
    error: req.query.error || null
  });
}

export async function changePassword(req, res) {
  const userId = req.session.userId;   // change to the key you actually store
  if (!userId) return res.redirect("/login");

  const { currentPassword, newPassword, confirmPassword } = req.body;

  if (!currentPassword || !newPassword || !confirmPassword) {
    return res.redirect("/settings?error=All fields are required");
  }

  if (newPassword !== confirmPassword) {
    return res.redirect("/settings?error=New passwords do not match");
  }

  if (newPassword.length < 8) {
    return res.redirect("/settings?error=Password must be at least 8 characters");
  }

  try {
    const { rows } = await pool.query(
      "SELECT password FROM users WHERE id = $1",
      [userId]
    );

    if (rows.length === 0) return res.redirect("/login");

    const match = await bcrypt.compare(currentPassword, rows[0].password);
    if (!match) {
      return res.redirect("/settings?error=Current password is incorrect");
    }

    const hash = await bcrypt.hash(newPassword, 10);
    await pool.query(
      "UPDATE users SET password = $1 WHERE id = $2",
      [hash, userId]
    );

    return res.redirect("/settings/password?message=Password updated");
  } catch (err) {
    console.error(err);
    return res.redirect("/settings/password?error=...");
  }
}