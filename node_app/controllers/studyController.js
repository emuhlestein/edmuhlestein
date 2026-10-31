export function showStudy(req, res) {
  res.render("study.html", {
    title: "Study",
    current_user: req.user || null,
  });
}