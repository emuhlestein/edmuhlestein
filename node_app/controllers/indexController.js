export function showHome(req, res) {
  console.log("showHome reached", req.session);

  try {
    res.render("index.html", {
      title: "Home",
      role: req.session?.role || null,
      isLoggedIn: !!req.session?.userId
    });
  } catch (err) {
    console.error("render failed:", err);
    res.status(500).send("render error");
  }
}