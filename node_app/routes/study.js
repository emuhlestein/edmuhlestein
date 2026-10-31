import { Router } from "express";
import { showStudy } from "../controllers/studyController.js";

export const studyRouter = Router();

studyRouter.get("/", showStudy);