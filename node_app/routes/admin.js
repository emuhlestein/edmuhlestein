import { Router } from "express";
import { showAdmin } from "../controllers/adminController.js";
import { pool } from "../db.js";

export const adminRouter = Router();

adminRouter.get("/", showAdmin);

adminRouter.post("/calendar", async (req, res) => {
  const { day, color } = req.body;
  await pool.query(
    `INSERT INTO calendar_colors (day, color)
     VALUES ($1, $2)
     ON CONFLICT (day) DO UPDATE SET color = EXCLUDED.color`,
    [day, color]
  );
  res.json({ ok: true });
});

adminRouter.get("/calendar/year/:year", async (req, res) => {
  const year = Number(req.params.year);
  const { rows } = await pool.query(
    `SELECT to_char(day, 'YYYY-MM-DD') AS day, color
     FROM calendar_colors
     WHERE day >= $1 AND day < $2
     ORDER BY day`,
    [`${year}-01-01`, `${year + 1}-01-01`]
  );
  res.json(rows);
});