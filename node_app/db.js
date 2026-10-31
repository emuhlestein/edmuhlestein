import pg from "pg";
import { settings } from "./settings.js";

export const pool = new pg.Pool({
  connectionString: settings.databaseUrl,
});