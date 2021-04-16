# PartisanNewsletters
Partisan Text in Newsletter Emails: Exploratory Analysis
In this analysis, I take the newsletters from federal lawmakers (data source: https://www.lindseycormack.com/dcinbox-data-downloads) from the 115th Congress (February 2017-December 2019, I exclude the month of the inauguration of new members). In this exploration, I seek to understand the relationship between the partisanship of the text and the partisanship of the region that the congressperson represents, determined y the Cook PVI (2017). I used the 2017 PVI, which is why I chose to analyze the 115th Congress; as of April 15 2021, a new PVI is available and I hope to update my analysis to reflect that.
The folder 115Congress_newsletter contains the newsletters as csv files.
partisanDistricts and partisanStates contain the cook PVI's for each district and state
stateDecoder.csv is used to convert between state codes (2-letter representations) and state names.
The outputs of this analysis are currently 4 bar charts representing the phrases that are most used by one group compared to another. They are:
RepOverDem.png: the words Republicans use most frequently compared to Democrats
DemOverRep.png: the words Democrats use most frequently compared to Republicans
RepOverNeut.png: the words Republicans use most frequently compared to Neutral members
DemOverNeut.png: the words Democrats use most frequently compared to Neutral members

Partisanship is determined by how far a district's PVI is from the median: if it is 5 points more republican, the sender is classified as a republican; if their district is 5 points more democratic, the sender is classified as a democrat, and if in-between, the sender is classified as neutral
