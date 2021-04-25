import json
import psycopg2


def import_data(data_url):
    conn = psycopg2.connect("dbname=mainddbb user=postgres password=postgres")
    cursor = conn.cursor()

    # save possible duplicates here
    deferred_data = []

    # cache company ids by linkedin urls
    company_urls = dict()

    # assume company data has related data nested inside each company
    with open(data_url) as json_file:
        data = json.load(json_file)
        for c in data['company']:

            id = None

            # normalize name
            name = c.company_name.lower().strip()
            common = ['llc', 'inc']
            for str in common:
                name = name.replace(str, '')

            # check for linkedin_url, if present we use it to define duplicate or not based on it
            if c.linkedin_url:
                if company_urls[c.linkedin_url]:
                    id = company_urls[c.linkedin_url]
                else:
                    cursor.execute("select id from companies where linkedin_url = '%s';", c.linkedin_url)
                    data = cursor.fetchall()
                    id = data[0]['id'] if data.length else None

                # create new company
                if not id:
                    cursor.execute(
                        "insert into companies (company_name,normalized_name,website_url,linkedin_url,last_update_time)"
                        " values (%s, %s, %s, %s) RETURNING id;", (c.company_name, name, c.website_url, c.linkedin_url,
                                                                   c.last_update_time))
                    id = cursor.fetchone()[0]

                # save id
                company_urls[c.linkedin_url] = id
            else:
                c.normalized_name = name
                deferred_data.append(name)

    # save deferred companies and related data to be moderated later
    with open('deferred.json', 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)
