#!/usr/bin/env node
/**
 * sixdegrees/auto-outreach.js — Fully automatic 6-degree outreach engine.
 *
 * Loads a chain config, sends personalized emails to multiple contacts per degree,
 * tracks sends in a local JSON file, checks for replies via Gmail IMAP.
 *
 * Usage:
 *   # Send outreach for degree 1 (first hop)
 *   node auto-outreach.js --degree 1
 *
 *   # Check for replies to all sent emails
 *   node auto-outreach.js --check-replies
 *
 *   # Show status of all outreach
 *   node auto-outreach.js --status
 *
 *   # Use a specific chain config
 *   node auto-outreach.js --degree 1 --config chains/elon-musk.json
 *
 * Environment:
 *   GMAIL_APP_PASSWORD — Required.
 *   GMAIL_ADDRESS      — Optional. Defaults to jianou.works@gmail.com.
 */

import { readFile, writeFile, mkdir } from 'node:fs/promises';
import { existsSync } from 'node:fs';
import { dirname, resolve } from 'node:path';
import { fileURLToPath } from 'node:url';
import { sendEmail, sendBatch, checkReplies } from '../gmail-engine/index.js';

const __dirname = dirname(fileURLToPath(import.meta.url));

// ── Config and State Paths ──────────────────────────────────────────

const DEFAULT_CONFIG = resolve(__dirname, 'outreach-chain.json');
const STATE_FILE = resolve(__dirname, 'outreach-state.json');

// ── Parse CLI args ──────────────────────────────────────────────────

function parseArgs(argv) {
  const args = {};
  for (let i = 2; i < argv.length; i++) {
    const key = argv[i];
    if (key === '--check-replies') {
      args.checkReplies = true;
    } else if (key === '--status') {
      args.status = true;
    } else if (key === '--dry-run') {
      args.dryRun = true;
    } else if (key.startsWith('--') && i + 1 < argv.length) {
      args[key.slice(2)] = argv[i + 1];
      i++;
    }
  }
  return args;
}

// ── State Management ────────────────────────────────────────────────

async function loadState() {
  try {
    if (existsSync(STATE_FILE)) {
      const content = await readFile(STATE_FILE, 'utf-8');
      return JSON.parse(content);
    }
  } catch {
    // Corrupted state file — start fresh
  }
  return {
    campaignId: `sixdegrees-${Date.now()}`,
    startedAt: new Date().toISOString(),
    currentDegree: 0,
    sends: [],        // { degree, to, subject, messageId, sentAt, status }
    replies: [],      // { from, messageId, inReplyTo, receivedAt, text }
  };
}

async function saveState(state) {
  state.updatedAt = new Date().toISOString();
  await writeFile(STATE_FILE, JSON.stringify(state, null, 2), 'utf-8');
}

// ── Chain Config ────────────────────────────────────────────────────

/**
 * Chain config format (outreach-chain.json):
 * {
 *   "target": "Elon Musk",
 *   "goal": "Get an introduction to Elon Musk",
 *   "degrees": [
 *     {
 *       "degree": 1,
 *       "label": "PyPSA open-source contributors",
 *       "contacts": [
 *         {
 *           "name": "Prof. Tom Brown",
 *           "email": "tom.brown@tu-berlin.de",
 *           "role": "PyPSA Lead Developer",
 *           "connection": "Fellow open-source energy researcher",
 *           "emailTemplate": {
 *             "subject": "PyPSA Contributors Network — Energy-Tesla Bridge",
 *             "body": "Dear Prof. Brown, ..."
 *           }
 *         },
 *         // ... more contacts at this degree
 *       ]
 *     },
 *     {
 *       "degree": 2,
 *       "label": "Energy policy / industry bridge",
 *       "contacts": [ ... ]
 *     }
 *   ]
 * }
 */

async function loadChainConfig(configPath) {
  const path = configPath || DEFAULT_CONFIG;
  if (!existsSync(path)) {
    // Create example config if it doesn't exist
    const example = createExampleConfig();
    await writeFile(path, JSON.stringify(example, null, 2), 'utf-8');
    console.log(`Created example chain config at: ${path}`);
    console.log('Edit it with your actual contacts, then run again.');
    return example;
  }
  const content = await readFile(path, 'utf-8');
  return JSON.parse(content);
}

function createExampleConfig() {
  return {
    target: 'Target Person',
    goal: 'Get an introduction to Target Person through a 6-degree chain',
    sender: {
      name: 'Jianou Jiang',
      title: 'Researcher, Oxford Thermofluids Institute',
      email: 'jianou.works@gmail.com',
    },
    degrees: [
      {
        degree: 1,
        label: 'Direct professional contacts',
        contacts: [
          {
            name: 'Contact Name',
            email: 'contact@example.com',
            role: 'Their Role',
            connection: 'How you know them / why they would help',
            emailTemplate: {
              subject: 'Subject line here',
              body: 'Dear Contact Name,\n\nYour personalized message here.\n\nBest regards,\nJianou Jiang',
            },
          },
        ],
      },
      {
        degree: 2,
        label: 'Second-degree connections',
        contacts: [],
      },
    ],
  };
}

// ── Outreach Logic ──────────────────────────────────────────────────

async function sendDegreeOutreach(degree, chain, state, dryRun) {
  const degreeConfig = chain.degrees.find((d) => d.degree === degree);

  if (!degreeConfig) {
    console.error(`No degree ${degree} found in chain config.`);
    console.error(`Available degrees: ${chain.degrees.map((d) => d.degree).join(', ')}`);
    return;
  }

  if (!degreeConfig.contacts || degreeConfig.contacts.length === 0) {
    console.error(`No contacts defined for degree ${degree}.`);
    console.error('Edit your chain config to add contacts.');
    return;
  }

  // Check which contacts at this degree have already been emailed
  const alreadySent = new Set(
    state.sends
      .filter((s) => s.degree === degree)
      .map((s) => s.to.toLowerCase())
  );

  const toSend = degreeConfig.contacts.filter(
    (c) => !alreadySent.has(c.email.toLowerCase())
  );

  if (toSend.length === 0) {
    console.log(`All ${degreeConfig.contacts.length} contacts at degree ${degree} have already been emailed.`);
    console.log('Use --check-replies to see if anyone responded.');
    return;
  }

  console.log(`\n=== Degree ${degree}: ${degreeConfig.label} ===`);
  console.log(`Target: ${chain.target}`);
  console.log(`Contacts to email: ${toSend.length} of ${degreeConfig.contacts.length}`);
  console.log(`Already sent: ${alreadySent.size}`);
  console.log('');

  if (dryRun) {
    console.log('[DRY RUN] Would send the following emails:\n');
    for (const contact of toSend) {
      console.log(`  To: ${contact.name} <${contact.email}>`);
      console.log(`  Subject: ${contact.emailTemplate.subject}`);
      console.log(`  Connection: ${contact.connection}`);
      console.log('');
    }
    return;
  }

  // Build email list
  const emails = toSend.map((contact) => ({
    to: `"${contact.name}" <${contact.email}>`,
    subject: contact.emailTemplate.subject,
    body: contact.emailTemplate.body,
    html: contact.emailTemplate.html || undefined,
    replyTo: chain.sender?.email || 'jianou.works@gmail.com',
    fromName: chain.sender?.name || 'Jianou Jiang',
  }));

  // Send with 3-second delay between each
  console.log('Sending emails...\n');
  const results = await sendBatch(emails, 3000);

  // Record results
  for (let i = 0; i < results.length; i++) {
    const contact = toSend[i];
    const result = results[i];

    const record = {
      degree,
      to: contact.email,
      toName: contact.name,
      subject: contact.emailTemplate.subject,
      messageId: result.messageId || null,
      sentAt: new Date().toISOString(),
      status: result.success ? 'sent' : 'failed',
      error: result.error || null,
    };

    state.sends.push(record);

    if (result.success) {
      console.log(`  SENT: ${contact.name} <${contact.email}>`);
      console.log(`    Message-ID: ${result.messageId}`);
    } else {
      console.error(`  FAILED: ${contact.name} <${contact.email}>`);
      console.error(`    Error: ${result.error}`);
    }
  }

  state.currentDegree = Math.max(state.currentDegree, degree);
  await saveState(state);

  const sentCount = results.filter((r) => r.success).length;
  const failCount = results.filter((r) => !r.success).length;
  console.log(`\nDegree ${degree} complete: ${sentCount} sent, ${failCount} failed.`);
}

async function checkForReplies(state) {
  const sentMessageIds = state.sends
    .filter((s) => s.status === 'sent' && s.messageId)
    .map((s) => s.messageId);

  if (sentMessageIds.length === 0) {
    console.log('No sent emails to check replies for.');
    return;
  }

  console.log(`Checking for replies to ${sentMessageIds.length} sent emails...`);

  const result = await checkReplies({
    messageIds: sentMessageIds,
    markRead: false,
    includeBody: true,
  });

  if (!result.success) {
    console.error(`Failed to check replies: ${result.error}`);
    return;
  }

  if (result.replies.length === 0) {
    console.log('No new replies found.');
    return;
  }

  console.log(`\nFound ${result.replies.length} reply(ies):\n`);

  for (const reply of result.replies) {
    const fromAddr = reply.from[0]?.address || 'unknown';
    const fromName = reply.from[0]?.name || '';

    // Find the original send
    const originalSend = state.sends.find(
      (s) => s.messageId && s.messageId.replace(/^<|>$/g, '') === reply.inReplyToId
    );

    console.log(`  From: ${fromName} <${fromAddr}>`);
    console.log(`  Date: ${reply.date}`);
    console.log(`  Subject: ${reply.subject}`);
    if (originalSend) {
      console.log(`  In reply to degree ${originalSend.degree} email to ${originalSend.toName}`);
    }
    if (reply.replyText) {
      console.log(`  Reply text: ${reply.replyText.slice(0, 200)}${reply.replyText.length > 200 ? '...' : ''}`);
    }
    console.log('');

    // Record the reply
    state.replies.push({
      from: fromAddr,
      fromName,
      messageId: reply.messageId,
      inReplyTo: reply.inReplyToId,
      receivedAt: reply.date,
      subject: reply.subject,
      text: reply.replyText || '',
      degree: originalSend?.degree || null,
    });
  }

  await saveState(state);
  console.log('State updated with new replies.');
}

function showStatus(state, chain) {
  console.log('\n=== SixDegrees Outreach Status ===\n');
  console.log(`Campaign: ${state.campaignId}`);
  console.log(`Target: ${chain?.target || 'Unknown'}`);
  console.log(`Started: ${state.startedAt}`);
  console.log(`Last updated: ${state.updatedAt || 'Never'}`);
  console.log(`Current degree: ${state.currentDegree}`);
  console.log('');

  // Group sends by degree
  const byDegree = {};
  for (const send of state.sends) {
    if (!byDegree[send.degree]) byDegree[send.degree] = [];
    byDegree[send.degree].push(send);
  }

  for (const [degree, sends] of Object.entries(byDegree).sort((a, b) => a[0] - b[0])) {
    const degreeConfig = chain?.degrees?.find((d) => d.degree === Number(degree));
    const label = degreeConfig?.label || '';
    const sent = sends.filter((s) => s.status === 'sent').length;
    const failed = sends.filter((s) => s.status === 'failed').length;
    const replies = state.replies.filter((r) => r.degree === Number(degree));

    console.log(`Degree ${degree}: ${label}`);
    console.log(`  Sent: ${sent}  Failed: ${failed}  Replies: ${replies.length}`);

    for (const send of sends) {
      const replyMark = state.replies.some(
        (r) => r.inReplyTo && send.messageId && r.inReplyTo === send.messageId.replace(/^<|>$/g, '')
      ) ? ' [REPLIED]' : '';
      const statusMark = send.status === 'sent' ? '+' : 'x';
      console.log(`    [${statusMark}] ${send.toName} <${send.to}>${replyMark}`);
    }
    console.log('');
  }

  if (state.replies.length > 0) {
    console.log(`Total replies: ${state.replies.length}`);
    for (const reply of state.replies) {
      console.log(`  - ${reply.fromName} <${reply.from}> (degree ${reply.degree})`);
    }
  } else {
    console.log('No replies yet.');
  }
}

// ── Main ────────────────────────────────────────────────────────────

async function main() {
  const args = parseArgs(process.argv);
  const configPath = args.config ? resolve(args.config) : DEFAULT_CONFIG;

  const state = await loadState();
  const chain = await loadChainConfig(configPath);

  if (args.status) {
    showStatus(state, chain);
    return;
  }

  if (args.checkReplies) {
    await checkForReplies(state);
    return;
  }

  if (args.degree) {
    const degree = parseInt(args.degree, 10);
    if (isNaN(degree) || degree < 1) {
      console.error('Error: --degree must be a positive integer.');
      process.exit(1);
    }
    await sendDegreeOutreach(degree, chain, state, !!args.dryRun);
    return;
  }

  // No action specified — show help
  console.log('SixDegrees Auto-Outreach Engine');
  console.log('');
  console.log('Usage:');
  console.log('  node auto-outreach.js --degree 1              Send emails for degree 1');
  console.log('  node auto-outreach.js --degree 1 --dry-run    Preview without sending');
  console.log('  node auto-outreach.js --check-replies         Check for replies');
  console.log('  node auto-outreach.js --status                Show outreach status');
  console.log('  node auto-outreach.js --config chain.json     Use specific chain config');
  console.log('');
  console.log('Environment:');
  console.log('  GMAIL_APP_PASSWORD    Required for sending and checking replies');
  console.log('');
  console.log(`Chain config: ${configPath}`);
  console.log(`State file:   ${STATE_FILE}`);
}

main().catch((err) => {
  console.error('Fatal error:', err.message);
  process.exit(1);
});
