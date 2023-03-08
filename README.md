
# ﻿SEZNAM WEBSCRAPER

## DESCRIPTION:

This project is a simple web scraper designed to collect news titles and the respective web links from the main page of seznam.cz, a Czech news portal.

The output is twofold:

1. On the one hand, the data is transferred into an existing PostgreSQL database, along with automatically generated timestamps. The table is created automatically. There can be collected results of multiple requests, however, duplicated news are not allowed and are automatically discarded.

2. On the other hand, the result of the last request is written down into a .txt file. In other words this is a digest reflecting a current stage of the main page, which is re-written each time we run the script. This digest contains only titles and web links, without timestamps, however, the web links are automatically shortened for better readability (using TinyURL). If the shortening of a web link fails, it is transferred to the digest unchanged. The user is informed about the number of such failures in the terminal, as well as about the overall number of titles gathered in the current digest.

## REQUIREMENTS:

1. **Python 3.10.6** + **Poetry** + libraries:

	1. request
	
	2. beautifulsoup4
	
	3. pyshorteners

2. **PostgreSQL 15**

3. A local PostgreSQL database created beforehand (can be empty).

## RUNNING THE SCRIPT:

Run the script via the command line. The default command looks like:

	PGDATABASE=”name of the Postgres database” PGUSER=”your Postgres username” PGPASSWORD=”your Postgres password” python main.py file_path

where:

- *PGDATABASE*, *PGUSER*, and *PGPASSWORD* are environment variables

- *file_path* is the name and/or the path to a .txt file which will contain the digest. If no *file_path* is given, the digest will be put into the *digest.txt* file, which is placed in the project folder.
