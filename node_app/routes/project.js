import { Router } from "express";
import { showProject } from "../controllers/projectController.js";

export const projectRouter = Router();

projectRouter.get("/", showProject);