# School Donor Recommendation System
### Summary
This app maps philantrophic donors with underfunded schools and recommends various categories and donation tiers for making donations for school supplies. This lightweight app also helps teachers and researchers for drafting proposals for seeking grants by providing top words and phrases from a database of 1.2 billion proposals sorted as per various academic catagories using Data Analytics and NLP

### Functionality
<ul>
  <li> The app recommends various school supplies to the donors as per their prefereneces using the bricc mortar algorithm.</li>
  <li> The app maintains database of latest project proposals submitted from schools across United States </li>
  <li> Provides top words for drafting business proposals using context based learning (NLP)
</ul>    
    
### Architecture
<ul>
  <p>Here, we have created 3-tiered API Architecture  with load balancing facilities for improving app security and performance. </p>
 <li> The first layer consists of an API Gateway for routing incoming requests and forwarding it to the webserver for processing the request. Hence, this app is build to handle millions of request in the production environment. </li>
 <li> Middle layer connects the incoming requests to the database server. All the interaction to the servers are via APIs to enhance system security. Proposals are stored in the databases using ETL batches and stored procedures. Data Analysis for making recommendation is done usign NLP in the layer.</li>
 <li> The system layer connects to the database and procures the relevant data. The SQL query is embedded in this layer </li>
  </ul>
