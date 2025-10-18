# Features Specification – UGC Marketplace MVP

## 1. User Registration & Authentication

### User story

As a new user (brand or influencer), I want to create an account so that I can
access the platform’s features.

### Acceptance criteria

- [ ] User can sign up via email/password.
- [ ] User can log in and log out securely.
- [ ] Password reset flow is implemented.
- [ ] OAuth login (Google) is supported.
- [ ] Role selection (Brand / Influencer) is required on first login.

### Example data/flows

**Input:**

- Email: `jane@brand.com`
- Password: `********`
- Role: `Brand`

**Expected output:**

- Account created.
- Redirect to onboarding dashboard for selected role.

### Constraints

- Must be GDPR-compliant (user consent, data deletion).
- Authentication tokens must expire automatically.
- Backend validation required for all inputs.

### Performance or UX targets

- Login/signup flow < 3 steps.
- Session establishment < 300 ms.

---

## 2. Brand – Create UGC Brief / Campaign

### User story

As a brand, I want to post a UGC campaign so that influencers can apply with
their proposals.

### Acceptance criteria

- [ ] Form allows input of title, description, content type, deliverables,
  budget, deadline.
- [ ] Brands can upload reference material (optional).
- [ ] Campaign status (Draft / Live / Closed) is displayed.
- [ ] Campaign visible only to influencers when status is Live.

### Example data/flows

**Input:**

- Title: “UGC Reel for Vegan Skincare Product”
- Format: `Instagram Reel`
- Budget: `€250`
- Deadline: `2025-11-15`

**Expected output:**

- Campaign visible in influencer marketplace feed.
- Applications open.

### Constraints

- Budget must be numeric and > 0.
- Deadline must be a future date.
- File upload max. 10 MB per file.

### Performance or UX targets

- Campaign creation form < 2 min to complete.
- Campaign listing visible < 200 ms after submission.

---

## 3. Influencer – Browse & Apply to Campaigns

### User story

As an influencer, I want to browse available campaigns and apply with my
proposal so that I can win paid collaborations.

### Acceptance criteria

- [ ] Influencer can filter campaigns by budget, category, platform, deadline.
- [ ] Application form allows short text pitch and optional portfolio link.
- [ ] Influencer can propose a price (if not fixed).
- [ ] Application confirmation email is sent.

### Example data/flows

**Input:**

- Campaign ID: `1234`
- Pitch: “I create authentic skincare reels with 20k reach.”
- Price: `€220`

**Expected output:**

- Application stored and visible to brand.
- Influencer notified about successful submission.

### Constraints

- Influencer must have completed their profile before applying.
- Cannot apply to expired campaigns.

### Performance or UX targets

- Application form submission < 500 ms.
- Campaign search results load < 300 ms.

---

## 4. Brand – Review Applications & Select Influencers

### User story

As a brand, I want to review all influencer applications so that I can select
the best match for my campaign.

### Acceptance criteria

- [ ] Applications are listed with profile info (followers, engagement,
  platform, pitch, price).
- [ ] Brand can shortlist, reject, or accept applications.
- [ ] Accepting triggers contract/payment workflow.
- [ ] Rejected applicants receive an automated notification.

### Example data/flows

**Input:**

- Application ID: `9876`
- Action: “Accept”

**Expected output:**

- Influencer status changes to “Accepted”.
- Payment request issued to brand.

### Constraints

- Only active campaigns can accept applications.
- Selection is irreversible after payment initiation.

### Performance or UX targets

- Application list loads < 400 ms.
- Action confirmation (accept/reject) < 1 s.

---

## 5. Messaging & Collaboration

### User story

As a brand or influencer, I want to exchange messages so that I can clarify
campaign details.

### Acceptance criteria

- [ ] 1:1 chat available after application submission.
- [ ] Messages stored securely and delivered in real time.
- [ ] Push/email notifications for new messages.
- [ ] Message history is accessible post-project.

### Example data/flows

**Input:**

- Sender: `Brand`
- Message: “Please deliver 2 draft reels by next week.”

**Expected output:**

- Message appears instantly in recipient’s inbox.
- Email notification triggered.

### Constraints

- No file uploads > 20 MB.
- Offensive content detection enabled.

### Performance or UX targets

- Message delivery latency < 500 ms.
- Chat UI responsive < 100 ms per action.

---

## 6. Payment & Escrow

### User story

As a brand, I want to pay securely through the platform so that the influencer
is paid only after delivery.

### Acceptance criteria

- [ ] Payment handled via integrated gateway (e.g., Stripe).
- [ ] Escrow holds funds until content approval.
- [ ] Refund mechanism available for disputes.
- [ ] Payout initiated automatically upon approval.

### Example data/flows

**Input:**

- Campaign ID: `1234`
- Payment: `€250`

**Expected output:**

- Funds debited from brand and held in escrow.
- Paid out to influencer after brand approval.

### Constraints

- Must comply with EU PSD2 regulations.
- Payout currency: EUR.

### Performance or UX targets

- Payment flow < 2 min end-to-end.
- Escrow release < 24 h after approval.

---

## 7. Content Delivery & Approval

### User story

As an influencer, I want to upload final content so that the brand can review
and approve it.

### Acceptance criteria

- [ ] Upload supports video, image, or text files.
- [ ] Brand can approve or request revisions.
- [ ] Once approved, payment is triggered.
- [ ] Content stored and accessible in project archive.

### Example data/flows

**Input:**

- File: `reel.mp4` (20 MB)
- Status: `Delivered`

**Expected output:**

- Brand receives notification.
- Approval workflow activated.

### Constraints

- Max upload size: 200 MB.
- File types: .mp4, .jpg, .png, .pdf.

### Performance or UX targets

- Upload time < 60 s for 200 MB.
- Approval/rejection action < 2 clicks.

---

## 8. Admin Panel

### User story

As a platform admin, I want to manage users, campaigns, and payments so that I
can maintain a secure and stable environment.

### Acceptance criteria

- [ ] Admin can view, suspend, or delete user accounts.
- [ ] Campaign moderation dashboard available.
- [ ] Payment transactions visible with status.
- [ ] Support/dispute tickets tracked.

### Example data/flows

**Input:**

- User ID: `u_5678`
- Action: `Suspend`

**Expected output:**

- Account status changed to “Suspended.”
- User notified via email.

### Constraints

- Admin access restricted to internal roles.
- All actions logged with timestamps.

### Performance or UX targets

- Dashboard load time < 500 ms.
- Action execution < 1 s.

---
