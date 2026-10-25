export function showAbout(req, res) {
  res.render("about.html", {
    title: "About",
    current_user: req.user || null,
  });
}