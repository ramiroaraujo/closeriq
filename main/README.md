# Main Excercise

First we need to define the criteria for a duplicate company. If it's duplicate 
because of the linkedin_url, then we can have an unique key on the table field
to avoid duplicates being created in the first place. That way we can warn the 
user when validating before submitting, and if we have an automated process for
importing the data from other datasources and we _know_ linkedin_url is unique 
we can use that criteria to avoid duplicating and link related records to the
previously existing company record.

The company_name field is trickier. Asuming a manual process we control, we can
check for similar company names and warn the user when submitting, but still 
allow for submission since there are companies that share the same name. In 
those cases this records should be flagged as 'checked', in order not to check
them for duplicates with other companies later.

Any automated process of importing data that might result in new companies 
being created in the database should:
1. Check for duplicate linkedin_url field if exists, and treat that as an 
unique identifier, thus not create a new company record and instead associate
   any related records with the existing company record with the same 
   linkedin_url field value.
2. Check for similarity in the company_name field. Better safe than sorry here,
so any possible duplicate should not be added, nor it's associated data. It
   should be deferred for later, to manually check and merge or create new 
   records. Maybe a natural language processing library could help to catch
   some possible duplicates. Otherwise, I would try to normalize the text, 
   remove common prefixes and postfixes (like Inc, LLC, etc) and check for
   duplicates. We'll need either a column with this normalized text, or a 
   helper table with the normalized text and a reference to the record with
   proper indexes to search for duplicates.
   
The possibility of creating a new company and associating records to it when
it's a duplicate sounds like too much risk to build any automated solution for.
I would keep this possible duplicates in a different table or datasource, then
create a UI for moderators to view the possible duplicates, review their 
company data, and allow then to merge to an existing company or create a new
one. In any case, each moderator decision would run a single import with both
the company data and related data associated with it.

In terms of data size, 1 million records it's not a problem to search for 
duplicated names if we have indexes in the normalized names and linkedin_url.

For the 20.000 records being created or updated daily, I'll assume there're 
not that many duplicates in terms of company names. The urls will be 
automatically solved, and the possible name duplicates should be manually 
solved. If there're indeed too many possible duplicates per day and the 
manual moderation turns out to be a bottleneck then we'll need to decide a
tradeoff between more automatic company merging (maybe using natural language
processing) or more moderators.