import { isLoggedIn } from "../utils/auth.js";

export function showAdmin(req, res) {
  res.render("admin.html", {
    title: "Admin",
    current_user: req.user || null,
    isLoggedIn: isLoggedIn(req)
  });
}