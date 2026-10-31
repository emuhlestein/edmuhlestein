import bcrypt from "bcrypt";          // or your existing hash helpers
import { getUserByEmail, createUser, authenticateUser } from "../services/user.js";

const TOKEN_MINUTES = Number(process.env.ACCESS_TOKEN_EXPIRE_MINUTES || 15);

function setTokenCookie(res, token) {
  res.cookie("access_token", token, {
    httpOnly: true,
    sameSite: "lax",
    secure: process.env.NODE_ENV === "production",
    maxAge: TOKEN_MINUTES * 60 * 1000,
  });
}

export function loginPage(req, res) {
  res.render("login.html", {
    error: req.query.error || null,
    email: req.query.email || "",
  });
}

export async function loginPost(req, res) {
  const { username, password } = req.body;

  const user = await authenticateUser(username, password);
  if (!user) {
    return res.status(401).render("login", {
      error: "Incorrect email or password. Please try again.",
      email: username,
    });
  }

  req.session.userId = user.id;
  req.session.email = user.email;
  req.session.role = user.user_role;

  res.redirect("/");
}

export function registerPage(req, res) {
  res.render("register", { error: null, form: {} });
}

export async function registerPost(req, res) {
  const { email, password, confirm_password } = req.body;
  const form = { email, password, confirm_password };

  // Basic checks (replace with a validator library if you prefer)
  if (!email || !password || password.length < 8) {
    return res.status(400).render("register", {
      error: "Email and a password of at least 8 characters are required.",
      form,
    });
  }
  if (password !== confirm_password) {
    return res.status(400).render("register", {
      error: "Passwords do not match.",
      form,
    });
  }

  if (await getUserByEmail(email)) {
    return res.status(400).render("register", {
      error: "Email already registered",
      form,
    });
  }

  let user;
  try {
    user = await createUser({ email, password });
  } catch (err) {
    return res.status(500).render("register", {
      error: "An error occurred during registration. Please try again.",
      form,
    });
  }

  req.session.userId = user.id;
  req.session.email = user.email;
  req.session.role = user.role;

  res.redirect("/dashboard");
}