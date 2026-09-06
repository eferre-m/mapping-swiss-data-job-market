CREATE TABLE IF NOT EXISTS skills (
    skill_id       TEXT PRIMARY KEY,
    canonical_name TEXT NOT NULL,
    category       TEXT,
    active         BOOLEAN NOT NULL DEFAULT true,
    created_at     TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE TABLE IF NOT EXISTS languages (
    lang_id        TEXT PRIMARY KEY,
    canonical_name TEXT NOT NULL,
    active         BOOLEAN NOT NULL DEFAULT true,
    created_at     TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE TABLE IF NOT EXISTS soft_skills (
    soft_id        TEXT PRIMARY KEY,
    canonical_name TEXT NOT NULL,
    active         BOOLEAN NOT NULL DEFAULT true,
    created_at     TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE TABLE IF NOT EXISTS jobs (
    job_id              TEXT PRIMARY KEY,
    date_captured       DATE,
    company             TEXT,
    role                TEXT,
    industry_raw        TEXT,
    source              TEXT,

    city_id             TEXT,
    city_canonical_name TEXT,
    canton              TEXT,
    work_mode_id        TEXT,
    workload_id         TEXT,

    contract            JSONB,
    education           JSONB,
    experience          JSONB,

    status              TEXT,
    notes               TEXT,

    created_at          TIMESTAMPTZ NOT NULL DEFAULT now(),
    updated_at          TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE TABLE IF NOT EXISTS job_skills (
    job_id         TEXT NOT NULL REFERENCES jobs(job_id) ON DELETE CASCADE,
    skill_id       TEXT NOT NULL REFERENCES skills(skill_id),
    requirement    TEXT,
    PRIMARY KEY (job_id, skill_id)
);

CREATE TABLE IF NOT EXISTS job_languages (
    job_id         TEXT NOT NULL REFERENCES jobs(job_id) ON DELETE CASCADE,
    lang_id        TEXT NOT NULL REFERENCES languages(lang_id),
    requirement    TEXT,
    level          TEXT,
    PRIMARY KEY (job_id, lang_id)
);

CREATE TABLE IF NOT EXISTS job_soft_skills (
    job_id         TEXT NOT NULL REFERENCES jobs(job_id) ON DELETE CASCADE,
    soft_id        TEXT NOT NULL REFERENCES soft_skills(soft_id),
    PRIMARY KEY (job_id, soft_id)
);

CREATE INDEX IF NOT EXISTS idx_jobs_date           ON jobs (date_captured);
CREATE INDEX IF NOT EXISTS idx_jobs_city           ON jobs (city_id);
CREATE INDEX IF NOT EXISTS idx_job_skills_skill    ON job_skills (skill_id, requirement);
CREATE INDEX IF NOT EXISTS idx_job_languages_lang  ON job_languages (lang_id);
CREATE INDEX IF NOT EXISTS idx_job_soft_skills_id  ON job_soft_skills (soft_id);