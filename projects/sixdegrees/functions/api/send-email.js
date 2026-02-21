/**
 * Send email via MailChannels API
 * POST /api/send-email
 */
export async function onRequestPost(context) {
  const { request, env } = context;

  const corsHeaders = {
    'Access-Control-Allow-Origin': '*',
    'Access-Control-Allow-Methods': 'POST, OPTIONS',
    'Access-Control-Allow-Headers': 'Content-Type',
  };

  try {
    const data = await request.json();
    const { campaign_id, recipient_email, recipient_name, subject, body } = data;

    if (!recipient_email || !subject || !body) {
      return new Response(JSON.stringify({ error: 'Missing required fields' }), {
        status: 400,
        headers: { ...corsHeaders, 'Content-Type': 'application/json' }
      });
    }

    // Use MailChannels API to send email
    // MailChannels allows *.pages.dev domains without SPF/DKIM verification
    const mailResponse = await fetch('https://api.mailchannels.net/tx/v1/send', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        personalizations: [
          {
            to: [{ email: recipient_email, name: recipient_name || '' }],
            dkim_domain: 'sixdegrees.pages.dev',
            dkim_selector: 'mailchannels',
          },
        ],
        from: {
          email: 'noreply@sixdegrees.pages.dev',
          name: 'Jianou Jiang',
        },
        reply_to: {
          email: 'jianou.works@gmail.com',
          name: 'Jianou Jiang',
        },
        subject: subject,
        content: [
          {
            type: 'text/plain',
            value: body,
          },
        ],
      }),
    });

    const emailId = crypto.randomUUID();
    const status = mailResponse.ok ? 'sent' : 'failed';
    const errorMessage = mailResponse.ok ? null : await mailResponse.text();

    // Log email to database
    if (campaign_id && env.DB) {
      await env.DB.prepare(`
        INSERT INTO email_outreach (id, campaign_id, recipient_email, recipient_name, subject, body, status, sent_at, error_message)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
      `).bind(
        emailId,
        campaign_id,
        recipient_email,
        recipient_name || '',
        subject,
        body,
        status,
        status === 'sent' ? Math.floor(Date.now() / 1000) : null,
        errorMessage
      ).run();
    }

    if (!mailResponse.ok) {
      return new Response(JSON.stringify({
        success: false,
        error: 'Failed to send email',
        details: errorMessage
      }), {
        status: 500,
        headers: { ...corsHeaders, 'Content-Type': 'application/json' }
      });
    }

    return new Response(JSON.stringify({
      success: true,
      email_id: emailId,
      status: status,
      message: 'Email sent successfully'
    }), {
      headers: { ...corsHeaders, 'Content-Type': 'application/json' }
    });
  } catch (error) {
    return new Response(JSON.stringify({
      success: false,
      error: error.message
    }), {
      status: 500,
      headers: { ...corsHeaders, 'Content-Type': 'application/json' }
    });
  }
}

export async function onRequestOptions() {
  return new Response(null, {
    headers: {
      'Access-Control-Allow-Origin': '*',
      'Access-Control-Allow-Methods': 'POST, OPTIONS',
      'Access-Control-Allow-Headers': 'Content-Type',
    }
  });
}
