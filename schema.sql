DROP TABLE IF EXISTS clothing;

CREATE TABLE clothing (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  filename TEXT NOT NULL,
  category TEXT NOT NULL,
  style TEXT NOT NULL,
  colors TEXT -- Storing colors as a comma-separated string of hex values
);
