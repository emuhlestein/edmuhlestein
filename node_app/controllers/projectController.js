import { isLoggedIn } from "../utils/auth.js";

export function showProject(req, res) {
  res.render("project.html", {
    title: "Project",
    current_user: req.user || null,
    isLoggedIn: isLoggedIn(req)
  });
}