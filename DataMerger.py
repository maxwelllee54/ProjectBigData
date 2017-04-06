import pandas as pd

csv = pd.read_csv('~/Downloads/WDI_csv/WDI_Data.csv', encoding = "ISO-8859-1")

list = ['Research and development expenditure (% of GDP)'
, 'Distance to frontier score (0=lowest performance to 100=frontier)',
'Business extent of disclosure index (0=less disclosure to 10=more disclosure)',
'Ease of doing business index (1=most business-friendly regulations)',
'New business density (new registrations per 1,000 people ages 15-64)',
'New businesses registered (number)',
'Firms using banks to finance working capital (% of firms)',
'Firms using banks to finance investment (% of firms)',
'Firms competing against unregistered firms (% of firms)',
'Time required to obtain an operating license (days)',
'Firms formally registered when operations started (% of firms)',
'Internationally-recognized quality certification (% of firms)',
'Time required to register property (days)',
'Procedures to register property (number)',
'Cost of business start-up procedures, female (% of GNI per capita)',
'Cost of business start-up procedures, male (% of GNI per capita)',
'Cost of business start-up procedures (% of GNI per capita)',
'Time required to start a business (days)',
'Time required to start a business, female (days)',
'Time required to start a business, male (days)',
'Start-up procedures to register a business (number)',
'Start-up procedures to register a business, female (number)',
'Start-up procedures to register a business, male (number)',
'Scientific and technical journal articles',
'Patent applications, nonresidents',
'Patent applications, residents',
'Researchers in R&D (per million people)',
'Technicians in R&D (per million people)']

csv.loc[]

print(csv.head())
