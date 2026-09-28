(() => {
  'use strict';
  const email = document.body.dataset.contactEmail.trim();
  const profileUrl = 'https://www.linkedin.com/in/jerry-zhou-43b51242/';
  const topics = {
    general: { subject: '从个人网站来打个招呼', lines: ['简单介绍一下我自己：', '我想聊的是：'], prompt: '简单说说你是谁、想聊什么就好。', label: '给我发邮件 ↗' },
    consult: { subject: '请教与咨询', lines: ['我的背景：', '目前遇到的问题：', '希望听到哪方面的看法：'], prompt: '可以从这几句开始：你的背景是什么？遇到了什么问题？希望听到哪方面的看法？', label: '聊聊我的问题 ↗' },
    project: { subject: '探讨项目合作', lines: ['项目在做什么：', '目前到了哪一步：', '希望你怎样参与：'], prompt: '可以从这几句开始：项目在做什么？目前到了哪一步？希望我怎样参与？', label: '聊聊项目合作 ↗' },
    exchange: { subject: '交流与分享', lines: ['我的背景：', '想交流的文章或主题：', '希望进一步聊的内容：'], prompt: '可以提一篇文章、一个想法，或一次交流邀请。活动邀请也可以附上时间和形式。', label: '聊聊这个话题 ↗' },
    'article-real-estate': { subject: '关于《浅谈美国房地产投资（一）》的交流', lines: ['我的背景：', '读完文章后的想法或问题：'] },
    'article-tools': { subject: '关于《为什么我花了 80 小时写的代码，最后亲手删了它》的交流', lines: ['我的背景：', '读完文章后的想法或问题：'] }
  };
  function mailto(key) {
    const topic = topics[key] || topics.general;
    const body = `你好 Jerry，\n\n${topic.lines.join('\n')}\n`;
    return `mailto:${email}?subject=${encodeURIComponent(topic.subject)}&body=${encodeURIComponent(body)}`;
  }
  if (email) document.querySelectorAll('[data-email]').forEach(link => {
    link.href = mailto(link.dataset.email);
    link.removeAttribute('target');
  });
  const topicButtons = [...document.querySelectorAll('[data-topic]')];
  const contactLink = document.getElementById('contact-mail');
  const prompt = document.getElementById('contact-prompt');
  let selected = 'general';
  function selectTopic(key) {
    selected = ['general', 'consult', 'project', 'exchange'].includes(key) ? key : 'general';
    topicButtons.forEach(button => button.setAttribute('aria-pressed', String(button.dataset.topic === selected)));
    contactLink.href = email ? mailto(selected) : profileUrl;
    contactLink.textContent = email ? topics[selected].label : '在 LinkedIn 联系我 ↗';
    if (email) contactLink.removeAttribute('target');
    prompt.textContent = topics[selected].prompt;
  }
  selectTopic('general');
  topicButtons.forEach(button => {
    button.hidden = false;
    button.addEventListener('click', () => selectTopic(button.dataset.topic === selected ? 'general' : button.dataset.topic));
  });
  document.querySelectorAll('[data-contact-topic]').forEach(link => link.addEventListener('click', () => selectTopic(link.dataset.contactTopic)));
  const copyButton = document.getElementById('copy-email');
  const emailField = document.getElementById('contact-email');
  const copyStatus = document.getElementById('copy-status');
  emailField.value = email;
  copyButton.hidden = !email;
  document.getElementById('email-copy').hidden = !email;
  copyButton.addEventListener('click', async () => {
    try {
      if (!navigator.clipboard?.writeText) throw new Error('Clipboard unavailable');
      await navigator.clipboard.writeText(email);
      copyStatus.textContent = '邮箱已复制，可以到你常用的邮箱里写信。';
    } catch (_) {
      emailField.focus();
      emailField.select();
      copyStatus.textContent = '邮箱已选中，可以手动复制。';
    }
  });
  document.getElementById('year').textContent = String(new Date().getFullYear());
})();
