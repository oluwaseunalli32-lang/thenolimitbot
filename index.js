const { Telegraf, Markup } = require('telegraf');

const bot = new Telegraf(process.env.BOT_TOKEN);
const APP_URL = process.env.WEB_APP_URL;

if (!process.env.BOT_TOKEN) throw new Error('BOT_TOKEN is missing');
if (!APP_URL) throw new Error('WEB_APP_URL is missing');

// /start -> reply keyboard with Mini App button
bot.start((ctx) => {
  return ctx.reply(
    'No Limit — text humanizer\n\nTap the button below to open the Mini App.',
    Markup.keyboard([
      [Markup.button.webApp('✍️ Humanize text', APP_URL)]
    ]).resize()
  );
});

// Receive text sent by tg.sendData() from the Mini App
bot.on('message', async (ctx) => {
  const msg = ctx.message;
  if (!msg || !msg.web_app_data) return;

  const text = msg.web_app_data.data || '';
  if (!text.trim()) return;

  await ctx.reply('Humanized text:\n\n' + text);
});

// Graceful shutdown for Render
bot.launch().then(() => {
  console.log('No Limit bot is running');
});

process.once('SIGINT', () => bot.stop('SIGINT'));
process.once('SIGTERM', () => bot.stop('SIGTERM'));
