CREATE TABLE people (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    phone VARCHAR(20),
    fax VARCHAR(20),
    image_url TEXT,
    position VARCHAR(100),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE counties (
    id SERIAL PRIMARY KEY,
    county_id CHAR(5) NOT NULL,
    name VARCHAR(100) UNIQUE NOT NULL,
    judicial_circuit VARCHAR(100) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE addresses (
    id SERIAL PRIMARY KEY,
    person_id INTEGER REFERENCES people(id) ON DELETE CASCADE,
    street_address VARCHAR(255),
    city VARCHAR(100),
    state VARCHAR(50),
    zip_code VARCHAR(10),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE person_counties (
    person_id INTEGER REFERENCES people(id) ON DELETE CASCADE,
    county_id INTEGER REFERENCES counties(id) ON DELETE CASCADE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (person_id, county_id)
);

CREATE INDEX idx_people_name ON people(name);
CREATE INDEX idx_people_position ON people(position);
CREATE INDEX idx_addresses_person_id ON addresses(person_id);
CREATE INDEX idx_person_counties_person_id ON person_counties(person_id);
CREATE INDEX idx_person_counties_county_id ON person_counties(county_id);