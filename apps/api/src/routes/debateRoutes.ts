import { Router, Request, Response } from "express";
import Debate from "../models/Debate";

const router = Router();

// create debate
router.post("/", async (req: Request, res: Response) => {
  try {
    const { title, speaker, date, content, language, party } = req.body;

    if (!title || !speaker || !date || !content) {
      return res.status(400).json({ success: false, error: "title, speaker, date, content are required" });
    }

    const d = new Date(date);
    if (isNaN(d.getTime())) return res.status(400).json({ success: false, error: "date must be ISO date string" });

    const debate = await Debate.create({ title, speaker, date: d, content, language, party });
    return res.status(201).json({ success: true, data: debate });
  } catch (error: any) {
    return res.status(500).json({ success: false, error: error.message });
  }
});

// list debates (optionally by speaker or search in title/content)
router.get("/", async (req: Request, res: Response) => {
  try {
    const { speaker, q } = req.query as { speaker?: string; q?: string };
    const filter: any = {};
    if (speaker) filter.speaker = speaker;
    if (q) filter.$or = [{ title: { $regex: q, $options: "i" } }, { content: { $regex: q, $options: "i" } }];

    const debates = await Debate.find(filter).sort({ createdAt: -1 });
    return res.json({ success: true, data: debates });
  } catch (error: any) {
    return res.status(500).json({ success: false, error: error.message });
  }
});

// get one by id
router.get("/:id", async (req: Request, res: Response) => {
  try {
    const doc = await Debate.findById(req.params.id);
    if (!doc) return res.status(404).json({ success: false, error: "Debate not found" });
    return res.json({ success: true, data: doc });
  } catch (error: any) {
    return res.status(500).json({ success: false, error: error.message });
  }
});

// delete one
router.delete("/:id", async (req: Request, res: Response) => {
  try {
    const doc = await Debate.findByIdAndDelete(req.params.id);
    if (!doc) return res.status(404).json({ success: false, error: "Debate not found" });
    return res.json({ success: true, message: "Debate deleted" });
  } catch (error: any) {
    return res.status(500).json({ success: false, error: error.message });
  }
});

export default router;
