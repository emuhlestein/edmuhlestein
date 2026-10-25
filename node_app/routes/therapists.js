import { Router } from "express";
import { showTherapists } from "../controllers/therapistsController.js";

export const therapistsRouter = Router();

therapistsRouter.get("/", showTherapists);