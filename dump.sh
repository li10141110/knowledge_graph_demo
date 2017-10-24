
# dump into neo4j
neo4j-import --into [your-path-to-database]/kgDemo --nodes data/person_node.txt --nodes data/company_node.txt --relationships data/management_edge.txt --delimiter TAB

# dump into mysql
mysql -u root -p[your-password] < dump.sql


