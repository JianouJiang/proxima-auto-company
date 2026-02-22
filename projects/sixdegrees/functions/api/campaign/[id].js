/**
 * GET /api/campaign/:id
 *
 * Fetch campaign details, email history, and live status.
 *
 * Response:
 * {
 *   campaign_id: string,
 *   target_name: string,
 *   target_company: string,
 *   status: string,
 *   strategy: string,
 *   selected_path: object,
 *   emails: array,
 *   created_at: number,
 *   last_updated_at: number
 * }
 */

export async function onRequestGet(context) {
  const { params, env } = context;
  const campaignId = params.id;

  try {
    if (!campaignId) {
      return new Response(
        JSON.stringify({ success: false, error: 'Campaign ID required' }),
        { status: 400, headers: { 'Content-Type': 'application/json' } }
      );
    }

    // Fetch campaign
    const campaign = await env.DB.prepare('SELECT * FROM campaigns WHERE id = ?')
      .bind(campaignId)
      .first();

    if (!campaign) {
      return new Response(
        JSON.stringify({ success: false, error: 'Campaign not found' }),
        { status: 404, headers: { 'Content-Type': 'application/json' } }
      );
    }

    // Parse results JSON
    let results = {};
    try {
      results = JSON.parse(campaign.results || '{}');
    } catch (e) {
      results = {};
    }

    // Fetch email outreach history
    const emailsQuery = await env.DB.prepare(
      'SELECT * FROM email_outreach WHERE campaign_id = ? ORDER BY created_at ASC'
    )
      .bind(campaignId)
      .all();

    const emails = emailsQuery.results.map((email) => ({
      email_id: email.id,
      recipient_email: email.recipient_email,
      recipient_name: email.recipient_name,
      subject: email.subject,
      body: email.body,
      status: email.status,
      sent_at: email.sent_at,
      error_message: email.error_message,
    }));

    // Build 6-degree chain from results
    const selectedPath = results.selected_path || {
      degree: 3,
      confidence: 0.75,
      chain: [
        { name: campaign.cv?.split('.')[0] || 'You', role: 'Sender', status: 'sender' },
        { name: 'Connection 1', role: 'First degree', status: 'draft' },
        { name: 'Connection 2', role: 'Second degree', status: 'draft' },
        { name: campaign.target_name, role: 'Target', status: 'draft' },
      ],
    };

    const response = {
      campaign_id: campaign.id,
      target_name: campaign.target_name,
      target_company: campaign.target_role,
      user_name: campaign.cv?.split('.')[0] || 'User',
      user_email: campaign.email,
      status: campaign.status,
      strategy: results.strategy || results.target_analysis || 'Strategy pending...',
      selected_path: selectedPath,
      emails,
      created_at: campaign.created_at,
      last_updated_at: campaign.updated_at,
    };

    return new Response(JSON.stringify(response), {
      status: 200,
      headers: { 'Content-Type': 'application/json' },
    });
  } catch (error) {
    console.error('Error fetching campaign:', error);
    return new Response(
      JSON.stringify({
        success: false,
        error: error.message || 'Internal server error',
      }),
      { status: 500, headers: { 'Content-Type': 'application/json' } }
    );
  }
}
