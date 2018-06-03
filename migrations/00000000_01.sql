-- Change columns types to the specific enum fields

-- Payables
-- type
create type enum_payables_type as enum ('credit', 'refund', 'chargeback');
alter table "Payables" alter column type type enum_payables_type using type :: enum_payables_type;
-- status
create type enum_payables_status as enum ('waiting_funds', 'paid', 'suspended');
alter table "Payables" alter column status type enum_payables_status using status :: enum_payables_status;
-- payment_method
create type enum_payables_payment_method as enum ('boleto', 'credit_card', 'debit_card');
alter table "Payables" alter column payment_method type enum_payables_payment_method using payment_method :: enum_payables_payment_method;

-- BalanceOperations
-- type
create type enum_balance_operations_object_type as enum ('payable', 'transfer', 'refund', 'fee_collection');
alter table "BalanceOperations" alter column object_type type enum_balance_operations_object_type using object_type :: enum_balance_operations_object_type;
-- status
create type enum_balance_operations_status as enum ('waiting_funds', 'available', 'transferred');
alter table "BalanceOperations" alter column status type enum_balance_operations_status using status :: enum_balance_operations_status;

-- Transfers
-- status
create type enum_transfers_status as enum ('pending_transfer', 'processing', 'canceled', 'failed', 'transferred');
alter table "Transfers" alter column status type enum_transfers_status using status :: enum_transfers_status;
-- type
create type enum_transfers_type as enum ('ted', 'doc', 'credito_em_conta', 'inter_recipient');
alter table "Transfers" alter column type type enum_transfers_type using type :: enum_transfers_type;
-- source_type
create type enum_transfers_source_type as enum ('recipient');
alter table "Transfers" alter column source_type type enum_transfers_source_type using source_type :: enum_transfers_source_type;
-- target_type
create type enum_transfers_target_type as enum ('bank_account', 'recipient');
alter table "Transfers" alter column target_type type enum_transfers_target_type using target_type :: enum_transfers_target_type;

-- BankAccounts
-- document_type
create type enum_bank_accounts_document_type as enum ('cpf', 'cnpj');
alter table "BankAccounts" alter column document_type type enum_bank_accounts_document_type using document_type :: enum_bank_accounts_document_type;
-- type
create type enum_bank_accounts_type as enum ('conta_corrente', 'conta_corrente_conjunta', 'conta_poupanca', 'conta_poupanca_conjunta');
alter table "BankAccounts" alter column type type enum_bank_accounts_type using type :: enum_bank_accounts_type;

-- FeeCollections
-- status
create type enum_fee_collections_status as enum ('waiting_funds', 'available');
alter table "FeeCollections" alter column status type enum_fee_collections_status using status :: enum_fee_collections_status;
-- type
create type enum_fee_collections_type as enum ('fee_adjustment', 'billing');
alter table "FeeCollections" alter column type type enum_fee_collections_type using type :: enum_fee_collections_type;
-- object_type
create type enum_fee_collections_object_type as enum ('payable', 'invoice');
alter table "FeeCollections" alter column object_type type enum_fee_collections_object_type using object_type :: enum_fee_collections_object_type;

-- Invoices
-- status
create type enum_invoices_status as enum ('pending', 'cancelled');
alter table "Invoices" alter column status type enum_invoices_status using status :: enum_invoices_status;
-- payment_method
create type enum_invoices_payment_method as enum ('fee', 'fee_collection', 'boleto');
alter table "Invoices" alter column payment_method type enum_invoices_payment_method using payment_method :: enum_invoices_payment_method;
-- type
create type enum_invoices_type as enum ('gateway', 'psp', 'boleto', 'transfers');
alter table "Invoices" alter column type type enum_invoices_type using type :: enum_invoices_type;

-- Recipients
-- transfer_interval
create type enum_recipients_transfer_interval as enum ('daily', 'weekly', 'monthly');
alter table "Recipients" alter column transfer_interval type enum_recipients_transfer_interval using transfer_interval :: enum_recipients_transfer_interval;
-- automatic_anticipation_type
create type enum_recipients_automatic_anticipation_type as enum ('full', '1025');
alter table "Recipients" alter column automatic_anticipation_type type enum_recipients_automatic_anticipation_type using automatic_anticipation_type :: enum_recipients_automatic_anticipation_type;
-- status
create type enum_recipients_status as enum ('registration', 'affiliation', 'active', 'refused', 'suspended', 'blocked', 'inactive');
alter table "Recipients" ALTER COLUMN status type enum_recipients_status using status :: enum_recipients_status;

-- BulkAnticipations
-- timeframe
create type enum_bulk_anticipations_timeframe as enum ('start', 'end');
alter table "BulkAnticipations" alter column timeframe type enum_bulk_anticipations_timeframe using timeframe :: enum_bulk_anticipations_timeframe;
-- status
create type enum_bulk_anticipations_status as enum ('pending', 'canceled', 'approved', 'refused');
alter table "BulkAnticipations" ALTER COLUMN status type enum_bulk_anticipations_status using status :: enum_bulk_anticipations_status;

-- Transactions
-- status
create type enum_transactions_status as enum ('paid', 'refunded', 'pending_refund', 'refused', 'waiting_payment', 'chargedback', 'authorized', 'processing');
alter table "Transactions" ALTER COLUMN status type enum_transactions_status using status :: enum_transactions_status;
-- payment_method
create type enum_transactions_payment_method as enum ('credit_card', 'boleto', 'debit_card');
alter table "Transactions" alter column payment_method type enum_transactions_payment_method using payment_method :: enum_transactions_payment_method;
-- capture_method
create type enum_transactions_capture_method as enum ('ecommerce', 'emv', 'magstripe');
alter table "Transactions" alter column capture_method type enum_transactions_capture_method using capture_method :: enum_transactions_capture_method;
-- card_pin_mode
create type enum_transactions_card_pin_mode as enum ('online', 'offline');
alter table "Transactions" alter column card_pin_mode type enum_transactions_card_pin_mode using card_pin_mode :: enum_transactions_card_pin_mode;

-- Customers
-- document_type
create type enum_customers_document_type as enum ('cpf', 'cnpj');
alter table "Customers" ALTER COLUMN document_type type enum_customers_document_type using document_type :: enum_customers_document_type;
