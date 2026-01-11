create table color (
    id integer primary key,
    color text not null
) strict;

insert into color (id, color)
values
(0, 'UNKNOWN'),
(1, 'RED'),
(2, 'BLUE'),
(3, 'YELLOW'),
(4, 'GREEN'),
(6, 'PURPLE'),
(7, 'WHITE');

create table status (
    id integer primary key,
    status text not null
) strict;

insert into status (id, status)
values
(1, 'TODO'),
(2, 'IN_PROGRESS'),
(3, 'COMPLETED'),
(4, 'FAILED');

create table order_type (
    id integer primary key,
    order_type text not null
) strict ;

insert into order_type (id, order_type)
values
(1, 'STORE'),
(2, 'ONLINE'),
(3, 'PHONE');

create table enum_as_fk (
    id integer primary key,
    name text not null,
    color integer not null,
    status integer not null,
    order_type integer not null,
    foreign key (color) references color(id),
    foreign key (status) references status(id),
    foreign key (order_type) references order_type(id)
) strict;

create index enum_as_fk_color_idx on enum_as_fk(color);
create index enum_as_fk_color_status_idx on enum_as_fk(color, status);
create index enum_as_fk_color_status_order_type_idx on enum_as_fk(color, status, order_type);
create index enum_as_fk_order_type_status_idx on enum_as_fk(order_type, status);