-- Users table
CREATE TABLE IF NOT EXISTS users (
    id TEXT PRIMARY KEY,
    email TEXT UNIQUE NOT NULL,
    credits_balance INTEGER DEFAULT 0,
    created_at INTEGER DEFAULT (strftime('%s', 'now')),
    updated_at INTEGER DEFAULT (strftime('%s', 'now'))
);

-- Campaigns table
CREATE TABLE IF NOT EXISTS campaigns (
    id TEXT PRIMARY KEY,
    user_id TEXT NOT NULL,
    email TEXT NOT NULL,
    cv TEXT NOT NULL,
    target_name TEXT NOT NULL,
    target_role TEXT,
    motivation TEXT NOT NULL,
    status TEXT DEFAULT 'pending', -- pending, processing, completed, failed
    credits_used INTEGER DEFAULT 0,
    results TEXT, -- JSON string of results
    created_at INTEGER DEFAULT (strftime('%s', 'now')),
    updated_at INTEGER DEFAULT (strftime('%s', 'now')),
    FOREIGN KEY (user_id) REFERENCES users(id)
);

-- Campaign steps table (track each agent search operation)
CREATE TABLE IF NOT EXISTS campaign_steps (
    id TEXT PRIMARY KEY,
    campaign_id TEXT NOT NULL,
    step_type TEXT NOT NULL, -- research_target, find_intermediary, draft_email
    step_description TEXT,
    credits_cost INTEGER DEFAULT 1,
    result TEXT, -- JSON result of this step
    status TEXT DEFAULT 'pending', -- pending, completed, failed
    created_at INTEGER DEFAULT (strftime('%s', 'now')),
    completed_at INTEGER,
    FOREIGN KEY (campaign_id) REFERENCES campaigns(id)
);

-- Credit transactions table
CREATE TABLE IF NOT EXISTS credit_transactions (
    id TEXT PRIMARY KEY,
    user_id TEXT NOT NULL,
    amount INTEGER NOT NULL, -- positive for purchase, negative for usage
    transaction_type TEXT NOT NULL, -- purchase, usage, refund
    plan TEXT, -- starter, growth, pro, unlimited (for purchases)
    campaign_id TEXT, -- for usage transactions
    created_at INTEGER DEFAULT (strftime('%s', 'now')),
    FOREIGN KEY (user_id) REFERENCES users(id),
    FOREIGN KEY (campaign_id) REFERENCES campaigns(id)
);

-- Email outreach table (tracks sent emails)
CREATE TABLE IF NOT EXISTS email_outreach (
    id TEXT PRIMARY KEY,
    campaign_id TEXT NOT NULL,
    recipient_email TEXT NOT NULL,
    recipient_name TEXT,
    subject TEXT NOT NULL,
    body TEXT NOT NULL,
    status TEXT DEFAULT 'pending', -- pending, sent, failed, bounced, replied
    sent_at INTEGER,
    error_message TEXT,
    created_at INTEGER DEFAULT (strftime('%s', 'now')),
    FOREIGN KEY (campaign_id) REFERENCES campaigns(id)
);

-- Indexes for performance
CREATE INDEX IF NOT EXISTS idx_campaigns_user_id ON campaigns(user_id);
CREATE INDEX IF NOT EXISTS idx_campaigns_email ON campaigns(email);
CREATE INDEX IF NOT EXISTS idx_campaigns_status ON campaigns(status);
CREATE INDEX IF NOT EXISTS idx_campaign_steps_campaign_id ON campaign_steps(campaign_id);
CREATE INDEX IF NOT EXISTS idx_credit_transactions_user_id ON credit_transactions(user_id);
CREATE INDEX IF NOT EXISTS idx_email_outreach_campaign_id ON email_outreach(campaign_id);
CREATE INDEX IF NOT EXISTS idx_email_outreach_status ON email_outreach(status);
