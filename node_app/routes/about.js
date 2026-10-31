import { Router } from "express";
import { showAbout } from "../controllers/aboutController.js";

export const aboutRouter = Router();

aboutRouter.get("/", showAbout);