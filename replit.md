# Mail & Link Generator

Kullanıcıların e-posta gönderip benzersiz bir capture linki oluşturmasını sağlayan, linke tıklandığında eski/yeni şifre toplayan web uygulaması.

## Run & Operate

- `pnpm --filter @workspace/api-server run dev` — run the API server (port 8080)
- `pnpm --filter @workspace/capture-page run dev` — run the frontend (port 18619)
- `pnpm run typecheck` — full typecheck across all packages
- `pnpm run build` — typecheck + build all packages
- `pnpm --filter @workspace/api-spec run codegen` — regenerate API hooks and Zod schemas from the OpenAPI spec
- `pnpm --filter @workspace/db run push` — push DB schema changes (dev only)
- Required env: `DATABASE_URL` — Postgres connection string

## Stack

- pnpm workspaces, Node.js 24, TypeScript 5.9
- API: Express 5 + Nodemailer (Gmail SMTP)
- DB: PostgreSQL + Drizzle ORM (`sessions` table)
- Validation: Zod (`zod/v4`), `drizzle-zod`
- Frontend: React + Vite + TailwindCSS + shadcn/ui
- API codegen: Orval (from OpenAPI spec)
- Build: esbuild (CJS bundle)

## Where things live

- OpenAPI spec: `lib/api-spec/openapi.yaml`
- DB schema: `lib/db/src/schema/sessions.ts`
- API routes: `artifacts/api-server/src/routes/sessions.ts`
- Frontend (capture page): `artifacts/capture-page/src/pages/capture.tsx`
- Kivy Android app: `kivy_app/main.py`
- Kivy setup guide: `kivy_app/KURULUM.md`

## Architecture decisions

- Sessions stored in PostgreSQL: token → {senderEmail, senderPassword, resultEmail, messageSubject, used}
- The Kivy Android app calls POST /api/sessions to register a token, then sends email via Python smtplib
- Email sending (result forwarding) happens on the backend using the stored sender credentials
- Gmail App Password required (not regular Gmail password)
- `used` flag prevents replay attacks (token can only be submitted once)

## Product

- Kullanıcı Kivy uygulamasını açar, 5 alanı doldurur
- Butona basılır: backend'de capture oturumu oluşturulur (benzersiz token), alıcıya e-posta gönderilir
- Alıcı linke tıklar: "Eski Şifre" ve "Yeni Şifre" formu açılır
- Form gönderilir: bilgiler Sonuç E-postası'na iletilir

## User preferences

_Populate as you build — explicit user instructions worth remembering across sessions._

## Gotchas

- `lib/api-zod/src/index.ts` must only export from `./generated/api` (not `./generated/types` — codegen conflict)
- After running codegen, manually verify `lib/api-zod/src/index.ts` only has `export * from "./generated/api";`
- Gmail App Password (16 char) required — normal Gmail password won't work
- After deploying, update `BASE_URL` in `kivy_app/main.py` with the production domain

## Pointers

- See the `pnpm-workspace` skill for workspace structure, TypeScript setup, and package details
