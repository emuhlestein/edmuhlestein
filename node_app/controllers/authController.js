import { getUserByEmail, createUser, authenticateUser } from "../services/user.js";

export function loginPage(req, res) {
  res.render("login", {
    error: req.query.error || null,
    email: req.query.email || "",
  });
}

export async function loginPost(req, res) {
  const { username, password } = req.body;

  console.log("loginPost reached", req.body);

  const user = await authenticateUser(username, password);
  if (!user) {
    return res.status(401).render("login", {
      error: "Incorrect email or password. Please try again.",
      email: username,
    });
  }

  console.log("Logged in user role:", user.user_role);   // <-- add this

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

export function logout(req, res) {
  req.session.destroy(() => {
    res.redirect("/");
  });
}