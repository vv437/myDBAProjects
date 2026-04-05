# DBA Project 1: Indian Cinema Database - COMPLETION REPORT

## Project Overview
Built a fully functional relational database for Indian cinema data using PostgreSQL (Neon) and Python.

## Data Sources
- 5 DOCX files: Best_Tamil_Movies, Best_Telugu_Movies, Best_Malayalam_Movies, Best_Hindi_Movies, Best_Kannada_movies
- **Total: 154 movies extracted and normalized**

## Database Schema (5 Tables, 3NF Normalized)
1. **industries** - 5 Indian film industries
2. **persons** - Crew members (actors, directors, etc.)
3. **movies** - Film data with industry linkage
4. **role_types** - 7 job functions (Director, Actor, etc.)
5. **movie_crew** - Many-to-many junction table

## DBA Skills Demonstrated
| Skill | Implementation |
|-------|---------------|
| Normalization (3NF) | Separated persons, movies, roles to eliminate redundancy |
| SQL/PL/pgSQL | 3 stored procedures: get_movies_by_industry, get_movies_by_person, add_movie |
| Indexing | 5 indexes: industry_id, release_year, title, full_name, movie_crew composite |
| Backups | pg_dump custom format, backup/restore scripts |
| Python Integration | psycopg2 extraction script from DOCX files |
| Testing | pgTAP: 11 tests (schema, data integrity, procedures) |

## Test Results
- Schema tests: 5/5 passed
- Data integrity: 4/4 passed  
- Procedure tests: 2/2 passed
- **Total: 11/11 tests passed**

## Statistics
| Metric | Value |
|--------|-------|
| Total Movies | 154 |
| Industries | 5 |
| Unique Persons | ~400+ (actors, directors, crew) |
| Crew Relationships | ~1,078 (154 movies × 7 roles) |

## Files in Repository
- `sql/01_schema.sql` - Database schema
- `extract_movies.py` - Data extraction script
- `backup.sh` / `restore.sh` - Disaster recovery scripts
- `test_suite.sql` - pgTAP test suite
- `PROJECT_COMPLETION.md` - This report

## Deployment
- Platform: Neon Serverless PostgreSQL (cloud)
- Zero local SSD usage
- Accessible from any browser
