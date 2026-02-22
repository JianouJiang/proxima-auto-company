/**
 * POST /api/intake
 *
 * Accepts intake form data, creates campaign, generates AI strategy.
 *
 * Request body:
 * {
 *   user_email: string,
 *   user_name: string,
 *   target_name: string,
 *   target_company: string,
 *   target_reason: string,
 *   user_background: string
 * }
 *
 * Response:
 * {
 *   success: boolean,
 *   campaign_id: string,
 *   message: string
 * }
 */

export async function onRequestPost(context) {
  const { request, env } = context;

  try {
    // Parse request body
    const body = await request.json();
    const {
      user_email,
      user_name,
      target_name,
      target_company,
      target_reason,
      user_background,
    } = body;

    // Validation
    if (!user_email || !user_name || !target_name || !target_company || !target_reason || !user_background) {
      return new Response(
        JSON.stringify({
          success: false,
          error: 'Missing required fields',
        }),
        { status: 400, headers: { 'Content-Type': 'application/json' } }
      );
    }

    // Generate campaign ID
    const campaignId = `camp_${Date.now()}_${Math.random().toString(36).substr(2, 9)}`;

    // Create or get user
    let user = await env.DB.prepare('SELECT * FROM users WHERE email = ?')
      .bind(user_email)
      .first();

    if (!user) {
      const userId = `user_${Date.now()}_${Math.random().toString(36).substr(2, 9)}`;
      await env.DB.prepare(
        'INSERT INTO users (id, email, credits_balance) VALUES (?, ?, ?)'
      )
        .bind(userId, user_email, 1) // 1 free campaign
        .run();
      user = { id: userId, email: user_email };
    }

    // Create campaign record
    await env.DB.prepare(`
      INSERT INTO campaigns (
        id, user_id, email, cv, target_name, target_role, motivation, status
      ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    `)
      .bind(
        campaignId,
        user.id,
        user_email,
        user_background,
        target_name,
        target_company,
        target_reason,
        'draft' // Initial status
      )
      .run();

    // Generate AI strategy using Anthropic Claude API
    let strategy = '';
    let selectedPath = null;

    try {
      const claudeResponse = await fetch('https://api.anthropic.com/v1/messages', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'x-api-key': env.ANTHROPIC_API_KEY,
          'anthropic-version': '2023-06-01',
        },
        body: JSON.stringify({
          model: 'claude-3-5-sonnet-20241022',
          max_tokens: 2000,
          messages: [
            {
              role: 'user',
              content: `You are a networking strategist. A user wants to reach "${target_name}" (${target_company}).

User background: ${user_background}

Reason for reaching out: ${target_reason}

Generate a connection strategy:
1. Analyze the target person's background (what they care about, their work, interests)
2. Suggest 2-3 potential connection paths (3-6 degrees)
3. Identify types of intermediaries who would be helpful
4. Rate each path by confidence (0-1)

Return a JSON object with this structure:
{
  "target_analysis": "brief analysis",
  "paths": [
    {
      "degree": 3,
      "confidence": 0.85,
      "strategy": "Path A: You → College Friend → Tesla Employee → ${target_name}",
      "intermediaries": ["College connections", "Tesla employees", "Energy sector professionals"]
    }
  ],
  "recommended_path_index": 0
}`,
            },
          ],
        }),
      });

      if (claudeResponse.ok) {
        const claudeData = await claudeResponse.json();
        const content = claudeData.content[0].text;

        // Try to extract JSON from the response
        const jsonMatch = content.match(/\{[\s\S]*\}/);
        if (jsonMatch) {
          const strategyData = JSON.parse(jsonMatch[0]);
          strategy = strategyData.target_analysis || 'AI-generated strategy';
          selectedPath = strategyData.paths[strategyData.recommended_path_index || 0];
        } else {
          strategy = content;
        }
      } else {
        strategy = 'Strategy generation pending. We will find the best connection path for you.';
      }
    } catch (aiError) {
      console.error('AI strategy generation failed:', aiError);
      strategy = 'Strategy generation pending. We will find the best connection path for you.';
    }

    // Update campaign with strategy
    await env.DB.prepare('UPDATE campaigns SET results = ?, status = ? WHERE id = ?')
      .bind(
        JSON.stringify({
          strategy,
          selected_path: selectedPath,
          target_analysis: strategy,
        }),
        'ready',
        campaignId
      )
      .run();

    return new Response(
      JSON.stringify({
        success: true,
        campaign_id: campaignId,
        message: 'Campaign created successfully',
      }),
      { status: 200, headers: { 'Content-Type': 'application/json' } }
    );
  } catch (error) {
    console.error('Error in intake API:', error);
    return new Response(
      JSON.stringify({
        success: false,
        error: error.message || 'Internal server error',
      }),
      { status: 500, headers: { 'Content-Type': 'application/json' } }
    );
  }
}
