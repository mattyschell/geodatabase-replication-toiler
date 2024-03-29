-- much of the complexity here is protection from bad data in the source
select 'SET client_min_messages = ''ERROR'';' from dual;
select 'truncate table subaddress;' from dual;
select 'commit;' from dual;
select 'begin;' from dual;
select 'insert into subaddress values ' from dual;
with subaddress_valid
as (select * from cscl.subaddress_evw
    where 
        ap_id is not null
    and sub_address_id is not null 
    and sub_address_id not in (select sub_address_id 
                               from cscl.subaddress_evw
                               group by sub_address_id
                               having count(sub_address_id) > 1))
select '('
     || sub_address_id
     || ',''' || melissa_suite || ''''
     || ',' || ap_id
     || ',''' || additional_loc_info || ''''
     || ',''' || building || ''''
     || ',''' || floor || ''''
     || ',''' || unit || ''''
     || ',''' || room || ''''
     || ',''' || seat || ''''
     || ',''' || created_by || ''''
     || case  
            when created_date is not null 
            then 
                ',''' || to_char(created_date) || ''''
            else ',null::date'
       end
     || ',''' || modified_by || ''''
     || case  
            when modified_date is not null 
            then 
                ',''' || to_char(modified_date) || ''''
            else ',null::date'
       end
     || ',' || NVL(boroughcode,'null')
     || case  
            when validation_date is not null 
            then 
                ',''' || to_char(validation_date) || ''''
            else ',null::date'
       end
     || ',''' || update_source || ''''
     || ',''' || usps_hnum || ''''
     || ',' || objectid
     || ',''' || globalid || ''''
     || '),'
from 
    subaddress_valid; 