
exports.up = function(knex, Promise) {
  return knex.schema.hasColumn('user', 'role').then((exists) => {
    if (exists) {
      return Promise.all([]);
    }

    return knex.schema.table('user', (t) => {
      t.integer('role').notNullable().default(0).after('neo_address');
    });
  });
};

exports.down = function(knex, Promise) {
  return Promise.all([]);
};
