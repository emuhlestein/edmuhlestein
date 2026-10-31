export function showHome(req, res) {
  const role = req.session?.role || null;

  res.render("index.html", {
    title: "Home",
    role,
  });
}