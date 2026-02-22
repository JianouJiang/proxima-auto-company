/**
 * POST /api/send
 *
 * Send an email for a campaign. Records email in DB and triggers Gmail SMTP send.
 *
 * Request body:
 * {
 *   campaign_id: string,
 *   email_id: string (optional),
 *   to: string,
 *   subject: string,
 *   body: string,
 *   recipient_name: string
 * }
 *
 * Response:
 * {
 *   success: boolean,
 *   email_id: string,
 *   message: string
 * }
 */

const corsHeaders = {
  'Access-Control-Allow-Origin': '*',
  'Access-Control-Allow-Methods': 'POST, OPTIONS',
  'Access-Control-Allow-Headers': 'Content-Type',
};

export async function onRequestPost(context) {
  const { request, env } = context;

  try {
    const body = await request.json();
    const { campaign_id, email_id, to, subject, body: emailBody, recipient_name } = body;

    if (!campaign_id) {
      return new Response(
        JSON.stringify({ success: false, error: 'campaign_id required' }),
        { status: 400, headers: { ...corsHeaders, 'Content-Type': 'application/json' } }
      );
    }

    // Verify campaign exists
    const campaign = await env.DB.prepare('SELECT * FROM campaigns WHERE id = ?')
      .bind(campaign_id)
      .first();

    if (!campaign) {
      return new Response(
        JSON.stringify({ success: false, error: 'Campaign not found' }),
        { status: 404, headers: { ...corsHeaders, 'Content-Type': 'application/json' } }
      );
    }

    let emailRecord;

    // Check if sending existing draft or creating new
    if (email_id) {
      emailRecord = await env.DB.prepare('SELECT * FROM email_outreach WHERE id = ?')
        .bind(email_id)
        .first();

      if (!emailRecord) {
        return new Response(
          JSON.stringify({ success: false, error: 'Email not found' }),
          { status: 404, headers: { ...corsHeaders, 'Content-Type': 'application/json' } }
        );
      }
    } else {
      // Create new email record
      const newEmailId = `email_${Date.now()}_${Math.random().toString(36).substr(2, 9)}`;

      await env.DB.prepare(`
        INSERT INTO email_outreach (
          id, campaign_id, recipient_email, recipient_name, subject, body, status
        ) VALUES (?, ?, ?, ?, ?, ?, ?)
      `)
        .bind(newEmailId, campaign_id, to, recipient_name, subject, emailBody, 'pending')
        .run();

      emailRecord = {
        id: newEmailId,
        recipient_email: to,
        recipient_name,
        subject,
        body: emailBody,
      };
    }

    // Mark email as queued
    await env.DB.prepare('UPDATE email_outreach SET status = ? WHERE id = ?')
      .bind('queued', emailRecord.id)
      .run();

    // NOTE: Actual email sending happens via local Gmail SMTP script
    // The user needs to run: node send-gmail.js --campaign-id [ID]
    // Or use the auto-outreach engine: node auto-outreach.js

    return new Response(
      JSON.stringify({
        success: true,
        email_id: emailRecord.id,
        status: 'queued',
        message: 'Email queued successfully. Run local Gmail SMTP script to send.',
        instructions: 'Use: node send-gmail.js --campaign-id ' + campaign_id,
      }),
      { status: 200, headers: { ...corsHeaders, 'Content-Type': 'application/json' } }
    );
  } catch (error) {
    console.error('Error in send API:', error);
    return new Response(
      JSON.stringify({
        success: false,
        error: error.message || 'Internal server error',
      }),
      { status: 500, headers: { ...corsHeaders, 'Content-Type': 'application/json' } }
    );
  }
}

export async function onRequestOptions() {
  return new Response(null, { headers: corsHeaders });
}
