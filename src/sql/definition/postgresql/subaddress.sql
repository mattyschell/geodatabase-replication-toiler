-- the source cscl database is completely unconstrained
-- it relies on application code to enforce data integrity
-- we will engage in some basic best practices here
-- drop in dev only.  Will be versioned and registered in real child
-- drop table if exists subaddress;
create table subaddress (
	sub_address_id          int4 constraint subaddress_pkc primary key,
	melissa_suite           varchar(50) not null,
	ap_id                   int4 not null,
	additional_loc_info     varchar(50) null,
	building                varchar(50) null,
	floor                   varchar(50) null,
	unit                    varchar(50) null,
	room                    varchar(50) null,
	seat                    varchar(50) null,
	created_by              varchar(50) null,
	created_date            date null,
	modified_by             varchar(50) null,
	modified_date           date null,
	boroughcode             int4 null,
	validation_date         varchar(50) null,
	update_source           varchar(50) null,
	usps_hnum               varchar(50) null,
	objectid                int4 not null,
	globalid                varchar(38) not null default '{00000000-0000-0000-0000-000000000000}'::character varying,
    constraint subaddress_objectid_uqc unique(objectid)
);
--no grants, grant in esrification