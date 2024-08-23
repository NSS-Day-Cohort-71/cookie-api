-- Create the flavors table
CREATE TABLE flavors (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL UNIQUE
);

-- Create the cookies table
CREATE TABLE cookies (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    flavor_id INTEGER NOT NULL,
    baked_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    eaten_at TIMESTAMP,
    FOREIGN KEY (flavor_id) REFERENCES flavors (id)
);

-- Create the toppings table
CREATE TABLE toppings (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL UNIQUE
);

-- Create a junction table for the many-to-many relationship between cookies and toppings
CREATE TABLE cookie_toppings (
    cookie_id INTEGER,
    topping_id INTEGER,
    FOREIGN KEY (cookie_id) REFERENCES cookies (id),
    FOREIGN KEY (topping_id) REFERENCES toppings (id),
    PRIMARY KEY (cookie_id, topping_id)
);

-- Insert some initial flavors
INSERT INTO flavors (name) VALUES
    ('Chocolate Chip'),
    ('Oatmeal Raisin'),
    ('Peanut Butter'),
    ('Sugar'),
    ('Double Chocolate');

-- Insert some initial toppings
INSERT INTO toppings (name) VALUES
    ('Sprinkles'),
    ('Chocolate Drizzle'),
    ('Nuts'),
    ('Powdered Sugar'),
    ('Frosting');

-- Create an index on the flavor_id in the cookies table for faster queries
CREATE INDEX idx_cookies_flavor_id ON cookies (flavor_id);

-- Create indexes on the junction table for faster queries
CREATE INDEX idx_cookie_toppings_cookie_id ON cookie_toppings (cookie_id);
CREATE INDEX idx_cookie_toppings_topping_id ON cookie_toppings (topping_id);



























            SELECT c.id,
                c.name name,
                f.name flavor_name,
                c.baked_at,
                t.name topping
            FROM cookies c
            JOIN flavors f ON f.id = c.flavor_id
            JOIN cookie_toppings ct ON c.id = ct.cookie_id
            JOIN toppings t ON t.id = ct.topping_id
            WHERE c.id = 1
            AND c.eaten_at IS NULL;
