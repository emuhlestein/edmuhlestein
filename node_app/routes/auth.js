import { Router } from "express";
import {
  loginPage,
  loginPost,
  registerPage,
  registerPost,
  logout,
} from "../controllers/authController.js";

export const authRouter = Router();

authRouter.get("/login", loginPage);
authRouter.post("/login", loginPost);
authRouter.get("/logout", logout);
authRouter.get("/register", registerPage);
authRouter.post("/register", registerPost);