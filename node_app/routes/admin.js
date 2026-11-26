import { Router } from "express";
import { showAdmin } from "../controllers/adminController.js";

export const adminRouter = Router();

adminRouter.get("/", showAdmin);