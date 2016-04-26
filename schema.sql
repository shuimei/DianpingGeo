drop table if exists entries;
create table entries (
  id INTEGER primary key autoincrement,
  name TEXT not null,
  password TEXT not null
);
drop table if exists store;
create table store (
  id INTEGER primary key autoincrement,
  location TEXT not null,
  region TEXT not null,
  category TEXT not null,
  subcategory TEXT not null,
  address TEXT not null,
  name TEXT not null,
  lng REAL not null,
  lat REAL not null,
  confidence int not null
);

