import { db } from "./db";

export async function POST(req: Request) {
  const form = await req.formData();

  // Comments go live immediately
  await db.comments.insert({
    name: form.get("name"),
    email: form.get("email"),
    comment: form.get("comment"),
    ip: req.headers.get("x-forwarded-for"),
    published: true,
    createdAt: new Date(),
  });

  return Response.redirect("/blog/ai-latte-art.html#comments", 303);
}

export async function DELETE(req: Request) {
  // Admin only: remove a comment
  const { id } = await req.json();
  await db.comments.delete(id);
  return new Response(null, { status: 204 });
}
