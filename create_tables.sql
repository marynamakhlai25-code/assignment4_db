-- PostgreSQL version
--assignment4 tennis club
create table players (
    player_id serial primary key,
    first_name varchar(100) not null,
    last_name varchar(100) not null,
    email varchar(150) unique not null,
    phone varchar(20),
    skill_level varchar(20) check (skill_level in ('Beginner', 'Intermediate', 'Advanced', 'Pro')),
    birth_date date,
    joined_at timestamp default current_timestamp
);

create table coaches (
    coach_id serial primary key,
    first_name varchar(100) not null,
    last_name varchar(100) not null,
    email varchar(150) unique not null,
    specialization varchar(100),
    hourly_rate numeric(10,2) check (hourly_rate > 0)
);

create table courts (
    court_id serial primary key,
    court_name varchar(50) not null,
    surface_type varchar(20) check (surface_type in ('Grass', 'Clay', 'Hard', 'Indoor')),
    has_lighting boolean default true
);

create table bookings (
    booking_id serial primary key,
    court_id int references courts(court_id) on delete cascade,
    player_id int references players(player_id) on delete cascade,
    coach_id int references coaches(coach_id) on delete set null,
    booking_date date not null,
    start_time time not null,
    end_time time not null,
    total_price numeric(10,2) default 0,
    check (end_time > start_time)
);

create table matches (
    match_id serial primary key,
    player1_id int references players(player_id) on delete cascade,
    player2_id int references players(player_id) on delete cascade,
    court_id int references courts(court_id) on delete cascade,
    match_date timestamp not null,
    score varchar(50),
    check (player1_id <> player2_id)
);

explain analyze
select * from bookings
where booking_date = '2024-06-15';

create index idx_bookings_date on bookings(booking_date);