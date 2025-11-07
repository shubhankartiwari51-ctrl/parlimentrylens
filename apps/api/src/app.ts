import express, { Request, Response, NextFunction } from "express";
import cors from "cors";
import debateRoutes from "./routes/debateRoutes";
import mediaRoutes from "./routes/mediaRoutes";
import aiRoutes from "./routes/aiRoutes";
const app = express();

// middlewares
app.use(cors());
app.use(express.json({ limit: "2mb" }));
app.use(express.urlencoded({ extended: true }));

// health
app.get("/", (_req, res) => res.send("API is running..."));

// routes
app.use("/api/debates", debateRoutes);
app.use("/api/media", mediaRoutes);
app.use("/api/ai", aiRoutes);
// 404
app.use((req, res) => {
  res.status(404).json({ success: false, error: `Route not found: ${req.method} ${req.originalUrl}` });
});

// error handler
app.use((err: any, _req: Request, res: Response, _next: NextFunction) => {
  console.error("Unhandled error:", err);
  const status = err.status || 500;
  res.status(status).json({ success: false, error: err.message || "Internal Server Error" });
});

export default app;
