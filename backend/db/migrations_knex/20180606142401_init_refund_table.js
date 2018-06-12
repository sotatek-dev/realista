
exports.up = (knex, Promise) => {
  return Promise.all([
    knex.schema.createTable('refund', (t) => {
      t.bigIncrements('id').primary().unsigned();
      t.integer('block_number').unsigned().index();
      t.bigint('block_timestamp').unsigned().index();
      t.string('txid', 100).notNullable().index();
      t.string('address', 100).notNullable().index();
      t.integer('amount').notNullable();
      t.tinyint('is_refunded').notNullable().default(0);
      t.string('refund_txid', 100).index();
      t.bigint('created_at');
      t.bigint('updated_at');
      t.integer('created_by');
      t.integer('updated_by');
      t.charset('utf8mb4');
      t.collate('utf8mb4_general_ci');
    })
  ]);
}

exports.down = (knex, Promise) => {
  return knex.schema
    .dropTableIfExists('refund');
}
