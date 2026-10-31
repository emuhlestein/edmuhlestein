export function showHome(req, res) {
  res.render("index.html", {
    title: "Home",
    role: req.session.role || null,
  });
}