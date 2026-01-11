create table enum_as_string (
    id integer primary key,
    name text not null,
    color text not null,
    status text not null,
    order_type text not null
) strict;

create index enum_as_string_color_idx on enum_as_string(color);
create index enum_as_string_color_status_idx on enum_as_string(color, status);
create index enum_as_string_color_status_order_type_idx on enum_as_string(color, status, order_type);
create index enum_as_string_order_type_status_idx on enum_as_string(order_type, status);
