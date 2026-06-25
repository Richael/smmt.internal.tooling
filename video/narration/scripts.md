# Narration — The Twelve Compounding Closed Loops

Voiceover script. One block per section. Written for text-to-speech: symbols expanded, no code.
Default voice: macOS `say` voice **Ava** (Enhanced) at rate 180 — see `build-narration.sh`.
Each `## ` header maps 1:1 to a Remotion section and a YouTube chapter.

---

## Intro (25s)

Here's an idea that quietly runs a whole marketing operation: the closed loop. A closed loop means data leaves one system, gets acted on in another, and then returns — as a converted customer, or as a sharper signal. So every cycle makes the next one better. In this architecture, four systems do the work: Shopify, Klaviyo, Meta with Instagram, and Amazon. And across them, twelve loops compound. Let's walk through all twelve.

## Loop 1 — Attribution then Segment then Re-seed (32s)

Loop one is the engine the others feed. Every time an order is paid, Shopify fires a webhook. We read the customer's journey, find the campaign that brought them in, and tag them — acquired via Meta, this campaign. The high-value buyers become a segment in Klaviyo, which syncs to Meta as a custom audience. Meta builds a lookalike from it, and we run that on Facebook and Instagram. New shoppers arrive, carrying their own tracking tags — and the loop closes. Each cycle, the seed gets cleaner and the lookalike gets better.

## Loop 2 — Purchase, Post-purchase, Repurchase (24s)

Loop two turns one sale into the next. A paid order in Shopify lands in Klaviyo as a Placed Order event. That kicks off a flow: thank you, then cross-sell, then a replenishment reminder timed to the product. The email carries a unique discount code. When it's redeemed, that's a new paid order — and we're back at the start. Retention, on a timer.

## Loop 3 — Abandoned-checkout multi-channel recovery (26s)

Loop three chases the cart two ways at once. When a checkout starts but doesn't finish, Klaviyo runs an abandoned-cart flow over email and S-M-S, while the same shopper drops into a Meta audience for retargeting on Facebook and Instagram. If they come back and buy, the order closes the loop — and they exit both the flow and the ad audience on the next sync, so you stop paying to chase someone who already converted.

## Loop 4 — Lead-gen nurture, Meta to customer (30s)

Loop four is the business-to-business workhorse. Someone fills out an Instant Form on Instagram or Facebook. Klaviyo's native lead sync drops them onto a list in real time, and a nurture flow begins. Days or weeks later they make their first purchase in Shopify — and loop one attributes it back to the exact form and campaign. The converter then feeds the high-value seed. A lead becomes a customer becomes better targeting.

## Loop 5 — Server-side conversion optimization (28s)

Loop five feeds Meta's optimizer clean signal. Shopify's Facebook and Instagram channel sends each purchase server-side through the Conversions A-P-I, while the browser pixel sends the same event. Both carry one shared event I-D, so Meta counts it once. Better signal means smarter delivery, which means more conversions — which means more signal. One warning: if the two senders mint different event I-Ds, Meta double-counts. Pick one authoritative sender and verify it.

## Loop 6 — Suppression and exclusion hygiene (24s)

Loop six stops you from paying to advertise to people who already bought. Recent purchasers and existing customers become a Meta exclusion audience, and your prospecting and lookalike ad sets exclude it. New customers convert, enter Shopify and Klaviyo, and join the suppression list on the next cycle. Spend keeps concentrating on genuinely new people.

## Loop 7 — Predictive value tiering (26s)

Loop seven lets Klaviyo's machine learning sort your customers. It predicts lifetime value, churn risk, and the next order date. High-value profiles become a lookalike seed and enter a V-I-P flow. High-churn-risk profiles get a win-back flow and retargeting. Then the outcome — a purchase, or a lapse — updates the prediction, and the customer re-tiers. The model learns from what actually happens.

## Loop 8 — Consent and identity propagation (26s)

Loop eight is the compliance loop, and it's not optional in Europe or California. When someone unsubscribes or opts out, that consent event removes them from every Meta audience they were in, flags them in Shopify, and suppresses them in Klaviyo. When an email or phone number changes, the profile updates and re-syncs. Consent state stays consistent everywhere — automatically, in near real time.

## Loop 9 — Off-Amazon demand to Amazon conversion (30s)

Loop nine connects your ads to your Amazon sales. There's no pixel on Amazon, so we wrap every destination link in an Amazon Attribution tag. Amazon then measures the clicks, the detail-page views, the add-to-carts, and the purchases — including new-to-brand — over a fourteen-day window. We pull those reports, mirror the conversions back to Meta as offline events, and shift spend toward what actually sells. The Brand Referral Bonus even returns about ten percent of those sales.

## Loop 10 — Cross-platform syndication and lookalike fan-out (28s)

Loop ten is the reuse engine. SMMT holds one canonical first-party audience — normalized and hashed once. We fan it out to a Meta custom audience and an Amazon advertiser audience at the same time, and let each platform build its own lookalikes. Converters return — on Shopify where we can join them by email, or on Amazon where we measure them as signal. One audience, every platform, growing each cycle.

## Loop 11 — Amazon-native retention and win-back (26s)

Loop eleven retains customers you're not allowed to email. Amazon gives back no marketing email, so retention happens entirely on Amazon. Repeat products go into Subscribe and Save for recurring revenue. Amazon-built segments — repeat buyers, high spenders, cart abandoners, at-risk customers — each get a percentage-off promotion. A repurchase re-enrolls them into those segments. The loop closes inside Amazon's walls.

## Loop 12 — Unified profile and insight enrichment (28s)

Loop twelve makes the whole system smarter. SMMT ingests everything — Shopify orders, Klaviyo profiles and predictions, Meta delivery, and Amazon's aggregate signals — and resolves identity where it can. Amazon's clean room joins first-party data with Amazon behavior to reveal cross-channel journeys, like a Meta impression leading to an Amazon purchase. Those insights sharpen the segments that feed loops one, seven, and ten. Better targeting lifts the very signal that flows back in.

## Outro (20s)

So that's twelve loops — but really it's one idea, twelve times. Every loop shares the same audience and the same identity spine: email as the universal key, flowing outbound to the platforms, never extracted back. The reuse engine ties them together, so the whole system is worth far more than any single loop. Build the spine once, and every loop compounds on top of it.
