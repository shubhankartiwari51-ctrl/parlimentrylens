import mongoose, { Schema, Document, Model } from "mongoose";

export interface ISpeaker extends Document {
  name: string;
  party?: string;
  constituency?: string;
}

const SpeakerSchema = new Schema<ISpeaker>(
  {
    name: { type: String, required: true, trim: true },
    party: { type: String, trim: true },
    constituency: { type: String, trim: true },
  },
  { timestamps: true }
);

const Speaker: Model<ISpeaker> = mongoose.models.Speaker || mongoose.model<ISpeaker>("Speaker", SpeakerSchema);
export default Speaker;
