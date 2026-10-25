import { Router } from "express";
import { showGame } from "../controllers/gameController.js";

export const gameRouter = Router();

gameRouter.get("/", showGame);