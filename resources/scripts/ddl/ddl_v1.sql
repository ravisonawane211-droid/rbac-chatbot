CREATE TABLE locations (
    location_id INT PRIMARY KEY,
    country VARCHAR(100) NOT NULL,
    city VARCHAR(100) NOT NULL,
    cost_index NUMERIC(5,2) NOT NULL
);

-- ============================
-- Employees Table
-- ============================
CREATE TABLE employees (
    employee_id VARCHAR(20) PRIMARY KEY,
    full_name VARCHAR(150) NOT NULL,
    role VARCHAR(100) NOT NULL,
    department VARCHAR(100) NOT NULL,
    email VARCHAR(150) UNIQUE,
    location_id INT,
    date_of_birth DATE NOT NULL,
    date_of_joining DATE NOT NULL,
    manager_id VARCHAR(20),
    salary NUMERIC(12,2) NOT NULL,
    leave_balance INT DEFAULT 0,
    leaves_taken INT DEFAULT 0,
    attendance_pct NUMERIC(5,2),
    performance_rating INT CHECK (performance_rating BETWEEN 1 AND 5),
    last_review_date TIMESTAMP,

    CONSTRAINT fk_location
        FOREIGN KEY (location_id)
        REFERENCES locations(location_id),

    CONSTRAINT fk_manager
        FOREIGN KEY (manager_id)
        REFERENCES employees(employee_id)
);


CREATE INDEX idx_employees_location_id ON employees(location_id);
CREATE INDEX idx_employees_manager_id ON employees(manager_id);
CREATE INDEX idx_employees_department ON employees(department);
