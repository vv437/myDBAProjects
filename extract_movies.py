import os
from docx import Document
import psycopg2
from psycopg2.extras import execute_values
from dotenv import load_dotenv

# Load connection string
load_dotenv()
DATABASE_URL = "postgresql://neondb_owner:npg_wb6TG5CvHdfl@ep-cold-hat-aiy1cpw7-pooler.c-4.us-east-1.aws.neon.tech/neondb?sslmode=require&channel_binding=require"

# Map filenames to industry names
INDUSTRY_MAP = {
    'Best_Tamil_Movies.docx': 'Tamil',
    'Best_Telugu_Movies.docx': 'Telugu',
    'Best_Malayalam_Movies.docx': 'Malayalam',
    'Best_Hindi_Movies.docx': 'Hindi',
    'Best_Kannada_Movies.docx': 'Kannada'
}

# Role mapping from your column headers
ROLE_MAP = {
    'Writer': 'Writer',
    'Director': 'Director',
    'Actor': 'Actor',
    'Actress': 'Actress',
    'Supporting Actor': 'Supporting Actor',
    'Producer': 'Producer',
    'Cinematography': 'Cinematographer'
}

def parse_docx(filename):
    """Extract movie rows from docx file"""
    doc = Document(filename)
    movies = []
    industry = INDUSTRY_MAP.get(filename, 'Unknown')
    
    # Skip header rows, find data rows
    in_data_section = False
    
    for para in doc.paragraphs:
        text = para.text.strip()
        if not text:
            continue
            
        # Detect header line with column names
        if 'SI. No.' in text or 'Movie' in text and 'Year' in text:
            in_data_section = True
            continue
            
        # Parse data line: Title, Year, Writer, Director, Actor, Actress, Supporting Actor, Producer, Cinematography
        if in_data_section and ',' in text:
            parts = [p.strip() for p in text.split(',')]
            if len(parts) >= 9:
                movie = {
                    'industry': industry,
                    'title': parts[0],
                    'year': int(parts[1]) if parts[1].isdigit() else None,
                    'writer': parts[2],
                    'director': parts[3],
                    'actor': parts[4],
                    'actress': parts[5],
                    'supporting_actor': parts[6],
                    'producer': parts[7],
                    'cinematographer': parts[8]
                }
                movies.append(movie)
    
    return movies

def insert_to_database(movies):
    """Insert parsed movies into Neon database"""
    conn = psycopg2.connect(DATABASE_URL)
    cur = conn.cursor()
    
    # Get industry IDs
    cur.execute("SELECT industry_id, name FROM industries")
    industry_ids = {name: id for id, name in cur.fetchall()}
    
    # Get role type IDs
    cur.execute("SELECT role_type_id, role_name FROM role_types")
    role_ids = {name: id for id, name in cur.fetchall()}
    
    persons_cache = {}  # Avoid duplicate person inserts
    
    for movie in movies:
        # Get industry_id
        industry_id = industry_ids.get(movie['industry'])
        if not industry_id:
            continue
            
        # Insert movie
        cur.execute("""
            INSERT INTO movies (industry_id, title, release_year)
            VALUES (%s, %s, %s)
            ON CONFLICT (title, release_year) DO NOTHING
            RETURNING movie_id
        """, (industry_id, movie['title'], movie['year']))
        
        result = cur.fetchone()
        if result:
            movie_id = result[0]
        else:
            # Movie exists, get its ID
            cur.execute("""
                SELECT movie_id FROM movies 
                WHERE title = %s AND release_year = %s
            """, (movie['title'], movie['year']))
            movie_id = cur.fetchone()[0]
        
        # Process crew members
        crew_roles = [
            ('Writer', movie['writer']),
            ('Director', movie['director']),
            ('Actor', movie['actor']),
            ('Actress', movie['actress']),
            ('Supporting Actor', movie['supporting_actor']),
            ('Producer', movie['producer']),
            ('Cinematographer', movie['cinematographer'])
        ]
        
        for role_name, person_name in crew_roles:
            if not person_name or person_name == '-':
                continue
                
            # Insert person (or get existing)
            if person_name not in persons_cache:
                cur.execute("""
                    INSERT INTO persons (full_name)
                    VALUES (%s)
                    ON CONFLICT DO NOTHING
                    RETURNING person_id
                """, (person_name,))
                
                result = cur.fetchone()
                if result:
                    person_id = result[0]
                else:
                    cur.execute("SELECT person_id FROM persons WHERE full_name = %s", (person_name,))
                    person_id = cur.fetchone()[0]
                    
                persons_cache[person_name] = person_id
            else:
                person_id = persons_cache[person_name]
            
            # Insert movie_crew link
            role_type_id = role_ids.get(role_name)
            if role_type_id:
                cur.execute("""
                    INSERT INTO movie_crew (movie_id, person_id, role_type_id)
                    VALUES (%s, %s, %s)
                    ON CONFLICT DO NOTHING
                """, (movie_id, person_id, role_type_id))
        
        conn.commit()
        print(f"Inserted: {movie['title']} ({movie['year']}) - {movie['industry']}")
    
    cur.close()
    conn.close()
    print(f"\nTotal movies processed: {len(movies)}")

def main():
    all_movies = []
    
    for filename in INDUSTRY_MAP.keys():
        if os.path.exists(filename):
            print(f"Processing {filename}...")
            movies = parse_docx(filename)
            all_movies.extend(movies)
            print(f"  Found {len(movies)} movies")
        else:
            print(f"File not found: {filename}")
    
    if all_movies:
        print(f"\nInserting {len(all_movies)} movies to database...")
        insert_to_database(all_movies)
    else:
        print("No movies found to insert")

if __name__ == "__main__":
    main()