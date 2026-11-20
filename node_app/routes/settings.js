import { Router } from "express";
import { showSettings, changePassword, showPasswordForm } from "../controllers/settingsController.js";
import { requireLogin } from "../middleware/requireLogin.js";

export const settingsRouter = Router();

settingsRouter.get("/", requireLogin, showSettings);
settingsRouter.get("/password", requireLogin, showPasswordForm);
settingsRouter.post("/password", requireLogin, changePassword);