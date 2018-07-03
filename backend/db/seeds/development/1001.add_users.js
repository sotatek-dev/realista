const bcrypt = require('bcryptjs');
const now = Date.now();

const seeds = [
  {
    id: 1, username: 'admin',
    email: 'sotatek.test@gmail.com',
    avatar_url: 'images/avatar.jpg',
    password: bcrypt.hashSync('1', bcrypt.genSaltSync(8)),
    full_name: 'Super User',
    neo_address: 'ITS_AN_INVALID_ADDRESS',
    role: '1',
    referral_id: 'admin',
    created_at: now,
    updated_at: now,
    created_by: 1,
    updated_by: 1,
  }
];

exports.seed = function (knex, Promise) {
  return Promise.join(
    knex('user').truncate(),
    knex('user').insert(seeds)
  )
};
