-- parsed_data 테이블 생성
CREATE TABLE IF NOT EXISTS parsed_data (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    text_input TEXT NOT NULL,
    item TEXT NOT NULL,
    quantity TEXT NOT NULL,
    action TEXT NOT NULL,
    created_date TEXT NOT NULL,
    production_date TEXT NOT NULL,
    expiration_date TEXT
);

-- item_list 테이블 생성
-- item_list 테이블 생성
CREATE TABLE IF NOT EXISTS item_list (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    item_name TEXT NOT NULL UNIQUE,
    shelf_life INTEGER NOT NULL,
    storage_method TEXT
);

