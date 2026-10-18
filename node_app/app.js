import express from "express";
import nunjucks from "nunjucks";
import { indexRouter } from "./routes/index.js";
import { healthRouter } from "./routes/health.js";

const app = express();
const port = Number(process.env.PORT || 3000);

nunjucks.configure("views", {
  autoescape: true,
  express: app,
  noCache: true,
});
app.set("view engine", "html");
app.use("/static", express.static("public"));

app.use("/", indexRouter);
app.use("/", healthRouter);

app.listen(port, "0.0.0.0", () => {
  console.log(`listening on ${port}`);
});