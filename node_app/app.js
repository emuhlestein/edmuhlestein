import express from "express";
import nunjucks from "nunjucks";
import { indexRouter } from "./routes/index.js";
import { healthRouter } from "./routes/health.js";
import { therapistsRouter } from "./routes/therapists.js";
import { studyRouter } from "./routes/study.js";
import { aboutRouter } from "./routes/about.js";
import { projectRouter } from "./routes/project.js";
import { gameRouter } from "./routes/game.js";

const app = express();
const port = Number(process.env.PORT || 3000);

nunjucks.configure("views", {
  autoescape: true,
  express: app,
  noCache: true,
});
app.set("view engine", "html");
app.use("/static", express.static("static"));

app.use("/", indexRouter);
app.use("/", healthRouter);
app.use("/therapists", therapistsRouter);
app.use("/study", studyRouter);
app.use("/about", aboutRouter);
app.use("/project", projectRouter);
app.use("/game", gameRouter);

app.listen(port, "0.0.0.0", () => {
  console.log(`listening on ${port}`);
});