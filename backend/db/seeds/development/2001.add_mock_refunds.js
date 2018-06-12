const bcrypt = require('bcryptjs');
const now = Date.now();

const seeds = [];
const maxSeeds = ~~(Math.random() * 100);
for (let i = 0; i < maxSeeds; i++) {
  seeds.push({
    block_number: ~~(Math.random() * 1000000),
    block_timestamp: now - ~~(Math.random() * 1000000),
    txid: Math.random().toString(36).substring(2, 66),
    address: Math.random().toString(36).substring(2, 36),
    amount: ~~(Math.random() * 100),
    created_at: now,
    updated_at: now,
    created_by: 1,
    updated_by: 1,
  });
}

exports.seed = function (knex, Promise) {
  return Promise.join(
    knex('refund').truncate(),
    knex('refund').insert(seeds)
  )
};
