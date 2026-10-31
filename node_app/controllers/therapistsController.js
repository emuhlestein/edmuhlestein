export function showTherapists(req, res) {
  res.render("therapists.html", {
    title: "Therapists",
    current_user: req.user || null,
  });
}