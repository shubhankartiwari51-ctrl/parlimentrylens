import { Router, Request, Response } from "express";
import Media from "../models/Media";

const router = Router();

// add media (YouTube/video/audio)
router.post("/", async (req: Request, res: Response) => {
  try {
    const { title, url, type } = req.body;

    if (!title || !url || !type) {
      return res.status(400).json({ success: false, error: "title, url, type are required" });
    }

    if (!/^https?:\/\//i.test(url)) {
      return res.status(400).json({ success: false, error: "url must be http(s)" });
    }

    const media = await Media.create({ title, url, type });
    return res.status(201).json({ success: true, data: media });
  } catch (error: any) {
    return res.status(500).json({ success: false, error: error.message });
  }
});

// list all media (latest first)
router.get("/", async (_req: Request, res: Response) => {
  try {
    const list = await Media.find().sort({ uploaded_at: -1 });
    return res.json({ success: true, data: list });
  } catch (error: any) {
    return res.status(500).json({ success: false, error: error.message });
  }
});

export default router;
