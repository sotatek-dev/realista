
/**
 * This file is auto-generated
 * Please don't update it manually
 * Run command `npm run schema` to re-generate this
 */

 module.exports = { RefundModel: 
   { block_number: { type: 'number', length: 10 },
     block_timestamp: { type: 'number', length: 20 },
     txid: { type: 'string', length: 300 },
     address: { type: 'string', length: 300 },
     amount: { type: 'number', length: 11 },
     is_refunded: { type: 'number', length: 4 },
     refund_txid: { type: 'string', length: 300 } },
  UserModel: 
   { username: { type: 'string', length: 120 },
     avatar_url: { type: 'string', length: 768 },
     email: { type: 'string', length: 120 },
     password: { type: 'string', length: 384 },
     full_name: { type: 'string', length: 135 },
     neo_address: { type: 'string', length: 300 },
     referral_id: { type: 'string', length: 30 },
     referrer_id: { type: 'string', length: 30 } } }