/**
 * ConnectPath AI Agent Worker
 * Cloudflare Worker that powers the AI agent connection service
 */

export default {
  async fetch(request, env) {
    const url = new URL(request.url);

    // CORS headers
    const corsHeaders = {
      'Access-Control-Allow-Origin': '*',
      'Access-Control-Allow-Methods': 'GET, POST, OPTIONS',
      'Access-Control-Allow-Headers': 'Content-Type',
    };

    if (request.method === 'OPTIONS') {
      return new Response(null, { headers: corsHeaders });
    }

    try {
      // Route handling
      if (url.pathname === '/api/campaigns' && request.method === 'POST') {
        return await handleCreateCampaign(request, env, corsHeaders);
      }

      if (url.pathname === '/api/dashboard' && request.method === 'GET') {
        return await handleDashboard(request, env, corsHeaders);
      }

      if (url.pathname === '/api/webhook/gumroad' && request.method === 'POST') {
        return await handleGumroadWebhook(request, env, corsHeaders);
      }

      if (url.pathname.startsWith('/api/campaign/') && request.method === 'GET') {
        const campaignId = url.pathname.split('/').pop();
        return await handleGetCampaign(campaignId, env, corsHeaders);
      }

      // Default: return not found
      return new Response('Not Found', { status: 404 });
    } catch (error) {
      return new Response(JSON.stringify({ error: error.message }), {
        status: 500,
        headers: { ...corsHeaders, 'Content-Type': 'application/json' }
      });
    }
  }
};

/**
 * Create a new campaign
 */
async function handleCreateCampaign(request, env, corsHeaders) {
  const data = await request.json();
  const { email, cv, target_name, target_role, motivation, plan } = data;

  // Validate input
  if (!email || !cv || !target_name || !motivation) {
    return new Response(JSON.stringify({ error: 'Missing required fields' }), {
      status: 400,
      headers: { ...corsHeaders, 'Content-Type': 'application/json' }
    });
  }

  const campaignId = generateId();

  // Get or create user
  let user = await env.DB.prepare('SELECT * FROM users WHERE email = ?').bind(email).first();

  if (!user) {
    const userId = generateId();
    await env.DB.prepare(
      'INSERT INTO users (id, email, credits_balance) VALUES (?, ?, ?)'
    ).bind(userId, email, 0).run();
    user = { id: userId, email, credits_balance: 0 };
  }

  // Create campaign
  await env.DB.prepare(`
    INSERT INTO campaigns (id, user_id, email, cv, target_name, target_role, motivation, status)
    VALUES (?, ?, ?, ?, ?, ?, ?, 'pending')
  `).bind(campaignId, user.id, email, cv, target_name, target_role || '', motivation).run();

  return new Response(JSON.stringify({
    success: true,
    campaign_id: campaignId,
    message: 'Campaign created. Complete payment to start AI agent.'
  }), {
    headers: { ...corsHeaders, 'Content-Type': 'application/json' }
  });
}

/**
 * Get dashboard data (credits + campaigns)
 */
async function handleDashboard(request, env, corsHeaders) {
  const url = new URL(request.url);
  const email = url.searchParams.get('email');

  if (!email) {
    return new Response(JSON.stringify({ error: 'Email required' }), {
      status: 400,
      headers: { ...corsHeaders, 'Content-Type': 'application/json' }
    });
  }

  const user = await env.DB.prepare('SELECT * FROM users WHERE email = ?').bind(email).first();

  if (!user) {
    return new Response(JSON.stringify({ credits: 0, campaigns: [] }), {
      headers: { ...corsHeaders, 'Content-Type': 'application/json' }
    });
  }

  const campaigns = await env.DB.prepare(
    'SELECT * FROM campaigns WHERE user_id = ? ORDER BY created_at DESC'
  ).bind(user.id).all();

  return new Response(JSON.stringify({
    credits: user.credits_balance,
    campaigns: campaigns.results.map(c => ({
      ...c,
      results: c.results ? JSON.parse(c.results) : null
    }))
  }), {
    headers: { ...corsHeaders, 'Content-Type': 'application/json' }
  });
}

/**
 * Gumroad webhook handler
 */
async function handleGumroadWebhook(request, env, corsHeaders) {
  const data = await request.formData();
  const email = data.get('email');
  const plan = data.get('plan') || 'starter';

  // Credit amounts per plan
  const creditPlans = {
    starter: 10,
    growth: 50,
    pro: 200,
    unlimited: 999999 // Effectively unlimited for 1 month
  };

  const creditsToAdd = creditPlans[plan] || 10;

  // Get user
  const user = await env.DB.prepare('SELECT * FROM users WHERE email = ?').bind(email).first();

  if (!user) {
    return new Response(JSON.stringify({ error: 'User not found' }), {
      status: 404,
      headers: { ...corsHeaders, 'Content-Type': 'application/json' }
    });
  }

  // Add credits
  await env.DB.prepare(
    'UPDATE users SET credits_balance = credits_balance + ?, updated_at = ? WHERE id = ?'
  ).bind(creditsToAdd, Math.floor(Date.now() / 1000), user.id).run();

  // Record transaction
  await env.DB.prepare(`
    INSERT INTO credit_transactions (id, user_id, amount, transaction_type, plan)
    VALUES (?, ?, ?, 'purchase', ?)
  `).bind(generateId(), user.id, creditsToAdd, plan).run();

  // Find pending campaigns and start processing
  const pendingCampaigns = await env.DB.prepare(
    'SELECT * FROM campaigns WHERE user_id = ? AND status = "pending" ORDER BY created_at ASC LIMIT 1'
  ).bind(user.id).all();

  if (pendingCampaigns.results.length > 0) {
    const campaign = pendingCampaigns.results[0];
    // Trigger agent processing (async)
    env.QUEUE.send({ type: 'process_campaign', campaign_id: campaign.id });
  }

  return new Response(JSON.stringify({ success: true }), {
    headers: { ...corsHeaders, 'Content-Type': 'application/json' }
  });
}

/**
 * Get single campaign details
 */
async function handleGetCampaign(campaignId, env, corsHeaders) {
  const campaign = await env.DB.prepare('SELECT * FROM campaigns WHERE id = ?').bind(campaignId).first();

  if (!campaign) {
    return new Response(JSON.stringify({ error: 'Campaign not found' }), {
      status: 404,
      headers: { ...corsHeaders, 'Content-Type': 'application/json' }
    });
  }

  const steps = await env.DB.prepare(
    'SELECT * FROM campaign_steps WHERE campaign_id = ? ORDER BY created_at ASC'
  ).bind(campaignId).all();

  return new Response(JSON.stringify({
    ...campaign,
    results: campaign.results ? JSON.parse(campaign.results) : null,
    steps: steps.results.map(s => ({
      ...s,
      result: s.result ? JSON.parse(s.result) : null
    }))
  }), {
    headers: { ...corsHeaders, 'Content-Type': 'application/json' }
  });
}

/**
 * Process campaign with AI agent (called from Queue)
 */
async function processCampaign(campaignId, env) {
  const campaign = await env.DB.prepare('SELECT * FROM campaigns WHERE id = ?').bind(campaignId).first();

  if (!campaign) return;

  // Update status to processing
  await env.DB.prepare('UPDATE campaigns SET status = "processing" WHERE id = ?').bind(campaignId).run();

  try {
    // Step 1: Research target person
    const researchStep = await createCampaignStep(
      campaignId,
      'research_target',
      `Research ${campaign.target_name}`,
      env
    );

    const targetResearch = await researchTargetPerson(campaign.target_name, campaign.target_role, env);
    await completeCampaignStep(researchStep.id, targetResearch, env);

    // Step 2: Find intermediaries
    const intermediariesStep = await createCampaignStep(
      campaignId,
      'find_intermediary',
      'Find connection intermediaries',
      env
    );

    const intermediaries = await findIntermediaries(campaign.cv, targetResearch, env);
    await completeCampaignStep(intermediariesStep.id, intermediaries, env);

    // Step 3: Draft outreach emails
    const draftStep = await createCampaignStep(
      campaignId,
      'draft_email',
      'Draft personalized outreach emails',
      env
    );

    const emailDrafts = await draftOutreachEmails(
      campaign.cv,
      campaign.motivation,
      targetResearch,
      intermediaries,
      env
    );
    await completeCampaignStep(draftStep.id, emailDrafts, env);

    // Calculate total credits used (3 steps)
    const creditsUsed = 3;

    // Deduct credits from user
    await env.DB.prepare(
      'UPDATE users SET credits_balance = credits_balance - ? WHERE id = ?'
    ).bind(creditsUsed, campaign.user_id).run();

    // Record usage transaction
    await env.DB.prepare(`
      INSERT INTO credit_transactions (id, user_id, amount, transaction_type, campaign_id)
      VALUES (?, ?, ?, 'usage', ?)
    `).bind(generateId(), campaign.user_id, -creditsUsed, campaignId).run();

    // Mark campaign as completed
    const results = {
      target_research: targetResearch,
      intermediaries: intermediaries,
      email_drafts: emailDrafts
    };

    await env.DB.prepare(`
      UPDATE campaigns SET status = 'completed', credits_used = ?, results = ?, updated_at = ?
      WHERE id = ?
    `).bind(creditsUsed, JSON.stringify(results), Math.floor(Date.now() / 1000), campaignId).run();

  } catch (error) {
    await env.DB.prepare(
      'UPDATE campaigns SET status = "failed", updated_at = ? WHERE id = ?'
    ).bind(Math.floor(Date.now() / 1000), campaignId).run();
  }
}

/**
 * AI Agent Functions
 */

async function researchTargetPerson(name, role, env) {
  const prompt = `Research this person: ${name}${role ? ` (${role})` : ''}

Find:
1. Professional background (education, career path)
2. Current role and company
3. Public interests and passions
4. Recent articles, interviews, or talks
5. Social media presence
6. Potential connection points (shared interests, mutual connections, common topics)

Return structured JSON.`;

  const response = await callClaude(prompt, env);
  return response;
}

async function findIntermediaries(userCV, targetResearch, env) {
  const prompt = `User CV: ${userCV}

Target research: ${JSON.stringify(targetResearch)}

Find 2-3 potential intermediaries who could connect the user to the target. Consider:
1. Shared industries or companies
2. Common educational backgrounds
3. Overlapping interests or networks
4. LinkedIn mutual connections (if available)
5. Professional communities or events

For each intermediary, provide:
- Name and role
- Why they're a good bridge
- How to find them
- Connection strength (weak/medium/strong)

Return structured JSON array.`;

  const response = await callClaude(prompt, env);
  return response;
}

async function draftOutreachEmails(userCV, motivation, targetResearch, intermediaries, env) {
  const prompt = `User CV: ${userCV}

User motivation: ${motivation}

Target research: ${JSON.stringify(targetResearch)}

Intermediaries: ${JSON.stringify(intermediaries)}

Draft personalized outreach emails:
1. One email to each intermediary (asking for introduction to target)
2. One direct email to target (in case intermediary route doesn't work)

Each email should:
- Be concise (150-200 words)
- Reference specific common ground
- Clearly state the ask
- Provide context on why this matters
- Include a soft CTA

Return structured JSON with email drafts.`;

  const response = await callClaude(prompt, env);
  return response;
}

async function callClaude(prompt, env) {
  // In production, use env.ANTHROPIC_API_KEY
  // For now, return mock data

  // Uncomment this for real API call:
  /*
  const response = await fetch('https://api.anthropic.com/v1/messages', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'x-api-key': env.ANTHROPIC_API_KEY,
      'anthropic-version': '2023-06-01'
    },
    body: JSON.stringify({
      model: 'claude-sonnet-4-5-20250929',
      max_tokens: 4096,
      messages: [{ role: 'user', content: prompt }]
    })
  });

  const data = await response.json();
  return JSON.parse(data.content[0].text);
  */

  // Mock response for V1
  return {
    summary: 'AI agent analysis complete',
    data: 'Mock data - integrate real Claude API for production'
  };
}

/**
 * Helper functions
 */

async function createCampaignStep(campaignId, stepType, description, env) {
  const stepId = generateId();
  await env.DB.prepare(`
    INSERT INTO campaign_steps (id, campaign_id, step_type, step_description, status)
    VALUES (?, ?, ?, ?, 'pending')
  `).bind(stepId, campaignId, stepType, description).run();

  return { id: stepId };
}

async function completeCampaignStep(stepId, result, env) {
  await env.DB.prepare(`
    UPDATE campaign_steps SET status = 'completed', result = ?, completed_at = ?
    WHERE id = ?
  `).bind(JSON.stringify(result), Math.floor(Date.now() / 1000), stepId).run();
}

function generateId() {
  return crypto.randomUUID();
}
