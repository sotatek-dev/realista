require('dotenv').config();

const _             = require('lodash');
const config        = require('../knexfile')[process.env.NODE_ENV];
const knex          = require('knex')(config);
const logger        = require('sota-core').getLogger('InitDB');
const migrate       = knex.migrate;

if (!_.includes(['test', 'development', 'staging'], process.env.NODE_ENV)) {
  logger.fatal('Cannot run this script on PRODUCTION ENVIRONMENT!!!');
  process.exit(1);
}

main()

function main () {
  rollback()
    .then(latest)
    .then(seedMySQL)
    .then(done)
    .catch(e => {
      logger.error(e.toString());
      process.exit(1);
    });
}

function rollback () {
  logger.info('Rollback all migrated scripts...')

  // Force unlock in case of bad state
  return migrate.forceFreeMigrationsLock()

  // Get completed migrations
  .then(function(){
    return migrate._listCompleted();
  })

  // Rollback migrations
  .then(function(completedMigrations){
    return migrate._waterfallBatch(0, completedMigrations.reverse(), 'down');
  })
}

function latest () {
  logger.info('Migrate latest MySQL DB schema...')
  return knex.migrate.latest()
}

function seedMySQL () {
  logger.info('Creating MySQL DB seeds...')
  return knex.seed.run()
}

function done () {
  process.exit(0)
}
