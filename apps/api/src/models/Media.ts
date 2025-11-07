import mongoose, { Schema, Document, Model } from "mongoose";

export interface IMedia extends Document {
  title: string;
  url: string;
  type: "video" | "audio" | "youtube";
  uploaded_at: Date;
}

const MediaSchema = new Schema<IMedia>(
  {
    title: { type: String, required: true, trim: true },
    url: { type: String, required: true, trim: true },
    type: { type: String, enum: ["video", "audio", "youtube"], required: true },
    uploaded_at: { type: Date, default: Date.now },
  },
  { timestamps: true }
);

const Media: Model<IMedia> = mongoose.models.Media || mongoose.model<IMedia>("Media", MediaSchema);
export default Media;
