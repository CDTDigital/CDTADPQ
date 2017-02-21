DROP TABLE IF EXISTS world;
DROP TABLE IF EXISTS migrations;

DROP EXTENSION IF EXISTS postgis CASCADE;

CREATE EXTENSION postgis;

CREATE TABLE world
(
);

CREATE TABLE migrations 
(
    last    TEXT
);

SELECT AddGeometryColumn('world', 'geom', 4326, 'POLYGON', 2);

INSERT INTO world (geom) VALUES (ST_SetSRID(ST_MakeBox2D(ST_MakePoint(-180, -90), ST_MakePoint(180, 90)), 4326));
