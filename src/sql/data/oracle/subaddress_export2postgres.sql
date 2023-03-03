select 'SET client_min_messages = ''ERROR'';' from dual;
select 'truncate table subaddress;' from dual;
select 'insert into subaddress values ('
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
     || ');'
from 
    cscl.subaddress_evw
where 
    ap_id is not null
and sub_address_id is not null;

   