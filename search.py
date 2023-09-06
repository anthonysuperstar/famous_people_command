import wikipedia
import sqlite3
import argparse

def main():
    #! ============================Creation of the arguments system
    parser = argparse.ArgumentParser(description='Search your favourite famous people on wikipedia')
    parser.add_argument('fname', type=str, help="First name")
    parser.add_argument('lname', type=str, help="Last name")
    args = parser.parse_args()
    
    #! ============================Reformation of the research
    search_query = f"{args.fname} {args.lname}".lower()
    print('Searching for ', args.fname + ' ' + args.lname)
    
    try:
        #! ==================== If wikipedia recognizes the query, it's added to the Table and the current table is displayed
        page = wikipedia.page(search_query)
        summary = wikipedia.summary(search_query)
        
        conn = sqlite3.connect("search.db")
        cursor = conn.cursor()
        
        cursor.execute("INSERT INTO famous_people(name, description) VALUES (?, ?)", (search_query, summary))
        conn.commit()
        
        cursor.execute("SELECT * FROM famous_people;")
        result = cursor.fetchall()
        for row in result:
            print(row)
        
        #! ==================== If there is no result 'Not Found' is displayed
    except wikipedia.exceptions.PageError:
        print('Not found')
        
        #! ==================== If it's too ambiguous, a list of closely related terms is displayed
    except wikipedia.exceptions.DisambiguationError as e: 
        print(f'By "{search_query}" do you mean one of these?:\n')
        for option in e.options[:8]:
            print(option)
            
        #! ==================== If there is something wrong with the DB the proper error is displayed
    except sqlite3.Error as e:
        print(f"DB error: {e}")


if __name__ == '__main__':
    main()

