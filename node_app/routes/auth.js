import { Router } from "express";
import {
  loginPage,
  loginPost,
  registerPage,
  registerPost,
} from "../controllers/authController.js";

export const authRouter = Router();

authRouter.get("/login", loginPage);
authRouter.post("/login", loginPost);
authRouter.get("/register", registerPage);
authRouter.post("/register", registerPost);