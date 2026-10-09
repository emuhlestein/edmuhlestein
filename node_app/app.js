import express from "express";

const app = express();
const port = Number(process.env.PORT || 3000);

app.get("/", (_req, res) => {
  res.type("html").send("<h1>Control</h1><p>Express is running.</p>");
});

app.get("/health", (_req, res) => {
  res.json({ status: "ok", service: "control" });
});

app.listen(port, "0.0.0.0", () => {
  console.log(`control listening on ${port}`);
});
