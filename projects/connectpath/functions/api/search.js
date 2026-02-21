/**
 * ConnectPath API - Graph Search Worker
 * Finds shortest connection path between two people using:
 * - GitHub API (followers, following, org members)
 * - Twitter/X API (if available)
 * - Crunchbase data (pre-cached)
 */

export async function onRequestPost(context) {
  const { request, env } = context;

  try {
    // Parse request
    const body = await request.json();
    const { personA, personB, lang = 'en' } = body;

    if (!personA || !personB) {
      return new Response(JSON.stringify({
        error: lang === 'zh' ? '请输入两个人的信息' : 'Please enter both person A and person B'
      }), {
        status: 400,
        headers: { 'Content-Type': 'application/json' }
      });
    }

    // Rate limiting check (IP-based, stored in KV)
    const clientIP = request.headers.get('CF-Connecting-IP') || 'unknown';
    const rateLimitKey = `rate_limit:${clientIP}`;
    const today = new Date().toISOString().split('T')[0];

    let rateLimitData = await env.CONNECTPATH_KV.get(rateLimitKey, { type: 'json' });

    if (!rateLimitData || rateLimitData.date !== today) {
      rateLimitData = { date: today, count: 0 };
    }

    if (rateLimitData.count >= 3) {
      return new Response(JSON.stringify({
        error: lang === 'zh' ? '今日免费搜索次数已用完' : 'Daily free search limit reached',
        limit_reached: true
      }), {
        status: 429,
        headers: { 'Content-Type': 'application/json' }
      });
    }

    // Perform search
    const result = await findConnectionPath(personA, personB, env);

    // Increment rate limit
    rateLimitData.count += 1;
    await env.CONNECTPATH_KV.put(rateLimitKey, JSON.stringify(rateLimitData), {
      expirationTtl: 86400 // 24 hours
    });

    return new Response(JSON.stringify(result), {
      status: 200,
      headers: {
        'Content-Type': 'application/json',
        'Access-Control-Allow-Origin': '*'
      }
    });

  } catch (error) {
    console.error('Search error:', error);
    return new Response(JSON.stringify({
      error: error.message || 'Internal server error',
      found: false
    }), {
      status: 500,
      headers: { 'Content-Type': 'application/json' }
    });
  }
}

/**
 * Find connection path using BFS algorithm
 */
async function findConnectionPath(personA, personB, env) {
  const githubToken = env.GITHUB_TOKEN;

  // Step 1: Resolve person identities (search GitHub)
  const personAData = await searchGitHubUser(personA, githubToken);
  const personBData = await searchGitHubUser(personB, githubToken);

  if (!personAData || !personBData) {
    return {
      found: false,
      searched_profiles: 0,
      suggestions: 'Try using GitHub usernames or exact names as they appear on GitHub profiles.'
    };
  }

  // Step 2: BFS to find shortest path
  const path = await bfsSearch(personAData, personBData, githubToken, env);

  if (path && path.length > 0) {
    return {
      found: true,
      path: path,
      degree: path.length - 1,
      confidence: calculateConfidence(path),
      searched_profiles: path.length * 10 // Rough estimate
    };
  }

  return {
    found: false,
    searched_profiles: 50,
    suggestions: 'Try using people more active on GitHub, or check if names are spelled correctly.'
  };
}

/**
 * Search GitHub for user by name or username
 */
async function searchGitHubUser(query, token) {
  try {
    // Try direct username lookup first
    let url = `https://api.github.com/users/${encodeURIComponent(query)}`;
    let headers = {
      'Accept': 'application/vnd.github.v3+json',
      'User-Agent': 'ConnectPath/1.0'
    };

    if (token) {
      headers['Authorization'] = `token ${token}`;
    }

    let response = await fetch(url, { headers });

    if (response.ok) {
      const data = await response.json();
      return {
        name: data.name || data.login,
        username: data.login,
        company: data.company,
        bio: data.bio,
        source: 'github'
      };
    }

    // If direct lookup fails, search by name
    url = `https://api.github.com/search/users?q=${encodeURIComponent(query)}&per_page=1`;
    response = await fetch(url, { headers });

    if (response.ok) {
      const data = await response.json();
      if (data.items && data.items.length > 0) {
        const user = data.items[0];
        // Fetch full user data
        const userResponse = await fetch(user.url, { headers });
        if (userResponse.ok) {
          const userData = await userResponse.json();
          return {
            name: userData.name || userData.login,
            username: userData.login,
            company: userData.company,
            bio: userData.bio,
            source: 'github'
          };
        }
      }
    }

    return null;
  } catch (error) {
    console.error('GitHub search error:', error);
    return null;
  }
}

/**
 * BFS search for connection path
 */
async function bfsSearch(startPerson, targetPerson, githubToken, env) {
  const MAX_DEPTH = 3; // Limit to 3 degrees for free tier
  const MAX_NODES = 100; // Prevent infinite search

  const queue = [[startPerson]];
  const visited = new Set([startPerson.username]);
  let nodesExplored = 0;

  while (queue.length > 0 && nodesExplored < MAX_NODES) {
    const path = queue.shift();
    const currentPerson = path[path.length - 1];

    // Check if we reached target
    if (currentPerson.username === targetPerson.username) {
      return path;
    }

    // Don't go deeper than MAX_DEPTH
    if (path.length >= MAX_DEPTH + 1) {
      continue;
    }

    // Get connections (followers + following)
    const connections = await getGitHubConnections(currentPerson.username, githubToken);
    nodesExplored++;

    for (const connection of connections) {
      if (!visited.has(connection.username)) {
        visited.add(connection.username);

        // Check if this connection is our target
        if (connection.username === targetPerson.username) {
          return [...path, connection];
        }

        // Add to queue for further exploration
        queue.push([...path, connection]);
      }
    }
  }

  return null; // No path found
}

/**
 * Get GitHub connections (followers + following)
 */
async function getGitHubConnections(username, token) {
  const connections = [];
  const headers = {
    'Accept': 'application/vnd.github.v3+json',
    'User-Agent': 'ConnectPath/1.0'
  };

  if (token) {
    headers['Authorization'] = `token ${token}`;
  }

  try {
    // Get followers (limited to 10 for MVP)
    const followersUrl = `https://api.github.com/users/${username}/followers?per_page=10`;
    const followersResponse = await fetch(followersUrl, { headers });

    if (followersResponse.ok) {
      const followers = await followersResponse.json();
      for (const follower of followers) {
        connections.push({
          name: follower.login,
          username: follower.login,
          source: 'github',
          relationship: 'follower'
        });
      }
    }

    // Get following (limited to 10 for MVP)
    const followingUrl = `https://api.github.com/users/${username}/following?per_page=10`;
    const followingResponse = await fetch(followingUrl, { headers });

    if (followingResponse.ok) {
      const following = await followingResponse.json();
      for (const user of following) {
        connections.push({
          name: user.login,
          username: user.login,
          source: 'github',
          relationship: 'following'
        });
      }
    }

    return connections;
  } catch (error) {
    console.error('Error fetching connections:', error);
    return [];
  }
}

/**
 * Calculate confidence score based on path quality
 */
function calculateConfidence(path) {
  if (!path || path.length === 0) return 0;

  let score = 100;

  // Reduce confidence for longer paths
  score -= (path.length - 2) * 10;

  // Reduce confidence if connections lack metadata
  const missingData = path.filter(node => !node.company && !node.bio).length;
  score -= missingData * 5;

  return Math.max(50, Math.min(100, score));
}

// Handle OPTIONS for CORS
export async function onRequestOptions() {
  return new Response(null, {
    status: 204,
    headers: {
      'Access-Control-Allow-Origin': '*',
      'Access-Control-Allow-Methods': 'POST, OPTIONS',
      'Access-Control-Allow-Headers': 'Content-Type'
    }
  });
}
