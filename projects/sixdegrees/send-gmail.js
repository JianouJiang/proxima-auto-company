#!/usr/bin/env node
/**
 * sixdegrees/send-gmail.js — Send email via Gmail SMTP (local script).
 *
 * Replaces the MailChannels Cloudflare Function. Run locally or from agents/cron.
 *
 * Usage:
 *   # Via command line args:
 *   node send-gmail.js --to "someone@example.com" --subject "Hello" --body "Hi there"
 *
 *   # Via stdin JSON:
 *   echo '{"to":"someone@example.com","subject":"Hello","body":"Hi there"}' | node send-gmail.js
 *
 *   # Via JSON file:
 *   node send-gmail.js --file email-task.json
 *
 * Environment:
 *   GMAIL_APP_PASSWORD — Required. Gmail App Password.
 *   GMAIL_ADDRESS      — Optional. Defaults to jianou.works@gmail.com.
 */

import { sendEmail } from '../gmail-engine/index.js';

// ── Parse arguments ─────────────────────────────────────────────────

function parseArgs(argv) {
  const args = {};
  for (let i = 2; i < argv.length; i++) {
    const key = argv[i];
    if (key.startsWith('--') && i + 1 < argv.length) {
      const name = key.slice(2);
      const value = argv[i + 1];
      args[name] = value;
      i++;
    }
  }
  return args;
}

async function readStdin() {
  return new Promise((resolve, reject) => {
    // If stdin is a TTY (no piped data), resolve empty immediately
    if (process.stdin.isTTY) {
      resolve('');
      return;
    }

    let data = '';
    process.stdin.setEncoding('utf-8');
    process.stdin.on('data', (chunk) => { data += chunk; });
    process.stdin.on('end', () => resolve(data.trim()));
    process.stdin.on('error', reject);

    // Timeout after 5 seconds if no data
    setTimeout(() => resolve(data.trim()), 5000);
  });
}

async function loadEmailTask() {
  const cliArgs = parseArgs(process.argv);

  // Option 1: --file path/to/task.json
  if (cliArgs.file) {
    const { readFile } = await import('node:fs/promises');
    const content = await readFile(cliArgs.file, 'utf-8');
    return JSON.parse(content);
  }

  // Option 2: CLI args --to --subject --body
  if (cliArgs.to && cliArgs.subject) {
    return {
      to: cliArgs.to,
      subject: cliArgs.subject,
      body: cliArgs.body || '',
      html: cliArgs.html || undefined,
      campaignId: cliArgs.campaignId || cliArgs['campaign-id'] || undefined,
    };
  }

  // Option 3: stdin JSON
  const stdinData = await readStdin();
  if (stdinData) {
    return JSON.parse(stdinData);
  }

  return null;
}

// ── Main ────────────────────────────────────────────────────────────

async function main() {
  const task = await loadEmailTask();

  if (!task) {
    console.error('Usage:');
    console.error('  node send-gmail.js --to "email" --subject "subj" --body "text"');
    console.error('  echo \'{"to":"email","subject":"subj","body":"text"}\' | node send-gmail.js');
    console.error('  node send-gmail.js --file email-task.json');
    console.error('');
    console.error('Env: GMAIL_APP_PASSWORD (required)');
    process.exit(1);
  }

  if (!task.to || !task.subject) {
    console.error('Error: "to" and "subject" are required fields.');
    process.exit(1);
  }

  const timestamp = new Date().toISOString();
  console.log(`[${timestamp}] Sending email to: ${task.to}`);
  console.log(`  Subject: ${task.subject}`);
  if (task.campaignId) {
    console.log(`  Campaign: ${task.campaignId}`);
  }

  const result = await sendEmail({
    to: task.to,
    subject: task.subject,
    body: task.body || '',
    html: task.html || undefined,
    replyTo: 'jianou.works@gmail.com',
    fromName: 'Jianou Jiang',
  });

  if (result.success) {
    console.log(`  Status: SENT`);
    console.log(`  Message-ID: ${result.messageId}`);
  } else {
    console.error(`  Status: FAILED`);
    console.error(`  Error: ${result.error}`);
    process.exit(2);
  }

  // Output machine-readable JSON on last line for piping
  console.log(JSON.stringify({
    success: result.success,
    messageId: result.messageId,
    to: task.to,
    subject: task.subject,
    campaignId: task.campaignId || null,
    timestamp,
  }));
}

main().catch((err) => {
  console.error('Fatal error:', err.message);
  process.exit(1);
});
