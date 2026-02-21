/**
 * Test script to send email via Gmail SMTP using Nodemailer
 * Run with: node send-test-email.js
 */

import nodemailer from 'nodemailer';

const transporter = nodemailer.createTransport({
  host: 'smtp.gmail.com',
  port: 587,
  secure: false, // use TLS
  auth: {
    user: 'jianou.works@gmail.com',
    pass: process.env.GMAIL_APP_PASSWORD || 'your-app-password-here'
  }
});

const emailData = {
  from: '"Jianou Jiang" <jianou.works@gmail.com>',
  to: 'tom.brown@tu-berlin.de',
  subject: 'PyPSA Contributors Network — Energy-Tesla Bridge Project',
  text: `Dear Prof. Brown,

I'm Jianou Jiang, a researcher at Oxford Thermofluids Institute and contributor to PyPSA's stochastic optimization features for energy system planning. I've been working on large-scale energy optimization for electrified systems (MINLP models with 60K+ variables) and believe there's a strategic opportunity to connect energy systems research with industrial AI applications at companies like Tesla.

Would you be open to a brief conversation about how PyPSA's framework could inform industrial energy optimization, and potentially connecting with researchers who might be interested in this bridge? Your perspective on the research-to-industry pathway would be invaluable.

Best regards,
Jianou Jiang
Oxford Thermofluids Institute
jianou.works@gmail.com`
};

async function sendEmail() {
  try {
    const info = await transporter.sendMail(emailData);
    console.log('✅ Email sent successfully!');
    console.log('Message ID:', info.messageId);
    console.log('Response:', info.response);
  } catch (error) {
    console.error('❌ Error sending email:', error.message);
    if (error.code) console.error('Error code:', error.code);
  }
}

sendEmail();
