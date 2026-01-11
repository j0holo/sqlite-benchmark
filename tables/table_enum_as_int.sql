create table enum_as_int (
    id integer primary key,
    name text not null,
    color integer not null,
    status integer not null,
    order_type integer not null
) strict;

create index enum_as_int_color_idx on enum_as_int(color);
create index enum_as_int_color_status_idx on enum_as_int(color, status);
create index enum_as_int_color_status_order_type_idx on enum_as_int(color, status, order_type);
create index enum_as_int_order_type_status_idx on enum_as_int(order_type, status);