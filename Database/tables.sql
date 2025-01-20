CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

CREATE TYPE organization AS ENUM(
    'university',
    'institute',
    'cathedra',
    'department'
);

CREATE TYPE academic_title_enum AS ENUM (
    'PhD',
    'DSc',
    'Prof.',
    'DVM',
    'MSc',
    'BSc'
);


-- Table for storing information about scientists
CREATE TABLE IF NOT EXISTS scientists (
    id UUID DEFAULT uuid_generate_v4 () PRIMARY KEY,
    first_name VARCHAR(100) NOT NULL,
    last_name VARCHAR(100) NOT NULL,
    academic_title VARCHAR(50) NOT NULL,
    position VARCHAR(255),
    research_area VARCHAR(255) NOT NULL,
    email VARCHAR(255),
    profile_url TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Table for storing information about organizations
CREATE TABLE IF NOT EXISTS organizations (
    id UUID DEFAULT uuid_generate_v4 () PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    type organization NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Table for storing the relationship between scientists and organizations
CREATE TABLE IF NOT EXISTS scientist_organization (
    id UUID DEFAULT uuid_generate_v4 () PRIMARY KEY,
    scientist_id UUID NOT NULL REFERENCES scientists (id) ON DELETE CASCADE,
    organization_id UUID NOT NULL REFERENCES organizations (id) ON DELETE CASCADE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Table for storing information about publications
CREATE TABLE publications (
    id UUID DEFAULT uuid_generate_v4 () PRIMARY KEY,
    title TEXT NOT NULL,
    journal VARCHAR(255),
    publisher VARCHAR(255),
    journal_type VARCHAR(255),
    publication_date DATE,
    journal_impact_factor FLOAT DEFAULT 0,
    ministerial_score INT DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Table for storing the relationships between scientists and publications 
CREATE TABLE scientists_publications (
    id UUID DEFAULT uuid_generate_v4 () PRIMARY KEY,
    scientist_id UUID NOT NULL REFERENCES scientists (id) ON DELETE CASCADE,
    publication_id UUID NOT NULL REFERENCES publications (id) ON DELETE CASCADE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP  
);  

-- Table for storing bibliometric indicators of scientists
CREATE TABLE bibliometrics (
    id UUID DEFAULT uuid_generate_v4 () PRIMARY KEY,
    h_index_wos INTEGER, -- Optional
    h_index_scopus INTEGER,
    publication_count INTEGER NOT NULL,
    ministerial_score FLOAT NOT NULL,
    scientist_id UUID REFERENCES scientists (id) ON DELETE CASCADE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE organizations_relationships (
    id UUID DEFAULT uuid_generate_v4() PRIMARY KEY,                 
    parent_id UUID,              
    child_id UUID,               
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP, -- Data utworzenia
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE research_areas (
    id UUID DEFAULT uuid_generate_v4() PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE scientists_research_areas (
    id UUID DEFAULT uuid_generate_v4() PRIMARY KEY,    
    scientist_id UUID REFERENCES scientists (id) ON DELETE CASCADE,
    research_area_id UUID REFERENCES research_areas (id) ON DELETE CASCADE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
