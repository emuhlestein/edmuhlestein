import { isLoggedIn } from "../utils/auth.js";

export function showHome(req, res) {
  console.log("showHome reached", req.session);

  try {
    res.render("index.html", {
      title: "Home",
      role: req.session?.role || null,
      isLoggedIn: isLoggedIn(req)
    });
  } catch (err) {
    console.error("render failed:", err);
    res.status(500).send("render error");
  }
}