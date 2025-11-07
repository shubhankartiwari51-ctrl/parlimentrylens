import mongoose, { Schema, Document, Model } from "mongoose";

export interface IDebate extends Document {
  title: string;
  speaker: string;
  date: Date;
  content: string;
  language?: string;
  party?: string;
}

const DebateSchema = new Schema<IDebate>(
  {
    title: { type: String, required: true, trim: true },
    speaker: { type: String, required: true, trim: true },
    date: { type: Date, required: true },
    content: { type: String, required: true, trim: true },
    language: { type: String, default: "EN" },
    party: { type: String },
  },
  { timestamps: true }
);

const Debate: Model<IDebate> = mongoose.models.Debate || mongoose.model<IDebate>("Debate", DebateSchema);
export default Debate;
