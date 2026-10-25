export function showGame(req, res) {
  res.render("game.html", {
    title: "Game",
    current_user: req.user || null,
  });
}