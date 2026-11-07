import express from "express";
import session from "express-session";
import nunjucks from "nunjucks";
import { settings } from "./settings.js";
import { indexRouter } from "./routes/index.js";
import { healthRouter } from "./routes/health.js";
import { therapistsRouter } from "./routes/therapists.js";
import { studyRouter } from "./routes/study.js";
import { aboutRouter } from "./routes/about.js";
import { projectRouter } from "./routes/project.js";
import { gameRouter } from "./routes/game.js";
import { authRouter } from "./routes/auth.js";

const app = express();
const port = Number(process.env.PORT || 3000);
const isProduction = settings.nodeEnv === "production";

nunjucks.configure("views", {
  autoescape: true,
  express: app,
  noCache: !isProduction,
});

// Middleware
app.set("trust proxy", 1);   // trust the first proxy (nginx)

app.use(session({
  secret: settings.secretKey || "dev-secret-change-me",
  resave: false,
  saveUninitialized: false,
  cookie: {
    secure: isProduction,   // only send over HTTPS
    httpOnly: true,         // JavaScript cannot read it-for XSS
    sameSite: "lax"         // limited cross-site sending
  }
}));
app.use(express.json());                          // parses JSON bodies
app.use(express.urlencoded({ extended: true }));  // parses form bodies
app.set("view engine", "html"); // don't need to include .html when calling res.render(). html is the expect extension
app.use("/static", express.static("static"));

// Routes
app.use("/", indexRouter);
app.use("/", healthRouter);
app.use("/therapists", therapistsRouter);
app.use("/study", studyRouter);
app.use("/about", aboutRouter);
app.use("/project", projectRouter);
app.use("/game", gameRouter);
app.use("/auth", authRouter);

app.listen(port, "0.0.0.0", () => {
  console.log(`listening on ${port}`);
});