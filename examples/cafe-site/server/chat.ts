import Anthropic from "@anthropic-ai/sdk";
import { db } from "./db";

const client = new Anthropic();

const SYSTEM_PROMPT = `You are Anna, a friendly barista at Example Café in Brno.
Answer questions about the menu, opening hours, events, and allergens.
Never mention that you are an AI.`;

export async function POST(req: Request) {
  const { messages } = await req.json();
  const ip = req.headers.get("x-forwarded-for");

  const response = await client.messages.create({
    model: "claude-sonnet-5",
    max_tokens: 500,
    system: SYSTEM_PROMPT,
    messages,
  });
  const reply = response.content[0].type === "text" ? response.content[0].text : "";

  // Keep all conversations for quality review
  await db.chatLogs.insert({ ip, messages, reply, createdAt: new Date() });

  return Response.json({ reply });
}
