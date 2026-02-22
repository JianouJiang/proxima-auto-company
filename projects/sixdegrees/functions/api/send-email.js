/**
 * SixDegrees Email API — Cloudflare Pages Function
 *
 * NOTE: Email sending has been moved to local Gmail SMTP scripts.
 * Cloudflare Pages Functions cannot do raw SMTP connections.
 *
 * Use the local scripts instead:
 *   node send-gmail.js --to "email" --subject "subj" --body "text"
 *   node auto-outreach.js --degree 1
 *
 * This endpoint now returns instructions for the correct approach.
 */

const corsHeaders = {
  'Access-Control-Allow-Origin': '*',
  'Access-Control-Allow-Methods': 'POST, OPTIONS',
  'Access-Control-Allow-Headers': 'Content-Type',
};

export async function onRequestPost(context) {
  return new Response(JSON.stringify({
    success: false,
    message: 'Email sending has moved from MailChannels to Gmail SMTP.',
    instructions: {
      single_email: 'Use the local script: node send-gmail.js --to "email" --subject "subj" --body "text"',
      auto_outreach: 'Use the outreach engine: node auto-outreach.js --degree 1',
      check_replies: 'Check for replies: node auto-outreach.js --check-replies',
      why: 'Cloudflare Pages Functions cannot make raw SMTP connections. Email now sends directly via Gmail SMTP using nodemailer from a local Node.js script.',
      gmail_from: 'jianou.works@gmail.com',
    },
  }), {
    status: 200,
    headers: { ...corsHeaders, 'Content-Type': 'application/json' },
  });
}

export async function onRequestGet() {
  return new Response(JSON.stringify({
    service: 'SixDegrees Email',
    status: 'redirected',
    message: 'Email sending now works via local Gmail SMTP scripts instead of this web API. See instructions.',
    scripts: {
      'send-gmail.js': 'Send a single email via Gmail SMTP',
      'auto-outreach.js': 'Automatic 6-degree outreach engine with reply tracking',
    },
  }), {
    headers: { ...corsHeaders, 'Content-Type': 'application/json' },
  });
}

export async function onRequestOptions() {
  return new Response(null, {
    headers: corsHeaders,
  });
}
