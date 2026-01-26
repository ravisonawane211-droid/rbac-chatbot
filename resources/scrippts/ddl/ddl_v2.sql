CREATE TABLE locations (
    location_id INT PRIMARY KEY,
    country VARCHAR(100) NOT NULL,
    city VARCHAR(100) NOT NULL,
    cost_index NUMERIC(5,2) NOT NULL
);

CREATE TABLE departments (
    department_id SERIAL PRIMARY KEY,
    department_name VARCHAR(100) NOT NULL UNIQUE,
    department_code VARCHAR(20) UNIQUE,
    description TEXT,
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);


-- ============================
-- Employees Table
-- ============================
CREATE TABLE employee (
    employee_id VARCHAR(20) PRIMARY KEY,
    full_name VARCHAR(150) NOT NULL,
    email VARCHAR(150) UNIQUE,
    role VARCHAR(100) NOT NULL,
    department_id INT NOT NULL,
    location_id INT NOT NULL,
    manager_id VARCHAR(20),
    date_of_joining DATE NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT fk_department
        FOREIGN KEY (department_id)
        REFERENCES departments(department_id),

    CONSTRAINT fk_location
        FOREIGN KEY (location_id)
        REFERENCES locations(location_id),

    CONSTRAINT fk_manager
        FOREIGN KEY (manager_id)
        REFERENCES employee(employee_id)
);


CREATE TABLE employee_org (
    employee_id VARCHAR(20) PRIMARY KEY,
    role VARCHAR(100) NOT NULL,
    department VARCHAR(100) NOT NULL,
    manager_id VARCHAR(20),

    CONSTRAINT fk_employee_org
        FOREIGN KEY (employee_id)
        REFERENCES employee(employee_id)
        ON DELETE CASCADE,

    CONSTRAINT fk_manager
        FOREIGN KEY (manager_id)
        REFERENCES employee(employee_id)
);

CREATE TABLE employee_compensation (
    employee_id VARCHAR(20) PRIMARY KEY,
    salary NUMERIC(12,2) NOT NULL,
    last_updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT fk_employee_comp
        FOREIGN KEY (employee_id)
        REFERENCES employee(employee_id)
        ON DELETE CASCADE
);

CREATE TABLE employee_performance (
    performance_id SERIAL PRIMARY KEY,
    employee_id VARCHAR(20) NOT NULL,
    performance_rating INT CHECK (performance_rating BETWEEN 1 AND 5),
    last_review_date TIMESTAMP,
    reviewer_id VARCHAR(20),

    CONSTRAINT fk_employee_perf
        FOREIGN KEY (employee_id)
        REFERENCES employee(employee_id)
        ON DELETE CASCADE,

    CONSTRAINT fk_reviewer
        FOREIGN KEY (reviewer_id)
        REFERENCES employee(employee_id)
);


CREATE TABLE employee_leave (
    employee_id VARCHAR(20) PRIMARY KEY,
    leave_balance INT DEFAULT 0,
    leaves_taken INT DEFAULT 0,
    last_updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT fk_employee_leave
        FOREIGN KEY (employee_id)
        REFERENCES employee(employee_id)
        ON DELETE CASCADE
);


CREATE TABLE employee_attendance (
    employee_id VARCHAR(20) PRIMARY KEY,
    attendance_pct NUMERIC(5,2),
    last_calculated TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT fk_employee_att
        FOREIGN KEY (employee_id)
        REFERENCES employee(employee_id)
        ON DELETE CASCADE
);


CREATE INDEX IF NOT EXISTS idx_locations_country ON locations(country);
CREATE INDEX IF NOT EXISTS idx_locations_city ON locations(city);

CREATE INDEX IF NOT EXISTS idx_departments_name ON departments(department_name);
CREATE INDEX IF NOT EXISTS idx_departments_active ON departments(is_active);

CREATE INDEX IF NOT EXISTS idx_employee_department ON employee(department_id);
CREATE INDEX IF NOT EXISTS idx_employee_location ON employee(location_id);
CREATE INDEX IF NOT EXISTS idx_employee_manager ON employee(manager_id);
CREATE INDEX IF NOT EXISTS idx_employee_role ON employee(role);
CREATE INDEX IF NOT EXISTS idx_employee_email ON employee(email);
CREATE INDEX IF NOT EXISTS idx_employee_joining_date ON employee(date_of_joining);

CREATE INDEX IF NOT EXISTS idx_employee_comp_salary ON employee_compensation(salary);

CREATE INDEX IF NOT EXISTS idx_employee_leave_balance ON employee_leave(leave_balance);
CREATE INDEX IF NOT EXISTS idx_employee_leave_taken ON employee_leave(leaves_taken);


CREATE INDEX IF NOT EXISTS idx_employee_attendance_pct ON employee_attendance(attendance_pct);

CREATE INDEX IF NOT EXISTS idx_employee_perf_employee ON employee_performance(employee_id);
CREATE INDEX IF NOT EXISTS idx_employee_perf_reviewer ON employee_performance(reviewer_id);
CREATE INDEX IF NOT EXISTS idx_employee_perf_rating ON employee_performance(performance_rating);
CREATE INDEX IF NOT EXISTS idx_employee_perf_review_date ON employee_performance(last_review_date);

