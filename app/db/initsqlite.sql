CREATE TABLE IF NOT EXISTS STATS (
    side_name   VARCHAR(10) PRIMARY KEY,
    wins        INT,
    CONSTRAINT sname CHECK (side_name IN ('Red', 'Black'))
);
CREATE TABLE IF NOT EXISTS PIECES (
    x         INT PRIMARY KEY,
    y         INT,
    color       VARCHAR(10),
    king        NUMBER(1),
    CONSTRAINT team_color CHECK (color IN ('Red', 'Black'))
);
CREATE TABLE IF NOT EXISTS BOARD (
    x         INT,
    y         INT,
    color       VARCHAR(10),
    king        NUMBER(1),
    PRIMARY KEY (x, y),
    CONSTRAINT team_color CHECK (color IN ('Red', 'Black', 'None'))
);