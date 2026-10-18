import { Router } from "express";
import { showHome } from "../controllers/indexController.js";

export const indexRouter = Router();

indexRouter.get("/", showHome);