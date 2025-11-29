const { encoding_for_model } = require('tiktoken');

const enc = encoding_for_model('gpt-4o');

const text = 'Hey there! my name is Soumadip Majila';

const tokens = enc.encode(text);
console.log('Tokens:', tokens);

const decoded = Buffer.from(enc.decode(tokens)).toString();
console.log('Decoded:', decoded);
