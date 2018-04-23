DROP TABLE STATS;
DROP TABLE BOARD;

CREATE TABLE STATS (
    side_name   VARCHAR(10) PRIMARY KEY,
    wins        NUMBER,
    game_over   NUMBER(1),
    turn        VARCHAR(10),
    CONSTRAINT sname CHECK (side_name IN ('Red', 'Black')),
    CONSTRAINT turnname CHECK (turn IN ('Red', 'Black'))

);
CREATE TABLE BOARD (
    tile       NUMBER PRIMARY KEY,
    color      VARCHAR(10),
    king       NUMBER(1),
    CONSTRAINT team_color CHECK (color IN ('Red', 'Black', 'None')),
    CONSTRAINT tile_check CHECK (tile BETWEEN 0 AND 31)
);

INSERT INTO BOARD VALUES (31, 'Black', 0);
