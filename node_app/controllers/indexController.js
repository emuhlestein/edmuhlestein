export function showHome(req, res) {
  res.render("index.html", {
    title: "Home",
    current_user: req.user || null,
  });
}