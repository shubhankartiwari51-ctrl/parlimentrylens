import express, { Request, Response } from "express";
import axios from "axios";

const router = express.Router();
const AI_BASE = process.env.AI_BASE || "http://ai:8001";

router.post("/analyze", async (req: Request, res: Response) => {
  try {
    const { text } = req.body;
    const response = await axios.post(`${AI_BASE}/analyze`, { text });
    res.status(200).json({ success: true, data: response.data });
  } catch (error: any) {
    res.status(500).json({ success: false, error: error.message });
  }
});

export default router;
